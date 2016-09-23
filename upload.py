import csv, datetime, os, sys
import psycopg2
from collections import namedtuple

Row = namedtuple('Row', ['uuid', 'date', 'amount', 'description', 'type', 'tags'])
allowed_tags = set([tag for line in open("tags.txt") for tag in line.rstrip().split(",")]) | {"", " "}
def process(row):
    # A row looks like [<UUID>, <Date>, <CheckNum>, <Description>, <Withdrawal Amount>, <Deposit Amount>, <Additional Info>, <Tags>] 
    # We turn this into a Row namedtuple with things switched around.
    uuid = row[0]
    try:
        date = datetime.datetime.strptime(row[1], "%m/%d/%Y")
    except Exception:
        date = datetime.datetime.strptime(row[1], "%m/%d/%y")
    
    amount = float(row[4] or 0) + float(row[5] or 0)
    description = row[6] # What the spreadsheet calls 'additional info'.
    type = row[3]
    tags = row[7]
    return Row(uuid, date, amount, description, type, tags)

def contains_data(line):
    return len(line) != 0 and not line.startswith("<")

def check_tags(tags):
    return all(tag in allowed_tags for tag in tags.split(",")) 

def insert(row):
    """ Adds a Row namedtuple to the database. """
    if not check_tags(row.tags):
        raise ValueError("Tags not recognized for row.", row)
    if "ignore" in row.tags:
        print "Ignoring row {}".format(row)
        return
    SQL = "INSERT INTO transactions (uuid, date, amount, description, type, tags) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (uuid) DO UPDATE SET tags = EXCLUDED.tags;"
    return cursor.execute(SQL, row)

if __name__ == "__main__":
    count = 0
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cursor:
            with open(sys.argv[1], "r+") as csvfile:
                contents = [line.rstrip() for line in csvfile if contains_data(line)]
                for row in csv.reader(contents): 
                    try:
                        insert(process(row))
                        count += 1
                    except psycopg2.Error as e:
                        print e.pgerror
                    except Exception as e:
                        print "Bad row:"
                        print row
                        raise

print "%s rows uploaded" % count
