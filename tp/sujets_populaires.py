import re
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords_fr = stopwords.words('french')


# --- Étape 1 : nettoyage de texte ---
def nettoyer_titre(titre):
    titre = titre.lower()
    titre = re.sub(r"[^\w\s]", "", titre)  # remove punctuation
    titre = re.sub(r"\d+", "", titre)      # remove digits
    return titre.strip()

# --- Étape 2 : extraire mots fréquents ---
def extraire_mots_frequents(titres, top_n=10, min_freq=2):
    titres_nets = [nettoyer_titre(t) for t in titres]
    vectorizer = CountVectorizer(stop_words=stopwords_fr)
    X = vectorizer.fit_transform(titres_nets)

    mots_freq = zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0])
    mots_tries = sorted(mots_freq, key=lambda x: x[1], reverse=True)

    return [mot for mot, freq in mots_tries if freq >= min_freq][:top_n]
# --- Étape 3 : mapping intelligent vers des sujets ---
MAPPING_SUJETS = {
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
    "peinture": "peinture murale"
}

def appliquer_mapping(mots):
    sujets = []
    for mot in mots:
        sujet = MAPPING_SUJETS.get(mot, mot)
        if sujet not in sujets:
            sujets.append(sujet)
    return sujets

# --- Fonction principale du module ---
def extraire_sujets(titres_videos, top_n=10):
    mots = extraire_mots_frequents(titres_videos, top_n=top_n)
    sujets = appliquer_mapping(mots)
    return sujets