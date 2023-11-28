import json
from collections import defaultdict
from datetime import datetime


'''
Programming Exercise:
Using the language of your choice, write a small application that:
• Reads all data from a .Json file (use the attached file trainings.txt).
• Generate output as JSON in the three following ways.
    • (task 1) List each completed training with a count of how many people have completed that training.
    • (task 2) Given a list of trainings and a fiscal year, (defined as 7/1/n-1 - 6/30/n), for each specified training, list all the that completed the training in the specified fiscal year.      
        • Use parameters: Trainings = "Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"; Fiscal Year = 2024
    • (task 3) Given a date, find all people that have any completed trainings that have already expired, or will expire within one month of the specified date (A training is considered expired the day after its expiration date). For each person found, list each completed training that met the previous criteria, with an additional field to indicate expired vs expires soon.
        • Use date: Oct 1St, 2023

• A note for all tasks. It is possible for a person to have completed the same training more than once. In this event, only the most recent completion should be considered.
Requirements for the above application:
• The app should work with any data in the specified format.
• The app should be checked into a publicly accessible Github or Azure Devops repository that the reviewers can pull and run, without any modification.
• In addition to the application code, your repository should contain the three output Json files.
'''

####################################################################################################################################################
# function that loads the input file
def load_data(file_name):
    # read the json file
    print ("Reading the json file...\n")
    f = open(file_name)
    # parse the json file
    data = json.load(f)
    f.close()
    return data


####################################################################################################################################################
# function that finds the most recent completion for each training for each person based on latest completion date/timestamp
def find_latest_completions ( data ) :
    # Dictionary to store the most recent completion for each training for each person
    person_latest_completion = defaultdict(dict)

    # handle different cases of date/timestamp formats
    date_formats = ["%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d"]
    
    # Find the most recent completion for each training for each person
    for person in data:
        person_name = person["name"]
        for completion in person["completions"]:
            certificate_name = completion["name"]
            timestamp = completion["timestamp"]
                        
            timestamp_date = None
            # try each format from the list "date_formats" and find which works the best
            for fmt in date_formats:
                try:
                    timestamp_date = datetime.strptime(timestamp, fmt)
                    break  # If successful, exit the loop
                except ValueError:
                    pass  # If parsing fails, try the next format 

            if timestamp_date is not None:
                timestamp_str = timestamp_date.strftime("%m/%d/%Y") 
                # if the certificate is not in the list of trainings
                if certificate_name not in person_latest_completion[person_name]:
                    person_latest_completion[person_name][certificate_name] = timestamp_str
                else:
                    # Update the timestamp if the current completion is more recent
                    curr_date = datetime.strptime(person_latest_completion[person_name][certificate_name], "%m/%d/%Y")
                    if timestamp_date > curr_date:
                        person_latest_completion[person_name][certificate_name] = timestamp_str

    return person_latest_completion


####################################################################################################################################################
# task 1 function - List each completed training with a count of how many people have completed that training.
def task1(data):
    print ("Task 1 is initiated")
    
    person_latest_completion = find_latest_completions(data)

    # Count unique certificates based on the most recent completion across all individuals
    certificate_counts = defaultdict(int)
    for person_certificates in person_latest_completion.values():
        for certificate, timestamp in person_certificates.items():
            certificate_counts[certificate] += 1

    # Convert certificate_counts to a list of dicts
    certificate_counts_list = [{"Name": certificate_name, "Completed": count} for certificate_name, count in certificate_counts.items()]

    certificate_counts_list.sort(key=lambda x: x["Name"])

    # generate a output json file that should contain the following: certificate_counts_list

    # save the json file using file
    file_path = 'completed_training_count.json'

    with open(file_path, 'w') as outfile:
        json.dump(certificate_counts_list, outfile, indent=4)

    print("Task 1 is completed, look for 'completed_training_count.json' file in the same directory\n")


####################################################################################################################################################
# task 2 function - 
# Given a list of trainings and a fiscal year, (defined as 7/1/n-1 - 6/30/n), for each specified training, list all the that completed the training in the specified fiscal year.      
#     • Use parameters: Trainings = "Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"; Fiscal Year = 2024
def task2 (data, trainings, fiscal_year):
    print ("Task 2 is initiated")
    # Dictionary to store the most recent completion for each training for each person
    person_latest_completion = find_latest_completions(data)

    # Dictionary to store people who completed trainings in the specified fiscal year
    people_completed_trainings = defaultdict(list)

    # Define the fiscal year start and end dates
    fiscal_year_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)

    # Checking if the previous year would result in a negative value, then setting it to 1
    if fiscal_year - 1 < 1:
        fiscal_year_start = datetime(1, 7, 1)

    # Iterating through collected completion data to find people who completed trainings in the specified fiscal year
    for person, completions in person_latest_completion.items():
        for training in trainings:
            if training in completions:
                completion_date = datetime.strptime(completions[training], "%m/%d/%Y")
                # Checking if completion date falls within the fiscal year
                if fiscal_year_start <= completion_date <= fiscal_year_end:
                    people_completed_trainings[training].append(person)

    # Generating output as a list of dictionaries
    people_completed_trainings_list = [{"Training": training, "People": people} for training, people in people_completed_trainings.items()]

    # Sorting the list by training name
    people_completed_trainings_list.sort(key=lambda x: x["Training"])
    # generate a output json file that should contain the following: people_completed_trainings_list

    # save the json file using file
    file_path = 'people_completed_trainings.json'

    with open(file_path, 'w') as outfile:
        json.dump(people_completed_trainings_list, outfile, indent=4)

    print("Task 2 is completed, look for 'people_completed_trainings.json' file in the same directory\n")


####################################################################################################################################################
# task 3 function -
# Given a date, find all people that have any completed trainings that have already expired, or will expire within one month of the specified date (A training is considered expired the day after its expiration date). For each person found, list each completed training that met the previous criteria, with an additional field to indicate expired vs expires soon.
#   • Use date: Oct 1St, 2023
def task3( data, given_date ) :
    print ("Task 3 is initiated")
    # Dictionary to store the most recent completion for each training for each person
    person_latest_completion = find_latest_completions(data)

    # Dictionary to find all people that have any completed trainings that have already expired or will expire in one month
    # ppl_expired_training = defaultdict(list)

    specified_date = given_date  # October 1st, 2023

    # Dictionary to store people with expired or expiring trainings and their respective completion details
    expired_or_expiring_trainings = defaultdict(list)

    # Iterate through the completion data to check for expired or expiring trainings
    for person, completions in person_latest_completion.items():
        for certificate, completion_date_str in completions.items():
            completion_date = datetime.strptime(completion_date_str, "%m/%d/%Y")
            # Calculate the difference between completion date and specified date
            days_until_expiry = (completion_date - specified_date).days
            if days_until_expiry < 0 or days_until_expiry <= 30:
                # Check if the completion has expired or will expire within one month of the specified date
                status = "expired" if days_until_expiry < 0 else "expires soon"
                expired_or_expiring_trainings[person].append({"certificate": certificate, "status": status})

    # Generating output for people with expired or expiring trainings
    output_expired_or_expiring = [{"person": person, "trainings": trainings} for person, trainings in expired_or_expiring_trainings.items()]

    # Saving the output to a JSON file or processing it further as needed
    file_path = 'expired_or_expiring_trainings.json'
    with open(file_path, 'w') as outfile:
        json.dump(output_expired_or_expiring, outfile, indent=4)

    print("Task 3 is completed, look for 'expired_or_expiring_trainings.json' file in the same directory\n")



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
# main:

print ("Welcome to the Assesment app!!\n")

# load the data
json_filename = 'trainings.txt'
loaded_file_data = load_data(json_filename)

# task 1
task1(loaded_file_data)

# task 2
# List of trainings
trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]

# Fiscal Year
fiscal_year = 2024
task2(loaded_file_data, trainings, fiscal_year)


# task 3
# Given date to find Oct 1st, 2023
given_date = datetime(2023, 10, 1)
task3(loaded_file_data, given_date)

print ("Thank you for using the Assesment app!!\n")
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
