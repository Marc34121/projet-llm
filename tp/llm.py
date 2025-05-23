# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import requests, json, re, random
from sklearn.feature_extraction.text import CountVectorizer
from sujets_populaires import extraire_sujets


API_KEY = '670f416022msh9b82781863db1afp109c3fjsnce7af4d57667'
RAPID_API_URL = 'https://yt-api.p.rapidapi.com/video/info'

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
}

# Étape 1 : Récupérer les informations d'une vidéo 
def get_info_video(id):
    params = {
        "id": id,
        "geo": "FR",
        "lang": "en"
    }
    response = requests.get(RAPID_API_URL, headers=headers, params=params)
    return response.json()

# Étape 2 : Extraire formats populaires à partir des titres
def extract_formats(titles):
    patterns = ["top \\d+", "défi", "astuce", "tuto", "24h", "vs", "meilleur", "pire", "test", "build"]
    formats = []
    for title in titles:
        for pat in patterns:
            if re.search(pat, title, re.IGNORECASE):
                formats.append(pat)
    return list(set(formats)) or ["défi", "tuto", "top 5"]

# Étape 3 : Générateur principal
def generer_idee(niche="gaming"):
    if niche == "gaming":
        sujet = random.choice(list(formats_gaming.keys()))
        format = random.choice(formats_gaming[sujet])
        hook = random.choice(hooks_gaming.get(format, [""]))
    elif niche == "bricolage":
        sujet = random.choice(list(formats_bricolage.keys()))
        format = random.choice(formats_bricolage[sujet])
        hook = random.choice(hooks_bricolage.get(format, [""]))
    else:
        return "Niche non prise en charge"
    
    return f"{format} : {sujet} {hook}".strip()





sujets_gaming = [
    "Fortnite", "Minecraft", "Valorant", "LoL", "Roblox", 
    "Call of Duty", "Jeux mobiles", "mods GTA V", "FIFA", "Rocket League"
]


formats_gaming = {
    "Minecraft": ["Top 5", "Défi 24h", "Je teste", "Build impossible", "Secrets du jeu"],
    "LoL": ["Top 5", "Réaction", "Défi 24h"],
    "Valorant": ["Top 5", "Défi 24h", "Je teste"],
    "FIFA": ["Top 5", "Je teste", "Speedrun"],
    "Roblox": ["Top 5", "Je teste", "Secrets du jeu"],
}

hooks_gaming = {
    "Top 5": ["des moments les plus WTF", "des clutchs de fou", "des fails les plus drôles"],
    "Défi 24h": ["sans mourir", "sur un seul jeu", "en ranked"],
    "Je teste": ["avec une main", "sur manette", "comme un noob"],
    "Build impossible": ["en hardcore", "sans utiliser de blocs rares"],
    "Réaction": ["à des plays de pro", "à mes anciennes games"],
    "Secrets du jeu": ["que personne ne connaît", "qui font bugger le jeu"],
    "Speedrun": ["avec des pièges", "à l’aveugle"],
}


formats_bricolage = {
    "Meubles en palette": ["Tuto", "Avant / Après", "Défi 24h"],
    "Rénovation appartement": ["Avant / Après", "Transformation extrême", "Défi 48h"],
    "Test d’outils (Lidl, Action, Amazon)": ["Test de produits", "Astuce de pro", "Fails"],
    "Bureau DIY / étagères murales": ["Tuto", "Avant / Après", "Transformation extrême"],
    "Recyclage créatif / upcycling": ["Tuto", "Défi 24h", "Astuce de pro"],
    "Époxy / bois / béton créatif": ["Tuto", "Transformation extrême", "Fails"],
    "Optimisation de rangement": ["Avant / Après", "Astuce de pro", "Tuto"],
}

hooks_bricolage = {
    "Tuto": ["avec du bois de récup", "sans outils électriques", "pour débutants"],
    "Avant / Après": ["avec un petit budget", "transformation bluffante", "en moins d’une journée"],
    "Défi 24h": ["avec seulement 3 outils", "en palette", "pour aménager un balcon"],
    "Défi 48h": ["dans un studio de 20m²", "en équipe", "sans percer les murs"],
    "Test de produits": ["acheté chez Action", "à moins de 20€", "qui buzzent sur TikTok"],
    "Astuce de pro": ["avec un outil maison", "connue des menuisiers", "qui évite les erreurs"],
    "Fails": ["que tout le monde fait", "à éviter absolument", "à ne pas reproduire"],
    "Transformation extrême": ["d’un meuble Ikea", "d’un garage en bureau", "d’une buanderie en dressing"]
}



videos1 = ["d6Wob4Lmo5g","wrjoGOPVcIE","HkVdG2htHbw","gCVyn7__qWw","6_8AlHTPKHc","zxD6nV1QCuY"]


nom_fichier="C:/Users/Mohan/Documents/tp/total.json"
videos_data = []

"""for i in range (len(videos1)) :
    infos_video = get_info_video(videos1[i])
    videos_data.append(infos_video)

with open(nom_fichier, "w", encoding="utf-8") as f:
    json.dump(videos_data, f, indent=2, ensure_ascii=False)"""
    
with open(nom_fichier, "r", encoding="utf-8") as f:
    data_videos = json.load(f)
    
titles = [v["title"] for v in data_videos]
print(titles)

print("Analyse des formats populaires...")
formats = extract_formats(titles)
print(formats)




sujets = extraire_sujets(titles)
print("📈 Sujets populaires détectés :", sujets)

# 🔄 Génération d'idées
for i in range(5):
    print(f"{i+1}. {generer_idee(niche='bricolage')}")
    
 

