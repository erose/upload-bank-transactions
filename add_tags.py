import psycopg2
import csv, sys, readline
from collections import namedtuple

Row = namedtuple('Row', ['uuid', 'date', 'amount', 'description', 'type', 'tags'])
allowed_tags = set([tag for line in open("tags.txt") for tag in line.rstrip().split(",")]) | {"", " "}

def autocomplete_tag_names(text, state):
    candidate_tags = sorted(tag for tag in allowed_tags if tag.startswith(text))
    return candidate_tags[state] if candidate_tags else None
readline.parse_and_bind('tab: complete')
readline.set_completer(autocomplete_tag_names)

if __name__ == "__main__":
    input_filename = sys.argv[1]
    ow = csv.writer(open('tagged-' + input_filename, "a"))
    for row in csv.reader(open(input_filename)):
        while True:
            print row[1:]
            tags = raw_input("Enter tags: ")
            if set(tags.split(",")) < allowed_tags:
                row[-1] = tags
                ow.writerow(row)
                break
            else:
                print "Bad tags"
