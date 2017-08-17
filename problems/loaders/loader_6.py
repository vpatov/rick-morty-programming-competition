with open('input_6.txt','r') as f:
	documents = f.read().split('-----')
	documents = [doc.split() for doc in documents]

print(documents)