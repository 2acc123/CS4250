#-------------------------------------------------------------------------
# AUTHOR: Anson Ng
# FILENAME: index.py
# SPECIFICATION: Creates an inverted index from a collection of documents
# FOR: CS 4250 - Assignment #1
# TIME SPENT: 2 hours 10 minutes
#-------------------------------------------------------------------------

# Importing Python libraries
import pandas as pd

# Reading the document collection
data = pd.read_csv("collection.csv")

# Defining the dictionary used for lemmatization
# --> add your Python code here
lemmas = {
    "homes": "home",
    "sales": "sale",
    "increases": "increase",
    "increasing": "increase",
    "rising": "rise"
}

# Creating the data structure that will store the inverted index
invertedIndex = {}

# Processing each document in the collection
for i, row in data.iterrows():
    docID = row["Document"]
    text = row["Text"]

    # Applying surface-level normalization
    text = text.lower()
    text = text.replace(".", "")

    # Tokenizing the document
    tokens = text.split()

    # Applying lemmatization
    tokens = [lemmas.get(token, token) for token in tokens]

    # Building the inverted index
    for token in tokens:
        if token not in invertedIndex:
            invertedIndex[token] = []

        if docID not in invertedIndex[token]:
            invertedIndex[token].append(docID)


# Printing the inverted index with terms ordered alphabetically
# Expected format:
# term1 : ['Doc1', 'Doc2']
# term2 : ['Doc3']
for term in sorted(invertedIndex):
    print(term, ":", invertedIndex[term])
