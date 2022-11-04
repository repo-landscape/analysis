import argparse
import json
import logging
import os
import psycopg2
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--dbConf', default='user=postgres host=127.0.0.1')
parser.add_argument('--dbPswd')
parser.add_argument('--filesLimit', type=int)
parser.add_argument('--filesOffset', type=int)
parser.add_argument('--truncate', action='store_true', help='Should the database table be truncated before the import')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('entityType', choices=['communities_infrastructures', 'datasets', 'datasources', 'organizations', 'other_research_products', 'projects', 'publications', 'relations', 'software'])
parser.add_argument('jsonFileOrDir')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(asctime)s: %(message)s', level=logging.DEBUG if args.verbose else logging.INFO)

con = psycopg2.connect(args.dbConf + (f' password= {args.dbPswd}' if args.dbPswd else ''))
cur = con.cursor()
if args.truncate:
    cur.execute("TRUNCATE {args.entityType}")
    con.commit()
if os.path.isfile(args.jsonFileOrDir):
    files = [args.jsonFileOrDir]
else:
    files = [os.path.join(args.jsonFileOrDir, x) for x in os.listdir(args.jsonFileOrDir) if x.endswith('.json')]
files.sort()
if args.filesOffset:
    files = files[args.filesOffset:]
if args.filesLimit:
    files = files[0:args.filesLimit]
nFile = 0
for file in files:
    nFile += 1
    logging.info(f'Processing file {file} ({nFile}/{len(files)})')
    with open(file, 'r') as fh:
        for line in fh:
            data = json.loads(line)
            if args.entityType == 'relations':
                cur.execute(
                    f"""
                    INSERT INTO {args.entityType} (sourceid, targetid, reltype, sourcetype, targettype, data) 
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (sourceid, targetid) DO UPDATE SET 
                        reltype = EXCLUDED.reltype, sourcetype = EXCLUDED.sourcetype, targettype = EXCLUDED.targettype, data = EXCLUDED.data
                    """,
                    (data['source']['id'], data['target']['id'], data['reltype']['name'], data['source']['type'], data['target']['type'], line)
                )
            else:
                cur.execute(
                    f"INSERT INTO {args.entityType} (id, data) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data",
                    (data['id'], line)
                )
    con.commit()

