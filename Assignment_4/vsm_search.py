#-------------------------------------------------------------------------
# AUTHOR: Anson Ng
# FILENAME: vsm_search.py
# SPECIFICATION: VSM search engine (TF-IDF + cosine similarity) evaluated with AP and MAP
# FOR: CS 4250 - Assignment #4
# TIME SPENT: 3 hours 39 minutes
#-----------------------------------------------------------*/

# importing required libraries
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# 1. Load the input files
# ---------------------------------------------------------
docs = pd.read_csv("docs.csv")
queries = pd.read_csv("queries.csv")
judgments = pd.read_csv("relevance_judgments.csv")

doc_ids = docs["doc_id"].tolist()

# ---------------------------------------------------------
# 2. Build the TF-IDF matrix for the documents
# ---------------------------------------------------------
# Requirement: remove stopwords only
vectorizer = TfidfVectorizer(stop_words="english")
doc_matrix = vectorizer.fit_transform(docs["text"])

# ---------------------------------------------------------
# 3. Process each query and compute AP values
# ---------------------------------------------------------
ap_scores = {}

for _, row in queries.iterrows():
    qid = row["query_id"]
    q_vec = vectorizer.transform([row["query_text"]])

    # cosine similarity between the query and every document
    sims = cosine_similarity(q_vec, doc_matrix).flatten()

    # rank all documents by similarity (descending); ties broken by doc order
    ranking = sorted(zip(doc_ids, sims), key=lambda x: -x[1])

    # relevant documents for this query
    q_j = judgments[judgments["query_id"] == qid]
    relevant = set(q_j[q_j["judgment"] == "R"]["doc_id"])

    # -----------------------------------------------------
    # 4. Compute Average Precision (AP)
    # -----------------------------------------------------
    hits = 0
    precision_sum = 0.0
    for rank, (doc_id, score) in enumerate(ranking, start=1):
        if doc_id in relevant:
            hits += 1
            precision_sum += hits / rank

    ap_scores[qid] = precision_sum / len(relevant) if relevant else 0.0

# ---------------------------------------------------------
# 5. Sort queries by AP in descending order
# ---------------------------------------------------------
sorted_aps = sorted(ap_scores.items(), key=lambda x: -x[1])

# ---------------------------------------------------------
# 6. Print the sorted queries and their AP scores
# ---------------------------------------------------------
print("====================================================")
print("Queries sorted by Average Precision (AP):")
for qid, ap in sorted_aps:
    print(f"{qid}: AP = {ap:.4f}")

map_score = sum(ap_scores.values()) / len(ap_scores)
print("----------------------------------------------------")
print(f"MAP = {map_score:.4f}")
