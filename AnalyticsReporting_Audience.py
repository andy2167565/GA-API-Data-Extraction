#!/usr/bin/python3.4
"""Google Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
import time
import socket


start_time = time.time()
print('-------------------< Audience >--------------------')

script_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_path, 'configFile', 'config.txt')) as f:
    config = f.readlines()
    config = {i.split("=")[0]: i.split("=")[1].replace("\n", "") for i in config if '#' not in i and i != '\n'}


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = os.path.join(script_path, 'configFile', 'client_secrets.json')
VIEW_ID = config["VIEW_ID"]  # user define

startDate = config["startDate"]  # user define, e.g.'2018-09-01', 'yesterday', '30daysAgo'
endDate = config["endDate"]  #time.strftime('%Y-%m-%d')  # endDate is set to today

filepath = os.path.join(script_path, 'outputs')
filename = 'Audience.csv'

if not os.path.exists(filepath):
    os.makedirs(filepath)

# GA parameters of metrics and dimensions
metrics_list = [{'expression': 'ga:users'}, {'expression': 'ga:percentNewSessions'},
                {'expression': 'ga:newUsers'}, {'expression': 'ga:bounceRate'},
                {'expression': 'ga:pageviewsPerSession'}, {'expression': 'ga:avgSessionDuration'},
                {'expression': 'ga:sessionsPerUser'}]
dimensions_list = [{'name': 'ga:date'}]
metrics_dimensions_list = [[metrics_list, dimensions_list]]

# Headers for csv output
header_row = ['Date', 'Users', '%_New_Sessions', 'New_Users',
              'Bounce_Rate', 'Pages_Session', 'Avg_Session_Duration', 'Number_of_Sessions_per_User']


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
                    'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                    'metrics': metrics_dimensions_list[i][0],
                    'dimensions': metrics_dimensions_list[i][1],
                    'includeEmptyRows': 'true'
                } for i in range(len(metrics_dimensions_list))
            ]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
        response: An Analytics Reporting API V4 response.
    """

    for report in response.get('reports', []):
        create_header = True
        if os.path.isfile(filepath):
            create_header = False

        f = open(os.path.join(filepath, filename), 'wt')

        # Wrap file with a csv.writer
        writer = csv.writer(f, lineterminator='\n')

        columnHeader = report.get('columnHeader', {})
        #dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        if create_header:
            writer.writerow(header_row)

        # Write row data
        row_count = 0
        if rows:
            for row in rows:
                dimensions = row.get('dimensions', [])
                metrics = [m['values'] for m in row.get('metrics', [])][0]
                data_row = []
                data_row.extend(dimensions)
                data_row.extend(metrics)

                writer.writerow(data_row)
                row_count += 1

            print('filepath = ' + filepath)
            print('filename = ' + filename)
            print('Number of rows = %d' % row_count)

        else:
            print('No Rows Found')

        # Close the file
        f.close()


def main():
    try:
        analytics = initialize_analyticsreporting()
        response = get_report(analytics)
        print_response(response)
    except socket.timeout:
        print('Timeout Error: The read operation timed out')


if __name__ == '__main__':
    main()

print('Execution time = %s seconds' % (time.time() - start_time))
