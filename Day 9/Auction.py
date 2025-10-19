from art import hammer

def without_a_dollar(bid_with_a_dollar):
    if bid_with_a_dollar[0] == '$':
        return int(bid_with_a_dollar[1:])
    elif bid_with_a_dollar[len(bid_with_a_dollar)-1] == '$':
        return int(bid_with_a_dollar[:len(bid_with_a_dollar)-2])
    else:
        return int(bid_with_a_dollar)

print(hammer)
print("This is auction!")
bids = {}
auction_continues = "yes"
while auction_continues.lower() == "yes":
    print("\n"*25)
    name = input ("What is your name?\n")
    bid = without_a_dollar(input("What is your bid?\n"))
    bids[name] = bid
    auction_continues = input("Are there any other to make a bid?\nType 'yes' or 'no'\n")
# max_name = ""
# max_bid = 0
# for name in bids:
#     if max_bid < bids[name]:
#         max_bid = bids[name]
#         max_name = name
max_name = max(bids, key=bids.get)
max_bid = bids[max_name]
print(f"\n\n\n\n\n\n\n\nAuction won by {max_name} with a bid of ${max_bid}!")