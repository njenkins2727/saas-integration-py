from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables using os.getenv()
api_key = os.getenv("UP_API_KEY")

@app.route("/")
def get_api(): #def = defines function + instead of {} we use indentation and colons:
    try: # try and expect NOT try catch 
        headers = {
            "Authorization": f"Bearer {api_key}" # f = string literal 
        }
        res = requests.get('https://api.up.com.au/api/v1/accounts/92102abc-5f5f-430c-803f-285eb2e4f281', headers=headers)
        response = res.json()
        # display_name = response['data'][2]['attributes']['displayName'] #retrieving specific data from response 
        print (json.dumps(response, indent=2))
        return f"<h1>success</h1>"
    except:
        print('Error: failed to get display name')

# PING WEBHOOK BY ID 
@app.route("/latestTransaction", methods=['POST'])
def latest_transaction():
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        res = requests.post('https://api.up.com.au/api/v1/webhooks/c479169f-6ac5-4ecd-9443-58b7670d273c/', headers=headers)
        response = res.json()
        print(f'Transaction sent! {response}')
        return '<h1> Transaction sent! </h1>'
    except Exception as e:
        print("ERROR: status 500 || Failed to POST webhook")

@app.route("/webhookAction", methods=['GET', 'POST'])
def handle_webhook():
    try:
        data = request.get_json()

        # 1. Check if the event type is TRANSACTION_CREATED
        if data['data']['attributes']['eventType'] == 'TRANSACTION_CREATED':
            print('New Transaction Created Webhook Received!')

            # 2. Extract the transaction ID
            transaction_id = data['data']['relationships']['transaction']['data']['id']
            print(f'Transaction ID: {transaction_id}')

            # 3. Make a GET request to retrieve full transaction details
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f'https://api.up.com.au/api/v1/transactions/{transaction_id}', headers=headers)
            transaction_data = response.json()
            
            # 4. filter out account that is losing money (when valueInBaseUnits > 0) 
            valueInBaseUnits = transaction_data['data']['attributes']['amount']['valueInBaseUnits']
            if valueInBaseUnits > 0:
                
                # 5. if valueInBaseUnits > 0: extract the data - value, description and created at
                    #5.1 Fetch account id and retrieve account details for displayName
                account_id = transaction_data['data']['relationships']['account']['data']['id']
                res = requests.get(f'https://api.up.com.au/api/v1/accounts/{account_id}', headers=headers)
                fetchAccount = res.json()
                displayName = fetchAccount['data']['attributes']['displayName']
                description = transaction_data['data']['attributes']['description']
                value = transaction_data['data']['attributes']['amount']['value']
                created_at = transaction_data['data']['attributes']['createdAt']
                print(f'Details needed: {description}, {value}, {created_at}, {displayName}!')
                
                # 6. use library to send an email with this data **CURRENT 
            else:
                return ''
        else:
            print(f'Failed to fetch transaction details. Status code: {response.status_code}')
            print(response.text)

        return '', 200
    except:
        return 'Error handle webhook'

## POST A WEBHOOK 
# @app.route("/webhookAction", methods=['GET', 'POST']) #Flask runs get requests only by default so need to specify **BOTH** GET and POST
# def POST_webhook(): #def = defines function + instead of {} we use indentation and colons:
#     try: # try and expect NOT try catch 
#         headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#         }   
#         json_data = {
#             'data': {
#                 'attributes': {
#                     'url': 'https://dd5f5e371a54.ngrok-free.app/webhookAction',
#                     'description': 'Test Webhook 2',
#                 },
#             },
#         }
#         res = requests.post('https://api.up.com.au/api/v1/webhooks', headers=headers, json=json_data)
#         response = res.json()
#         print (f'Webhook created - 201: {json.dump(response, indent=2)}')
#         return f"<h1>Webhook created - 201: {response}</h1>"
#     except:
#         print(f'Error: failed to create Webhook - 500: {response}')

## GET ALL WEBHOOKS
# @app.route("/webhookAction") 
# def GET_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }

#         res = requests.get('https://api.up.com.au/api/v1/webhooks?page[size]=10', headers=headers)
#         response = res.json()
#         print(f'SUCCESS: status 200 || These are created webhooks: {json.dumps(response, indent=2)}')
#         return f'SUCCESS: status 200 || These are created webhooks: {json.dumps(response, indent=2)}'
#     except Exception as e:
#         print("ERROR: status 500 || Failed to GET webhooks")

# # GET WEBHOOK BY ID 
# @app.route("/webhookAction")
# def GET_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }

#         res = requests.get('https://api.up.com.au/api/v1/webhooks/c479169f-6ac5-4ecd-9443-58b7670d273c/', headers=headers)
#         response = res.json()
#         print(f'SUCCESS: status 200 || This is the created webhooks: {json.dumps(response, indent=2)}')
#         return f'SUCCESS: status 200 || This is the created webhooks: {response}'
#     except Exception as e:
#         print("ERROR: status 500 || Failed to GET webhook")

# #  DELETE WEBHOOK
# @app.route("/deleteWebhook", methods=["GET", "DELETE"])
# def delete_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }
#         res = requests.delete('https://api.up.com.au/api/v1/webhooks/{id}', headers=headers)
#         response = res.json()
#         print(f'Webhook Successfully deleted! {json.dumps(response, indent=2)}')
#         return '<h1>Webhook Deleted</h1>'
#     except:
#         print('Error deleting webhook')