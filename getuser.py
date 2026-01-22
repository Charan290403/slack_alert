
# find user from slack and extract the number 

def get_phone(id,username):
    import requests
    from config import SLACK_BOT_TOKEN

    resp = requests.get(
        "https://slack.com/api/users.list",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        timeout=5
    ).json()

    if not resp.get("ok"):
        raise Exception("Slack users.list failed")

    for user in resp["members"]:
        if user.get("name") == username:
            phone = user["profile"].get("phone")
            user_id = user["id"]
            return phone

    raise Exception(f"User @{username} not found")
