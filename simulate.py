import requests
import time
import random
import os
from dotenv import load_dotenv
from logger import log_data

load_dotenv()
API_URL=os.getenv("API_URL")
if API_URL is None:
    print("API_URL is missing")
else:
    print("API_URL:",API_URL)
sections= ['Kiln','Cement Mill','Crusher']
components= ['Ball Mill','Roller Press','Vertical Mill']
subcomponents= ['Gearbox','Hydraulic System','Mill Bearing','Motor']

while True:
    try:
        component=random.choice(components)
        subcomponent=random.choice(subcomponents)
        section=random.choice(sections)
        Payload={
            "machine_age_days":random.randint(100,2000),
            "temperature":random.uniform(30,100),
            "vibration":random.uniform(2,10),
            "pressure":random.uniform(6,30),
            "component":component,
            "subcomponent":subcomponent,
            "section":section
        }
        response=requests.post(API_URL,json=Payload)
        results=response.json()[0]
        log_data(Payload,results)
        print("----NeW DATA---")
        print(f"MACHINE: {section} | {component} | {subcomponent}")
        print("Failure Probability",results["Failure Probability"])
        print("Maintenance",results["Maintenance"])
        print("Final Score",results["Final Score"])
        print("Maintenance Score",results["Maintenance Score"])
        print("Anomaly",results["Anomaly"])
        
        if results["Final Score"]>0.6:
            print("HIGH RiSK ALERT")
        elif results["Final Score"]>0.4:
            print("SChedule Maintenance")
        else:
            print("Normal Operations")
    except Exception as e:
        print("Error",e)

    time.sleep(5)

    
