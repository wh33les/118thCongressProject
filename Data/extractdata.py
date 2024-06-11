# Modules

# To list files in a directory
import os

# Time for execution of the code
import time # for debugging

# For .json files
import json

# For data frames
import pandas as pd

# Count dictionary values
from collections import Counter

# Pick a random item from a list
import random

# Print dictionaries prettily
import pprint

# Functions

# Takes in a politician's id (as an integer) and makes a dictionary with the politicians's
# name, party, and state.
def politician_info(politician_id):
    with open('2023-2024_118th_Congress\\people\\'+str(politician_id)+'.json', 'r') as voter_file:
        voter_obj = json.load(voter_file)
        info = {
            "name":voter_obj["person"]["name"],
            "party":voter_obj["person"]["party"],
            "state":voter_obj["person"]["district"][3:5],
        }
        return info

# Takes in a vote's id (as an integer) and gets the votes, with parties and states, and the counts, 
# as a dictionary.
def roll_call_info(roll_call_id):
    with open('2023-2024_118th_Congress\\vote\\'+str(roll_call_id)+'.json', 'r') as vote_file:
        vote_obj = json.load(vote_file)
        info = {
            "people":[]
        }
        # Fill in the people dictionaries
        roll_call_votes = vote_obj["roll_call"]["votes"]
        for vote in roll_call_votes:   
            rc_vt_index = roll_call_votes.index(vote)
            voter = politician_info(roll_call_votes[rc_vt_index]["people_id"])
            voter["vote"] = roll_call_votes[rc_vt_index]["vote_text"]
            info["people"].append(voter)
        # Add the numbers of each type of vote for each party
        c_yea = Counter()
        c_nay = Counter()
        c_absent = Counter()
        c_nv = Counter()
        for item in info["people"]:
            if item["vote"] == "Yea":
                c_yea[item["party"]] += 1
            if item["vote"] == "Nay":
                c_nay[item["party"]] += 1
            if item["vote"] == "Absent":
                c_absent[item["party"]] += 1   
            if item["vote"] == "NV":
                c_nv[item["party"]] += 1    
        info["Yea"] = dict(c_yea)
        info["Nay"] = dict(c_nay)
        info["Absent"] = dict(c_absent)
        info["NV"] = dict(c_nv)
        return info
		
# Functions, cont.

# Create a dictionary item for a bill, given its name in the file format given by legiscan, no extension.
def bill_metadata(bill_name):   
    with open("2023-2024_118th_Congress\\bill\\"+bill_name+".json", 'r') as bill_file:
        # Convert to a python object
        obj = json.load(bill_file)

        # Initialize a dictionary with the data I want about the bill
        bill = {
            "chamber":obj["bill"]["body"], 
            "bill_type":obj["bill"]["bill_type"],
            "title":obj["bill"]["bill_number"]+":  "+obj["bill"]["title"],
            "summary":obj["bill"]["description"],
            "introduced":obj["bill"]["history"][0]["date"]
        }

        # Sponsor(s)
        # Get the people with their party and state
        bill["sponsor(s)"]={
            "people":[]
        }
        sps = obj["bill"]["sponsors"]
        for sponsor in sps:
            sp_index = sps.index(sponsor)
            with open('2023-2024_118th_Congress\\people\\'+str(sps[sp_index]["people_id"])+'.json', 'r') as voter_file:
                    voter_obj = json.load(voter_file)

                    # Append dictionary
                    bill["sponsor(s)"]["people"].append(politician_info(sps[sp_index]["people_id"]))   
        # Add the number of each party
        c_party = Counter()
        for item in bill["sponsor(s)"]["people"]:
            c_party[item["party"]] += 1
        bill["sponsor(s)"].update(c_party)            

        # Add the subject(s) of the bill
        bill["subject(s)"]=[]
        for subject in obj["bill"]["subjects"]:
            bill["subject(s)"].append(subject["subject_name"])

        # Number of actions and latest action
        bill["actions"] = len(obj["bill"]["history"])
        bill["latest_action"] = obj["bill"]["history"][len(obj["bill"]["history"])-1]["action"]

        # Phase
        
        hist = obj["bill"]["history"]
        bill["pass_house"] = {}
        bill["pass_senate"] = {}
        bill["became_law"]= {}
        
        # Find in the history whether it passed
        house_vote = list(filter(lambda event: (event["action"].startswith("On passage Passed") or
            "Agreed to by the Yeas and Nays" in event["action"]
            or "Agreed to by voice vote" in event["action"]) and event["chamber"]== "H", hist))
        senate_vote = list(filter(lambda event: event["action"].startswith("Passed Senate") 
            or "passed without amendment by Unanimous Consent" in event["action"]
            or ("passed" in event["action"] and event["chamber"] == "S"), hist))
        signed_by_pres = list(filter(lambda event: event["action"].startswith("Became Public Law"), hist))
        
        # Date, if passed
        # House
        bill["pass_house"]["passed"] = (len(house_vote) != 0)
        if bill["pass_house"]["passed"] == True:
            bill["pass_house"]["date"] = house_vote[0]["date"]
        else:
            bill["pass_house"]["date"] = ""
        # Senate
        bill["pass_senate"]["passed"] = (len(senate_vote) != 0)
        if bill["pass_senate"]["passed"] == True:
            bill["pass_senate"]["date"] = senate_vote[0]["date"]
        else:
            bill["pass_senate"]["date"] = ""
        # Law
        bill["became_law"]["signed"] = (len(signed_by_pres) != 0)
        if bill["became_law"]["signed"] == True:
            bill["became_law"]["date"] = signed_by_pres[0]["date"]
        else:
            bill["became_law"]["date"] = ""
        
        # Votes, if passed   
        votes = obj["bill"]["votes"]
        # House
        vote_to_pass_house = list(filter(lambda roll_call: 
            (roll_call["desc"].startswith("On Passage") 
            or roll_call["desc"].startswith("On Motion to Suspend the Rules and Pass"))
            and roll_call["chamber"]=="H", votes))
        if len(vote_to_pass_house) != 0:
            #print("vote_to_pass_house:") # for debugging
            #print(vote_to_pass_house) # for debugging
            vt_index = votes.index(vote_to_pass_house[0])
            bill["pass_house"]["votes"] = roll_call_info(votes[vt_index]["roll_call_id"])
        elif bill["pass_house"]["passed"] == True:
            bill["pass_house"]["votes"] = "Voice vote"
        else:
            bill["pass_house"]["votes"] = {}
        # Senate
        vote_to_pass_senate = list(filter(lambda roll_call: 
            (roll_call["desc"].startswith("On Passage") or roll_call["desc"].startswith("On the Joint Resolution")) 
            and roll_call["chamber"]=="S", votes))
        if len(vote_to_pass_senate) != 0:
            #print("vote_to_pass_senate:") # for debugging
            #print(vote_to_pass_senate) # for debugging
            vt_index = votes.index(vote_to_pass_senate[0])
            bill["pass_senate"]["votes"] = roll_call_info(votes[vt_index]["roll_call_id"])
        else:
            if bill["pass_senate"]["passed"] == True:
                bill["pass_senate"]["votes"] = {
                    "people":"Unanimous",
                    "Yea":{"D":48, "R":49, "I":3},
                    "Nay":{},
                    "Absent":{},
                    "NV":{}
                }
            else:
                bill["pass_senate"]["votes"] = {}
            
        # Return
        return bill
        
# List all the bills

raw_bills_files_list = os.listdir("2023-2024_118th_Congress\\bill")
#print(raw_bills_files_list) # for debugging
print("There are "+str(len(raw_bills_files_list))+" bills.") # for debugging

# Choose a bill
which_bill = "HB3935" #input("Choose a bill (input the appreviation according to the file name format, \
#without the extension) or type Random for a random bill.\n") 
if which_bill == "Random":
    selected_bill = random.choice(raw_bills_files_list).split(".")[0]
else:    
    selected_bill = which_bill 
selected_index = raw_bills_files_list.index(selected_bill+".json")

# Print the original file
print("Selected the "+str(selected_index+1)+"th bill, "+selected_bill+".\n")
print("Here is the original file:")
with open("2023-2024_118th_Congress\\bill\\"+selected_bill+".json", 'r') as bill_file:
    # Convert to a python object
    obj = json.load(bill_file)

    # See the contents of bill_file, formatted nicely
    json_formatted_str = json.dumps(obj, indent=4) 
    print(json_formatted_str) 
    
# Print my metadata
print("\nHere is my metadata:")
pprint.pprint(bill_metadata(selected_bill), sort_dicts=False)