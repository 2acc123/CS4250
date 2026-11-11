import re
from collections import Counter
from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017")["cs4250_assignment3"]
documents = db["documents"]
inverted_index = db["inverted_index"]


def tokenize(text):
    # lowercase + remove punctuation, nothing else
    return re.sub(r"[^\w\s]", "", text.lower()).split()


def add_postings(doc_id, text):
    for term, tf in Counter(tokenize(text)).items():
        # upsert creates the term document if it doesn't exist yet
        inverted_index.update_one(
            {"term": term},
            {"$push": {"postings": {"docId": doc_id, "tf": tf}}},
            upsert=True)


def remove_postings(doc_id):
    inverted_index.update_many(
        {"postings.docId": doc_id},
        {"$pull": {"postings": {"docId": doc_id}}})
    # remove any term with no postings left
    inverted_index.delete_many({"postings": {"$size": 0}})


def insert_document(doc):
    documents.insert_one(doc)
    add_postings(doc["_id"], doc["text"])


def update_document(doc):
    remove_postings(doc["_id"])
    documents.replace_one({"_id": doc["_id"]}, doc)
    add_postings(doc["_id"], doc["text"])


def delete_document(doc_id):
    documents.delete_one({"_id": doc_id})
    remove_postings(doc_id)


if __name__ == "__main__":
    documents.delete_many({})
    inverted_index.delete_many({})

    insert_document({"_id": 1, "text": "Summer rain is common in Florida."})    # Op 1
    insert_document({"_id": 2, "text": "Summer is hot in Arizona."})            # Op 2
    update_document({"_id": 1, "text": "Summer rain is hot rain in Florida."})  # Op 3
    insert_document({"_id": 3, "text": "Hot summer rain in California."})       # Op 4
    delete_document(1)                                                          # Op 5

    for d in inverted_index.find({}, {"_id": 0}).sort("term", 1):
        print(d)
