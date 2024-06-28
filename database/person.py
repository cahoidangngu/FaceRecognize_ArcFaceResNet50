# from database.collection import Collection
# from bson.objectid import ObjectId


# class Person(Collection):
#     def add_person(self, person):
#         insert_result = self.insert_one(person)

#         return str(insert_result.inserted_id)

#     def find_by_id(self, id):
#         result = self.find_one({"_id": ObjectId(id)})

#         return result

#     def get_all(self):
#         result = self.find({})

#         return result



class Person:
    def __init__(self, database):
        self.database = database

    def add_person(self, person):
        query = "INSERT INTO persons (name) VALUES (%s)"
        params = (person['name'],)
        self.database.execute_query(query, params)
        return self.database.cursor.lastrowid

    def get_all(self):
        query = "SELECT * FROM persons"
        return self.database.fetch_all(query)

    def find_by_id(self, person_id):
        query = "SELECT * FROM persons WHERE id = %s"
        params = (person_id,)
        return self.database.fetch_one(query, params)