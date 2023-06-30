from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from tensorflow.keras.models import load_model
import PIL.Image as pi
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import numpy as np
import os
# Create your views here.

classes = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
print("loading model")
model = load_model("API/model.h5")
print("model loaded")
def index(request):

    msg = """
    <div style="text-align: center; ">
        <H1> hello world</H1>
    <div>    
    """
    return HttpResponse(msg)

@api_view(["GET", "POST"])
def get_text(request):
    if request.method == "GET":
        msg = {"message": request.method}
        return Response(msg)
    elif request.method == "POST":
        path = request.data["image"]
        try:
            path = urlretrieve(path, filename="API/out.png")[0]
            captcha = predict(path)
            return Response({"message": captcha})
        except Exception as e:
            return Response({"message": "retry", "error": str(e)})

def predict(img_path):
    image = pi.open(img_path).convert("L")
    img = np.array(image)
    plt.imsave(r"API/tempimg.jpg", img, cmap="binary")
    img = plt.imread(r"API/tempimg.jpg")
    img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
    pts = [[(7, 0), (27, 40)], [(27, 0), (47, 40)], [(47, 0), (67, 40)], [(67, 0), (87, 40)], [(87, 0), (107, 40)], [(107, 0), [127, 40]]]
    imgs = []
    for (x1, _), (x2, _) in pts:
        i = img[:, x1:x2]
        imgs.append(i)
    imgs = np.array(imgs).reshape(-1, 40, 20, 1)
    output = model.predict(imgs, verbose=0)
    cp = ""
    for o in output:
        cp += classes[np.argmax(o)]
    os.remove("API/out.png")
    os.remove("API/tempimg.jpg")
    return { "text": cp}
