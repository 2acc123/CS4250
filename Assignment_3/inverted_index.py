#-------------------------------------------------------------------------
# author: Anson Ng
# filename: inverted_index.py
# specification: maintains a mongodb inverted index that stays in sync
#                with a collection of documents (insert, update, delete)
# for: cs 4250 - assignment #3
# time spent: 1 hour 33 minutes
#-------------------------------------------------------------------------

# importing python libraries
import string
from pymongo import MongoClient

# connecting to mongodb
client = MongoClient("mongodb://localhost:27017/")

# accessing the database and collections
db = client["assignment3"]
documents = db["documents"]
inverted_index = db["inverted_index"]

# start from a clean state so the script can be run repeatedly
documents.delete_many({})
inverted_index.delete_many({})

# inverted index schema:
# { "_id": term, "postings": [ { "docId": 1, "tf": 2 }, ... ] }

#-------------------------------------------------------------------------
# function: getTermFrequencies
# specification: receives a text and returns the frequency of each term
#-------------------------------------------------------------------------
def getTermFrequencies(text):

    # converting text to lowercase
    text = text.lower()

    # removing punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # splitting the text into terms
    terms = text.split()

    # returning the term frequencies
    frequencies = {}
    for term in terms:
        frequencies[term] = frequencies.get(term, 0) + 1
    return frequencies

#-------------------------------------------------------------------------
# function: addPosting
# specification: adds a posting to an existing term or creates a new term
#-------------------------------------------------------------------------
def addPosting(term, docId, tf):

    # searching for the term in the inverted index
    entry = inverted_index.find_one({"_id": term})

    # creating a new term if it does not exist
    if entry is None:
        inverted_index.insert_one({
            "_id": term,
            "postings": [{"docId": docId, "tf": tf}]
        })

    # adding a posting if the term already exists
    else:
        inverted_index.update_one(
            {"_id": term},
            {"$push": {"postings": {"docId": docId, "tf": tf}}}
        )

#-------------------------------------------------------------------------
# function: removePosting
# specification: removes a document posting from a term and deletes the
# term if its postings list becomes empty
#-------------------------------------------------------------------------
def removePosting(term, docId):

    # removing the posting from the term
    inverted_index.update_one(
        {"_id": term},
        {"$pull": {"postings": {"docId": docId}}}
    )

    # retrieving the term after removing the posting
    entry = inverted_index.find_one({"_id": term})

    # deleting the term if its postings list is empty
    if entry is not None and len(entry["postings"]) == 0:
        inverted_index.delete_one({"_id": term})

#-------------------------------------------------------------------------
# function: insertDocument
# specification: inserts a document and updates the inverted index
#-------------------------------------------------------------------------
def insertDocument(document):

    # inserting the document into the documents collection
    documents.insert_one(document)

    # obtaining the term frequencies
    frequencies = getTermFrequencies(document["text"])

    # updating the inverted index
    for term, tf in frequencies.items():
        addPosting(term, document["_id"], tf)

#-------------------------------------------------------------------------
# function: updateDocument
# specification: updates a document and makes the corresponding changes
# to the inverted index
#-------------------------------------------------------------------------
def updateDocument(docId, newText):

    # retrieving the current document
    document = documents.find_one({"_id": docId})
    if document is None:
        return

    # obtaining the old and new term frequencies
    oldFrequencies = getTermFrequencies(document["text"])
    newFrequencies = getTermFrequencies(newText)

    # processing terms that existed in the old document
    for term, oldTf in oldFrequencies.items():
        if term in newFrequencies:
            # the term is still present, so update its frequency if it changed
            if newFrequencies[term] != oldTf:
                inverted_index.update_one(
                    {"_id": term, "postings.docId": docId},
                    {"$set": {"postings.$.tf": newFrequencies[term]}}
                )
        else:
            # the term no longer appears in the document
            removePosting(term, docId)

    # processing terms that occur only in the new document
    for term, newTf in newFrequencies.items():
        if term not in oldFrequencies:
            addPosting(term, docId, newTf)

    # updating the document text
    documents.update_one({"_id": docId}, {"$set": {"text": newText}})

#-------------------------------------------------------------------------
# function: deleteDocument
# specification: deletes a document and removes all of its postings from
# the inverted index
#-------------------------------------------------------------------------
def deleteDocument(docId):

    # retrieving the document before deleting it
    document = documents.find_one({"_id": docId})
    if document is None:
        return

    # obtaining the terms contained in the document
    terms = getTermFrequencies(document["text"]).keys()

    # removing the document from every corresponding posting list
    for term in terms:
        removePosting(term, docId)

    # deleting the document
    documents.delete_one({"_id": docId})

#-------------------------------------------------------------------------
# executing the sequence of operations
#-------------------------------------------------------------------------

# operation 1: document 1 is obtained
document1 = {
    "_id": 1,
    "text": "Summer rain is common in Florida."
}
insertDocument(document1)

# operation 2: document 2 is obtained
document2 = {
    "_id": 2,
    "text": "Summer is hot in Arizona."
}
insertDocument(document2)

# operation 3: document 1 is updated
updateDocument(
    1,
    "Summer rain is hot rain in Florida."
)

# operation 4: document 3 is obtained
document3 = {
    "_id": 3,
    "text": "Hot summer rain in California."
}
insertDocument(document3)

# operation 5: document 2 is deleted
deleteDocument(2)

# operation 6: print the content of the documents and inverted_index collections
print("documents collection:")
for doc in documents.find().sort("_id", 1):
    print(doc)

print("\ninverted_index collection:")
for entry in inverted_index.find().sort("_id", 1):
    print(entry)
