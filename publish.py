import requests
import google.auth.transport.requests
from google.oauth2 import service_account


KEY_FILE = 'service_key.json'  # Make sure this file name matches yours (get this from your google cloud console)
URL_TO_INDEX = 'https://your_site' // This should match yours
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def force_index():
    print(f" Attempting to force index: {URL_TO_INDEX}...")

    try:
        # 1. Load credentials from the JSON file
        creds = service_account.Credentials.from_service_account_file(
            KEY_FILE, scopes=SCOPES
        )

        # 2. Refresh the token 
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        
        auth_token = creds.token
        print("Auth Success: Token generated.")

    except Exception as e:
        print(f"Auth Failed: {e}")
        return

    # 3. Build the request payload
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    body = {
        "url": URL_TO_INDEX,
        "type": "URL_UPDATED"
    }

    # 4. Send the POST request to Google
    try:
        response = requests.post(ENDPOINT, headers=headers, json=body)
        
        print(f" Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS! Request accepted by Google.")
            print("Response:", response.json())
        else:
            print(" FAILED.")
            print("Response:", response.text)
            
    except Exception as e:
        print(f" Network Error: {e}")

if __name__ == "__main__":
    force_index()
