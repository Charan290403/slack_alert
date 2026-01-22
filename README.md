## — Alert Trigger Service (Frontend + Backend)

This service provides a **single public entry point** that receives alert triggers and routes them to backend alerting logic.
The backend performs user resolution and sends notifications via **Twilio (WhatsApp / Call)**.

The system is designed so that **only one public URL** is exposed externally.
All other services communicate internally.

---

## High-Level Architecture

```
External Trigger (Slack Command)
        |
        |  HTTPS (Public URL)
        ↓
Frontend Entry Service  (frontend.py)
        |
        |  Internal HTTP
        ↓
Backend Alert Service   (slack-client.py)
        |
        ├── User Resolution
        ├── Business Logic
        └── Twilio Notification
```

---

## Folder Structure

```
project-root/
├── frontend.py                  # Frontend entry point (PUBLIC)
├── slack-client.py           # Backend alert logic (PRIVATE)      
│-----get_user.py         # Resolve user → phone number
│── twilio_service.py   # WhatsApp / Call integration
│── config.py           # Backend configuration
├── requirements.txt
├── .env
└── README.md
```

---

## Component Responsibilities

### 1️⃣ Frontend Entry Point (`frontend.py`)

**Purpose**

* Acts as the **only public-facing service**
* Receives alert trigger requests
* Performs basic parsing and validation
* Forwards requests to backend

**Key Characteristics**

* Exposed to the internet
* Stateless
* Lightweight
* No Twilio or user lookup logic

**Public Endpoint**

```
POST /slack/events
```

✅ This is the **ONLY URL** that must be configured in the external system.

---

### 2️⃣ Backend Alert Logic (`slack-client.py`)

**Purpose**

* Implements all alert processing logic
* Resolves users to phone numbers
* Sends WhatsApp / call alerts via Twilio

**Key Characteristics**

* NOT publicly exposed
* Accessible only from frontend
* Contains business rules
* Handles failures and retries

**Internal Endpoint**

```
POST /alert
```

---

### 3️⃣ User Resolution (`get_user.py`)

**Purpose**

* Maps trigger-provided user identifiers to real phone numbers
* Reads from:

  * Slack API
  * Internal user mappings
  * Directory services (future)

---

### 4️⃣ Twilio Service (`twilio_service.py`)

**Purpose**

* Sends outbound notifications
* WhatsApp message
* Voice call (optional)

**No inbound webhooks required**

---

## Configuration

### `.env` (Required)

Contains **all secrets and environment-specific values**.

Example:

```
SLACK_BOT_TOKEN=xxxx
SLACK_SIGNING_SECRET=xxxx

TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

⚠️ This file **must not** be committed to source control.

---

## Deployment Model

* All components run in **one container**
* Process supervision handled via `supervisord`
* Deployed on a single EC2 instance
* Frontend listens on port `3000`
* Backend listens on port `5002`

---

## External Integration Requirement (IMPORTANT)

### Only One Thing Is Required Externally

You only need to provide **one public URL**:

```
http(s)://<PUBLIC_EC2_IP_OR_DOMAIN>:3000/slack/events
```

This URL is configured as:

* Trigger endpoint
* Command callback
* External alert entry

👉 **No other ports or URLs are exposed**
👉 **Backend is never directly accessed**




