from flask import Flask, request, jsonify
import requests

BACKEND_URL = "http://127.0.0.1:5002/alert"

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    print("🔥 Slack route hit")
    print("Content-Type:", request.content_type)

    # ---------- SLASH COMMAND ----------
    if request.content_type.startswith("application/x-www-form-urlencoded"):
        text = request.form.get("text", "")
        user_id = request.form.get("user_id")
        


        print("📩 Slash command text:", text)
        print("👤 From user:", user_id)

        mentioned_users = extract_mentions_from_text(text)

        
        call_backend(text, mentioned_users, user_id)

        return jsonify({
            "response_type": "ephemeral",
            "text": "🟢 Alert processing ....."
        }), 200

        

        # Slack REQUIRES a response within 3 seconds
        

    
   

 #extracting mention user from text
 
import re

def extract_mentions_from_text(text):
    """
    Extract usernames from slash command text like:
    'hi @charanb901'
    """
    usernames = re.findall(r'@([a-zA-Z0-9._-]+)', text)

    print("👤 Extracted usernames:", usernames)
    return usernames





# Calling backend 

def call_backend(text, username, id):
    try:
        requests.post(
            BACKEND_URL,
            json={
                "message": text,
                "mentioned_users":username,
                 "user_id":id
            },
            timeout=5
        )
        print("✅ Backend called")
    except Exception as e:
        print("❌ Backend call failed:", e)

    


if __name__ == "__main__":
    print("🚀 Slack bot running on port 3000")
    app.run(host="0.0.0.0", port=3000)
