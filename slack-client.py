print("🔥 backend_api.py file loaded")

from flask import Flask, request,jsonify
from getuser import get_phone
from twilio_service import send_whatsapp
from config import PORT
import requests


app = Flask(__name__)


@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json(silent=True) or {}
 
    text = data.get("message", "")
    mentioned_users = data.get("mentioned_users", [])
    id=data.get("user_id","")

    print("📩 Alert received:", text)
    print("👤 Mentioned users:", mentioned_users)

    
    if not mentioned_users:
        print("⚠️ No users mentioned – skipping")
        return "OK", 200

    
    username = "".join(mentioned_users)

    

    try:
        phone = get_phone(id,username)   # get phone number from slack

        if not phone:
            print(f"⚠️ @{username} has no phone number")
            

        print(f"📞 Sending alert to @{username} -> {phone}")
        send_whatsapp(text, phone)

    except Exception as e:
        print(f"❌ Failed for @{username}:", e)
    
    
    return "OK", 200


if __name__ == "__main__":
    print("🚀 Backend running on port", PORT)
    app.run(port=PORT)
