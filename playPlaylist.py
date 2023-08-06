import os.path
import webbrowser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # No valid credentials -> login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: # Create first time
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
    
    try:
        service = build('youtube', 'v3', credentials=creds)

        # TO-Play Playlist ID
        playlist_id = "PLVIgHowVgwQc9p_lxyPKBojP1fDGYI1M9"

        # Extract videos
        playlist_items = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        ).execute()

        # Get all video's ID (if needed)
        IDs = [item['contentDetails']['videoId'] for item in playlist_items['items']]
        # To play the playlist, we just need to play the first video
        url = f"https://www.youtube.com/watch?v={IDs[0]}&list={playlist_id}"
        webbrowser.open(url)
    except HttpError as error:
        print("An error occured", error)


if __name__ == "__main__":
    main()