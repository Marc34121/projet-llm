from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
#from app.services import get_info_video, 
from app.services import extraire_formats,get_video_comments
#from app.routes import sujet
from app.trends import extraire_sujets
from app.titlegen import generer_idees
from app.youtube import get_trending_gaming_videos
import json
#import os
#import HTTPException

app = FastAPI()
#app.include_router(sujet.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

videos_niche = {
    "bricolage": ["d6Wob4Lmo5g","wrjoGOPVcIE","HkVdG2htHbw","gCVyn7__qWw","6_8AlHTPKHc","zxD6nV1QCuY"],
    "gaming": ["zCKtXbnLX24","Ux9-wRRarr8","bx-ECHAuM58","tzOeY16lB64","KShfU9V7eBc","86McFSfqBoE","JXzQVpNL3lQ"],
    "cuisine": ["6ig-cfCGxNM","_ZPrOQikg0s","KSmoLQK297o","k_w3wD_eFBU","8lJ4j4kRaQc","yLTVKfCDuwk", "HuGwRSXGFUg"],
}


@app.get("/")
def home():
    return {"message": "Bienvenue sur ton générateur de vidéos tendance!"}


nom_fichier="C:/Users/Mohan/Documents/video-idea-gen/niche.json"
#☻nom_fichier="C:/Users/Mohan/Documents/video-idea-gen/total.json"

#if (os.path.exists(nom_fichier)):
    #os.remove(nom_fichier)
    
fic_cuisine="C:/Users/Mohan/Documents/video-idea-gen/cuisine.json"
fic_gaming="C:/Users/Mohan/Documents/video-idea-gen/gaming.json"
fic_brico="C:/Users/Mohan/Documents/video-idea-gen/bricolage.json"

#if (os.path.exists(nom_fichier)):
    #os.remove(nom_fichier)

videos_data = []

def getFichier(niche):
    fic_niche=""
    if niche == "cuisine":
        fic_niche = fic_cuisine
    elif niche == "gaming" :
        fic_niche = fic_gaming
    elif niche == "bricolage":
        fic_niche = fic_brico
    else:
        return "Niche non prise en charge"
    return fic_niche

    
@app.get("/videosYoutube")
def videosYoutube(niche: str = Query(...)):
    data_videos=get_trending_gaming_videos(niche,10)
    
    if not data_videos:
        return {"videos": []}

    videos = []
    for v in data_videos:
        video_id = v.get("id")
        title = v.get("snippet", {}).get("title")
        if video_id and title:
            videos.append({"id": video_id, "title": title})
    
    
    #with open(nom_fichier, "w", encoding="utf-8") as f:
        #json.dump(data_videos, f, indent=2, ensure_ascii=False)
    #print("videos YTB catVideoId:", videos)
    return {"videos": videos}
    



@app.get("/listeVideos")
def listeVideos(niche: str = Query(...)):  
    
    
    nom_fichier=getFichier(niche)
    with open(nom_fichier, "r", encoding="utf-8") as f:
        data_videos = json.load(f)
        
    videos = [{"id": v["id"]} for v in data_videos]
    
    if videos is None:
        return {"videos": []}
    return {"videos": videos}


@app.get("/recupTitres")
def recupTitres(niche : str = Query(...)):
    #videos = videos_niche.get(niche)   
    titres=[]
    """for video_id in videos :
        infos_video = get_info_video(video_id)
        titre_videos.append({
            "id": video_id,
            "titre": infos_video["title"]})
        videos_data.append(infos_video)

    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(videos_data, f, indent=2, ensure_ascii=False)"""
    
    nom_fichier=getFichier(niche)
    with open(nom_fichier, "r", encoding="utf-8") as f:
        data_videos = json.load(f)
        
    titres = [{"id": v["id"], "title": v["title"]} for v in data_videos]
        
    print(titres)
    return {"titres": titres}
    
@app.get("/recupFormats")
def recupFormats(niche:str=Query(...)):
    
    #nom_fichier=getFichier(niche)
    #with open(nom_fichier, "r", encoding="utf-8") as f:
    #    data_videos = json.load(f)
        
    listevideos= videosYoutube(niche)  
    titles = [video['title'] for video in listevideos['videos']]
    formats = extraire_formats(titles)
    
    return {"formats":formats}

@app.get("/recupSujets")
def recupSujets(niche:str=Query(...),top_n: int = 10):
    
    #nom_fichier=getFichier(niche)
    #with open(nom_fichier, "r", encoding="utf-8") as f:
    #    data_videos = json.load(f)
    
    listevideos= videosYoutube(niche)
    
    #titles = [v["title"] for v in data_videos]
    titles = [video['title'] for video in listevideos['videos']]
    sujets = extraire_sujets(titles,niche)
    
    return {"sujets":sujets}

@app.get("/recupIdees")
def recupIdees(niche:str=Query(...)):
    
    #nom_fichier=getFichier(niche)
    #with open(nom_fichier, "r", encoding="utf-8") as f:
    #    data_videos = json.load(f)
       
    listevideos= videosYoutube(niche)
    titles = [video['title'] for video in listevideos['videos']]
    formats = extraire_formats(titles)
    sujets = extraire_sujets(titles,niche)
   
    idees = generer_idees(formats,sujets,niche)
    print ("idees:",idees)
    return {"sujets":sujets , "idees":idees }

@app.get("/recupComments")
def recupComments(niche:str=Query(...)):
    listevideos = videosYoutube(niche)
    ids = [video['id'] for video in listevideos['videos']]
    comments=[]
    for id in ids:
        comment = get_video_comments(id, 25)
        comments.extend(comment)
        
    #print ("liste commentaire : ", listeComments   ) 
    return comments
        
    
