import requests

ENDPOINT = "https://opentdb.com/api.php"
parameters = {
    "amount" : 50,
    "difficulty" : "easy",
    "type" : "boolean"
}

response = requests.get(url = ENDPOINT, params=parameters)
response.raise_for_status()
question_data = response.json()["results"]
