# Create a script that uses the Survey Monkey (https://www.surveymonkey.com) service,
# creates a survey, and sends an invitation to go through it.
# The script should accept a JSON file with questions for the survey and a text file with a list of email addresses.
# There should be at least 3 questions and 2 recipients.

import os
import sys
import json
import re
import argparse
import requests


parser = argparse.ArgumentParser(description="Creates a Survey Monkey survey, and sends invitation to email addresses. Needs the API Access Token stored in the $SRVY_API_KEY env variable.")
parser.add_argument("questions", type=str, help="Json file with questions for the survey")
parser.add_argument("email", type=str, help="Text file with the email addresses (one per line)")
args = parser.parse_args()

api_key = os.environ["SRVY_API_KEY"]

base_header = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    'Authorization': "Bearer "+api_key
    }

with open(args.questions) as file:


    #convert the json file to the API request format. I'm not very proud of this one
    body = []
    for survey in json.load(file).items():
        pages = []
        for page in survey[1].items():
            questions = []
            for number, question in enumerate(page[1].items(), start=1):
                choices = []
                for desc_and_answer in question[1].items():
                    if desc_and_answer[0]=="Description":
                        heading = {"heading": desc_and_answer[1]}
                    elif desc_and_answer[0]=="Answers":
                        answers = []
                        for answer in desc_and_answer[1]:
                            answers.append({"text": answer})
                        choices += answers
                answers = {"answers": {"choices:": choices}}
                question_complete={
                    "headings": [heading],
                    "position": number,
                    "family": "single_choice",
                    "subtype": "vertical",
                    "answers":{
                           "choices": choices 
                        }
                    }
                questions.append(question_complete)
            pages.append({"questions": questions})
        
        body = {"title": survey[0], "pages": pages}
    
    #read, load and check the email file
    emails = []
    with open(args.email) as file_mail:
        for num, line in enumerate(file_mail.readlines(),start=1):
            if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', line.strip()):
                emails.append(line.strip())
            else:
                print("There is an invalid email address in the file provided!")
                print("Line",num)
                print(line)
                sys.exit(1)
        if not emails:
            print("The file provided is empty, please provide at least one address")
            sys.exit(1)
    #send the api requests
    print("Trying to create the survey api request...")
    survey_response = requests.post("https://api.surveymonkey.com/v3/surveys",headers=base_header, json=body, timeout=20)

    if survey_response.status_code in range(200,299):
        print("Survey created sucessfully!")
        survey_id = survey_response.json()["id"]
    else:
        print("There was a problem with the api request!")
        print(json.dumps(survey_response.json(),indent=2))
        sys.exit(1)
    
    print("Sending the email api requests...")
    collector_request = requests.post(f"https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors",headers=base_header, json={"type": "email"}, timeout=20)
    if collector_request.status_code not in range(200,299):
        print("There was a problem with the collector api request!")
        print(json.dumps(collector_request.json(),indent=2))
        sys.exit(1)
    collector_id = collector_request.json()["id"]

    message_request = requests.post(f"https://api.surveymonkey.com/v3/collectors{collector_id}/messages",headers=base_header, json={"type": "email"}, timeout=20)
    if message_request.status_code not in range(200,299):
        print("There was a problem with the message api request!")
        print(json.dumps(message_request.json(),indent=2))
        sys.exit(1)
    message_id = message_request.json()["id"]

    recepients_body = [{"email": email} for email in emails]

    recepients_request = requests.post(f"https://api.surveymonkey.com/v3/collectors{collector_id}/messages/{message_id}/recipients/bulk",headers=base_header, json={"contacts": recepients_body}, timeout=20)
    if recepients_request.status_code not in range(200,299):
        print("There was a problem with the recipients api request!")
        print(json.dumps(recepients_request.json(),indent=2))
        sys.exit(1)
    
    send_message = requests.post(f"https://api.surveymonkey.com/v3/collectors{collector_id}/messages/{message_id}/send",headers=base_header, timeout=20)
    if message_request.status_code not in range(200,299):
        print("There was a problem with the send api request!")
        print(json.dumps(message_request.json(),indent=2))
        sys.exit(1)
    else:
        print("The emails were sent sucessfully!")

    
