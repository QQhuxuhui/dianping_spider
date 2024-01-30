import pandas as pd
from pymongo import MongoClient

def read_data_from_collection(db, collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    return data

def export_all_data_to_excel(database_name, excel_filename):
    # 连接 MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # 选择数据库
    db = client[database_name]

    # 获取所有集合名称
    collections = db.list_collection_names()

    # 创建一个空的 DataFrame
    all_data = pd.DataFrame()

    # 循环处理每个集合
    for collection_name in collections:
        print(f"从集合中导出数据: {collection_name}")
        data = read_data_from_collection(db, collection_name)

        # 将数据转换为 DataFrame
        collection_data = pd.DataFrame(data)

        # 追加到整体数据框中
        all_data = all_data.append(collection_data, ignore_index=True)

    # 关闭 MongoDB 连接
    client.close()

    # 导出到 Excel 文件
    all_data.to_excel(excel_filename, index=False)
    print(f"所有数据已导出到 {excel_filename}")

if __name__ == "__main__":
    # MongoDB 数据库名称
    mongodb_database_name = 'dianping'

    # Excel 文件名
    excel_filename = 'output.xlsx'

    # 导出所有数据到 Excel
    export_all_data_to_excel(mongodb_database_name, excel_filename)
