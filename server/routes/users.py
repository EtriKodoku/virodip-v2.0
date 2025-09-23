import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

user_bp = Blueprint('user_bp', __name__)

def get_graph_access_token():
    url = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token"
    data = {
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def create_b2c_user(user_data):
    token = get_graph_access_token()
    url = "https://graph.microsoft.com/v1.0/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=user_data, headers=headers)
    resp.raise_for_status()
    return resp.json()

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    # You may want to validate data here!
    user_data = {
        "accountEnabled": True,
        "displayName": data["displayName"],
        "mailNickname": data["mailNickname"],
        "userPrincipalName": data["userPrincipalName"],  # e.g. johndoe@yourtenant.onmicrosoft.com
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": data["password"]  # You may want to generate a strong password
        }
    }
    try:
        result = create_b2c_user(user_data)
        return jsonify(result), 201
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": e.response.json()}), 400

@user_bp.route('/delete', methods=['DELETE'])
def delete_user_by_id(user_id: str):
	access_token = get_graph_access_token()
	url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	resp = requests.delete(url, headers=headers)
	resp.raise_for_status()
	return resp.status_code