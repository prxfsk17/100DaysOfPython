import requests
import datetime as dt

TOKEN = "dhsajkbb21kbj3k1jb321bkjjfkfsl213"
USERNAME = "prxfsk"
pixela_endpoint = "https://pixe.la/v1/users"
user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_id = "idpgs17"
graph_params={
    "id" : graph_id,
    "name" : "Steps graph",
    "unit" : "steps",
    "type" : "int",
    "color" : "ajisai"
}
graph_head={
    "X-USER-TOKEN" : TOKEN
}
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
# response = requests.post(url=graph_endpoint, headers=graph_head, json=graph_params)
# print(response.text)

post_pixel_url=f"{graph_endpoint}/{graph_id}"
today=dt.datetime.now().strftime("%Y%m%d")

post_pixel_params={
    "date" : today,
    "quantity" : input("How many steps did you make today? ")
}
response=requests.post(url=post_pixel_url, headers=graph_head, json=post_pixel_params)
print(response.text)

update_delete_url=f"{post_pixel_url}/{today }"
put_pixel_params={
    "quantity" : "6000"
}
# response=requests.put(url=update_delete_url, headers=graph_head, json=put_pixel_params)
# print(response.text)

# response=requests.delete(url=update_delete_url, headers=graph_head)
# print(response.text)