# https://www.youtube.com/watch?v=vISRn5qFrkM
from flask import Flask, request, jsonify, abort,render_template,url_for
import io
import json                    
import base64
from conn import nps_conn
import os                  
import logging             
import numpy as np
from PIL import Image
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
today=datetime.now()

from vision import localize_objects
new=today.strftime("%d-%m-%Y")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR,"upload")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def read():
    context={}
    context["ip"]=request.remote_addr
    context["err"]=os.path.join(BASE_DIR,"new")
    return render_template("scan.html",context=context)

@app.route("/test", methods=['GET'])
def test():
    return render_template("test.html")

@app.route("/scan", methods=['POST'])
def scan():         
    # print(request.json)      
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # PIL image object to numpy array
    img_arr = np.asarray(img)      
    print('img shape', img_arr.shape)
    dir=os.path.join(BASE_DIR,"image")
    img.save(dir+"\\"+new+".jpg")
    result_dict = {}
    object=localize_objects(dir+"\\"+new+".jpg")
    for index,i in enumerate(object):
        result_dict[f"object{index}"]=i.name
    return result_dict

@app.route("/form", methods=['POST'])
def form():         
    if request.method == 'POST':
        file1 = request.files['fileToUpload']
        # location=request.form.get("loc")
        ip=request.form.get("ipA")
        country=request.form.get("coun")
        region=request.form.get("reg")
        city=request.form.get("cit")
        lat=request.form.get("lat")
        lon=request.form.get("lon")
        avail=False
        final={}



        # path = os.path.join(BASE_DIR, file1.filename)
        # file1.save(path)
        # guess=localize_objects(path)
        # ram={}
        # #try:
        # p=nps_conn()
        # for i,name in enumerate(guess):
        #     doc=p.SearchProduct(name.name.lower())
        #     if doc:
        #         loc=p.SearchCity(location)
        #         if loc:
        #             avail=p.SearchItem(doc,loc)
        #             if avail:
        #                 break
        #     else:
        #         r=p.InsertProduct(name.name.lower())
        #         return f"inserted id: {r}"
        # #except Exception:
        #     # print("Check the following :")
        #     # print("\t1. Check connection String")
        #     # print("\t2. Intenet connectivity")
        # if avail:
        #     return f"{name.name} : {avail} available"
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("NPS").sheet1
        records = sheet.get_all_records()
        for i in records:
            if i.get('') == city:
                avail=True
                final=i
                print(i)
        if avail==True:
            print(final)
            return f"ITEM AVAILABLE <br> {final}"
        else:
            return "Error occure while searching"
    return "ok"

connection = nps_conn()

@app.route("/questionnaire-form", methods=["GET", "POST"])
def questionnaire_form():
    if request.methods == "GET":
        connection.GetQuestionnaireForm()
    elif request.method == "POST":
        connection.PostQuestionnaireForm()        
@app.route("/questionnaires", methods=["GET"])
def get_questionnaires():
    connection.GetQuestionnaires()

def run_server_api():
    app.run(debug=True)
  
  
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
