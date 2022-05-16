from googleapiclient.discovery import build


def search(query):
    api_key = "AIzaSyD5-rQrP9eUTa4vP5N1d587mlR1B2XUGPk"

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults="1").execute()

    return "https://www.youtube.com/watch?v=" + request['items'][0]['id']['videoId']
