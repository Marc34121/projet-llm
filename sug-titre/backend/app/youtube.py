from app.config import settings
import requests

def get_trending_gaming_videos(niche,max_results=1):
    url = f"{settings.YOUTUBE_API_URL}/videos"
    
    if not settings.YOUTUBE_API_KEY or not settings.YOUTUBE_API_URL:
        raise ValueError("Clé API ou URL de l'API YouTube non définie.")
    video_category_id=""
    if niche== "gaming":
        video_category_id = "20"
    else :
        video_category_id = "26"
            
    
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": "FR",
        "videoCategoryId": video_category_id,
        "maxResults": max_results,
        "key": settings.YOUTUBE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API YouTube: {e}")
        return []
    except ValueError:
        print("Erreur de décodage JSON dans la réponse de l'API.")
        return []