import random

TEMPLATES_C = [
    "Top {n} des {sujet}s {qualificatif}s",
    "Comment faire un {sujet} {qualificatif}",
    "{n} recettes de {sujet}s pour {public}",
    "{sujet} en moins de {temps}",
    "{sujet} sans {contrainte}",
    "Idées de {sujet}s {qualificatif}s à tester"
]

TEMPLATES_B = [
    "{form_video} : Top {n} des {sujet}s {qualificatif}s",
    "{form_video} :Comment fabriquer un {sujet} {qualificatif}",
    "{form_video} : {n}  construction de {sujet}s pour {public}",
    "{form_video} : {sujet} en moins de {temps}",
    "{form_video} : {sujet} sans {contrainte}",
    "{form_video} : Idées de {sujet}s {qualificatif}s à tester"
]

TEMPLATES_G = [
    "{form_video} : Top {n}  {sujet} {contrainte} pour {public}",
    "{form_video} : circuit {sujet} en moins de {temps}"
]



PUBLICS_G =  ["jeunes publics","hardcore gamer","Mobile gamer","compétitif"]
PUBLICS_C = ["étudiants", "débutants", "familles", "petits budgets"]
PUBLICS_B = ["jeunes adultes", "jeunes couples","étudiants", 
                   "audience tech & home office", "public économique",
                   "audience écologique","bricoleur du dimanche","MacGyver"]

TEMPS_C = ["10 minutes", "15 minutes", "5 minutes"]
TEMPS_B = ["2 heures tout rond", "4 heures chrono","3 heures chrono", "1 heure pile"]
TEMPS_G=["5 minutes", "2 heures chrono"  ]

CONTRAINTES_C = ["four", "cuisson", "œufs", "lactose"]
CONTRAINTES_B = ["outil", "colle", "visserie", "percer"]
CONTRAINTES_G = ["avec une seule main", "avec un joystick qui drift","les yeux bandés" ]

NOMBRES = [3, 5, 7]


QUALIFICATIFS_C = ["rapide", "facile", "pas cher", "healthy"]
QUALIFICATIFS_B = ["rapide", "facile", "écologique", "high design" ]
QUALIFICATIFS_G = ["pas cher", ]


#FORMAT_B = extract_formats(niche="bricolage")
#FORMAT_C = extract_formats(niche="cuisine")
#FORMAT_G = extract_formats(niche="gaming")*/

def generer_idees(formats_videos,sujets,niche,nb_idees=5):
    idees = []
    if niche=="cuisine":
        PUBLICS = PUBLICS_C
        QUALIFICATIFS = QUALIFICATIFS_C
        TEMPS=TEMPS_C
        CONTRAINTES=CONTRAINTES_C
        TEMPLATES=TEMPLATES_C  
    elif niche == "bricolage":
        PUBLICS = PUBLICS_B
        CONTRAINTES=CONTRAINTES_B
        QUALIFICATIFS = QUALIFICATIFS_B
        TEMPS=TEMPS_B
        TEMPLATES=TEMPLATES_B
    elif niche == "gaming":
        PUBLICS = PUBLICS_G
        CONTRAINTES=CONTRAINTES_G
        QUALIFICATIFS = QUALIFICATIFS_G
        TEMPS = TEMPS_G
        TEMPLATES=TEMPLATES_G
 
    for _ in range(nb_idees):
        template = random.choice(TEMPLATES)
        sujet = random.choice(sujets)
        titre = template.format(
            form_video = random.choice(formats_videos),
            sujet=sujet,
            qualificatif=random.choice(QUALIFICATIFS),
            public=random.choice(PUBLICS),
            temps=random.choice(TEMPS),
            contrainte=random.choice(CONTRAINTES),
            n=random.choice(NOMBRES)
        )
        idees.append(titre)
    return idees