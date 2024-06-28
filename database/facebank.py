# from database.collection import Collection
# from utils import decode_image, encode_image


# class Facebank(Collection):
#     def __init__(self, name, database, embedding_path):
#         super().__init__(name, database)

#         self.embedding_path = embedding_path
#         self.num_candidates = 100

#     def add_face(self, image, embedding, person_id):
#         encoded_image = encode_image(image)

#         face = {
#             "image": encoded_image,
#             "image_shape": image.shape,
#             "person_id": person_id,
#             "embedding": embedding.reshape(-1).tolist(),
#         }

#         self.insert_one(face)

#     def get_faces_by_person_id(self, person_id):
#         result = list(self.find({"person_id": person_id}))

#         for face in result:
#             face["image"] = decode_image(
#                 bytes=face["image"], target_shape=face["image_shape"]
#             )

#         return result

#     def get_similar_face(self, embedding, limit=10):
#         print(f"embeding: {embedding}")

#         pipeline = [
#                 {
#                     "$vectorSearch": {
#                         "queryVector": embedding,
#                         "path": self.embedding_path,
#                         "numCandidates": self.num_candidates,
#                         "limit": limit,
#                         "index": "vector_index",
#                     },
#                 },
#                 {
#                     "$project": {
#                         "_id": 1,
#                         "person_id": 1,
#                         "score": {"$meta": "vectorSearchScore"},
#                     },
#                 },
#             ]
#         results = self.collection.aggregate(pipeline)
#         print(results)

#         # Chuyển đổi CommandCursor thành danh sách và in ra từng phần tử
#         results_list = list(results)
#         print(f"Total results: {len(results_list)}")
#         for result in results_list:
#             print(f"in result: {result}")
#         return list(results)

import numpy as np
import json

class Facebank:
    def __init__(self, database):
        self.database = database

    def add_face(self, image, person_id, embedding):
        image_blob = image.tobytes()
        embedding_blob = np.array(embedding).tobytes()
        image_shape = image.shape  # Store image shape
        query = "INSERT INTO facebank (person_id, image, embedding, image_shape) VALUES (%s, %s, %s, %s)"
        params = (person_id, image_blob, embedding_blob, str(image_shape))
        self.database.execute_query(query, params)

    def get_faces_by_person_id(self, person_id):
        query = "SELECT * FROM facebank WHERE person_id = %s"
        params = (person_id,)
        faces = self.database.fetch_all(query, params)
        for face in faces:
            image_shape = tuple(map(int, face['image_shape'].strip('()').split(', ')))
            face['image'] = np.frombuffer(face['image'], dtype=np.uint8).reshape(image_shape)
            face['embedding'] = np.frombuffer(face['embedding'], dtype=np.float32)
        return faces
    
    def get_embeddings(self):
        query = "SELECT person_id, embedding FROM facebank"
        embeddings = self.database.fetch_all(query)
        return embeddings
    
    def compute_cos(self ,feat1, feat2):
        from numpy.linalg import norm
        feat1 = np.array(feat1).ravel()
        feat2 = np.array(feat2).ravel()
    
        sim = np.dot(feat1, feat2) / (norm(feat1)*norm(feat2))
        return sim
    
    def get_similar_face(self, embedding):
        all_embeddings = self.get_embeddings()
        embedding_vectors = [np.frombuffer(emb['embedding'], dtype=np.float32) for emb in all_embeddings]
        person_ids = [emb['person_id'] for emb in all_embeddings]

        # Compute similarities
        similarities_cos = [self.compute_cos(embedding, emb) for emb in embedding_vectors]
        similar_faces_cos = [{"person_id": person_ids[i], "score": similarities_cos[i]} for i in range(len(similarities_cos))]
        
        print(similar_faces_cos)
        return similar_faces_cos

        # Accumulate scores and counts
        # scores = {}
        # counts = {}
        # for face in similar_faces:
        #     person_id = face["person_id"]
        #     score = face["score"]
        #     if person_id in scores:
        #         scores[person_id] += score
        #         counts[person_id] += 1
        #     else:
        #         scores[person_id] = score
        #         counts[person_id] = 1

        # # Compute average scores
        # average_scores = [{"person_id": person_id, "score": scores[person_id] / counts[person_id]} for person_id in scores]

        # # Sort by average score in descending order
        # average_scores.sort(key=lambda x: x["score"], reverse=True)

        # print(average_scores)
        # return average_scores
    
    def close(self):
        self.db.close()