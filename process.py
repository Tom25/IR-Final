# Algorithm:
#  1. Load in initial set of terms for each political topic, creating vectors
#     of these terms for each topic.
#  2. Iterate through all transcript documents and compute the cosine similarity
#     between each document and each of the four topics' term vectors. Whichever
#     topic's vectors are most similar to the document's vector, add the most
#     "significant" terms in that document to the corresponding topic's vector.
#       - Aside: how do we determine which terms are "significant?"
#  3. Perform a second iteration through all of the transcript documents, once
#     again computing cosine similarity between each document's vector and each
#     topic's vector. Determine again which topic each document should belong to
#     by choosing the topic for which the document has the highest similarity 
#     score. Maintain a list of all document numbers assigned to each topic
#     and add each document to the proper list for each topic.
#  4. The user can then search by topic on the command line.

from math import sqrt

# Global variables
topic_vectors = {}
doc_vectors = {}

# This function expects the topics_terms.txt file to contain each pre-defined
# keyword for each topic to be on a separate line, and each new topic section
# to be denoted by a separate line starting with "T: " followed by the topic's
# name.
def initialize_topic_vectors():
    topics_file = open("topics_terms.txt", "r")
    topic = None  # current topic in file iteration

    for line in topics_file:
        line = line.strip()
        if line.startswith("T: "):
            # New topic has begun in file
            topic = line[3:].strip()  # extract topic name and set as current topic
            topic_vectors[topic] = {}  # initialize new term vector for topic
        elif line == "":
            continue
        else:
            # Add term to the current topic's term vector
            topic_vectors[topic][line] = 1.0

def initialize_document_vectors():
    pass

def cosine_sim(vec1, vec2):
    num     = 0
    sum_sq1 = 0
    sum_sq2 = 0

    val1 = vec1.keys()
    val2 = vec2.keys()

    # Determine shortest length vector. This should speed things up if one 
    # vector is considerably longer than the other.
    if len(val1) > len(val2):
        tmp  = vec1
        vec1 = vec2
        vec2 = tmp

    # Calculate the cross product
    key = None
    val = None

    for key in vec1:
        vec2_value = 0
        if key in vec2:
            vec2_value = vec2[key]
        num += vec1[key] * vec2_value

    # Calculate the sum of squares
    for term in val1:
        sum_sq1 += term * term
    for term in val2:
        sum_sq2 += term * term

    return num / sqrt( sum_sq1 * sum_sq2 );

def main():
    initialize_topic_vectors()
    initialize_document_vectors()

main()
