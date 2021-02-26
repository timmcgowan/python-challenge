# Python script for analyzing the financial records of your company. 
# financial dataset = budget_data.csv.
# composed of two columns: Date and Profit/Losses. 
import logging
import os
import csv
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Ensure your working dir is were you are running the script
logging.basicConfig(filename='debug.log',level=logging.DEBUG) # Because I prefer logs
logging.info("Analysis Initiated")
logging.info(os.path.dirname(os.path.abspath(__file__)))

## Got help on this one -> https://stackoverflow.com/questions/11325019/how-to-output-to-the-console-and-file/45917982
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

# Data Files - Variables to make my code reusable for the next project (DRY)
fname = 'budget_data.csv' # Data/Resource file name
ffolder = 'Resources' # Data/Resource folder nameif 
afolder = 'Analysis' # Data/Resource folder nameif 
afilename = 'tmcgowan_results.txt' # Output text file name

#logging.info("Opening path started", os.path.join(ffolder, fname) )
csvData = os.path.join(ffolder, fname)
if not os.path.exists(afolder):
    os.makedirs(afolder)
reportfile = os.path.join(afolder, afilename)

#Some output formatting
linebreak = "-------------------------------------"

# Math helper (change)
def vchange(curr,prev):
    try:
        return(curr - prev)
    except TypeError:
        logging.error('Can not perform math on non-numbers', curr, prev)
        exit()  


# Write to file
f = open(reportfile, "w")
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)

# Formating Display
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
    change_values = {} # Changes month to month
    previous_value = 0
    first_value = None
    ftotal = 0

    value_dict = {rows[0]:int(rows[1]) for rows in csvreader}

    for month, val in value_dict.items():
        if first_value is None: 
            first_value = val #Hold first dollar value
            previous_value = first_value # hold for math
            logging.debug("First Value : %s", first_value)
            change_values[month] =  0
        else :
            logging.debug("Previous Value : %s", previous_value)
            change_values[month] = vchange(val,previous_value)
            logging.debug("Adding change value: %s", change_values[month])
        previous_value = val
        logging.debug("Updated Previous Value: %s", previous_value)
        #ftotal = ftotal + int(row[1])

    print('Total Months: ', len(value_dict))
    ftotal = sum(value_dict.values()) 
    # The net total amount of "Profit/Losses" over the entire period
    print('{0} ${1:{grp}d}'.format('Total: ', ftotal, grp=','))
    # Calculate the changes in "Profit/Losses" over the entire period, then find the average of those changes
    average_monthly_change = sum(change_values.values()) / len(change_values.keys())
    print('{0} ${1:.2f}'.format('Average Change: ', int(average_monthly_change)))
    
    minMonth = min(change_values, key=change_values.get)
    maxMonth = max(change_values, key=change_values.get)
    
    # The greatest increase in profits (date and amount) over the entire period
    print('{0} {1} (${2})'.format('Greatest Increase in Profits: ', maxMonth, change_values[maxMonth]))

    # The greatest decrease in losses (date and amount) over the entire period
    print('{0} {1} (${2})'.format('Greatest Decrease in Profits: ', minMonth, change_values[minMonth]))

  
    # Reset back to the original & close results file
    sys.stdout = original
    f.close()
###  EXAMPLE OUTPUT
# Financial Analysis
# ----------------------------
# Total Months: 86
# Total: $38382578
# Average  Change: $-2315.12
# Greatest Increase in Profits: Feb-2012 ($1926159)
# Greatest Decrease in Profits: Sep-2013 ($-2196167)
