import argparse
import datetime
import json
import logging
import os
import psycopg2
import sys
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('--dbConf', default='user=postgres host=127.0.0.1')
parser.add_argument('--dbPswd')
parser.add_argument('--filesLimit', type=int)
parser.add_argument('--filesOffset', type=int)
parser.add_argument('--truncate', action='store_true', help='Should the database table be truncated before the import')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('entityType', choices=['communities_infrastructures', 'dataset', 'datasource', 'organization', 'other_research_product', 'project', 'publication', 'relation', 'software'])
parser.add_argument('jsonFileOrDir')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(asctime)s: %(message)s', level=logging.DEBUG if args.verbose else logging.INFO)
T0 = datetime.datetime.now()

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
nLine = 0
for file in files:
    nFile += 1
    logging.info(f'Processing file {file} ({nFile}/{len(files)})')
    try:
        with open(file, 'r') as fh:
            for line in fh:
                nLine += 1
                line = line.replace('\\u0000', '')
                data = json.loads(line)
                if args.entityType == 'relation':
                    cur.execute(
                        f"""
                        INSERT INTO relations (sourceid, targetid, reltype) 
                        VALUES (%s, %s, %s) 
                        """,
                        (data['source']['id'], data['target']['id'], data['reltype']['name'])
                    )
                else:
                    cur.execute(
                        f"INSERT INTO entities (id, type, data) VALUES (%s, %s, %s) ON CONFLICT (id, type) DO UPDATE SET data = EXCLUDED.data",
                        (data['id'], args.entityType, line)
                    )
        con.commit()
    except Exception as e:
        traceback.print_exc()
        con.rollback()
T0 = (datetime.datetime.now() - T0).total_seconds()
logging.info(f'{nFile} files and {nLine} lines processed in {T0} s (on average {T0 / nFile} s per file and {1000 * T0 / nLine} s per 1k lines)')
