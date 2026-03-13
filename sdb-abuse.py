import requests
import json
import argparse
import sys
from ezipset import ezIPSet
import re
import sys
from pathlib import Path
from pysondb import db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'

headers = {
    'Accept': 'application/json',
    'Key': 'b1ba681a88355b464973b2d3417ab9a26131c56e9135d7955ca9f597c37410b8008f689d8d198eae'
}

# Regular expression to match IPv4 addresses at the start of each log line
IP_REGEX = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})')

# accesslog
logfile = "/var/log/ispconfig/httpd/hetgezondheidscentrum.nl/access.log"
database = db.getDb("ipabusedb.json")

def main():
  # Create the parser
  #parser = argparse.ArgumentParser()
  # Add an argument
  #parser.add_argument('--ip', type=str, required=True)
  # Parse the argument
  #args = parser.parse_args()
  #data = queryabuseipdb(args.ip)
  #print(data)
  #iptoipset(data)



  # Example usage: python script.py /var/log/apache2/access.log
  #if len(sys.argv) != 2:
  #    print(f"Usage: {sys.argv[0]} <path_to_access_log>")
  #    sys.exit(1)

  # log_file = sys.argv[1]
  log_file = logfile
  ip_addresses = extract_ips(log_file)
  counter = 0

  entries= checkdb()
  print(f"These ids are 3 months old:\t {entries}")
  if ip_addresses:
      print(f"Found {len(ip_addresses)} unique IP addresses:")
      for ip in sorted(ip_addresses):
          inipset = checkipipset(ip)
          dbpresent = dbpresentcheck(ip)
          if inipset or dbpresent:
              print(f"{ip}\t : database: {dbpresent}\t | \tipset : {inipset}" )
          else:
              data = queryabuseipdb(ip)
              counter += 1
              if data:
                  print(f"{ip}\t : Adding ip to ipset")
                  iptoipset(data)
              else:
                  print(f"{ip}\t : Not listed on ipabusedb.com")
  print(f"usage of the api at ipabusedb.com: \t {counter}")

def queryabuseipdb(qip: str):
  querystring = {
    'ipAddress': qip,
    'maxAgeInDays': '90',
    }
  response = requests.request(method='GET', url=url, headers=headers, params=querystring)
  decodedResponse = json.loads(response.text)
  database.add(decodedResponse)
  if (decodedResponse["data"]["abuseConfidenceScore"] != 0) or ( decodedResponse["data"]["abuseConfidenceScore"] != 0):
      ip = (decodedResponse["data"]["ipAddress"])
      return ip

def checkipipset(cii: str):
    ipset = ezIPSet(raise_on_errors=False)
    ipthere = ipset.test_entry("wp-block",cii,raise_on_test_failed=False)
    return ipthere


def dbpresentcheck(dcii: str):
    rows = database.getAll()
    ip_addresses = [row["data"]["ipAddress"] for row in rows]
    if dcii in ip_addresses:
        return True 
    else:
        return False


def iptoipset(iip: str):
    ipset = ezIPSet(raise_on_errors=False)
    ipset.create_set('wp-block',set_type='hash:ip',family='inet',timeout=210000,with_comment=True)
    ipset.add_entry('wp-block',iip,ignore_if_exists=True)


def checkdb():
    three_months_ago = datetime.now() - relativedelta(months=3)
    datestring = three_months_ago.strftime("%Y-%m-%d")
    idlist = []
    with open("ipabusedb.json", "r", encoding="utf-8") as f:
        obj = json.load(f)

    rows = [
        (item["data"]["ipAddress"], item["data"]["lastReportedAt"], item["id"])
        for item in obj["data"]
    ]
    for row in rows:
        ip, report, idr = row
        try:
            if report.startswith(datestring):
                print(idr)
                idlist.append(idr)
        except AttributeError:
            continue
    return idlist



def cleanupdb(cleanupentries):
    deleted_ids = database(cleanupentries)
    return deleted_ids

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
    main()


#ipAddress
#isPublic
#ipVersion
#isWhitelisted
#abuseConfidenceScore
#countryCode
#usageType
#isp
#domain
#hostnames
#isTor
#totalReports
#numDistinctUsers
#lastReportedAt
