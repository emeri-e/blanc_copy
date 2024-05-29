import json

# Read JSON data from file
with open('core_app_root/json_datas/bank_codes.json', 'r') as file:
    banks_data = file.read()

# Parse JSON
banks = json.loads(banks_data)

# Print when the key is '082'
if "082" in banks:
    print(banks["082"])
