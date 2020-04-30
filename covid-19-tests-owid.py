
# ---
# name: covid-19-tests-owid
# deployed: true
# config: index
# schedule:
#   frequency: daily
#   timezone: UTC
#   days: []
#   times:
#   - hour: 7
#     minute: 0
# title: Covid-19 Tests (Our World In Data)
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
#   - name: entity
#     type: string
#     description: The country/entity performing the tests
#   - name: date
#     type: string
#     description: The date of the tests
#   - name: total
#     type: string
#     description: The cumulative total number of tests performed
#   - name: total_daily_change
#     type: integer
#     description: The daily change in cumulative total number of tests performed
#   - name: total_per_thousand
#     type: number
#     description: Cumulative total per thousand
#   - name: total_per_thousand_daily_change
#     type: number
#     description: The daily change in cumulative total per thousand
#   - name: three_day_rolling_mean_daily_change
#     type: number
#     description: The three-day rolling mean daily change
#   - name: three_day_rolling_mean_daily_change_per_thousand
#     type: number
#     description: The three-day rolling mean daily change per thousand
#   - name: source_url
#     type: string
#     description: The source url for the information
#   - name: source_label
#     type: string
#     description: The source label for the information
#   - name: notes
#     type: string
#     description: Notes for the information
# examples:
#   - '"entity,date,total"'
#   - '"", "+CDC +\"United States\""'
# notes: |-
#   Data from Our World In Data, based on data collected by the Our World in Data team from official reports
#   Additional Resources:
#   * Our World In Data Covid-19 GitHub Repo Source Data: \
#     https://github.com/owid/covid-19-data/tree/master/public/data
#   * Our World In Data Covid-19 Tracking Page: \
#     https://ourworldindata.org/coronavirus
#   * Our World In Data Covid-19 Testing Sources: \
#     https://ourworldindata.org/covid-testing#source-information-country-by-country
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
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv'

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
    item['entity'] = row.get('entity','')
    item['date'] = row.get('date','')
    item['total'] = to_number(row.get('cumulative total',''))
    item['total_daily_change'] = to_number(row.get('daily change in cumulative total',''))
    item['total_per_thousand'] = to_number(row.get('cumulative total per thousand',''))
    item['total_per_thousand_daily_change'] = to_number(row.get('daily change in cumulative total per thousand',''))
    item['three_day_rolling_mean_daily_change'] = to_number(row.get('3-day rolling mean daily change',''))
    item['three_day_rolling_mean_daily_change_per_thousand'] =to_number( row.get('3-day rolling mean daily change per thousand',''))
    item['source_url'] = row.get('source url','')
    item['source_label'] = row.get('source label','')
    item['notes'] = row.get('notes','')
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
