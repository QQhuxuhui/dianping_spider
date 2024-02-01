import pymongo

# 连接到MongoDB数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")  # 根据实际情况更改连接字符串和端口

# 选择数据库
db = client["dianping"]  # 将 "your_database_name" 替换为你的数据库名称
# 选择集合（类似于关系数据库中的表）
collection = db["region_1"]  # 将 "region" 替换为你的集合名称

# 查询数据 - 获取所有文档
query = {}

# 获取数据
regions = collection.find(query)

# 打印结果
# for region in resions:
#     print(region)


# 选择集合（类似于关系数据库中的表）
collection = db["classfy_1"]  # 将 "region" 替换为你的集合名称

# 查询数据 - 获取所有文档
query = {}

# 获取数据
classfys = collection.find(query)
# for region in resions:
#     print('区域名称:', region.get('区域名称'), ', 区域ID:', region.get('区域id'))
# 打印结果
url_data_list = [];

# for classfy in classfys:
#     print(classfy.get('分类名称'))

regions_list = list(regions)

for classfy in classfys:
    url = classfy.get('href')
    for region in regions_list:
        print('区域名称:', region.get('区域名称'), ', 区域ID:', region.get('区域id'), ', 分类名称', classfy.get('分类名称'))
        href = region.get('href');
        last_slash_index = href.rfind('/')
        regionId = href[last_slash_index + 1:]
        url_new = url + regionId
        data = {
            'url': url_new,
            '区域名称': region.get('区域名称'),
            '区域id': region.get('区域id'),
            '分类名称': classfy.get('分类名称'),
            '分类id': classfy.get('分类id'),
        }
        url_data_list.append(data)

 # 保存入库       


# 选择集合（类似于关系数据库中的表）
collection = db["url_1"]  # 将 "your_collection_name" 替换为你的集合名称

# 将多个文档插入到集合中
insert_result = collection.insert_many(url_data_list)

# 打印插入的文档的ObjectIds
print("插入的文档的ObjectIds:", insert_result.inserted_ids)


# 关闭连接
client.close()
