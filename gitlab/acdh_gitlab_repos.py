import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('apiKey')
parser.add_argument('--columns', nargs='+', default=['id', 'path_with_namespace', 'web_url', 'visibility', 'created_at', 'last_activity_at', 'issues_enabled', 'jobs_enabled', 'wiki_enabled', 'merge_requests_enabled', 'snippets_enabled', 'container_registry_access_level', 'shared_runners_enabled', 'ci_forward_deployment_enabled', 'request_access_enabled', 'auto_devops_enabled', 'auto_devops_deploy_strategy', 'packages_enabled', 'service_desk_enabled'], help='for possible columns list take a look at response sample on https://docs.gitlab.com/ee/api/projects.html#list-all-projects')
parser.add_argument('--filters', default='', help='additional projects endpoint query parameters as a query string')
parser.add_argument('--format', default='csv', choices=['csv', 'markdown'])
parser.add_argument('--contributors', action='store_true')
parser.add_argument('--variables', action='store_true')
args = parser.parse_args()

separator = ';'
rowprefix = ''
rowsuffix = ''
if args.format == 'markdown':
    separator = ' | '
    rowprefix = '| '
    rowsuffix = ' |'    

print(rowprefix + separator.join(args.columns) + rowsuffix)
if args.format == 'markdown':
    row = '|'
    for i in args.columns:
        row += '-' * (len(i) + 2) + '+'
    row = row[0:-1] + '|'
    print(row)

url = 'https://gitlab.com/api/v4/projects?membership=true&per_page=1000&pagination=keyset&order_by=id&sort=asc&private_token=' + args.apiKey + '&' + args.filters
data = []
while url:
    resp = requests.get(url)
    data += resp.json()
    url = resp.headers['Link'].split(';')[0][1:-1] if 'Link' in resp.headers else False
    break
for project in data:
    row = []
    for col in args.columns:
        row.append(str(project[col]) if col in project else '')
    print(rowprefix + separator.join(row) + rowsuffix)

if args.contributors:
    accessLevels = {'0': 'none', '5': 'minimal', '10': 'guest', '20': 'reporter', '30': 'developer', '40': 'maintainer', '50': 'owner'}
    print()
    if args.format == 'markdown':
        print('| id | path_with_namespace| user | user_name | access_level |')
        print('|----+--------------------|------|-----------|--------------|')
    else:
        print('id;path_with_namespace;user;user_name;access_level')
    for project in data:
        url = f"https://gitlab.com/api/v4/projects/{project['id']}/members/all?private_token={args.apiKey}"
        resp = requests.get(url)
        for i in resp.json():
            row = [str(project['id']), project['path_with_namespace'], i['username'], i['name'], accessLevels[str(i['access_level'])]]
            tx = rowprefix + separator.join(row) + rowsuffix
            print(tx.encode('utf8'))

if args.variables:
    print()
    if args.format == 'markdown':
        print('| id | path_with_namespace| type | key | value |')
        print('|----+--------------------|------|-----|-------|')
    else:
        print('id;path_with_namespace;type,key,value')
    for project in data:
        url = f"https://gitlab.com/api/v4/projects/{project['id']}/variables?private_token={args.apiKey}"
        resp = requests.get(url)
        if resp.status_code == 200:
            for i in resp.json():
                row = [str(project['id']), project['path_with_namespace'], i['variable_type'], i['key'], i['value']]
                print(rowprefix + separator.join(row) + rowsuffix)
        elif resp.status_code == 403:
            row = [str(project['id']), project['path_with_namespace'], 'forbidden access', '', '']
            print(rowprefix + separator.join(row) + rowsuffix)
            
    
