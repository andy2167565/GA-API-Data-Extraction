#!/usr/bin/python3.4
"""Google Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
import time
import socket
from datetime import datetime, timedelta


start_time = time.time()
print('------------< Site Content_All Pages >-------------')

script_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_path, 'configFile', 'config.txt')) as f:
    config = f.readlines()
    config = {i.split("=")[0]: i.split("=")[1].replace("\n", "") for i in config if '#' not in i and i != '\n'}


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = os.path.join(script_path, 'configFile', 'client_secrets.json')
VIEW_ID = config["VIEW_ID"]  # user define

startDate = config["startDate"]  # user define, e.g.'2016-03-03', 'yesterday', '30daysAgo'
endDate = config["endDate"]  #time.strftime('%Y-%m-%d')  # endDate is set to today

filepath = os.path.join(script_path, 'outputs')
filename = 'Site_Content_All_Pages.csv'

if not os.path.exists(filepath):
    os.makedirs(filepath)

# GA parameters of metrics and dimensions
metrics_list = [{'expression': 'ga:pageviews'}, {'expression': 'ga:uniquePageviews'},
                {'expression': 'ga:avgTimeOnPage'}, {'expression': 'ga:entrances'},
                {'expression': 'ga:bounceRate'}, {'expression': 'ga:exits'},
                {'expression': 'ga:exitRate'}, {'expression': 'ga:pageValue'}]
dimensions_list = [{'name': 'ga:date'}, {'name': 'ga:pagePath'}]
metrics_dimensions_list = [[metrics_list, dimensions_list]]

# Headers for csv output
header_row = ['Date', 'Page', 'Pageviews', 'Unique_Pageviews',
              'Avg_Time_on_Page', 'Entrances', 'Bounce_Rate', 'Exits',
              '%_Exit', 'Page_Value']


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    """Queries the Analytics Reporting API V4.

    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
        The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'pageSize': 1000000,
                    'dateRanges': [{'startDate': startDate, 'endDate': startDate}],
                    'metrics': metrics_dimensions_list[i][0],
                    'dimensions': metrics_dimensions_list[i][1],
                    'includeEmptyRows': 'true'
                } for i in range(len(metrics_dimensions_list))
            ]
        }
    ).execute()


def print_response_exist(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.
    """

    for report in response.get('reports', []):
        with open(os.path.join(filepath, filename), 'a') as f:
            writer = csv.writer(f, lineterminator='\n')

            #columnHeader = report.get('columnHeader', {})
            #dimensionHeaders = columnHeader.get('dimensions', [])
            #metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            rows = report.get('data', {}).get('rows', [])

            # Write row data
            if rows:
                for row in rows:
                    dimensions = row.get('dimensions', [])
                    metrics = [m['values'] for m in row.get('metrics', [])][0]
                    data_row = []
                    data_row.extend(dimensions)
                    data_row.extend(metrics)

                    # Encode to big5, then decode back to cp950 and ignore error characters
                    data_row = [n.encode('big5', 'ignore').decode('cp950', 'ignore') for n in data_row]
                    #.encode('utf-8').decode('cp950', 'ignore')

                    writer.writerow(data_row)
            else:
                print('No Rows Found')


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.
    """

    for report in response.get('reports', []):
        with open(os.path.join(filepath, filename), 'w') as f:
            # Wrap file with a csv.writer
            writer = csv.writer(f, lineterminator='\n')

            #columnHeader = report.get('columnHeader', {})
            #dimensionHeaders = columnHeader.get('dimensions', [])
            #metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            rows = report.get('data', {}).get('rows', [])

            # Write header
            writer.writerow(header_row)

            # Write row data
            if rows:
                for row in rows:
                    dimensions = row.get('dimensions', [])
                    metrics = [m['values'] for m in row.get('metrics', [])][0]
                    data_row = []
                    data_row.extend(dimensions)
                    data_row.extend(metrics)

                    # Encode to big5, then decode back to cp950 and ignore error characters
                    data_row = [n.encode('big5', 'ignore').decode('cp950', 'ignore') for n in data_row]
                    #.encode('utf-8').decode('cp950', 'ignore')

                    writer.writerow(data_row)
            else:
                print('No Rows Found')


def addDate(startDate):
    datetime_object = datetime.strptime(startDate, '%Y-%m-%d')
    nextDate = datetime_object + timedelta(days=1)
    return nextDate


def dateTrans(startDate, endDate):
    if startDate == 'today':
        startDate = datetime.today()
    elif startDate == 'yesterday':
        startDate = datetime.today() - timedelta(days=1)
    elif startDate[-7:] == 'daysAgo':
        Days = int(startDate[:-7])
        startDate = datetime.today() - timedelta(days=Days)
    else:
        try:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
        except ValueError:
            print('Incorrect startDate format, should be one of the following:\n',
                  '1)YYYY-MM-DD\n',
                  '2)today\n',
                  '3)yesterday\n',
                  '4)NdaysAgo(where N is a positive integer)')
            startDate = None

    if endDate == 'today':
        endDate = datetime.today()
    elif endDate == 'yesterday':
        endDate = datetime.today() - timedelta(days=1)
    elif endDate[-7:] == 'daysAgo':
        Days = int(endDate[:-7])
        endDate = datetime.today() - timedelta(days=Days)
    else:
        try:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        except ValueError:
            print('Incorrect endDate format, should be one of the following:\n',
                  '1)YYYY-MM-DD\n',
                  '2)today\n',
                  '3)yesterday\n',
                  '4)NdaysAgo(where N is a positive integer)')
            endDate = None

    return startDate, endDate


def getLastDate(filepath, filename):
    with open(os.path.join(filepath, filename)) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reversed(list(reader)):
            if row:
                last_line = row
                last_date = last_line[0]
                last_date = '{0}-{1}-{2}'.format(last_date[:4], last_date[4:6], last_date[-2:])
                last_date = datetime.strptime(last_date, '%Y-%m-%d')
                return last_date
            else:
                return None


def getRowCount(filepath, filename):
    with open(os.path.join(filepath, filename)) as f:
        reader = csv.reader(f)
        next(reader)
        row_count = sum(1 for row in reader)
        return row_count


if __name__ == '__main__':
    # Transform date type according to user inputs
    startDate, endDate = dateTrans(startDate, endDate)

    # Check if user has entered the right date format
    if startDate and endDate:
        # Check if date range order is correct
        if startDate.date() > endDate.date():
            print('Incorrect date range: startDate should be before or equal to endDate')
        else:
            # Check if the output file has already existed
            if os.path.isfile(os.path.join(filepath, filename)):
                # Get row count of existing file
                prev_row_count = getRowCount(filepath, filename)
                # Get last date in file
                lastDate = getLastDate(filepath, filename)
                # Check if last date actually exists
                if lastDate:
                    lastDateNext = lastDate + timedelta(days=1)
                    # If lastDateNext is before startDate, use lastDateNext as startDate
                    if lastDateNext < startDate:
                        startDate = lastDateNext
                    # If startDate is before lastDateNext
                    elif lastDateNext > startDate:
                        # If lastDateNext is before or equal to endDate, use lastDateNext as startDate
                        if lastDateNext <= endDate:
                            startDate = lastDateNext
                        # If lastDateNext is after endDate
                        else:
                            print('Data in this date range has already exist')
                            quit()

                while startDate.date() <= endDate.date():
                    startDate = startDate.strftime('%Y-%m-%d')  # datetime to string
                    print('Capturing data on', startDate, '...')
                    try:
                        analytics = initialize_analyticsreporting()
                        response = get_report(analytics)
                        print_response_exist(response)
                    except socket.timeout:
                        print('Timeout Error: The read operation timed out')
                    startDate = addDate(startDate)

            else:
                prev_row_count = 0
                # Write rows for first date
                startDate = startDate.strftime('%Y-%m-%d')  # datetime to string
                print('Capturing data on', startDate, '...')
                try:
                    analytics = initialize_analyticsreporting()
                    response = get_report(analytics)
                    print_response(response)
                except socket.timeout:
                    print('Timeout Error: The read operation timed out')
                startDate = addDate(startDate)

                # Write rows for the following dates
                while startDate.date() <= endDate.date():
                    startDate = startDate.strftime('%Y-%m-%d')  # datetime to string
                    print('Capturing data on', startDate, '...')
                    try:
                        analytics = initialize_analyticsreporting()
                        response = get_report(analytics)
                        print_response_exist(response)
                    except socket.timeout:
                        print('Timeout Error: The read operation timed out')
                    startDate = addDate(startDate)

    # Read total number of rows
    with open(os.path.join(filepath, filename), 'r') as f:
        reader = csv.reader(f)
        next(reader)
        row_count = sum(1 for row in reader)
        print('Total number of rows = %s' % row_count)
        print('Number of rows for current load = %s' % (row_count - prev_row_count))
    print('filepath = ' + filepath)
    print('filename = ' + filename)

print('Execution time = %s seconds' % (time.time() - start_time))
