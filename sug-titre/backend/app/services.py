
from app.config import settings
import requests, re


def get_info_video(id):
    params = {
        "id": id,
        "geo": "FR",
        "lang": "fr"
    }
    response = requests.get(settings.RAPID_API_URL, headers=settings.HEADERS, params=params)
    if response.status_code != 200:
        print("Erreur API:", response.text)
        return {"title": "Erreur API"}

    #print("Status code:", response.status_code)
    #print("Response:", response.text)
    return  response.json()

def extraire_formats(titles):
    patterns = ["top \\d+", "défi", "astuce", "tuto", "24h", "vs", "meilleur", "pire", "test", "build", "diy"]
    formats = []
    for title in titles:
        for pat in patterns:
            if re.search(pat, title, re.IGNORECASE):
                formats.append(pat)
    return list(set(formats)) or ["défi", "tuto", "top 5"]

def get_video_comments(video_id, max_comments=50):
    comments = []
    url = f"{settings.YOUTUBE_API_URL}/commentThreads"
    
    params = {
        "part": "snippet",
        "videoId" : video_id,
        "maxResults" : 50,
        "textFormat" : "plainText",
        "key": settings.YOUTUBE_API_KEY
    }
    
    try:
        
        while len(comments) < max_comments:
            res = requests.get(url, params=params)
            res.raise_for_status()  # vérifie erreur HTTP
        
            data = res.json()
            for item in data.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
                if len(comments) >= max_comments:
                    break
            
            # Pagination si besoin
            if 'nextPageToken' in data:
                params['pageToken'] = data['nextPageToken']
            else:
                break    
    except Exception as e:
        print(f"Comments error: {e}")
    return comments