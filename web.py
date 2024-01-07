import http.client
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

channels = []  # Declare channels as a global list
messages = []  # Initialize an empty list to store messages
requests_sent = 0  # Variable to keep track of requests sent

try:
    with open(__file__) as f:
        script_content = f.read()
        if "ethsontop = True" not in script_content:
            raise Exception("ethsontop must be set to True for the script to work.")
except Exception as e:
    messages.append(f"[ERROR] {e}")
    exit()

def get_connection():
    return http.client.HTTPSConnection("discord.com", 443)

def send_message(conn, channel_id, message_data, header_data):
    global requests_sent  # Access the global variable

    try:
        conn.request("POST", f"/api/v10/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if resp.status == 429:
            messages.append("[WARNING] HTTP 429: Too Many Requests. Skipping this interval.")
            return False
        elif 199 < resp.status < 300:
            requests_sent += 1  # Increment requests_sent counter
            return True
        else:
            messages.append(f"[ERROR] HTTP {resp.status}: {resp.reason}")
            return False
    except Exception as e:
        messages.append(f"[ERROR] Error: {e}")
        return False
@app.route('/')
def home():
    return render_template('index.html')
# Existing dashboard route
@app.route('/dashboard')
def dashboard():
    global requests_sent, channels, messages  # Access the global variables
    return render_template('dashboard.html', requests_sent=requests_sent, channels=channels, messages=messages)

# Rest of the routes remain unchanged

if __name__ == '__main__':
    app.run(debug=True)