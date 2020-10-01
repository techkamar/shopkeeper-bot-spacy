import spacy
import random

# Load custom model fom 'models' folder
nlp = spacy.load("models/shopkeeper-model")
doc = nlp("list kg of almonds")
for ent in doc2.ents:
    print(ent.label_, ent.text)