#!/usr/bin/env python3
# Traffic data parser
# Copyright 2018, Aswin Babu Karuvally

# import essential libraries
import csv
import argparse
from datetime import datetime
import xlsxwriter

# extract contents form the csv file
def extract_data(csv_contents, report_file):
    # declare essential variables
    detector_1 = {}
    detector_2 = {}
    vehicle_count = 0
    row_count = 1

    # open the excel file
    workbook = xlsxwriter.Workbook(report_file)
    worksheet = workbook.add_worksheet()

    # format the worksheet
    worksheet.set_column('A:A', 18)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 15)
    bold = workbook.add_format({'bold': True})

    # add headers to worksheet
    worksheet.write(0, 0, 'Unique ID', bold)
    worksheet.write(0, 1, 'Entry Time', bold)
    worksheet.write(0, 2, 'Exit Time', bold)
    worksheet.write(0, 3, 'Time Difference', bold)

    # separate data from two detectors
    for row in csv_contents:
        # ignore empty rows
        if len(row) > 4:
            if row[0] == 'DET001':
                detector_1.update({row[2]: row[1]})
            elif row[0] == 'DET002':
                detector_2.update({row[2]: row[1]})

    # select only vehicles in both detectors
    for unique_id in detector_1:
        if unique_id in detector_2:
            vehicle_count += 1

            # create time object from the start and end time
            entry_time = datetime.strptime(detector_1[unique_id],
            '%Y-%m-%d %H:%M:%S')

            exit_time = datetime.strptime(detector_2[unique_id],
            '%Y-%m-%d %H:%M:%S')

            # find the absolute time difference
            time_difference = exit_time - entry_time

            # add contents to the report
            worksheet.write(row_count, 0, unique_id)
            worksheet.write(row_count, 1,
            entry_time.strftime('%Y-%m-%d %H:%M:%S'))
            
            worksheet.write(row_count, 2,
            exit_time.strftime('%Y-%m-%d %H:%M:%S'))

            worksheet.write(row_count, 3, str(time_difference))

            # increment the row count
            row_count += 1

    # close the workbook
    workbook.close()


# the main function
def main():
    # declare valid arguments
    parser = argparse.ArgumentParser(description=
    'Simple script to parse through the traffic data')

    parser.add_argument('source')
    parser.add_argument('report')
    arguments = parser.parse_args()

    # open the csv file
    try:
        csv_file = open(arguments.source)
    except IOError:
        print('unable to read the file, exiting...')
        exit()

    # parse the csv file
    csv_contents = csv.reader(csv_file)

    # extract data and output to excel file
    extract_data(csv_contents, arguments.report)

# call the main function
main()
