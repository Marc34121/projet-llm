# -*- coding: utf-8 -*-
"""
Created on Thu May 22 16:10:54 2025

@author: hugok
"""

from flask import Flask, request, jsonify, render_template
import re
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = "AIzaSyDgbPIBjjGaow1PFcqAaws-iL-Bn3YfV3A"

def extract_channel_id(url):
    """
    Extract channel ID or username or handle from URL.
    Supporte :
    - https://www.youtube.com/channel/CHANNEL_ID
    - https://www.youtube.com/user/USERNAME
    - https://www.youtube.com/@HANDLE
    """
    # Channel ID (long string)
    m = re.search(r"(?:youtube\.com/channel/)([A-Za-z0-9_\-]+)", url)
    if m:
        return m.group(1), "channelId"

    # User name
    m = re.search(r"(?:youtube\.com/user/)([A-Za-z0-9_\-]+)", url)
    if m:
        return m.group(1), "forUsername"

    # Handle (starts with @)
    m = re.search(r"(?:youtube\.com/@)([A-Za-z0-9_\-]+)", url)
    if m:
        return m.group(1), "handle"

    return None, None


def get_channel_id_from_username(username):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={username}&key={YOUTUBE_API_KEY}"
    resp = requests.get(url).json()
    items = resp.get("items")
    if items and len(items) > 0:
        return items[0]["id"]
    return None

def get_channel_id_from_handle(handle):
    """
    Recherche via la recherche YouTube (pour handle) : on cherche la chaîne correspondant au handle.
    """
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={handle}&type=channel&key={YOUTUBE_API_KEY}"
    resp = requests.get(url).json()
    items = resp.get("items")
    if items and len(items) > 0:
        # Vérifie si le handle correspond au snippet.channelTitle ou customUrl (pas toujours dispo)
        for item in items:
            snippet = item.get("snippet", {})
            title = snippet.get("channelTitle", "").lower()
            if handle.lower() in title:
                return item["snippet"]["channelId"]
        # Sinon retourne le premier
        return items[0]["snippet"]["channelId"]
    return None

def get_channel_data(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={YOUTUBE_API_KEY}"
    resp = requests.get(url).json()
    items = resp.get("items")
    if not items:
        return None
    c = items[0]
    snippet = c["snippet"]
    stats = c["statistics"]
    return {
        "id": c["id"],
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "publishedAt": snippet.get("publishedAt"),
        "thumbnails": snippet.get("thumbnails", {}),
        "subscriberCount": int(stats.get("subscriberCount", 0)),
        "viewCount": int(stats.get("viewCount", 0)),
        "videoCount": int(stats.get("videoCount", 0)),
    }

def get_uploads_playlist_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={YOUTUBE_API_KEY}"
    resp = requests.get(url).json()
    items = resp.get("items")
    if not items:
        return None
    contentDetails = items[0]["contentDetails"]
    return contentDetails["relatedPlaylists"]["uploads"]

def get_videos_from_playlist(playlist_id, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    resp = requests.get(url).json()
    items = resp.get("items", [])
    videos = []

    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in items if item.get("snippet") and item["snippet"].get("resourceId")]

    # Obtenir les détails des vidéos en batch
    if not video_ids:
        return videos

    video_details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={','.join(video_ids)}&key={YOUTUBE_API_KEY}"
    details_resp = requests.get(video_details_url).json()
    details_items = details_resp.get("items", [])

    for item in details_items:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})
        videos.append({
            "videoId": item["id"],
            "title": snippet.get("title", ""),
            "publishedAt": snippet.get("publishedAt", ""),
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0)),
            "tags": snippet.get("tags", []),
            "description": snippet.get("description", ""),
            "duration": content.get("duration", ""),
            "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", "")
        })
    return videos

def generate_recommendations(channel_data, videos):
    recs = []

    if channel_data["subscriberCount"] < 10000:
        recs.append("Travaille à augmenter la fréquence de publication pour accélérer la croissance.")
    else:
        recs.append("Ta communauté est solide, continue de publier régulièrement.")

    # Moyennes
    if videos:
        avg_views = sum(v["viewCount"] for v in videos) / len(videos)
        avg_likes = sum(v["likeCount"] for v in videos) / len(videos)
        avg_comments = sum(v["commentCount"] for v in videos) / len(videos)

        recs.append(f"Les vidéos reçoivent en moyenne {int(avg_views):,} vues, {int(avg_likes):,} likes et {int(avg_comments):,} commentaires.")
        # Reco sur thème selon tags fréquents
        tag_count = {}
        for vid in videos:
            for tag in vid["tags"]:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        if tag_count:
            sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
            main_tag = sorted_tags[0][0]
            recs.append(f"Ton contenu est souvent centré sur le thème « {main_tag} ». Explore les sous-thèmes connexes pour varier et attirer plus de spectateurs.")
        # Reco sur engagement
        engagement_rate = (avg_likes + avg_comments) / avg_views if avg_views > 0 else 0
        if engagement_rate < 0.05:
            recs.append("L'engagement semble faible par rapport aux vues. Encourage plus les commentaires et likes dans tes vidéos.")
        else:
            recs.append("Bonne interaction avec ta communauté, continue comme ça !")

    else:
        recs.append("Peu de vidéos analysées, impossible de générer des recommandations avancées.")

    recs.append("Considère des collaborations avec des créateurs ayant une audience complémentaire pour élargir ta portée.")
    recs.append("Analyse les tendances YouTube régulièrement pour adapter tes sujets.")

    return recs


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detailed_analyze", methods=["POST"])
def detailed_analyze():
    data = request.json
    channel_url = data.get("channelUrl", "")
    if not channel_url:
        return jsonify({"error": "URL de chaîne manquante"}), 400

    id_value, id_type = extract_channel_id(channel_url)
    if not id_value:
        return jsonify({"error": "Impossible d'extraire l'identifiant de la chaîne"}), 400

    if id_type == "channelId":
        channel_id = id_value
    elif id_type == "forUsername":
        channel_id = get_channel_id_from_username(id_value)
        if not channel_id:
            return jsonify({"error": "Utilisateur introuvable"}), 404
    elif id_type == "handle":
        channel_id = get_channel_id_from_handle(id_value)
        if not channel_id:
            return jsonify({"error": "Chaîne introuvable pour ce handle"}), 404
    else:
        return jsonify({"error": "Type d'identifiant inconnu"}), 400

    channel = get_channel_data(channel_id)
    if not channel:
        return jsonify({"error": "Impossible de récupérer les données de la chaîne"}), 404

    uploads_playlist_id = get_uploads_playlist_id(channel_id)
    if not uploads_playlist_id:
        return jsonify({"error": "Impossible de récupérer la playlist des vidéos"}), 404

    videos = get_videos_from_playlist(uploads_playlist_id, max_results=10)

    # Calcul moyennes
    if videos:
        avg_views = sum(v["viewCount"] for v in videos) / len(videos)
        avg_likes = sum(v["likeCount"] for v in videos) / len(videos)
        avg_comments = sum(v["commentCount"] for v in videos) / len(videos)
    else:
        avg_views = avg_likes = avg_comments = 0

    recommendations = generate_recommendations(channel, videos)

    return jsonify({
        "channel": channel,
        "videos": videos,
        "averages": {
            "views": round(avg_views),
            "likes": round(avg_likes),
            "comments": round(avg_comments),
        },
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True)





