import json

with open("user.json", "r") as input_file:
    data = json.load(input_file)

print(type(data["relationships"]))

usernames = []

blacklist = [] # put usernames that you dont want to get in the list here

for element in data["relationships"]:
    if element["type"] == "FRIEND" and not element["user"]["username"] in blacklist:
        print(
            f"{element['user']['username'] or '':<30}{element['user']['global_name'] or '':<30}"
        )
        usernames.append(element["user"]["username"])

print(usernames)
