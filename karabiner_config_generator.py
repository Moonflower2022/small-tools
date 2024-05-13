import json
qwerty_string  = "qwertyuiopasdfghjkl;zxcvbnm"
colemak_string = "qwfpgjluy;arstdhneiozxcvbkm"


# Generate QWERTY to Colemak key mapping for lowercase letters
qwerty_to_colemak = {}
for qwerty_key, colemak_key in zip(qwerty_string, colemak_string):
    qwerty_to_colemak[qwerty_key] = colemak_key

# Generate JSON configuration
json_config = []
for qwerty_key, colemak_key in qwerty_to_colemak.items():
    if qwerty_key != colemak_key:
        if colemak_key == ";":
            colemak_key = "semicolon"
        if qwerty_key == ";":
            qwerty_key = "semicolon"
        config_entry = {
            "from": {
                "key_code": qwerty_key
            },
            "to": [
                {
                    "key_code": colemak_key
                }
            ]
        }
        json_config.append(config_entry)


extra_mappings = {
    "caps_lock": "left_control",
    "left_control": "caps_lock"
}

for key1, key2 in extra_mappings.items():
    config_entry = {
        "from": {
            "key_code": key1
        },
        "to": [
            {
                "key_code": key2
            }
        ]
    }
    json_config.append(config_entry)

file_name = "config.json"

# Write the JSON configuration to a file
with open(file_name, "w") as json_file:
    json.dump(json_config, json_file, indent=4)

print("JSON configuration has been written to", file_name)
