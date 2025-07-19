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
        res = requests.get('https://api.up.com.au/api/v1/accounts', headers=headers)
        response = res.json()
        # display_name = response['data'][2]['attributes']['displayName'] #retrieving specific data from response 
        print (json.dumps(response, indent=2))
        return f"<h1>success</h1>"
    except:
        print('Error: failed to get display name')


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

# # PING WEBHOOK BY ID 
# @app.route("/ping", methods=['GET', 'POST'])
# def ping_webhook():
#         try:
#             headers = {
#                 'Authorization': f'Bearer {api_key}',
#                 'Content-Type': 'application/json',
#             }
#             res = requests.post('https://api.up.com.au/api/v1/webhooks/c479169f-6ac5-4ecd-9443-58b7670d273c/ping', headers=headers)
#             response = res.json()
#             print(f'Ping sent! {response}')
#             return '<h1> Ping sent! </h1>'
#         except Exception as e:
#             print("ERROR: status 500 || Failed to GET webhook")

# @app.route("/webhookAction", methods=['POST'])
# def handle_webhook():
#     try:
#         data = request.get_json()
#         print(f'Webhook received! {json.dumps(data, indent=2)}')
#         return ''
#     except:
#         return 'Error handle webhook'

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