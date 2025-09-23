import requests
from config.azure_config import azure_config

def get_graph_access_token():
    url = f"https://login.microsoftonline.com/{azure_config.AZURE_TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": azure_config.AZURE_CLIENT_ID,
        "client_secret": azure_config.AZURE_CLIENT_SECRET,
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

def delete_user_by_id(user_id: str):
	access_token = get_graph_access_token()
	url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	resp = requests.delete(url, headers=headers)
	resp.raise_for_status()
	return resp.status_code
