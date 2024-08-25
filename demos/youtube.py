from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

load_dotenv()

yt_api_key = os.getenv('YOUTUBE_API_KEY')

youtube = build("youtube", "v3", developerKey=yt_api_key)


def search_videos(query, max_results=10):
    try:
        search_response = (
            youtube.search()
            .list(q=query, type="video", part="id,snippet", maxResults=max_results)
            .execute()
        )

        videos = []
        for search_result in search_response.get("items", []):
            video = {
                "title": search_result["snippet"]["title"],
                "video_id": search_result["id"]["videoId"],
                "description": search_result["snippet"]["description"],
            }
            videos.append(video)

        return videos

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None


query = "Python tutorial"
results = search_videos(query)

if results:
    for video in results:
        print(f"Video: {video['title']} (ID: {video['video_id']})")
        print(f"Description: {video['description']}")
        print("---")
