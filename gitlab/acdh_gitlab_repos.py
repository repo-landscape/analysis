import argparse
import csv
import json
import logging
import re
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('apiKey')
parser.add_argument('outputFile')
parser.add_argument('--format', default='csv', choices=['csv', 'markdown', 'json'])
parser.add_argument('--endpoint', default='projects', choices=['projects', 'events', 'variables', 'pipelines', 'members/all'], help='GitLab API endpoint to query.')
parser.add_argument('--listColumns', action='store_true', help='When provided, no data is fetched and only a list of available columns is displayed. This operation may still take quite some time as columns list is computed from the actual data (examples in GitLab documentation are sometimes outdated).')
parser.add_argument('--filters', default='', help='Additional GitLab enpoint query parameters as a query string, e.g. "visibility=private&last_activity_after=2022-01-01T00:00:00" for the "projects" endpoint. Consult the GitLab API documentation for available parameters (https://docs.gitlab.com/ee/api/api_resources.html).')
parser.add_argument('--orderBy', default='id', help='Passed directly to the GitLab API. For available values consult the GitLab API documentation of a given endpoint.')
parser.add_argument('--sort', default='asc', choices=['asc', 'desc'])
parser.add_argument('--apiBase', default='https://gitlab.com/api/v4/', help='GitLab API base URL. Default is https://gitlab.com/api/v4/.')
parser.add_argument('--limitParents', type=int, default=-1, help='Limits the number of records fetched from parent endpoints (e.g. number of projects processed before continuing to querying the users endpoint). Useful for testing as it reduces the execution time (but also cause output data to be incomplete).')
parser.add_argument('--columns', nargs='+', default=None, help='List of columns to be included in the output. If not provided, all columns are included.')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(levelname)s: %(message)s', encoding='utf-8', level=logging.DEBUG if args.verbose else logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# a helper for paging handling
def fetchWithPaging(url, orderBy='id', sort='asc', limit=-1, projectId=None):
    url = f'{url}&pagination=keyset&order_by={orderBy}&sort={sort}&per_page=100'
    data = []
    while url and (len(data) < limit or limit < 0):
        logging.debug(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            data += resp.json()
            logging.info(f'    {len(data)} records collected in total')
        else:
            logging.warning(f'    {resp.status_code} returned for {url}')
        url = False
        if 'Link' in resp.headers:
            link = [x.strip().split(';') for x in resp.headers['Link'].split(',')]
            link = [x for x in link if x[1].strip() == 'rel="next"']
            if len(link) > 0:
                url = link[0][0][1:-1]
    if limit > 0 and len(data) > limit:
        logging.info(f'    Limiting number of records to {limit}')
        data = data[0:limit]
    if projectId:
        for i in data:
            i['project_id'] = projectId
    return data

# if needed, fetch the data from the first-level endpoint
if args.endpoint == 'projects':
    endpoint = args.endpoint
    ids = ['']
else:
    logging.info(f'# Fetching data from the projects endpoint')
    url = f'{args.apiBase}projects?private_token={args.apiKey}&membership=true&{args.filters}'
    ids = fetchWithPaging(url, 'id', 'asc', 100 if args.listColumns else args.limitParents)
    ids = [i['id'] for i in ids]
    endpoint = f'projects/%id%/{args.endpoint}'

# events endpoint requires one more step - collecting users
if args.endpoint == 'events':
    logging.info(f'Collecting users list')
    n = 1
    url = f'{args.apiBase}projects/%id%/users?private_token={args.apiKey}&{args.filters}'
    userIds = set()
    for i in ids:
        logging.info(f'Fetching data from the projects/{str(i)}/users endpoint ({n}/{len(ids)} {int(100 * n / len(ids))}%)')
        data = fetchWithPaging(url.replace('%id%', str(i)), args.orderBy, args.sort, 100 if args.listColumns else args.limitParents)
        userIds = userIds.union(set([x['id'] for x in data])) 
        n += 1
    ids = list(userIds)
    endpoint = 'users/%id%/events'
    logging.info(f'{len(ids)} users collected')

# fetch the actual endpoint data
url = f'{args.apiBase}{endpoint}?private_token={args.apiKey}&membership=true&{args.filters}'
data = []
n = 1
for i in ids:
    logging.info(f'Fetching data from the {endpoint.replace("%id%", str(i))} endpoint ({n}/{len(ids)} {int(100 * n / len(ids))}%)')
    data += fetchWithPaging(
        url.replace('%id%', str(i)), 
        args.orderBy, 
        args.sort, 
        100 if args.listColumns else -1, 
        i if args.endpoint in ['variables', 'pipelines', 'members/all'] else None
    )
    n += 1

# process columns list
columns = set()
for i in data:
    columns = columns.union(set(i.keys()))

if args.listColumns:
    logging.info('Available columns:')
    logging.info(', '.join(sorted(list(columns))))
    logging.info(f'Please look at the https://docs.gitlab.com/ee/api/{re.sub(".*/", "", endpoint)} for details')
    exit()

if args.columns:
    columns = [x for x in args.columns if x in columns]

# apply columns list on data
data = [{x: i[x] for x in list(set(i.keys()).intersection(columns))} for i in data]

# generate output
columns = list(columns)
    
with open(args.outputFile, 'w') as out:
    logging.info(f'Writting output in the {args.format} to {args.outputFile}')
    if args.format == 'json':
        json.dump(data, out)
    elif args.format == 'markdown':
        out.write('| ' + ' | '.join(columns) + ' |\n')
        row = '|'
        for i in columns:
            row += '-' * (len(i) + 2) + '|'
        out.write(row + '\n')
        for i in data:
            row = [str(i[j]) if j in i else '' for j in columns]
            out.write('| ' + ' | '.join(row) + ' |\n')
    elif args.format == 'csv':
        writer = csv.writer(out, delimiter=';')
        writer.writerow(columns)
        for i in data:
            row = [str(i[j]) if j in i else '' for j in columns]
            writer.writerow(row)

