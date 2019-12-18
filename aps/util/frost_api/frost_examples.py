import requests
import pprint
import json


"""
from https://frost.met.no/langex_python
"""

def get_client_id():
    """
    Requires a file "client_id.json" with the following content:
    {"client_id":  "12493b54-c073-4c44-7a41-633a3569f636"}

    :return:
    """
    with open("client_id.json") as file:
        _id = json.load(file)
        return _id["client_id"]


def get_element_info():
    """
    retrieve information about a certain element (parameter) or search for part of element-name.
    :return:
    """
    client_id = get_client_id()
    # Get all elements that hav "precipitation" in their id
    url = r"https://frost.met.no/elements/v0.jsonld?ids=*precipitation*&lang=en-US"

    rsp = requests.get(url, auth=(client_id, ''))

    print(rsp.text)

#
# """
#
# This program shows how to retrieve info for a single source from the Frost service.
#
# The HTTP request essentially consists of the following components:
#   - the endpoint, frost.met.no/sources
#   - the source ID to get information for
#   - the client ID used for authentication
#
# The source ID is read from a command-line argument, while the client ID is read from
# the environment variable CLIENTID.
#
# Save the program to a file example.py, make it executable (chmod 755 example.py),
# and run it e.g. like this:
#
#   $ CLIENTID=8e6378f7-b3-ae4fe-683f-0db1eb31b24ec ./example.py SN18700
#
# or like this to get info for sources matching a pattern:
#
#   $ CLIENTID=8e6378f7-b3-ae4fe-683f-0db1eb31b24ec ./example.py SN187*
#
# (Note: the client ID used in the example should be replaced with a real one)
#
# The program has been tested on the following platforms:
#   - Python 2.7.3 on Ubuntu 12.04 Precise
#   - Python 2.7.12 and 3.5.2 on Ubuntu 16.04 Xenial
#
# """
#
# import sys, os
# import requests # See http://docs.python-requests.org/
#
# def get_source_info():
#
#     # extract command-line argument
#     if len(sys.argv) != 2:
#        sys.stderr.write('usage: ' + sys.argv[0] + ' <source ID>\n')
#        sys.exit(1)
#     source_id = sys.argv[1]
#
#     # extract environment variable
#     if not 'CLIENTID' in os.environ:
#         sys.stderr.write('error: CLIENTID not found in environment\n')
#         sys.exit(1)
#     client_id = os.environ['CLIENTID']
#
#     # issue an HTTP GET request
#     r = requests.get(
#         'https://frost.met.no/sources/v0.jsonld',
#         {'ids': source_id},
#         auth=(client_id, '')
#     )
#
#     def codec_utf8(s):
#         #return s.encode('utf-8').decode('utf-8') # should be used for Python 3
#         return s.encode('utf-8') # should be used for Python 2
#
#     # extract some data from the response
#     if r.status_code == 200:
#         for item in r.json()['data']:
#             sys.stdout.write('ID: {}\n'.format(item['id']))
#             sys.stdout.write('Name: {}\n'.format(codec_utf8(item['name'])))
#             if 'geometry' in item:
#                 sys.stdout.write('longitude: {}\n'.format(item['geometry']['coordinates'][0]))
#                 sys.stdout.write('latitude: {}\n'.format(item['geometry']['coordinates'][1]))
#             if 'municipality' in item:
#                 sys.stdout.write('Municipality: {}\n'.format(codec_utf8(item['municipality'])))
#             if 'county' in item:
#                 sys.stdout.write('County: {}\n'.format(codec_utf8(item['county'])))
#             sys.stdout.write('Country: {}\n'.format(codec_utf8(item['country'])))
#             if 'externalIds' in item:
#                 for ext_id in item['externalIds']:
#                     sys.stdout.write('external ID: {}\n'.format(ext_id))
#             else:
#                 sys.stdout.write('no external IDs found\n')
#     else:
#         sys.stdout.write('error:\n')
#         sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
#         if 'error' in r.json():
#             assert(r.json()['error']['code'] == r.status_code)
#             sys.stdout.write('\tmessage: {}\n'.format(r.json()['error']['message']))
#             sys.stdout.write('\treason: {}\n'.format(r.json()['error']['reason']))
#         else:
#             sys.stdout.write('\tother error\n')



if __name__ == "__main__":
    # a = get_client_id()
    get_element_info()

