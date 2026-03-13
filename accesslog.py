import re
import sys
from pathlib import Path

# Regular expression to match IPv4 addresses at the start of each log line
IP_REGEX = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})')

def extract_ips(log_file_path):
    """
    Extracts unique IP addresses from an Apache access log file.
    
    :param log_file_path: Path to the Apache access log file
    :return: A set of unique IP addresses
    """
    ips = set()

    try:
        log_path = Path(log_file_path)
        if not log_path.is_file():
            raise FileNotFoundError(f"Log file not found: {log_file_path}")

        with log_path.open("r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                match = IP_REGEX.match(line)
                if match:
                    ips.add(match.group(1))

    except Exception as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        return set()

    return ips


if __name__ == "__main__":
    # Example usage: python script.py /var/log/apache2/access.log
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_access_log>")
        sys.exit(1)

    log_file = sys.argv[1]
    ip_addresses = extract_ips(log_file)

    if ip_addresses:
        print(f"Found {len(ip_addresses)} unique IP addresses:")
        for ip in sorted(ip_addresses):
            print(ip)
    else:
        print("No IP addresses found or log file is empty.")
