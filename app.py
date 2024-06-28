from database.database import Database
from database.facebank import Facebank
from database.person import Person
from face_detector import FaceDetector
from face_embedder import FaceEmbedder
import math


class App:
    def __init__(self) -> None:
        self.database = Database(
            host="localhost",
            database="face_recognition",
            user="root",
            password="140603"
        )
        self.face_detector = FaceDetector()
        self.face_embedder = FaceEmbedder()
        self.person_col = Person(database=self.database)
        self.facebank_col = Facebank(database=self.database)
        print("App initialized!")

    def get_embedding(self, image):
        face = self.face_detector.detect_face(image)
        embedding = self.face_embedder.embed_face(face)
        return embedding, face

    def add_new_person(self, name, image):
        embedding, face = self.get_embedding(image)
        person_id = self.person_col.add_person({"name": name})
        self.facebank_col.add_face(image=face, person_id=person_id, embedding=embedding)
        return person_id

    def add_new_face(self, person_id, image):
        embedding, face = self.get_embedding(image)
        self.facebank_col.add_face(image=face, embedding=embedding, person_id=person_id)
        
    def get_all_people(self):
        return self.person_col.get_all()

    def get_faces_by_person_id(self, person_id):
        return self.facebank_col.get_faces_by_person_id(person_id)


    def vote_preds(self, sim_faces):
        pred = {}  
        for idx, face in enumerate(sim_faces):
            pid = face["person_id"]
            score = face["score"]
            weighted_score = score / (math.log(idx + 1) + 1)
            if pid in pred:
                pred[pid].append(weighted_score)
            else:
                pred[pid] = [weighted_score]
        for pid, scores in pred.items():
            pred[pid] = sum(scores) / len(scores)
        max_voting = 0
        max_pid = None
        for pid, score in pred.items():
            if score > max_voting:
                max_voting = score
                max_pid = pid
        sim_of_likely_pid = []
        for face in sim_faces:
            if face["person_id"] == max_pid:
                sim_of_likely_pid.append(face["score"])
        if len(sim_of_likely_pid) > 0:
            return max_pid, sum(sim_of_likely_pid) / len(sim_of_likely_pid)
        else:
            return max_pid, 0 

    def get_person_info(self, person_id):
        return self.person_col.find_by_id(person_id)

    def identify_faces(self, image):
        detected_faces = self.face_detector.detect_multi_faces(image)
        for face in detected_faces:
            cropped_face = face["image"]
            embedding = self.face_embedder.embed_face(cropped_face)
            sim_faces = self.facebank_col.get_similar_face(embedding=embedding.tolist())
            pid, score = self.vote_preds(sim_faces)
            print(score)
            if score > 0.4:
                face["identity"] = self.get_person_info(pid)
                face["identity"]["score"] = score
            else:
                face["identity"] = None
        return detected_faces