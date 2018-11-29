import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO

from img2tag import img2tag, face2tag

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \
    "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
face_url = 'https://how-old.net/Images/faces2/main007.jpg'

img2tag(image_url)
print('\n')
face2tag(face_url)

# # Replace <Subscription Key> with your valid subscription key.
# # https://westcentralus.api.cognitive.microsoft.com/vision/v1.0

# # https://westcentralus.api.cognitive.microsoft.com/vision/v2.0

# # 3cf2a24b1b684fcb811117c122df5c46

# # 8dd6aae04c2246e0a457bb96df22274a
# subscription_key = "3463cdb302b34070b267ad59a82ae7aa"
# assert subscription_key

# # You must use the same region in your REST call as you used to get your
# # subscription keys. For example, if you got your subscription keys from
# # westus, replace "westcentralus" in the URI below with "westus".
# #
# # Free trial subscription keys are generated in the westcentralus region.
# # If you use a free trial subscription key, you shouldn't need to change
# # this region.
# vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

# analyze_url = vision_base_url + "analyze"

# # Set image_url to the URL of an image that you want to analyze.
# image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \
#     "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"

# headers = {'Ocp-Apim-Subscription-Key': subscription_key }
# params  = {'visualFeatures': 'Categories,Description,Color',
#             'language': 'zh'}
# data    = {'url': image_url}
# response = requests.post(analyze_url, headers=headers, params=params, json=data)
# response.raise_for_status()

# # The 'analysis' object contains various fields that describe the image. The most
# # relevant caption for the image is obtained from the 'description' property.
# analysis = response.json()
# print(json.dumps(response.json()))
# image_caption = analysis["description"]["captions"][0]["text"].capitalize()

# # Display the image and overlay it with the caption.
# image = Image.open(BytesIO(requests.get(image_url).content))
# plt.imshow(image)
# plt.axis("off")
# _ = plt.title(image_caption, size="x-large", y=-0.1)
# plt.show()