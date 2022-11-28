import argparse
import os
import re


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('file', nargs='+', help='debug.log file')
    args = parser.parse_args()

    query_times = list()

    for file in args.file:
        if os.path.isfile(file):
            query_times.extend(parse_file(file))

    query_times.sort()

    for query in query_times:
        timestamp = query[0]
        time = query[1]
        print("{}|{}".format(timestamp, time))


def parse_file(file):
    start_regex = r"[0-9]+\soperations"
    # TODO Add query_regex as CLI argument. Keep r".*[0-9]+\smsec" as the base regex.
    query_regex = r"keyspace\.table.*[0-9]+\smsec"
    timestamp_regex = r"[0-9\-]+\w\s[0-9:,]+"
    time_regex = r"[0-9]+\smsec"

    open_file = open(file, "r")

    reading = False
    timestamp = ""
    slow_queries = list()

    # Parse file for slow operations
    for line in open_file:
        start_match = re.search(start_regex, line)
        query_match = re.search(query_regex, line)

        # If found slow operations
        if start_match is not None:
            reading = True
            timestamp = re.search(timestamp_regex, line).group(0)
        # If we're reading slow queries and they're the query we want
        elif reading and query_match is not None:
            if timestamp == "":
                print("Slow operation date was not found")

            time_match = re.search(time_regex, line)
            time_split = time_match.group(0).split()
            time = int(time_split[0])
            data = (timestamp, time)
            slow_queries.append(data)
        else:
            reading = False
            timestamp = ""

    return slow_queries


if __name__ == "__main__":
    main()
