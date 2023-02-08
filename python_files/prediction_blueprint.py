from flask import Blueprint, Flask, request
from keras_vggface import VGGFace, utils
from keras_vggface.utils import preprocess_input
from mtcnn import MTCNN
import cv2 as cv
import numpy as np

prediction_blueprint = Blueprint('prediction_blueprint', __name__)

vggface = VGGFace(model='vgg16')
detector_obj = MTCNN()



@prediction_blueprint.route('/predict', methods=['POST'])
def index():
    image = request.get_json().get('image')

    face = extract_face('../uploads/' + image)
    face = face.astype('float32')
    input_sample = np.expand_dims(face, axis=0)
    samples = preprocess_input(input_sample)

    pred = vggface.predict(samples)
    # print(pred)

    output = utils.decode_predictions(pred)
    # print(output)

    prediction = output[0][0][0].replace("b'", "").replace("'", "")
    return prediction


def extract_face(address):
    img = cv.imread(address)

    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    face = detector_obj.detect_faces(rgb_img)[0]
    x, y, w, h = face['box']

    actual_face = img[y:y + h, x:x + w]  # This crop only section of image that contain person Face
    actual_face = cv.resize(actual_face, (224, 224))

    return np.asarray(actual_face)
