class Collection:
    def __init__(self, name, database):
        self.name = name
        self.database = database
        self.collection = self.database.get_collection(self.name)

    def insert_one(self, data) -> str:
        return self.collection.insert_one(data)

    def find_one(self, query) -> dict:
        return self.collection.find_one(query)

    def find(self, query) -> list:
        return self.collection.find(query)
