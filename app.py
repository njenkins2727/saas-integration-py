import os
import requests
import json
import smtplib
import datetime
from flask import Flask, request
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the variables using os.getenv()
api_key = os.getenv("UP_API_KEY")

@app.route("/")
def home(): #def = defines function + instead of {} we use indentation and colons:
    try: # try and expect NOT try catch 
        print ('Python Running!')
        return f"<h1>Python Flask app running in the background!</h1>"
    except:
        print('Error: failed to fetch home page.')

@app.route("/webhookReceiver", methods=['GET', 'POST'])
def handle_webhook():
    try:
        data = request.get_json()

        # 1. Check if the event type is TRANSACTION_CREATED
        if data['data']['attributes']['eventType'] == 'TRANSACTION_CREATED':
            print('New transaction created webhook received!')

            # 2. Extract the transaction ID
            transaction_id = data['data']['relationships']['transaction']['data']['id']
            print(f'Transaction ID {transaction_id}')

            # 3. Make a GET request to retrieve full transaction details
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f'https://api.up.com.au/api/v1/transactions/{transaction_id}', headers=headers)
            transaction_data = response.json()
            print('Transaction data retrieved')
            # 4. filter out account that is losing money (when valueInBaseUnits > 0) 
            valueInBaseUnits = transaction_data['data']['attributes']['amount']['valueInBaseUnits']
            if valueInBaseUnits > 0:
                try:
                    print(f'Finding account info...')
                    # 5. if valueInBaseUnits > 0: extract the data - value, description and created at
                        #5.1 Fetch account id and retrieve account details for displayName
                    account_id = transaction_data['data']['relationships']['account']['data']['id']
                    res = requests.get(f'https://api.up.com.au/api/v1/accounts/{account_id}', headers=headers)
                    fetchAccount = res.json()
                    displayName = fetchAccount['data']['attributes']['displayName']
                    description = transaction_data['data']['attributes']['description']
                    value = transaction_data['data']['attributes']['amount']['value']
                    created_at = transaction_data['data']['attributes']['createdAt']
                        #5.2 Format timestamp for readability 
                    dt = datetime.fromisoformat(created_at)
                    formatted_timestamp = dt.strftime(f"%d %b %Y, %H:%M:%S")
                    print(f'Account info found! {description}, {value}, {formatted_timestamp}, {displayName}!')
                    
                    # 6. Send an email with this data
                    sender_email = 'nathistheone@gmail.com'
                    receiver_email = 'njenkins2727@gmail.com'

                    subject = 'Test Email'
                    body = f"""
                    Yo Nathan,

                    ${value} Landed into "{displayName}" account @ {formatted_timestamp}! This was a {description}.

                    Best regards,
                    Nathan :3
                    """

                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    message["Subject"] = subject

                    message.attach(MIMEText(body, "plain"))

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, 'vkuyvmypkxbdwdeh')
                        server.send_message(message)
                        print('Email sent successfully: Check inbox!')
                except:
                    print('Error sending email to account that recieved money')
            else:
                return ''
        else:
            print(f'Failed to fetch transaction details. Status code: {response.status_code}')
            print(response.text)

        return '', 200
    except:
        return 'Error handle webhook'

## POST A WEBHOOK 
# @app.route("/createWebhook", methods=['GET', 'POST']) #Flask runs get requests only by default so need to specify **BOTH** GET and POST
# def POST_webhook(): #def = defines function + instead of {} we use indentation and colons:
#     try: # try and expect NOT try catch 
#         headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#         }   
#         json_data = {
#             'data': {
#                 'attributes': {
#                     'url': 'https://upemailscript.onrender.com/webhookReceiver',
#                     'description': 'Webhook for Up automated email script',
#                 },
#             },
#         }
#         res = requests.post('https://api.up.com.au/api/v1/webhooks', headers=headers, json=json_data)
#         response = res.json()
#         print (f'Webhook created - 201: {json.dumps(response, indent=2)}')
#         return f"<h1>Webhook created - 201: {json.dumps(response, indent=2)}</h1>"
#     except:
#         print(f'Error: failed to create Webhook - 500: {response}')

##GET ALL WEBHOOKS
# @app.route("/getWebhooks") 
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

#verify api token 
# @app.route("/verify") 
# def GET_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }
#         res = requests.get('https://api.up.com.au/api/v1/util/ping', headers=headers)
#         response = res.json()
#         print(f'SUCCESS: status 200 || Verify token: {json.dumps(response, indent=2)}')
#         return f'SUCCESS: status 200 || Verify token: {json.dumps(response, indent=2)}'
#     except Exception as e:
#         print("ERROR: status 500 || Failed to  Verify token")

# GEt all accounts
# @app.route("/getAllAccounts") 
# def GET_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }
#         res = requests.get('https://api.up.com.au/api/v1/accounts?page[size]=2', headers=headers)
#         response = res.json()
#         print(f'SUCCESS: status 200 || Fetched Accounts: {json.dumps(response, indent=2)}')
#         return f'SUCCESS: status 200 || Fetched Accounts: {json.dumps(response, indent=2)}'
#     except Exception as e:
#         print("ERROR: status 500 || Failed to  Verify token")

# # GET WEBHOOK BY ID 
# @app.route("/getWebhookById")
# def GET_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }

#         res = requests.get('https://api.up.com.au/api/v1/webhooks/7fa75087-d500-4c61-973d-a003f8b82cf2/', headers=headers)
#         response = res.json()
#         print(f'SUCCESS: status 200 || This is the created webhooks: {json.dumps(response, indent=2)}')
#         return f'SUCCESS: status 200 || This is the created webhooks: {response}'
#     except Exception as e:
#         print("ERROR: status 500 || Failed to GET webhook")

#  DELETE WEBHOOK
# @app.route("/deleteWebhook", methods=["GET", "DELETE"])
# def delete_webhook():
#     try:
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#         }
#         res = requests.delete('https://api.up.com.au/api/v1/webhooks/7fa75087-d500-4c61-973d-a003f8b82cf2', headers=headers)
#         response = res.json()
#         print(f'Webhook Successfully deleted! {json.dumps(response, indent=2)}')
#         return '<h1>Webhook Deleted</h1>'
#     except:
#         print('Error deleting webhook')