from flask_migrate import Migrate
from flask import make_response, request
from flask_restful import Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash
from config import app, db, api
from models import db, Seller, Business, BusinessCategory, Product, Attribute, ProductCategory, Inventory, Review, SaleHistory, Order, Order_Item, Order_Status, ShopifyInfo, Payment, Message, OrderHistory, Address, Buyer 
import datetime
import traceback

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)



if __name__ == '__main__':
    app.run(port=5555, debug=True)

# note: ROUTE classes MUST be called DIFFERENT than MODEL class

## START ############## LOGIN / USER ################
    
#### SELLER ####
    

#### BUYER ####
    

## END ############## LOGIN / USER ################
    

################ BUSINESS ################
    
# GET /businesses 
# note: ROUTE classes MUST be called DIFFERENT than MODEL class
class Businesses(Resource):
    def get(self):
        #1 query
        bs = Business.query.all()
        if not bs:
            return {"error": "Business not found."}, 404
        #2 dict aka res into JSON obj
        b_dict = [b.to_dict() for b in bs]
        #3 res
        res = make_response(
            b_dict,
            200
        )
        return res
    
#POST /businesses
    def post(self):
        #1. set data as JSON
        data=request.get_json()
        #2 create instance
        new_bis = Business(
            business_name=data.get('business_name'),
            business_address=data.get('business_address'),
            business_img=data.get('business_img'),
            business_banner_img=data.get('business_banner_img'),
            business_desc=data.get('business_desc'),
        )
        #3 add/commit to database
        db.session.add(new_bis)
        db.session.commit()

        #4 dict aka res into JSON obj
        new_bis_dict=new_bis.to_dict()

        #5 res
        res=make_response(
            new_bis_dict,
            201
        )
        #6 return res
        return res
#add route
api.add_resource(Businesses, "/businesses")


#GET /businesses/<int:id>
class OneBusiness(Resource):
    def get(self, id):
        #1 query
        one_bs = Business.query.filter_by(id=id).first()
        if not one_bs:
            return {"error": "Business not found."}, 404
        #2 dict aka res into JSON obj
        one_bs_dict = one_bs.to_dict()
        res = make_response(
            one_bs_dict,
            200
        )
        return res
    
#PATCH /businesses/<int:id>
    
    def patch(self, id):
        #1 query by id
        bis= Business.query.filter_by(id=id).first()

        #2 get data from request in JSON format
        data= request.get_json()


        #3 update values in the model
        for attr in data:
            setattr(bis, attr, data.get(attr))

        #4 update the database
        db.session.add(bis)
        db.session.commit()

        #5 return res
        return make_response(bis.to_dict(), 200)
    
#DELETE /businesses/<int:id>
    def delete(self, id):
        #1 get by id
        one_bs= Business.query.filter_by(id=id).first()
        if not one_bs:
            return {"error": "Business not found."}, 404
        #2 delete from database
        db.session.delete(one_bs)
        db.session.commit()

        return make_response({}, 204)


#add route
api.add_resource(OneBusiness, "/businesses/<int:id>")
    

################ BUSINESS CATEGORIES ################
    

################ PRODUCTS ################
    

################ ATTRIBUTES ################
    

################ PRODUCT CATEGORIES ################
    

################ INVENTORY ################
    

################ REVIEWS ################
    

################ SALE HISTORY ################
    

################ ORDERS ################
    

################ ORDER ITEMS ################
    

################ ORDER STATUS ################
    

################ SHOPIFY INFO ################
    

################ PAYMENT ################
    

################ MESSAGING ################
    

################ ORDER HISTORY ################
    

################ ADDRESS ################
    

 