import argparse
import json
import os
import psycopg2

parser = argparse.ArgumentParser()
parser.add_argument('--dbConf', default='user=postgres host=127.0.0.1')
parser.add_argument('--dbPswd')
parser.add_argument('entityType', choices=['communities_infrastructures', 'datasets', 'datasources', 'organizations', 'other_research_products', 'projects', 'publications', 'relations', 'software'])
parser.add_argument('jsonFileOrDir')
args = parser.parse_args()

con = psycopg2.connect(args.dbConf + (f' password= {args.dbPswd}' if args.dbPswd else ''))
cur = con.cursor()
if os.path.isfile(args.jsonFileOrDir):
    files = [args.jsonFileOrDir]
else:
    files = [os.path.join(args.jsonFileOrDir, x) for x in os.listdir(args.jsonFileOrDir) if x.endswith('.json')]
for file in files:
    with open(file, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            cur.execute(
                f"INSERT INTO {args.entityType} (id, data) VALUES (%s, %s)",
                (data['id'], line)
            )
    con.commit()

