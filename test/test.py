from pymongo import MongoClient

# 连接到MongoDB数据库
client = MongoClient('mongodb://localhost:27017/')

# 选择数据库和集合
db = client['dianping']
collection = db['info']

# 统计集合中的文档数量
document_count = collection.count_documents({})

print(f"Total number of documents in the collection: {document_count}")
