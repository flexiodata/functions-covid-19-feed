
# ---
# name: covid-19-cases-jhu
# deployed: true
# config: index
# schedule:
#   frequency: daily
#   timezone: UTC
#   days: []
#   times:
#   - hour: 7
#     minute: 10
# title: Covid-19 Cases (Johns Hopkins)
# description: Returns data about Covid-19 cases from the John Hopkins Covid-19 GitHub Repository
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
#   - name: country_region
#     type: string
#     description: The country/region name
#   - name: province_state
#     type: string
#     description: The province/state name
#   - name: location
#     type: string
#     description:
#   - name: latitude
#     type: number
#     description: The latitude for the location
#   - name: longitude
#     type: number
#     description: The longitude for the location
#   - name: confirmed
#     type: integer
#     description: The number of confirmed cases
#   - name: deaths
#     type: integer
#     description: The number of deaths
#   - name: recovered
#     type: integer
#     description: The number of recovered cases
#   - name: active
#     type: integer
#     description: The number of active cases
#   - name: date
#     type: string
#     description: The date of the information in UTC
#   - name: fips
#     type: integer
#     description: The fips number
# examples:
#   - '"country_region, province_state, location, confirmed, deaths, recovered"'
#   - '"", "location:\"New York City\""'
#   - '"location, confirmed, deaths", "+Illinois +Cook +date:[2020-04-01 TO 2020-04-30]"'
# notes: |-
#   Additional Resources:
#   * Johns Hopkins Covid-19 GitHub Repo Source Data: \
#     https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
#   * Johns Hopkins Covid-19 GitHub Repo Source Data README: \
#     https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
#   * Johns Hopkins Covid-19 GitHub Repo: \
#     https://github.com/CSSEGISandData/COVID-19
#   * Johns Hopkins Covid-19 Visualization: \
#     https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
#   * Johns Hopkins Center for Systems Science and Engineering (CSSE): \
#     https://systems.jhu.edu/
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
    repo   = 'CSSEGISandData/COVID-19'
    folder = 'csse_covid_19_data/csse_covid_19_daily_reports'
    mindate = '2020-03-22'

    # set the output type to ndjson for loading into an index
    flex.output.content_type = 'application/x-ndjson'

    # get the files to download
    files = get_files_to_download(repo, folder, mindate)

    # get the data for each line in each file and write it to
    # stdout with one json object per-line (ndjson) for loading
    # into an index
    for f in files:
        for row in get_data(f):
            item = json.dumps(row) + "\n"
            flex.output.write(item)

def get_files_to_download(repo, folder, mindate):

    # find out the files available for the given repo/folder
    url = 'https://api.github.com/repos/' + repo + '/contents/' + folder
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Flex.io Covid-19 Integration'
    }
    r = requests_retry_session().get(url, headers=headers)
    data = json.loads(r.text)

    # filter the files to csvs with a timestamp on or after the minimum date
    items = []
    for d in data:
        file = d['name']
        # make sure we have a csv
        if '.csv' not in file:
            continue
        # filename is in format MM-DD-YYYY.csv; get date in YYYYMMDD format
        dt = file.split('.')[0].split('-')
        date_str = dt[2] + '-' + dt[0] + '-' + dt[1]
        if date_str < mindate:
            continue
        # return the file and the date
        file_info = {'url': 'https://raw.githubusercontent.com/' + repo + '/master/' + folder + '/' + file, 'date': date_str}
        items.append(file_info)

    # get the most recent file first
    items = sorted(items, key = lambda i: i['date'],reverse=True)
    return items

def get_data(file_info):

    # get the data
    headers = {
        'User-Agent': 'Flex.io Covid-19 Integration'
    }
    request = requests_retry_session().get(file_info['url'], stream=True, headers=headers)
    with closing(request) as r:
        # get each line and return a dictionary item for each line
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            data = get_item(row, file_info['date'])
            yield data

def get_item(row, date):
    # convert keys to lowercase and make sure the values are formatted
    row = {k.lower(): v for k, v in row.items()}
    item = OrderedDict()
    item['country_region'] = row.get('country_region','')
    item['province_state'] = row.get('province_state','')
    item['location'] = row.get('admin2','')
    item['latitude'] = to_number(row.get('lat',0))
    item['longitude'] = to_number(row.get('long_',0))
    item['confirmed'] = to_number(row.get('confirmed',0))
    item['deaths'] = to_number(row.get('deaths',0))
    item['recovered'] = to_number(row.get('recovered',0))
    item['active'] = to_number(row.get('active',0))
    #item['date'] = row.get('last_update','')
    item['date'] = date # use date from file because date in content is formatted variably
    item['fips'] = to_number(row.get('fips',''))
    return item

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 503, 504),
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
