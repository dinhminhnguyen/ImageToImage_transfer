from __future__ import division, print_function
import cv2
import imageio
import numpy as np
from keras.models import load_model
from torch import load
from numpy import vstack
from matplotlib import pyplot
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization
from flask import Flask, redirect, url_for, request, render_template,Response
from werkzeug.utils import secure_filename
from keras.preprocessing.image import img_to_array
from fastai.vision import *
from PIL import Image
# Define a flask app
app = Flask(__name__)

path = Path('path')

classes = ['Summer', 'Winter']
data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=256).normalize(imagenet_stats)
learn = cnn_learner(data2, models.resnet34)
learn.load('seasontrainer')


cust = {'InstanceNormalization': InstanceNormalization}
model_AtoB = load_model('path/models/g_model_AtoB_007700.h5', cust)
model_BtoA = load_model('path/models/g_model_BtoA_000500.h5', cust)

def model_predict(img_path):
    """
       model_predict will return the preprocessed image
    """
    img = open_image(img_path)
    pred_class, pred_idx, outputs = learn.predict(img)
    print(pred_class)
    return pred_class

def model_transfer_StoW(img_path):
    """
       model_predict will return the preprocessed image
   """
    A_real = Image.open(img_path)
    A_real = img_to_array(A_real)
    A_real = (A_real ) / 255
    #A_real = (A_real + 1) / 2.0
    A_real = A_real[np.newaxis, :]
    B_generated = model_AtoB.predict(np.array(A_real))
    A_reconstructed = model_BtoA.predict(B_generated)
    A_real = A_real[0, :, : , :]
    B_generated = B_generated[0, :, :, :]
    A_reconstructed = A_reconstructed[0 , :, :,:]
    A_real = Image.fromarray((A_real * 255).astype(np.uint8)).convert('RGB')
    B_generated = Image.fromarray((B_generated*255).astype(np.uint8)).convert('RGB')
    A_reconstructed = Image.fromarray((A_reconstructed * 255).astype(np.uint8)).convert('RGB')
    fileName1 = "static/uploads/" + str(random.random()) + ".jpg"
    fileName2 = "static/uploads/" + str(random.random()) + ".jpg"
    B_generated.save(fileName1)
    A_reconstructed.save(fileName2)
    return fileName1 , fileName2


def model_transfer_WtoS(img_path):
    """
       model_predict will return the preprocessed image
   """
    B_real = Image.open(img_path)
    B_real = img_to_array(B_real)
    B_real = (B_real ) / 255
    #B_real = (B_real + 1) / 2.0
    B_real = B_real[np.newaxis, :]
    A_generated = model_BtoA.predict(np.array(B_real))
    B_reconstructed = model_AtoB.predict(A_generated)
    A_generated = A_generated[0, :, :, :]
    B_reconstructed = B_reconstructed[0 , :, :,:]
    A_generated = Image.fromarray((A_generated*255).astype(np.uint8)).convert('RGB')
    B_reconstructed = Image.fromarray((B_reconstructed * 255).astype(np.uint8)).convert('RGB')
    fileName1 = "static/uploads/" + str(random.random()) + ".jpg"
    fileName2 = "static/uploads/" + str(random.random()) + ".jpg"
    A_generated.save(fileName1)
    B_reconstructed.save(fileName2)
    return fileName1, fileName2

@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/transfer', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path)
        # Make prediction
        predict = model_predict(file_path)
        if (str(predict) == "Winter"):
            preds, reconst = model_transfer_WtoS(file_path)
            return  str(preds)
        if (str(predict) == "Summer"):
            preds, reconst = model_transfer_StoW(file_path)
            return  str(preds), str(reconst)
    return None


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)
        return str(preds)
    return None
@app.route('/about.html')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    
    app.run()
