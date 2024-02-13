# coding: utf-8
import re
from math import log10,log2
import pandas as pd
import plotly.express as px
file = open("les_miserables","r",encoding="utf-8")

texte = file.read()

liste_phrases = re.split("[.]",texte) # on coupe le texte en bouts de phrase "," et "."


for i in range(len(liste_phrases)):
    liste_phrases[i] =  re.sub("[':;()]"," ",liste_phrases[i].strip().lower() )

texte_sans_ponctuation = re.sub("[:();,.'’]"," ",texte).strip().lower()
liste_mots= re.split("\s{1}",texte_sans_ponctuation) # on sépare sur les espaces


dico_nb_occurence_par_mot = {}

for mot in liste_mots : # im
    if  re.match("^\d*$",mot) == None :
        if re.match("^\w?$",mot) == None :
            if mot in dico_nb_occurence_par_mot.keys() :
                dico_nb_occurence_par_mot[mot] += 1
            else :
                dico_nb_occurence_par_mot[mot] = 1


def tf (mot,dico_occurence):
    nombre_mots= sum(dico_occurence.values())
    return log2((dico_occurence[mot]/nombre_mots)/0.0000009 )

def real_tf (mot,dico_occurence):
    nombre_mots= sum(dico_occurence.values())
    return dico_occurence[mot]/nombre_mots

def  idf(mot,liste_phrases):
    nombre_phrases= len(liste_phrases)
    nombre_occurence = 0
    for phrase in liste_phrases :
        if mot in phrase :
            nombre_occurence +=1
    return log10(nombre_phrases/nombre_occurence)


nombre_mots = sum(dico_nb_occurence_par_mot.values())


liste_mots_idf = []

for mot in dico_nb_occurence_par_mot.keys():
    liste_mots_idf.append([mot,idf(mot,liste_phrases),real_tf(mot,dico_nb_occurence_par_mot),tf(mot,dico_nb_occurence_par_mot),idf(mot,liste_phrases)*tf(mot,dico_nb_occurence_par_mot),dico_nb_occurence_par_mot[mot]])


df = pd.DataFrame(liste_mots_idf,columns = ["mot","idf","tf","tf_ajusté","tf_idf","nombre_occurences"])



mots_caracteristique =  df.sort_values("tf_idf",ascending=False).head(20)
file.close()

fig = px.scatter(mots_caracteristique, x="tf_ajusté", y="idf",size="tf_idf", color="nombre_occurences",hover_name="mot")
fig.show()