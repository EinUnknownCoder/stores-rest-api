from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Store_id cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            try:
               item.price = data['price']
            except: 
                return {'message': 'An error occured inserting the item.'}, 500    
        else:
            try:
                item = ItemModel(name, **data)
            except:
                return {'message': 'An error occured inserting the item.'}, 500
        
        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200