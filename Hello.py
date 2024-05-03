import random

import requests
import streamlit as st


with st.sidebar:
    work_order = st.text_input("Work Order ID", key="work_order", value="")
    installed_product = st.text_input("Installed Product ID", key="installed_product", value="")
    org_type = st.text_input("Org Type", key="org_type", value="")
    access_token = st.text_input("Access Token", key="access_token", value="")
    aig_url = st.text_input("AIG URL", key="aig_url", value="")
    from_value = st.text_input("From", key="from_value", value="")
    api_key_value = st.text_input("API Key", key="api_key_value", value="")

st.title("💬 Chatbot")

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []
    st.session_state["conversation_id"] = random.randint(1, 2_000_000_000)

for msg in st.session_state["conversation"]:
    st.chat_message(msg["role"]).write(msg["message"])

user_message = {
    "talker_id": "me",
    "role": "user",
    "timestamp": "2024-03-15T11:00:00"
}

if user_question := st.chat_input():
    if not access_token:
        st.info("missing access token")
        st.stop()
  
    st.session_state["conversation"].append({
        "talker_id": "me",
        "role": "user",
        "message": user_question,
        "timestamp": "2024-03-15T11:00:00"
    })
    user_message["message"] = user_question
    st.chat_message("user").write(user_question)

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'X-Auth-Origin': org_type,
        'X-Auth-Type': 'salesforce',
        'x-conversation-id': str(st.session_state["conversation_id"]),
        'from': from_value,
        'x-api-key': api_key_value
    }
    body = {
        "user_message": user_message,
        "conversation": st.session_state.conversation,
        "context": {
            "entity": work_order or installed_product,
            "entity_resource": "SVMXC__Service_Order__c" if work_order else "SVMXC__Installed_Product__c",
            "conversation_id": st.session_state["conversation_id"]
        }
    }
    response = requests.post(aig_url, headers=headers, json=body, timeout=300)
    if response.status_code != 200:
        st.info(f"error response: {response.text}")
    else:
        response_message = response.json()["message"]
        st.session_state["conversation"].append({
            "talker_id": "ai",
            "role": "ai",
            "message": response_message,
            "timestamp": "2024-03-15T11:00:00"
        })

        st.chat_message("ai").write(response_message)
