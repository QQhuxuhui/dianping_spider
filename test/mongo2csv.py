import csv
from pymongo import MongoClient

def read_data_from_collection(db, collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    return data

def write_data_to_csv(data, csv_filename):
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果 CSV 文件为空，写入标题
        if csvfile.tell() == 0:
            writer.writeheader()

        # 写入数据
        for row in data:
            writer.writerow(row)

def export_all_data_to_csv(database_name, csv_filename):
    # 连接 MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017/')
    
    # 选择数据库
    db = client[database_name]

    # 获取所有集合名称
    collections = db.list_collection_names()

    # 循环处理每个集合
    for collection_name in collections:
        print(f"Exporting data from collection: {collection_name}")
        data = read_data_from_collection(db, collection_name)
        write_data_to_csv(data, csv_filename)

    # 关闭 MongoDB 连接
    client.close()
    print(f"All data has been exported to {csv_filename}")

if __name__ == "__main__":
    # MongoDB 数据库名称
    mongodb_database_name = 'dianping'

    # CSV 文件名
    csv_filename = 'output.csv'

    # 导出所有数据到 CSV
    export_all_data_to_csv(mongodb_database_name, csv_filename)
