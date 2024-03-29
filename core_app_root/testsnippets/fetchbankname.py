import requests
from requests.exceptions import JSONDecodeError

# Define your secret key and base URL
secret_key = 'sk_live_7f39f77453508b7b3b71d48e4dc5fdbbdfe9d2e7'
base_url = 'https://api.paystack.co'

import requests

# Define your secret key and base URL
base_url = 'https://api.paystack.co'

# Define endpoint and parameters
endpoint = '/bank/resolve'
params = {
    'account_number': '0761211732',
    'bank_code': '044'
}

# Define headers
headers = {
    'Authorization': f'Bearer {secret_key}'
}

# Make GET request
response = requests.get(f'{base_url}{endpoint}', params=params, headers=headers)

# Print response
print(response.json())
