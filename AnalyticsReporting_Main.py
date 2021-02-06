#!/usr/bin/python3.4
import os
import time


start_time = time.time()
print('============== Start data extraction ==============')

script_path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_path, 'outputs')

for file in os.listdir(script_path):
    if file.endswith(".py") and file != 'AnalyticsReporting_Main.py':
        os.system('python ~/ga/%s' % file)

file_num = 0
for file in os.listdir(filepath):
    if file.endswith(".csv"):
        file_num += 1

print('===================================================')
print('Number of tables generated = %d' % file_num)
print('Total execution time = %s seconds' % (time.time() - start_time))
print('===================================================')
