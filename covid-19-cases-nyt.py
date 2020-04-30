
# ---
# name: covid-19-cases-nyt
# deployed: true
# config: index
# schedule:
#   frequency: daily
#   timezone: UTC
#   days: []
#   times:
#   - hour: 7
#     minute: 5
# title: Covid-19 Cases (New York Times)
# description: Returns data about Covid-19 cases from the New York Times Covid-19 GitHub Repository
# params:
#   - name: properties
#     type: array
#     description: The properties to return, given as a string or array; defaults to all properties; see "Returns" for available properties
#     required: false
#   - name: filter
#     type: array
#     description: Search query to determine the rows to return, given as a string or array
#     required: false
# returns:
#   - name: state
#     type: string
#     description: The state name
#   - name: county
#     type: string
#     description: The county name
#   - name: cases
#     type: number
#     description: The number of cases in the state/county
#   - name: deaths
#     type: number
#     description: The number of deaths in the state/county
#   - name: date
#     type: string
#     description: The date of the information
#   - name: fips
#     type: integer
#     description: The fips number
# examples:
#   - '"date, state, county, cases, deaths"'
#   - '"", "\"New York\""'
#   - '"county, cases", "+Illinois +date:2020-04-01"'
# notes: |-
#   Data from The New York Times, based on reports from state and local health agencies
#   Additional Resources:
#   * New York Times Covid-19 GitHub Repo Source Data: \
#     https://github.com/nytimes/covid-19-data
#   * New York Times Covid-19 Tracking Page: \
#     https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html
# ---

import csv
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from contextlib import closing
from collections import OrderedDict
from time import sleep

def flex_handler(flex):

    # configuration
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

    # set the output type to ndjson for loading into an index
    flex.output.content_type = 'application/x-ndjson'

    # get the data for each line in each file and write it to
    # stdout with one json object per-line (ndjson) for loading
    # into an index
    for row in get_data(url):
        item = json.dumps(row) + "\n"
        flex.output.write(item)

def get_data(url):

    # get the data
    headers = {
        'User-Agent': 'Flex.io Covid-19 Integration'
    }
    request = requests_retry_session().get(url, stream=True, headers=headers)
    with closing(request) as r:
        # get each line and return a dictionary item for each line
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            data = get_item(row)
            yield data

def get_item(row):
    # convert keys to lowercase and make sure the values are formatted
    row = {k.lower(): v for k, v in row.items()}
    item = OrderedDict()
    item['state'] = row.get('state','')
    item['county'] = row.get('county','')
    item['cases'] = to_number(row.get('cases',0))
    item['deaths'] = to_number(row.get('deaths',0))
    item['date'] = row.get('date','')
    item['fips'] = to_number(row.get('fips',''))
    return item

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def to_number(value):
    try:
        v = value
        return float(v)
    except ValueError:
        return value
