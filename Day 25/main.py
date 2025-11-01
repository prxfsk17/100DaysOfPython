# with open("Day 25/weather_data.csv") as f:
#     data = f.readlines()
# print(data)
#
# import csv
# with open("Day 25/weather_data.csv") as f:
#     data = csv.reader(f)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)
# data = pandas.read_csv("Day 25/weather_data.csv")
# print(type(data))
# print(data)
#
# print(data.to_dict())
# print(data["temp"].to_list())
# print(data["temp"].max())
#
# print(data.condition)
# sunday = (data[data.temp == data.temp.max()])
# print(sunday.temp*9/5+32)
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
# data = pandas.DataFrame(data_dict)
# data.to_csv("Day 25/new_data.csv")

# import pandas

# data = pandas.read_csv("Day 25/Squirrel_Data.csv")
# gray_count = len(data[data["Primary Fur Color"] == "Gray"])
# red_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
# black_count = len(data[data["Primary Fur Color"] == "Black"])
# data_dict = {
#     "Fur Color": ["Gray", "Red", "Black"],
#     "Count": [gray_count, red_count, black_count]
# }
# data_count = pandas.DataFrame(data_dict)
# print(data_count)

import US_States_game
US_States_game.play()

