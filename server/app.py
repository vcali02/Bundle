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
        #1 set data as JSON
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
class BusinessById(Resource):
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
api.add_resource(BusinessById, "/businesses/<int:id>")
    

################ BUSINESS CATEGORIES ################

#GET /business_categories
class BusinessCategories(Resource):
    def get(self):
        #1 query
        bcs=Business.query.all()
        if not bcs:
            return {"error": "Business not found."}, 404
        #2 turn to JSON w dict
        bcs_dict=[bc.to_dict() for bc in bcs]
        #3 res
        res= make_response(
            bcs_dict,
            200
        )
        return res
    
#POST /business_categories
    def post(self):
        #1 set data as JSON
        data=request.get_json()
        #2 create instance
        new_bis_cat=BusinessCategory(
            category_name=data.get('cat')
        )
        #3 add to db
        db.session.add(new_bis_cat)
        db.session.commit()

        #4 dict aka res into JSON obj
        new_bis_cat_dict=new_bis_cat.to_dict()

        #5 res to JSON obj
        res= make_response(
             new_bis_cat_dict,
             201
        )
        return res 
        
#add route
api.add_resource(BusinessCategories, "/business_categories")


#GET /business_categories/<int:id>
class BusinessCategoryById(Resource):
    def get(self, id):
        one_bc=BusinessCategory.query.filter_by(id=id).first()
        if not one_bc:
            return {"error": "Business Category not found."}, 404
        one_bc_dict= one_bc.to_dict()
        res= make_response(
            one_bc_dict,
            200
        )

#PATCH /business_categories/<int:id>
        
    def patch(self, id):
        #1 query by id
        bc= BusinessCategory.query.filter_by(id=id).first()

        #2 get data from request in JSON format
        data= request.get_json()


        #3 update values in the model
        for attr in data:
            setattr(bc, attr, data.get(attr))

        #4 update the database
        db.session.add(bc)
        db.session.commit()

        #5 return res
        return make_response(bc.to_dict(), 200)
        

#DELETE /business_categories/<int:id>
    def delete(self, id):
        #1 get by id
        one_bc= BusinessCategory.query.filter_by(id=id).first()
        if not one_bc:
            return {"error": "Business not found."}, 404
        #2 delete from database
        db.session.delete(one_bc)
        db.session.commit()

        return make_response({}, 204)
        
api.add_resource(BusinessCategoryById, "/business_categories/<int:id>")
        

    

################ PRODUCTS ################

#GET
class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        response = make_response(
            products,
            200
        )
        return response
    #POST
    def post(self):
        try: 
            data = request.get_json()
            print (data)
            product = Product(
                product_name=data["product_name"],
                product_description=data["product_description"],
                product_img=data["product_img"],
                product_price=data["product_price"],
            )
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            return make_response({
                "errors": [e.__str__()]
            }, 422)
        response = make_response(
            product.to_dict(),
            201
        )
        return response
api.add_resource(Products, '/products')



################ PRODUCTSBYID ################
    #GET
class ProductsByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            abort(404, "Product not found")
        product_dict = product.to_dict()
        response = make_response(
            product_dict,
            200
        )
        return response
    #POST
    #PATCH
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            return make_response({'error': 'product not found'},
            404
            )
        data = request.get_json()
        for attr in data:
            setattr(product, attr, data[attr])
        db.session.add(product)
        db.session.db.session.commit()
                
        return make_response(product.to_dict(), 202)

    #DELETE
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            make_response(
                {"error": "product not foun"},
                404
            )
        db.session.delete(product)
        db.session.commit()
api.add_resource(ProductsByID, '/product/<int: id>')            


            

######### ATTRIBUTES ################
    


            
################ PRODUCT CATEGORIES ################
    

################ INVENTORY ################
    

################ REVIEWS ################
class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Product.query.all()]
        response = make_response(
            reviews,
            200
        )
        return response
    #POST
    def post(self):
        try: 
            data = request.get_json()
            print (data)
            review = Review(
                review = db.Column(db.String, nullable=False)
                rating = db.Column(db.Integer, nullable=False)
                review_img = db.Column(db.LargeBinary, nullable=False)
                review_name=data["review_name"],
                review_description=data["review_description"],
                review_img=data["review_img"],
                review_price=data["review_price"],
            )
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            return make_response({
                "errors": [e.__str__()]
            }, 422)
        response = make_response(
            product.to_dict(),
            201
        )
        return response
api.add_resource(Reviews, '/review')
################ REVIEWSBYID ################

    #GET
class ReviewsByID(Resource):
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, "Review not found")
        review_dict = review.to_dict()
        response = make_response(
            review_dict,
            200
        )
        return response
    #POST
    #PATCH
    def patch(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return make_response({'error': 'review not found'},
            404
            )
        data = request.get_json()
        for attr in data:
            setattr(review, attr, data[attr])
        db.session.add(review)
        db.session.db.session.commit()
                
        return make_response(review.to_dict(), 202)

    #DELETE
    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            make_response(
                {"error": "review not found"},
                404
            )
        db.session.delete(review)
        db.session.commit()
api.add_resource(ReviewsByID, '/review/<int: id>')     
    

################ SALE HISTORY ################
    

################ ORDERS ################
    

################ ORDER ITEMS ################
    

################ ORDER STATUS ################
    

################ SHOPIFY INFO ################
    

################ PAYMENT ################
    

################ MESSAGING ################
    

################ ORDER HISTORY ################
    

################ ADDRESS ################
    

 