from math import sqrt
import string
import os
import Queue
import sys

# Global variables
topic_vectors = {}
cand_names = ["SANDERS", "CLINTON"]
doc_vectors = { cand_names[0]: [], cand_names[1]: [] }
doc_texts   = { cand_names[0]: [], cand_names[1]: [] }

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
		# Add term to the current topic's term vector

		topic_vectors[topic][line] = 1

def initialize_document_vectors():
	for cand_name in cand_names:
		for subdir, dirs, files in os.walk("./Speeches/" + cand_name):
			for file in files:
				f = open("./Speeches/" + cand_name + "/" + file, "r")
				for line in f:
					doc = line.strip()
					# Store original text of document at same index as doc vector
					doc_texts[cand_name].append(doc)
					# Remove punctuation
					doc = doc.translate(string.maketrans("",""), string.punctuation)
					doc_terms = doc.split()
					# Create new doc vector
					doc_vector = {}
					# Build term frequency vector for document
					for term in doc_terms:
						if term in doc_vector:
							doc_vector[term] += 1
						else:
							doc_vector[term] = 1
					# Add to document vectors list for this candidate
					doc_vectors[cand_name].append(doc_vector)

def cosine_sim(vec1, vec2):
	num     = 0
	sum_sq1 = 0
	sum_sq2 = 0

	val1 = vec1.values()
	val2 = vec2.values()

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

	sum_mult = sum_sq1 * sum_sq2
	if sum_mult == 0:
		return 0
	return num / sqrt(sum_mult);

def compute_similarities(topic_vector, num_results, cand_name):
	pqueue = Queue.PriorityQueue()
	for i in range(len(doc_vectors[cand_name])):
		doc_vector = doc_vectors[cand_name][i]
		sim = cosine_sim(topic_vector, doc_vector)
		# Put negative of similarity into pqueue because we want it to sort
		# such that the greatest similarity is at the top
		pqueue.put((-sim, i))

	# Fetch top num_results docs
	return_list = []
	for i in range(num_results):
		return_list.append(pqueue.get())

	return return_list

def build_topic_vector(line):
	topic_vector = {}
	terms = line.split()
	for term in terms:
		if term in topic_vector:
			topic_vector[term] += 1
		else:
			topic_vector[term] = 1

	return topic_vector

def print_results(results, cand_name, topic):
	print("-" * 50)
	print("Top " + str(len(results)) + " results for " + cand_name)
	print("  TOPIC: " + topic)
	print("-" * 50)
	print("")

	# Print each result and the document text to go with it
	for i in range(len(results)):
		result_heading = "EXCERPT #" + str(i + 1) + ":"
		print(result_heading)
		print("-" * len(result_heading))
		print(doc_texts[cand_name][results[i][1]])
		print("")

	print("")

def main():
	initialize_topic_vectors()
	initialize_document_vectors()

	# Print welcome message
	print("""
--------------------------------------------------------------------
Welcome to the Democratic Debate Viewpoint Extractor

This tool allows you to select between the two democratic candidates
(Bernie Sanders and Hillary Clinton) and identify topics that they
have discussed in the official debates for the 2016 Democratic
primaries.
--------------------------------------------------------------------
""")

	# Start main menu
	while True:
		print("""
Main Menu
---------""")

		# Select candidate name
		cand_name = None
		while True:
			print("""
Select candidate to analyze:
   1) Bernie Sanders
   2) Hillary Clinton
Enter 'q' to quit program.
""")
			sys.stdout.write("Option: ")
			opt = sys.stdin.readline().strip()
			if opt == "1":
				cand_name = cand_names[0]
				break
			elif opt == "2":
				cand_name == cand_names[1]
				break
			elif opt.lower() == "q":
				# Quit program
				print("")
				print("Goodbye!")
				sys.exit(0)
			else:
				print("Error: invalid option, please try again")

		# Select topic type
		use_preset_topic = True
		while True:
			print("""
Select the type of topic you want to search by:
   1) Choose from a list of pre-defined topics
   2) Input your own custom topic
""")
			sys.stdout.write("Option: ")
			opt = sys.stdin.readline().strip()
			if opt == "1":
				break
			elif opt == "2":
				use_preset_topic = False
				break
			else:
				print("Error: invalid option, please try again")

		# Have user choose the actual topic
		topic_vector = None
		topic_name   = None
		if use_preset_topic:
			# User wants to choose from list of pre-defined topics
			while True:
				print("""
Select the type of topic you want to search by:""")
				topics = topic_vectors.keys()
				for i in range(len(topics)):
					print("   " + str(i + 1) + ") " + topics[i].title())
				print("")
				sys.stdout.write("Option: ")

				# Cast option to integer
				try:
					opt = int(sys.stdin.readline().strip())
				except ValueError:
					print("Error: invalid option, please try again")
					continue

				# Execute on option
				if opt >= 1 and opt <= len(topics):
					opt = opt - 1
					topic_vector = topic_vectors[topics[opt]]
					topic_name   = topics[opt]
					break
				else:
					print("Error: invalid option, please try again")
		else:
			# User wants to specify a custom topic
			while True:
				print("""
Please type a list of relevant terms defining your topic, each separated by a space.
Keywords: """)

				opt = sys.stdin.readline().strip()
				# Generate a vector with the given topic keywords
				topic_vector = build_topic_vector(opt)
				topic_name   = opt

		# Ask user for max number of results to return
		num_results = None
		while True:
			sys.stdout.write("Number of results to be reported: ")

			# Cast option to integer
			try:
				opt = int(sys.stdin.readline().strip())
			except ValueError:
				print("Error: invalid option, please try again")
				continue

			# Correct num results if bounds are wrong
			if opt > len(doc_vectors[cand_name]):
				opt = len(doc_vectors[cand_name])
			elif opt < 1:
				opt = 5  # default of 5 results
			num_results = opt
			break

		# Finally, compute similarities and return results
		results = compute_similarities(topic_vector, num_results, cand_name)
		print_results(results, cand_name, topic_name)

main()
