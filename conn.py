from dns import exception
from flask import request, Response, render_template, url_for
from pymongo import MongoClient
import json
import certifi
# utils
from utils import getDayFromYear, zeroStrings


class nps_conn():
    def __init__(self):
        self.conn_string = "mongodb+srv://vj.n2ih9.mongodb.net/DB_IMAGE?retryWrites=true&w=majority"
        self.conn = MongoClient(self.conn_string, tlsCAFile=certifi.where())
        self.db = self.conn.get_database("dowellnps")

    def SearchProduct(self, product):
        col = self.db.get_collection("Product")
        pname = col.find({"product_name": product})
        for produs in pname:
            return produs["product_id"]

    def SearchCity(self, gps):
        col1 = self.db.get_collection("City")
        cname = col1.find({"gps": gps})
        for cit in cname:
            return cit["city_code"]

    def InsertProduct(self, newproduct):
        cat = self.db.get_collection("Product")
        fetch_record = cat.find({}).sort("_id", -1)
        for id in fetch_record:
            r = id["product_id"]+1
        try:
            object = cat.insert_one(
                {"product_name": newproduct, "product_id": r, "category": 10})
            return object.inserted_id
        except Exception:
            return "Error occured while inserting"

    def SearchItem(self, product, city):
        col2 = self.db.get_collection("Item_Details")
        city_pro = col2.find({"product_id": product, "city_code": city})
        for item in city_pro:
            return item["quota"]

    def GetQuestionnaires(self):
        try:
            data = list(self.db.questionnaire.find({}))
            for item in data:
                item["_id"] = f"{item['_id']}"
            return Response(
                response=json.dumps({'message': 'success', "data": data}),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            return Response(
                response=json.dumps({
                    "message": "some error occurred", "error": str(ex)
                }),
                status=404,
                mimetype="application/json"
            )

    def GetQuestionnaireForm(self):
        try:
            categories = list(self.db.category.find(
                {}, {'name': 1,  '_id': 0}))
            continents = list(self.db.continent.find({}))
            return render_template('./questionnaire-form.html',
                                   context={"submit_url": url_for(
                                       "questionnaire_form"), "categories": categories, "continents": continents}
                                   )
        except Exception as ex:
            return Response(response=json.dumps({"message": "some error occurred", "error": f"{ex}"}), status=404, mimetype="application/json")

    def PostQuestionnaireForm(self):
        try:
            submittedForm = request.get_json()
            filled_form = {
                'platform': submittedForm['platform_input'],
                'category': submittedForm['category_input'],
                'region': submittedForm['region_input'],
                'product': submittedForm['product_input'],
                'brand': submittedForm['brand_input'],
                'satisfaction': submittedForm['level_satisfaction'],
                'interested': submittedForm['interested_input'],
                'email': submittedForm['email_input'],
                'user': request.remote_user,
                'addr': request.remote_addr,
            }
            platform_id = self.db.platform.find_one(
                {"name": filled_form['platform']}, {'ID': 1, '_id': 0}
            )['ID']
            region_id = self.db.region.find_one(
                {'name': filled_form['region']}, {'ID': 1, '_id': 0}
            )['ID']
            day = getDayFromYear()
            category_id = self.db.category.find_one(
                {'name': filled_form['category']}, {'ID': 1, '_id': 0}
            )['ID']
            product_id = self.db.product.find_one(
                {'name': filled_form['product']}, {'ID': 1, '_id': 0}
            )['ID']
            satisfation_level = filled_form['satisfaction']
            interested = 1 if filled_form['interested'] == 'Yes' else 0
            platform_id = zeroStrings(platform_id, 2)
            region_id = zeroStrings(region_id, 3)
            day = zeroStrings(day, 4)
            category_id = zeroStrings(category_id, 4)
            product_id = zeroStrings(product_id, 4)
            satisfation_level = zeroStrings(satisfation_level, 4)
            interested = zeroStrings(interested, 4)
            EVENT_ID = f"{platform_id}.{region_id}.{day}.{category_id}.{product_id}.{satisfation_level}.{interested}"
            filled_form['EVENT_ID'] = EVENT_ID
            dbResponse = self.db.questionnaire.insert_one(filled_form)
            return Response(response=json.dumps({"message": "success"}), status=201, mimetype="application/json")
        except Exception as ex:
            return Response(response=json.dumps({"message": "some error occurred", "error": str(ex)}), status=404, mimetype="application/json")
