def get_solution(f):
	from collections import Counter
	from math import log

	documents = f.read().split('-----')
	documents = [doc.split() for doc in documents]

	max_tf_idf, max_tf_idf_word = 0, None
	idfs = {}
	tot_num_docs = len(documents)
	for document in documents:
		words = set(document)
		for word in words:
			if word in idfs:
				idfs[word] += 1
			else:
				idfs[word] = 1

	for word in idfs:
		idfs[word] = log(tot_num_docs / idfs[word] ,10)

	for document in documents:
		words = Counter(document)
		tot_doc_terms = len(document)
		for word in words:
			tf = words[word] / tot_doc_terms
			tf_idf = tf * idfs[word]
			if tf_idf > max_tf_idf:
				max_tf_idf = tf_idf
				max_tf_idf_word = word



	return max_tf_idf_word


if __name__ == '__main__':
	print(get_solution(open('input_6.txt','r')))