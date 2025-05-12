import json

class retrieval:
    def __init__(self, key):
        self.key = key
    def jiansuo(self):
        obj = {}
        with open("./json/inverted_index.json", 'r') as f:
            obj = json.loads(f.read())
        id_list = obj[self.key]

        document1 = []
        with open("./json/data1.json", 'r') as f:
            document1 = json.loads(f.read())
        document2 = []
        with open("./json/data2.json", 'r') as f:
            document2 = json.loads(f.read())
        documents = document1 + document2

        result = []
        mylist = []
        for i,p in enumerate(id_list):
            if len(mylist)==10:
                result.append(mylist)
                mylist = []
            else:
                mylist.append({
                    "href": documents[p - 1]["url"],
                    "title": documents[p - 1]["title"],
                    "text": documents[p - 1]["body"]
                })
        result.append(mylist)
        return result

