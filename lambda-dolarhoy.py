import json 
import boto3 
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

#function definition 
def lambda_handler(event,context): 
    dynamodb = boto3.resource('dynamodb') 
    #table name 
    table = dynamodb.Table('dolarhoy') 
    #inserting values into table 
    
    url = 'https://dolarhoy.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text)
    results = soup.find_all("div", class_="val")
    
    ds = (datetime.today() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    
    response = table.put_item( 
       Item={ 
            "ds":ds,
            'blue-c': re.sub('\$','', results[0].text),
            'blue-v': re.sub('\$','', results[1].text),
            'oficial-c': re.sub('\$','', results[4].text),
            'oficial-v': re.sub('\$','', results[5].text),
            'bolsa-c': re.sub('\$','', results[6].text),
            'bolsa-v': re.sub('\$','', results[7].text),
            'ccl-c': re.sub('\$','', results[8].text),
            'ccl-v': re.sub('\$','', results[9].text),
            'cripto-c': re.sub('\$','', results[10].text),
            'cripto-v': re.sub('\$','', results[11].text),  
            'solidario': re.sub('\$','', results[12].text)
        } 
    ) 
    return response
