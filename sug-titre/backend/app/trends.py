import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

# --- Étape 1 : nettoyage de texte ---
def nettoyer_titre(titre):
    titre = titre.lower()
    titre = re.sub(r"[^\w\s]", "", titre)  # remove punctuation
    titre = re.sub(r"\d+", "", titre)      # remove digits
    return titre.strip()

# --- Étape 2 : extraire mots fréquents ---
def extraire_mots_frequents(titres, top_n=10, min_freq=2):
    titres_nets = [nettoyer_titre(t) for t in titres]
    stopwords_fr = stopwords.words('french')
   
    vectorizer = CountVectorizer(stop_words=stopwords_fr)
    X = vectorizer.fit_transform(titres_nets)
    mots_freq = zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0])
    mots_tries = sorted(mots_freq, key=lambda x: x[1], reverse=True)
    
    return [mot for mot, freq in mots_tries if freq >= min_freq][:top_n]
    #return [s[0] for s in mots_tries[:5]]

# --- Étape 3 : mapping intelligent vers des sujets ---
MAPPING_SUJETS_BRICO = {
    "palette": "meubles en palette",
    "garage": "transformation extrême",
    "studio": "aménagement petit espace",
    "balcon": "aménagement extérieur",
    "outils": "test d’outils",
    "action": "test d’outils",
    "époxy": "époxy / résine",
    "bois": "tuto bois",
    "rangement": "optimisation rangement",
    "visseuse": "test d’outils",
    "perceuse": "test d’outils",
    "transformation": "avant / après",
    "défi": "défi 24h",
    "erreurs": "fails bricolage",
    "peinture": "peinture murale",
    "menuiserie" : "meuble"
}

MAPPING_SUJETS_CUISINE = {
    "pâtes": "recette",
    "spaghetti": "pâtes",
    "lasagne": "pâtes",
    "carbonara": "pâtes",

    "gâteau": "dessert",
    "tarte": "dessert",
    "mousse": "dessert",
    "brownie": "dessert",

    "sushis": "traiteur",

    "salade": "entrée",
    "entrée": "entrée",
    "crudités": "entrée",

    "curry": "plat",
    "gratin": "plat",
    "poêlée": "plat",
    "ragoût": "plat",

    "four": "cuisson",
    "poêle": "cuisson",
    "cuisson": "cuisson",
    "vapeur": "cuisson",
    "micro-ondes": "cuisson",

    "vegan": "végétarien",
    "végétarien": "végétarien",
    "sans viande": "végétarien",
    "sans lactose": "végétarien",

    "rapide": "rapide",
    "facile": "rapide",
    "express": "rapide",

    "pas cher": "économique",
    "économique": "économique",
    "budget": "économique"
}

MAPPING_SUJETS_GAMING = {
    
    # Jeux populaires
    "fortnite": "battle royale",
    "warzone": "battle royale",
    "pubg": "battle royale",
    "valorant": "fps",
    "csgo": "fps",
    "counter-strike": "fps",
    "overwatch": "fps",
    "apex": "fps",
    "minecraft": "sandbox",
    "roblox": "sandbox",
    "gta": "open world",
    "zelda": "aventure",
    "elden ring": "rpg",
    "skyrim": "rpg",
    "fifa": "sport",
    "nba": "sport",
    "rocket league": "sport",
    "lol": "moba",
    "league of legends": "moba",
    "dota": "moba",
    "genshin impact": "rpg",
    "among us": "party game",

    # Types de vidéos
    "funny": "moments drôles",
    "fails": "moments drôles",
    "best moments": "highlights",
    "highlights": "highlights",
    "gameplay": "gameplay",
    "compilation": "montage",
    "trailer": "annonce",
    "review": "critique",
    "test": "critique",
    "guide": "tutoriel",
    "tutorial": "tutoriel",
    "tips": "astuces",
    "walkthrough": "solution",
    "speedrun": "speedrun",

    # Joueurs / contextes
    "noob": "débutant",
    "pro": "compétitif",
    "ranked": "classé",
    "troll": "fun",
    "1v1": "duel",
    "clutch": "compétitif",
    "montage": "montage",
    "mod": "modding",
    "rp": "jeu de rôle",
    "hardcore": "difficile",
    "challenge": "défi",

    # Plateformes / modes
    "pc": "plateforme",
    "console": "plateforme",
    "xbox": "plateforme",
    "playstation": "plateforme",
    "ps5": "plateforme",
    "mobile": "plateforme",
    "multiplayer": "multijoueur",
    "solo": "solo"

}
MAPPING={}


def appliquer_mapping(mots,niche):
    sujets = []
    if niche =="gaming":
        MAPPING=MAPPING_SUJETS_GAMING
    elif niche == "bricolage":
        MAPPING=MAPPING_SUJETS_BRICO
    elif niche == "cuisine":
        MAPPING= MAPPING_SUJETS_CUISINE
    else :
        MAPPING={}
        
    for mot in mots:
        sujet = MAPPING.get(mot, mot)
        if sujet not in sujets:
            sujets.append(sujet)
    return sujets

# --- Fonction principale du module ---
def extraire_sujets(titres_videos, niche, top_n=10):
    mots = extraire_mots_frequents(titres_videos, top_n = top_n)  
    print ("mots:", mots)
    sujets = appliquer_mapping(mots,niche)  
    return sujets