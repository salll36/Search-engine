import json
import jieba

def create_inverted_index(documents):
    inverted_index = {}
    for i,document in enumerate(documents):
        for word in document:
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(i+1)
    return inverted_index



document1 = []
with open("./json/data1.json", 'r') as f:
    document1 = json.loads(f.read())
document2 = []
with open("./json/data2.json", 'r') as f:
    document2 = json.loads(f.read())
documents = document1+document2



new_documents = []
for p in documents:
    new_documents.append(jieba.lcut(p['title']))

inverted_index = create_inverted_index(new_documents)

info = json.dumps(inverted_index)
with open("./json/inverted_index.json", 'w') as f:
    f.write(info)