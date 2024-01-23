import requests
import pandas as pd
from datetime import datetime
import json
import streamlit as st

############################
# FETCH UP TO DATE API TOKEN 
url = "https://api.amazon.com/auth/o2/token"


rtoken = st.secrets["rtoken"]
client_id = st.secrets["client_id"]
client_secret =  st.secrets["client_secret"]


body = {
        "refresh_token": f"{rtoken}",
        "client_id":f"{client_id}",
        "client_secret":f"{client_secret}",
        "grant_type":"refresh_token"
        }

try:
    response = requests.post(url, json=body)

        # Checking if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        #print(response.text)
        print("token is:")
        data = json.loads(response.text)
        lwa_token = data['access_token']
        print(lwa_token)
    else:
        print("Request failed with status code:", response.status_code)
except:
    print("well that didn't work hmmm")


########################
# PAGE BODY - CURRENT CAMPAIGN TABLE
st.header('Current campaigns')

# GET ALL CAMPAIGNS
url = "https://api.eu.amazonalexa.com/v1/proactive/campaigns"

headers = {
    "Host": "api.eu.amazonalexa.com",
    "Accept": "application/json",
    "Authorization": f"Bearer {lwa_token}"
}

#Making the GET request
response = requests.get(url, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    print("Request successful!")
else:
    print("Request failed with status code:", response.status_code)
    
## CREATE A FUNCTION TO CREATE A TABLE OF ALL CORE FUNCTION INFORMATION
# List to store flattened data
flattened_data = []

# Iterate through the JSON to extract relevant data
for item in parsed_json['results']:
    campaign_id = item['campaignId']
    for variant in item['suggestion']['variants']:
        # There might be multiple content values in each variant
        for content_value in variant['content']['values']:
            locale = content_value['locale']
            body = content_value['datasources']['displayText']['body']
            title = content_value['datasources']['displayText']['title']
            img = content_value['datasources']['background']['backgroundImageSource']
            
            # Append the extracted data to the list
            flattened_data.append({
                'campaignId': campaign_id,
                'locale': locale,
                'body': body,
                'title': title,
                'img': img
            })

# Create DataFrame
dfCampaigns = pd.DataFrame(flattened_data)

# Display the DataFrame
st.dataframe(dfCampaigns)
    
    
    
# review data for list of campaigns
#review_data = response.text

# DELETE A CAMPAIGN


# ADD A CAMPAIGN


# GET ALL UNIT IDS


# PAGE HEADINGS AND FILE UPLOAD FOR LOADING CAMPAIGNS
#st.write('Please upload the unit ids')
#st.text('Note: this should include the fields: Customer Search Term, Spend, 14 Day Total Sales, Campaign Name')