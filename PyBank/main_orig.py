# Python script for analyzing the financial records of your company. 
# financial dataset = budget_data.csv. 
# composed of two columns: Date and Profit/Losses. 
# (Thankfully, your company has rather lax standards for accounting so the records are simple.)

import logging
import os
import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Ensure your working dir is were you are running the script
logging.basicConfig(filename='debug.log',level=logging.DEBUG) # Because I prefer logs
logging.info("Analysis Initiated")
logging.info(os.path.dirname(os.path.abspath(__file__)))

# Data Files - Variables to make my code reusable for the next project (DRY)
fname = 'budget_data.csv' # Data/Resource file name
ffolder = 'Resources' # Data/Resource folder nameif 

#logging.info("Opening path started", os.path.join(ffolder, fname) )
csvData = os.path.join(ffolder, fname)

#Some output formatting
linebreak = "-------------------------------------"

# Math helper (change)
def vchange(curr,prev):
    try:
        return(curr - prev)
    except ValueError:
        logging.error('Can not perform math on non-numbers', curr, prev)
        exit()  

def pchange(curr,prev):
    if curr == prev:
        return 100
    try:
        return(abs(curr - prev) / prev) * 100
    except ZeroDivisionError:   #For the 0 issue
        return 0  

# Formating Display
for i in range(4): 
    print(" ")
print("Financial Analysis")
print(linebreak)

# Read in the CSV file
with open(csvData, 'r') as csvfile:
    logging.debug("Open file: %s", csvData)
    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter=',')
    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    logging.info("CSV Headers: %s", csv_header)
    #csv_record_count = len(list(csvreader))  ## this is number of lines After Header 
    #logging.info("Total Entries %s", csv_record_count) 

# Analyze the records to calculate each of the following:
    # The total number of months included in the dataset
    list_months = [] # Used to rack and count "unique", not just rows.
    list_values = [] # Used to rack & count values
    change_values = [] # Changes month to month
    previous_value = 0
    first_value = None
    ftotal = 0

    for row in csvreader:
        list_months.append(row[0])
        if first_value is None: 
            first_value = int(row[1]) #Hold first dollar value
            previous_value = int(row[1]) # hold for math
        
        list_values.append(int(row[1]))
        logging.debug("Previous Value : %s", previous_value)
        change_value = vchange(int(row[1]), previous_value)
        logging.debug("Adding change value: %s", vchange)
        change_values.append(change_value)
        previous_value = int(row[1])
        logging.debug("Updated Previous Value: %s", previous_value)
        #ftotal = ftotal + int(row[1])
    print('Total Months: ', len(list_months))
    ftotal = sum(list_values) 
    # The net total amount of "Profit/Losses" over the entire period
    print('{0} ${1:{grp}d}'.format('Total: ', ftotal, grp=','))
    # Calculate the changes in "Profit/Losses" over the entire period, then find the average of those changes
    average_monthly_change = sum(change_values) / len(change_values)
    print('{0} ${1:.2f}'.format('Average Change: ', int(average_monthly_change), ))

# The greatest increase in profits (date and amount) over the entire period
    

# The greatest decrease in losses (date and amount) over the entire period

# Output to terminal and text file. 

###  EXAMPLE OUTPUT
# Financial Analysis
# ----------------------------
# Total Months: 86
# Total: $38382578
# Average  Change: $-2315.12
# Greatest Increase in Profits: Feb-2012 ($1926159)
# Greatest Decrease in Profits: Sep-2013 ($-2196167)
