import cv2
import torch
import bson
import numpy as np


def draw_bounding_boxes(src_img, detections, color=(255, 255, 255)):
    img_with_bb = src_img.copy()

    for det in detections:
        x, y, w, h = det["box"]
        identity = det["identity"]

        label = (
            "unknown"
            if identity is None
            else f'{identity["name"]} ({identity["score"]:.2f})'
        )

        cv2.rectangle(img_with_bb, (x, y), (x + w, y + h), (255, 0, 0), 2)
        imgHeight, imgWidth, _ = src_img.shape

        thick = int((imgHeight + imgWidth) // 900)
        cv2.putText(
            img_with_bb,
            label,
            (x, y - 12),
            0,
            1e-3 * imgHeight,
            color,
            thick // 3,
        )

    return img_with_bb


def get_device():
    # if torch.cuda.is_available():
    #     return torch.device("cuda")
    # else:
    return torch.device("cpu")


def to_cuda(elements):
    if torch.cuda.is_available():
        return elements.cuda()
    return elements


def encode_image(image):
    return bson.binary.Binary(image)


def decode_image(bytes, target_shape, dtype=np.uint8):
    image = np.frombuffer(bytes, dtype=dtype)
    image = image.reshape(target_shape)

    return image


def convert_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
