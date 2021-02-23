# Python script for helping a small, rural town modernize its vote counting process.
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
fname = 'election_data.csv' # Data/Resource file name
ffolder = 'Resources' # Data/Resource folder nameif 
reportfile = 'ElectionResults.txt' # Output text file name

#logging.info("Opening path started", os.path.join(ffolder, fname) )
csvData = os.path.join(ffolder, fname)

#Some output formatting
linebreak = "-------------------------"

# Write to file
outfile = open(reportfile, "w")
original = sys.stdout
sys.stdout = Tee(sys.stdout, outfile)


########################  Main Section ######################################

# Formating Display
print("Election Results")
print(linebreak)

### Read in the CSV file
with open(csvData, 'r') as csvfile:
    logging.debug("Open file: %s", csvData)
    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter=',')
    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    logging.info("CSV Headers: %s", csv_header)
    #csv_record_count = len(list(csvreader))  ## this is number of lines After Header 
    #logging.info("Total Entries %s", csv_record_count) 
    
    county_dict = {}
    candidate_dict = {}
    #county_votes = {}
    #candidate_votes = {}
    vote_count = 0

    # The dataset is composed of three columns: Voter ID, County, and Candidate. 
    for row in csvreader :  # This would be so much easier using pandas.
        vote_count = vote_count + 1
        # # Track by county    >>>  WILL have to fix later
        # if row[1] in county_votes.keys():
        #     logging.info('%s County Key Exists', row[1])
        #     if row[2] in county_votes[row[1]].items():
        #         logging.info('%s County key with %s Candidate Key Exists', row[1], row[2])
        #         county_votes[row[1]][row[2]] = county_votes[row[1]][row[2]] + 1
        #     else:
        #         logging.info('%s County key with %s Does not exist', row[1], row[2])
        #         county_votes[row[1]][row[2]] = 1
        # else:
        #     logging.info('%s County Key Does not Exist', row[1])
        #     county_votes[row[1]] = {row[2]:1}

        #Candidate Votes
        if row[2] in candidate_dict.keys():
            #logging.info('%s Candidate Key Exists', row[2])
            candidate_dict[row[2]] = candidate_dict[row[2]] + 1
        else:
            #logging.info('%s Candidate Key Does not Exist', row[2])
            candidate_dict[row[2]] = 1
    
# The total number of votes cast
number_candidates = len(candidate_dict)
#print(f"{number_candidates} Candidates Voted For!")
print(f"Total Votes: ", vote_count)
print(linebreak)
# A complete list of candidates who received votes
for key, val in candidate_dict.items():
    pvotes = round(((val / vote_count)*100), 2)
    print(f"{key}: {pvotes:.3f}% ({val})")
# The percentage of votes each candidate won
# The total number of votes each candidate won
print(linebreak)
# The winner of the election based on popular vote
winner = max(candidate_dict, key=candidate_dict.get)
print(f"Winner: {winner}")
print(linebreak)

# Set stdout back to the original
sys.stdout = original
outfile.close()

########### Criteria ##################
# The dataset is composed of three columns: Voter ID, County, and Candidate. 

    # The total number of votes cast
    # A complete list of candidates who received votes
    # The percentage of votes each candidate won
    # The total number of votes each candidate won
    # The winner of the election based on popular vote

########## EXAMPLE OUTPUT ####################
#    Election Results
# -------------------------
# Total Votes: 3521001
# -------------------------
# Khan: 63.000% (2218231)
# Correy: 20.000% (704200)
# Li: 14.000% (492940)
# O'Tooley: 3.000% (105630)
# -------------------------
# Winner: Khan
# -------------------------

#In addition, your final script should both print the analysis to the terminal and export a text file with the results.