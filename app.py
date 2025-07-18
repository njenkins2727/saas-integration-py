from flask import Flask
import os
import requests

app = Flask(__name__)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables using os.getenv()
api_key = os.getenv("UP_API_KEY")
database_url = os.getenv("DATABASE_URL")

@app.route("/")
def get_api():
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    res = requests.get('https://api.up.com.au/api/v1/accounts', headers=headers)
    response = res.json()
    display_name = response['data'][1]['attributes']['displayName']
    print (display_name)
    return f"<h1>{display_name}</h1>"

if __name__ == '__main__':
    app.run(debug=True)





