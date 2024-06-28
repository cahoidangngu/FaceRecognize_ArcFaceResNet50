from mtcnn import MTCNN
from utils import to_cuda


class FaceDetector:
    def __init__(self) -> None:
        self.detector = MTCNN()

    def get_area(self, box):
        w, h = box[2], box[3]

        return w * h

    def detect_multi_faces(self, img, min_confidence=0.8):
        detected_boxes = self.detector.detect_faces(img)
        cropped_faces = []

        for dect in detected_boxes:
            if dect["confidence"] >= min_confidence:
                x, y, w, h = dect["box"]
                payload = {
                    "image": img[y : y + h, x : x + w].copy(),
                    "box": dect["box"],
                }
                cropped_faces.append(payload)

        return cropped_faces

    def detect_face(self, img, min_confidence=0.8):
        """
        Input: img
        Output: cropped face
        """
        min_confidence = 0.9
        detected_boxes = self.detector.detect_faces(img)

        detected_boxes.sort(key=lambda x: self.get_area(x["box"]), reverse=True)

        for dect in detected_boxes:
            if dect["confidence"] >= min_confidence:
                x, y, w, h = dect["box"]
                return img[y : y + h, x : x + w].copy()

        assert False, "No face detected"
