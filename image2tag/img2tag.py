# -*- coding: utf-8 -*-
import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import json
from PIL import Image
from io import BytesIO
# Replace <Subscription Key> with your valid subscription key.
# https://westcentralus.api.cognitive.microsoft.com/vision/v1.0

# https://westcentralus.api.cognitive.microsoft.com/vision/v2.0

# 3cf2a24b1b684fcb811117c122df5c46

# 8dd6aae04c2246e0a457bb96df22274a


def img2tag(image_url):
    """
    :param image_url: Set image_url to the URL of an image that you want to analyze.
    :return analysis: The 'analysis' object contains various fields that describe the image. 
    The most relevant caption for the image is obtained from the 'description' property.
    """

    subscription_key = "3463cdb302b34070b267ad59a82ae7aa"
    assert subscription_key

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the westcentralus region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"


    headers = {'Ocp-Apim-Subscription-Key': subscription_key }
    params  = {'visualFeatures': 'Categories,Description,Color',
                'language': 'zh'}
    data    = {'url': image_url}
    response = requests.post(analyze_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    return response.json()['description']['tags'][:4]

def face2tag(face_url):

    subscription_key = "af84b808acd242f09b2c826707bdb1e1"
    assert subscription_key

    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    response = requests.post(face_api_url, params=params, headers=headers, json={"url": face_url})
    analysis = response.json()
    print(json.dumps(response.json()))
    return analysis
