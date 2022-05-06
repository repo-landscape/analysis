# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    import urllib3
    import json

    jsonfn = 'gitlab-list_2022.json'

    key = 'glpat-xinShZakar9yrWvpYK2_'
    url = 'https://gitlab.com/api/v4/projects?visibility=private&per_page=300&private_token=' + key
    http = urllib3.PoolManager()

    r = http.request('GET', url)
    # r.data
    obj = json.loads(r.data)

    # TODO: add paging - https://docs.gitlab.com/ee/api/index.html#pagination
    # use "Link" header to get to next/last !

    # r.headers
    with open(jsonfn, 'w') as outfile:
        json.dump(obj, outfile)

    print(len(obj))
    print (json.dumps(obj, indent=2))
    filtered_dict = [ x for x in obj if x ['name_with_namespace'] == 'ACDH-CH / InTavia / intavia nlp suite']
    print(filtered_dict)
    # print (obj["name_with_namespace"])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
