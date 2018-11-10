import yaml

from pymongo import MongoClient, ASCENDING, DESCENDING

from repo.controllers.path_manager import MONGO_CONFIG_PATH


class MongoManager():
    def __init__(self, host=None, port=None):
        if host is None:
            with open(MONGO_CONFIG_PATH) as f:
                conf = yaml.safe_load((f.read()))

            host = conf['host']

        if port is None:
            with open(MONGO_CONFIG_PATH) as f:
                conf = yaml.safe_load((f.read()))

            port = conf['port']

        self.host = host
        self.port = port
        self.db = None
        self.client = MongoClient(host, port)  # MongoDBに接続する。
        self.collection = None

    def set_db(self, db_name):
        self.db = getattr(self.client, db_name)

    def set_collection(self, collecton_name):
        self.collection = getattr(self.db, collecton_name)

    def get_latest_record(self):
        return self.collection.find().sort("time", DESCENDING)[0]

    def initialize_collection(self):
        return self.collection.delete_many({})


if __name__ == '__main__':
    pass
