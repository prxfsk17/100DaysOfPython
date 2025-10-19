capitals = {
    "France" : "Paris",
    "Germany" : "Berlin",
    "Italy" : "Rome"
}

travel_log = {
    "France" : ["Paris", "Lille", "Dijon"],
    "Germany" : ["Stuttgart", "Berlin"],
    "Italy" : ["Rome", "Rimini"]
}

print(travel_log["Italy"][1])

nested_list = ["A", 123, [1, 2, 3]]
print(nested_list[2][1])

another_dict = {
    "capitals" : capitals,
    "all cities" : travel_log
}
print(another_dict["capitals"]["Italy"])
print(another_dict["all cities"]["Italy"][1])