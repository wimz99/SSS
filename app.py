from cgi import test
from sklearn.preprocessing import scale
from oclass import scaler
from url import *
import pandas as pd
from flask import Flask, render_template, request, url_for,redirect
import pickle
from oscaler import *
import tensorflow as tf
from tensorflow.keras.models import load_model


app = Flask(__name__)

# model_dir = "./mnist_model"

scalerobj = scaler()

@app.route("/")

def front():
    
    return render_template("index.html")

@app.route("/response", methods=('GET', 'POST'))
def solution():

    if request.method == 'POST':
        url = request.form['URL']
        if url == "":
            return render_template("index.html")

        obj = UrlF(url)
        data_test = pd.DataFrame(obj.run(),index=[0])
        cols = data_test.columns.tolist()
        cols.sort()
        data_test = data_test[cols]
        #print(data_test)
        data_test = scalerobj.scale(data_test)
        # localhost_save_option = tf.saved_model.SaveOptions(experimental_io_device="/job:localhost")

        test_data = pd.DataFrame(data_test)
        # print(test_data)
      
        model2 = load_model("model.h5")
        y = model2.predict(test_data)
        # print(y)
        ans = {
            'benign':y[0][0],
            'Defacement':y[0][1],
            'Malicious':y[0][2],
            'Phishing':y[0][3],
            'Spam':y[0][4]
        }
    return render_template("response.html",value = ans)