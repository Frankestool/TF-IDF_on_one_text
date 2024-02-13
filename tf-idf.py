# coding: utf-8
import re
from math import log10,log2
import pandas as pd
import plotly.express as px
file = open("les_miserables","r",encoding="utf-8")

texte = file.read()

liste_phrases = re.split("[.]",texte) # we cut the text in sentences on : "," et "."


for i in range(len(liste_phrases)):
    liste_phrases[i] =  re.sub("[':;()]"," ",liste_phrases[i].strip().lower() ) # we remove theses symbols of each sentence 

texte_sans_ponctuation = re.sub("[:();,.'’]"," ",texte).strip().lower() # We remove the punctuation of the text 
liste_mots= re.split("\s{1}",texte_sans_ponctuation) # we split on spaces 


dico_nb_occurence_par_mot = {}
for mot in liste_mots : # we create "dico_nb_occurence_par_mot", a dictionnary witch contains the name and occurence numbers of each word 

    if  re.match("^\d*$",mot) == None :
        if re.match("^\w?$",mot) == None :
            if mot in dico_nb_occurence_par_mot.keys() :
                dico_nb_occurence_par_mot[mot] += 1
            else :
                dico_nb_occurence_par_mot[mot] = 1

# classic implementation of term frequency =  ( number of occurence of each word ) / ( total number of word )
def real_tf (mot,dico_occurence):
    nombre_mots= sum(dico_occurence.values())
    return dico_occurence[mot]/nombre_mots

# We use logarithm to minimize ratio between "stop" word and rare word, classic tf ratio was to high it weighted too much on idf , we called it adjusted_tf
def tf (mot,dico_occurence): 
    nombre_mots= sum(dico_occurence.values())
    return log2((dico_occurence[mot]/nombre_mots)/0.0000009 )


# We use classic idf formula adapted on pieces of sentences, idf_t=   log10( total number of sentences  / number of sentence where the word t is present )
def  idf(mot,liste_phrases):
    nombre_phrases= len(liste_phrases)
    nombre_occurence = 0
    for phrase in liste_phrases :
        if mot in phrase :
            nombre_occurence +=1
    return log10(nombre_phrases/nombre_occurence)

# we count the total words ( punctuation is not counted ) 
nombre_mots = sum(dico_nb_occurence_par_mot.values())


liste_mots_idf = []
for mot in dico_nb_occurence_par_mot.keys():  # we create a matrice containing the word,idf, classic-tf, adjusted_tf, tf_idf
    liste_mots_idf.append([mot,idf(mot,liste_phrases),real_tf(mot,dico_nb_occurence_par_mot),tf(mot,dico_nb_occurence_par_mot),idf(mot,liste_phrases)*tf(mot,dico_nb_occurence_par_mot),dico_nb_occurence_par_mot[mot]])

# we convert it into a dataframe 
df = pd.DataFrame(liste_mots_idf,columns = ["mot","idf","tf","tf_ajusté","tf_idf","nombre_occurences"])


# we select the first 20 word sorted by adjusted_tf*idf 
mots_caracteristique =  df.sort_values("tf_idf",ascending=False).head(20)
file.close()

fig = px.scatter(mots_caracteristique, x="tf_ajusté", y="idf",size="tf_idf", color="nombre_occurences",hover_name="mot")
fig.show()
