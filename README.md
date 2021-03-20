# Google Analytics API Data Extraction
Data Extraction on website for combinations of backend user information via [Google Analytics API](https://analytics.google.com/analytics/web/?authuser=0#/provision)

## Directory Structure
    .
    ├── configFile                                  # Contains all the configuration files required in the scripts
    │   ├── client_secrets.json                     # Service key to connect to Google Analytics API
    │   ├── config.txt                              # Configuration parameters required in the scripts
    │   └── requirements.txt                        # Required Python packages
    ├── outputs                                     # Contains all the output csv (automatically generated)
    └── ...

## Configuration Parameters
<table>
  <tr>
    <td><strong>Parameter Name</strong></td>
    <td><strong>Description</strong></td>
    <td><strong>Type</strong></td>
    <td><strong>Example</strong></td>
  </tr>
  <tr>
    <td>VIEW_ID</td>
    <td>The ID to verify which view to extract in GA.</td>
    <td>Refer to Google Analytics</td>
    <td>123456789</td>
  </tr>
  <tr>
    <td rowspan="4">startDate</td>
    <td rowspan="4">Define start date to extract the data.</td>
      <td>YYYY-MM-DD</td>
      <td>2020-01-01</td>
  </tr>
  <tr>
    <td>today</td>
    <td>today</td>
  </tr>
  <tr>
    <td>yesterday</td>
    <td>yesterday</td>
  </tr>
  <tr>
    <td>NdaysAgo (N: non-zero integer)</td>
    <td>30daysAgo</td>
  </tr>
  <tr>
    <td rowspan="4">endDate</td>
    <td rowspan="4">Define end date to extract the data.</td>
      <td>YYYY-MM-DD</td>
      <td>2020-01-01</td>
  </tr>
  <tr>
    <td>today</td>
    <td>today</td>
  </tr>
  <tr>
    <td>yesterday</td>
    <td>yesterday</td>
  </tr>
  <tr>
    <td>NdaysAgo (N: non-zero integer)</td>
    <td>30daysAgo</td>
  </tr>
</table>

## Output Table Structure
<table>
  <tr>
    <td><strong>Category</strong></td>
    <td><strong>Output File Name</strong></td>
  </tr>
  <tr>
    <td>Monthly</td>
    <td>MTD_USERS_SESSIONS.csv</td>
  </tr>
  <tr>
    <td>Audience</td>
    <td>Audience.csv</td>
  </tr>
  <tr>
    <td rowspan="3">Behavior</td>
      <td>Frequency_Recency_Count of Session.csv</td>
  </tr>
  <tr>
    <td>Engagement.csv</td>
  </tr>
  <tr>
    <td>Behavior Flow.csv</td>
  </tr>
  <tr>
    <td>Devices</td>
    <td>Devices.csv</td>
  </tr>
  <tr>
    <td>Social</td>
    <td>Social Network Referral.csv</td>
  </tr>
  <tr>
    <td rowspan="2">Site Content</td>
      <td>Site Content_All Pages.csv</td>
  </tr>
  <tr>
    <td>Site Content_Landing Page.csv</td>
  </tr>
  <tr>
    <td rowspan="2">Events</td>
      <td>Events.csv</td>
  </tr>
  <tr>
    <td>Events_Pages.csv</td>
  </tr>
</table>

## Logic Flow
1.	Enable Google Analytics API in [Google API Console](https://console.developers.google.com/flows/enableapi?apiid=analytics&credential=client_key) to get service key
2.	Execute ```AnalyticsReporting_Main.py``` to trigger other scripts
3.	Read configuration from ```config.txt```
4.	Connect to GA through ```client_secrets.json```
5.	Capture data for each table respectively
6.	Save data as CSV files

## How to Execute
### Install packages
```
pip install -r requirements.txt
```

### Run the script
```
python AnalyticsReporting_Main.py
```
***
Copyright © 2019 [Andy Lin](https://github.com/andy2167565). All rights reserved.
