from flask import Flask, request
from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)
 
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured creating the store.'}, 500

        return store.json(), 200

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {'message': 'Store deleted.'}, 200            

class StoreList(Resource):
    def get(self):
        #return {'stores': [store.json() for store in StoreModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), StoreModel.query.all()))}
