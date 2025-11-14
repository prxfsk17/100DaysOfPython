from openai import OpenAI
import requests
import json
import datetime as dt
from dotenv import load_dotenv
import os
import pyperclip

load_dotenv()

TOKEN=os.getenv("TOKEN")
API_KEY=os.getenv("API_KEY")
API_URL=os.getenv("API_URL")
API_SHEET_URL=os.getenv("API_SHEET_URL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
user_prompt = input("Tell me what exercises you did: ")

api = OpenAI(api_key=API_KEY, base_url=API_URL)

completion = api.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=256,
    )

response = completion.choices[0].message.content

now = dt.datetime.now()
date=now.strftime("%d/%m/%Y")
time=now.strftime("%H:%M:%S")
text=response.replace("```", "").replace("json","")
pyperclip.copy(repr(text))
print(text)
json_obj=json.loads(text)
print(json_obj)
exercises_list=[]
for exercise in json_obj["Exercises"]:
    exercises_list.append({
        "workout":{
            "date": date,
            "time": time,
            "exercise" : exercise["Exercise"].title(),
            "duration" : exercise["Duration"],
            "calories" : exercise["Calories"]
        }
    })
header={
    "Authorization": f"Bearer {TOKEN}"
}
for exercise in exercises_list:
    response = requests.post(url=API_SHEET_URL, headers=header, json=exercise)
    response.raise_for_status()
    print(response.text, response.status_code)
