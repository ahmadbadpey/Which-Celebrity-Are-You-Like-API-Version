from flask import Blueprint, Flask, request
from keras_vggface import VGGFace, utils
from keras_vggface.utils import preprocess_input
from mtcnn import MTCNN
import cv2 as cv
import numpy as np
import json, requests

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

    founded_person = output[0][0][0].replace("b'", "").replace("'", "")
    # return founded_person

    result = {
        "success": True,
        "message": {}
    }

    if founded_person:
        celeb_name = get_best_title_wiki_page(founded_person)

        if celeb_name:
            result['message']['celeb_name'] = celeb_name

            celeb_images = get_celeb_images(celeb_name)

            if celeb_images:
                result['message']['celeb_images'] = celeb_images

            return result
        else:
            return {
                "success": False,
                "message": "Best Title Not Found!"
            }

    else:
        return {
            "success": False,
            "message": "Not Found any things !",
        }


def extract_face(address):
    img = cv.imread(address)

    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    face = detector_obj.detect_faces(rgb_img)[0]
    x, y, w, h = face['box']

    actual_face = img[y:y + h, x:x + w]  # This crop only section of image that contain person Face
    actual_face = cv.resize(actual_face, (224, 224))

    return np.asarray(actual_face)


def get_best_title_wiki_page(celeb_name):
    endpoint = "https://en.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "list": "search",
        "srsearch": celeb_name,
        "format": "json",
        "origin": "*"
    }
    best_title = None

    try:
        response = requests.get(endpoint, params=parameters)
        data = json.loads(response.text)
        best_title = data["query"]["search"][0]["title"]
    except Exception as e:
        print(e)

    return best_title


def get_celeb_images(celeb_name):
    endpoint = "https://en.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "titles": celeb_name,
        "prop": "images",
        "iiprop": "url",
        "format": "json",
        "origin": "*"
    }

    try:
        response = requests.get(endpoint, params=parameters)
        data = json.loads(response.text)

        page_id = list(data["query"]["pages"].keys())[0]
        images = data["query"]["pages"][page_id]["images"]

        filtered_images = [image for image in images if
                           "file:" + celeb_name.lower() in image[
                               "title"].lower() or "file:" + celeb_name.lower().replace(" ", "") in image[
                               "title"].lower()]

        image_urls = [f"https://en.wikipedia.org/wiki/Special:Redirect/file/{image['title'].replace('File:', '')}" for
                      image in filtered_images]

        cel_images = image_urls[0:4]

        return cel_images

    except Exception as e:
        print("Getting Images API request failed", e)
