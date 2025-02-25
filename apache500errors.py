import re
from collections import defaultdict
from datetime import datetime

# Define the path to the Apache error log file
LOG_FILE = "error.log"

# error log entries with :error] which indicates a 500 error
LOG_PATTERN = re.compile(r'\[(.*?)\] \[.*?:error\]')

def parse_error_log(file_path):
    #store the date and hour entries with 500 error
    error_counts = defaultdict(int)

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = LOG_PATTERN.search(line)

            if match:
                #Extract the timestamp
                timestamp = match.group(1)
                hour = datetime.strptime(timestamp, "%a %b %d %H:%M:%S.%f %Y").strftime("%Y-%m-%d %H")

                error_counts[hour] += 1  # Group by hour

    return error_counts


def calculate_average(errors_per_hour):
    if not errors_per_hour:
        # Avoid division by zero if no errors are found
        return 0

    total_errors = sum(errors_per_hour.values())
    total_hours = len(errors_per_hour)
    return total_errors / total_hours


if __name__ == "__main__":
    errors_per_hour = parse_error_log(LOG_FILE)

    errors_per_hour = calculate_average(errors_per_hour)

    print(f"Number of HTTP 500 errors per hour: {errors_per_hour:.2f}")