from flask import Flask
import os
import requests

app = Flask(__name__)

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
        display_name = response['data'][2]['attributes']['displayName'] #retrieving specific data from response 
        print (display_name)
        return f"<h1>{display_name}</h1>"
    except:
        print('Error: failed to get display name')

if __name__ == '__main__':
    app.run(debug=True)