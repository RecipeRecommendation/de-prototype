import pandas as pd
from flask import Flask, jsonify
from flask_restful import Api, reqparse, Resource

import constants
from self_order import self_order
import json
from object_detection.yolov5.detect import *
from random_suggestion import random_suggestion
from collaborative_recommender import collaborative_recommender
from youtube_search_query import youtube_search_query as ysq

app = Flask(__name__)
api = Api(app)

shoppinglist = reqparse.RequestParser()
shoppinglist.add_argument('item', type=str, required=True)
shoppinglist.add_argument('quantity', type=str, required=True)

items = json.load(open(constants.ROOT+'/resources/items.json'))


class WelcomeMSG(Resource):
    @staticmethod
    def get():
        return {'message': 'Welcome to Recipe Recommendation API.'}


api.add_resource(WelcomeMSG, '/')


# --------------------------------------- FUTURE WORK --------------------------------------------- #
class GetShoppingList(Resource):
    @staticmethod
    def get(item_id):  # Get specific item details
        try:
            return jsonify({item_id: items[item_id]})
        except KeyError:
            return jsonify({'message': 'Item not in list'})


api.add_resource(GetShoppingList, '/self_order/get_shopping_list/<string:item_id>')


class AddShoppingList(Resource):  # Modifying the Shopping List
    @staticmethod
    def put(item_id):
        args = shoppinglist.parse_args()
        items[item_id] = args
        with open('bigbasket/items.json', 'w') as fp:
            json.dump(items, fp, indent=4)
        return jsonify({item_id: args})


api.add_resource(AddShoppingList, "/self_order/add_shopping_list/<string:item_id>")
# --------------------------------------- FUTURE WORK --------------------------------------------- #

class Checkout(Resource):
    @staticmethod
    def get():
        self_order.self_order()
        with open(constants.ROOT+'/resources/items.json', 'w') as fp:
            json.dump({}, fp, indent=4)
        return jsonify({'message': True})


api.add_resource(Checkout, '/self_order/checkout')


class ObjectDetection(Resource):

    @staticmethod
    def get():
        final = main(parse_opt())
        with open(constants.ROOT+"/resources/classes.txt", "r") as a_file:
            list_of_lists = []
            for line in a_file:
                stripped_line = line.strip()
                line_list = stripped_line.split()
                list_of_lists.append(line_list)

        dic = {}
        for st in final:
            index = 0
            for line in list_of_lists:
                if st in line[0]:
                    print(st)
                    dic1 = {'item': st, "quantity": ''}
                    dic[str(index)] = dic1
                    if index > 22:
                        break
                index += 1

        with open(constants.ROOT+"/resources/detected_ingredients.json", "w") as outfile:
            json.dump(dic, outfile)
        return jsonify(dic)


api.add_resource(ObjectDetection, '/object/detection')


class CollaborativeRecommender(Resource):

    @staticmethod
    def get(recipe_id):
        recommendations_knn = collaborative_recommender.recommender(recipe_id)
        rec_knn = {}
        i = 0
        for j in recommendations_knn:
            rec_knn[i] = j
            i += 1

        return jsonify(rec_knn)


api.add_resource(CollaborativeRecommender, '/recommender/collaborative/<int:recipe_id>')


class RandomSuggestion(Resource):

    @staticmethod
    def get():
        df = pd.read_csv(constants.ROOT + "/resources/recipe_data.csv")
        recommendations = random_suggestion.recommender(df)
        recipes = {}
        for recipe_id in recommendations:
            recipes[recipe_id] = (df[df["recipe_id"] == recipe_id]["recipeName"]).tolist()[0]
        return jsonify(recipes)


api.add_resource(RandomSuggestion, '/recommender/random')


class YoutubeSearchQuery(Resource):

    @staticmethod
    def get(query):
        result = ysq.search(query)

        return jsonify({"link": result})


api.add_resource(YoutubeSearchQuery, '/youtube/<string:query>')


