from flask_migrate import Migrate
from flask import make_response, request
from flask_restful import Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash
from config import app, db, api
from models import db, Seller, Business, BusinessCategory, Product, Attribute, ProductCategory, Inventory, Review, SaleHistory, Order, Order_Item, Order_Status, ShopifyInfo, Payment, Message, OrderHistory, Address, Buyer
import datetime
import traceback
import os
import ipdb
import base64

migrate = Migrate(app, db)
buyer_login_manager = LoginManager()
buyer_login_manager.init_app(app)
seller_login_manager = LoginManager()
seller_login_manager.init_app(app)


@buyer_login_manager.user_loader
def load_buyer(buyer_id):
    return Buyer.query.filter_by(id=buyer_id).first()


@seller_login_manager.user_loader
def load_seller(seller_id):
    return Seller.query.filter_by(id=seller_id).first()


# DELETE LATER
class CheckSession(Resource):
    def get(self):
        if current_user.is_authenticated:
            user = current_user.to_dict()
            return user, 200
        return {"error": "unauthorized"}, 401


api.add_resource(CheckSession, '/check_session')

#### SELLER ####

class Sellers(Resource):
    @login_required
    def get(self):
        try:
            seller = current_user
            if seller:
                return {
                    "id": seller.id,
                    "name": seller.seller_name,
                    "email": seller.seller_email
                }, 200
            else:
                return {'error': "Seller account not found"}, 404
        except Exception as e:
            return {'error': 'An error occurred while fetching the seller account', 'Message': {e}}, 500
        
    @login_required
    def patch(self):
        try:
            seller = current_user
            if seller:
                data = request.get_json()
                seller.seller_email = data.get('seller_email', seller.seller_email)

                password = data.get('seller_password')
                if password:
                    hashed_password = generate_password_hash(password)
                    seller.password_hash = hashed_password
                
                db.session.commit()
                return {
                    "id": seller.id,
                    "name": seller.seller_name,
                    "email": seller.seller_email
                }, 200
            else:
                return {'Error': 'Seller not found'}, 404
        except Exception as e:
            return {'Error': 'An error occurred while updating the seller', 'Message': {e}}, 500
        
    @login_required
    def delete(self):
        try: 
            data = request.get_json()
            password = data['password']
            seller = current_user

            if seller:
                if seller.authenticate(password):
                    db.session.delete(seller)
                    db.session.commit()
                    return {}, 204
            else:
                return {'Error': 'User not found'}, 404
        except Exception as e:
            return {'Error': 'An error occured while deleting the seller', 'Message': {e}}, 500

api.add_resource(Sellers, '/sellers')

class SellerSignup(Resource):
    def post(self):
        data = request.get_json()

        try:
            seller_img = data['seller_img']
            with open(seller_img, 'rb') as img:
                image_data = img.read()
                encoded_image = base64.b64encode(image_data)
        except:
            image_path = os.path.join(
                "images", "blank-profile-picture-973460_960_720.png")
            with open(image_path, 'rb') as img:
                image_data = img.read()
                encoded_image = base64.b64encode(image_data)

        new_seller = Seller(
            seller_name=data['seller_name'],
            seller_email=data['seller_email'],
            seller_username=data['seller_username'],
            seller_img=encoded_image
        )
        new_seller.password_hash = data['seller_password']

        db.session.add(new_seller)
        db.session.commit()

        login_user(new_seller, remember=True)

        return new_seller.to_dict(), 201


api.add_resource(SellerSignup, '/seller_signup')


class SellerLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('seller_email')
            password = data.get('seller_password')

            seller = Seller.query.filter(Seller.seller_email == email).first()

            if seller:
                if seller.authenticate(password):
                    login_user(seller, remember=True)
                    return seller.to_dict(), 200
                else:
                    return {'error': 'Couldn\'t authenticate password'}
            if not seller:
                return {'error': '404: User not found'}, 404
        except Exception as e:
            return {'error': {e}}, 401


api.add_resource(SellerLogin, '/seller_login')


@app.route('/seller_logout', methods=["POST"])
@login_required
def seller_logout():
    logout_user()
    return 'you logged out'

#### BUYER ####

class Buyers(Resource):
    @login_required
    def get(self):
        try:
            buyer = current_user
            if buyer:
                return {
                    "id": buyer.id,
                    "name": buyer.buyer_name,
                    "email": buyer.buyer_email
                }, 200
            else:
                return {'error': "buyer account not found"}, 404
        except Exception as e:
            return {'error': 'An error occurred while fetching the buyer account', 'Message': {e}}, 500
        
    @login_required
    def patch(self):
        try:
            buyer = current_user
            if buyer:
                data = request.get_json()
                buyer.buyer_email = data.get('buyer_email', buyer.buyer_email)

                password = data.get('buyer_password')
                if password:
                    hashed_password = generate_password_hash(password)
                    buyer.password_hash = hashed_password
                
                db.session.commit()
                return {
                    "id": buyer.id,
                    "name": buyer.buyer_name,
                    "email": buyer.buyer_email
                }, 200
            else:
                return {'Error': 'buyer not found'}, 404
        except Exception as e:
            return {'Error': 'An error occurred while updating the buyer', 'Message': {e}}, 500
        
    @login_required
    def delete(self):
        try: 
            data = request.get_json()
            password = data['password']
            buyer = current_user

            if buyer:
                if buyer.authenticate(password):
                    db.session.delete(buyer)
                    db.session.commit()
                    return {}, 204
                else:
                    return {'error': 'Couldn\'t authenticate password'}
            else:
                return {'Error': 'User not found'}, 404
        except Exception as e:
            return {'Error': 'An error occured while deleting the buyer', 'Message': {e}}, 500

api.add_resource(Buyers, '/buyers')

class BuyerSignup(Resource):
    def post(self):
        data = request.get_json()
        try:
            buyer_img = data['buyer_img']
            with open(buyer_img, 'rb') as img:
                image_data = img.read()
                encoded_image = base64.b64encode(image_data)
        except:
            image_path = os.path.join(
                "images", "blank-profile-picture-973460_960_720.png")
            with open(image_path, 'rb') as img:
                image_data = img.read()
                encoded_image = base64.b64encode(image_data)

        new_buyer = Buyer(
            buyer_name=data['buyer_name'],
            buyer_email=data['buyer_email'],
            buyer_username=data['buyer_username'],
            buyer_image=encoded_image
        )
        new_buyer.password_hash = data['buyer_password']
        print(type(encoded_image))
        db.session.add(new_buyer)
        db.session.commit()

        login_user(new_buyer, remember=True)

        return new_buyer.to_dict(), 201


api.add_resource(BuyerSignup, '/buyer_signup')


class BuyerLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('buyer_email')
            password = data.get('buyer_password')

            buyer = Buyer.query.filter(Buyer.buyer_email == email).first()

            if buyer:
                if buyer.authenticate(password):
                    login_user(buyer, remember=True)
                    print(buyer.to_dict())
                    return buyer.to_dict(), 200
                if not buyer:
                    return {'error': '404: User not found'}, 404
        except Exception as e:
            return {'error': {e}}, 401


api.add_resource(BuyerLogin, '/buyer_login')


@app.route('/buyer_logout', methods=["POST"])
@login_required
def buyer_logout():
    logout_user()
    return 'you logged out'


## END ############## LOGIN / USER ################


################ BUSINESS ################

# GET /businesses
# note: ROUTE classes MUST be called DIFFERENT than MODEL class
class Businesses(Resource):
    # NO MAX RECURSION
    # FULLY FUNCTIONAL
    def get(self):
        # 1 query
        bs = Business.query.all()
        if not bs:
            return {"error": "Business not found."}, 404
        # 2 dict aka res into JSON obj
        b_dict = [b.to_dict(
            only=(
                "business_name",
                "business_address",
                "business_img",
                "business_banner_img",
                "business_desc",
                "bis_category_id",
                "business_category",
            )
        ) for b in bs]
        # 3 res
        res = make_response(
            b_dict,
            200
        )
        return res

# POST /businesses
    def post(self):
        # 1 set data as JSON
        data = request.get_json()
        # 2 create instance
        new_bis = Business(
            business_name=data.get('business_name'),
            business_address=data.get('business_address'),
            business_img=data.get('business_img'),
            business_banner_img=data.get('business_banner_img'),
            business_desc=data.get('business_desc')
        )
        # 3 add/commit to database
        db.session.add(new_bis)
        db.session.commit()

        # 4 dict aka res into JSON obj
        new_bis_dict = new_bis.to_dict()

        # 5 res
        res = make_response(
            new_bis_dict,
            201
        )
        # 6 return res
        return res


# add route
api.add_resource(Businesses, "/businesses")


# GET /businesses/<int:id>
class BusinessById(Resource):
    def get(self, id):
        # 1 query
        one_bs = Business.query.filter_by(id=id).first()
        if not one_bs:
            return {"error": "Business not found."}, 404
        # 2 dict aka res into JSON obj
        one_bs_dict = one_bs.to_dict()
        res = make_response(
            one_bs_dict,
            200
        )
        return res

# PATCH /businesses/<int:id>

    def patch(self, id):
        # 1 query by id
        bis = Business.query.filter_by(id=id).first()

        # 2 get data from request in JSON format
        data = request.get_json()

        # 3 update values in the model
        for attr in data:
            setattr(bis, attr, data.get(attr))

        # 4 update the database
        db.session.add(bis)
        db.session.commit()

        # 5 return res
        return make_response(bis.to_dict(), 200)

# DELETE /businesses/<int:id>
    def delete(self, id):
        # 1 get by id
        one_bs = Business.query.filter_by(id=id).first()
        if not one_bs:
            return {"error": "Business not found."}, 404
        # 2 delete from database
        db.session.delete(one_bs)
        db.session.commit()

        return make_response({}, 204)


# add route
api.add_resource(BusinessById, "/businesses/<int:id>")

###### BUSINESSBYSTATE #####
class BusinessByState(Resource):
    def get(self, business_state):
        state = Business.query.filter_by(business_state=business_state).all()
        if not state:
            return {"error": "State not found"},
            404
        return [business.to_dict() for business in state]
    
api.add_resource(BusinessByState, '/BusinessByState/<str: business_state')

#GET /business_by_category
class BusinessByCategory(Resource):

    def get(self, category):
            # 1 query
            bs = Business.query.filter_by(bis_category_id=category).all()
            if not bs:
                return {"error": "Business not found."}, 404
            # 2 dict aka res into JSON obj
            b_dict = [b.to_dict(
                only=(
                    "business_name", 
                    "business_img", 
                    "business_desc", 
                    "bis_category_id", 
                    "business_category",
                    )
                ) for b in bs]
            # 3 res
            res = make_response(
                b_dict,
                200
            )
            return res
    
api.add_resource(BusinessByCategory, "/business_by_category/<int:category>")

################ BUSINESS CATEGORIES ################

# GET /business_categories
class BusinessCategories(Resource):
    # NO MAX RECURSION
    # FULLY FUNCTIONAL
    def get(self):
        # 1 query
        bcs = BusinessCategory.query.all()
        if not bcs:
            return {"error": "Business not found."}, 404
        # 2 turn to JSON w dict
        bcs_dict = [bc.to_dict() for bc in bcs]
        # 3 res
        res = make_response(
            bcs_dict,
            200
        )
        return res

# NOT NEEDED; NO USER NEEDS TO POST; ONLY DEVS
# AVAILABLE FOR TESTING PURPOSES
# POST /business_categories
    # def post(self):
    #     # 1 set data as JSON
    #     data = request.get_json()
    #     # 2 create instance
    #     new_bis_cat = BusinessCategory(
    #         category_name=data.get('category_name')
    #     )
    #     # 3 add to db
    #     db.session.add(new_bis_cat)
    #     db.session.commit()

    #     # 4 dict aka res into JSON obj
    #     new_bis_cat_dict = new_bis_cat.to_dict()

    #     # 5 res to JSON obj
    #     res = make_response(
    #         new_bis_cat_dict,
    #         201
    #     )
    #     return res


# add route
api.add_resource(BusinessCategories, "/business_categories")


# GET /business_categories/<int:id>
class BusinessCategoryById(Resource):
    def get(self, id):
        one_bc = BusinessCategory.query.filter_by(id=id).first()
        if not one_bc:
            return {"error": "Business Category not found."}, 404
        one_bc_dict = one_bc.to_dict()
        res = make_response(
            one_bc_dict,
            200
        )
        return res

# PATCH /business_categories/<int:id>
# NOT NEEDED; NO USER NEEDS TO POST; ONLY DEVS
# AVAILABLE FOR TESTING PURPOSES
    # def patch(self, id):
    #     # 1 query by id
    #     bc = BusinessCategory.query.filter_by(id=id).first()

    #     # 2 get data from request in JSON format
    #     data = request.get_json()

    #     # 3 update values in the model
    #     for attr in data:
    #         setattr(bc, attr, data.get(attr))

    #     # 4 update the database
    #     db.session.add(bc)
    #     db.session.commit()

    #     # 5 return res
    #     return make_response(bc.to_dict(), 200)


# DELETE /business_categories/<int:id>

    def delete(self, id):
        # 1 get by id
        one_bc = BusinessCategory.query.filter_by(id=id).first()
        if not one_bc:
            return {"error": "Business not found."}, 404
        # 2 delete from database
        db.session.delete(one_bc)
        db.session.commit()

        return make_response({}, 204)


api.add_resource(BusinessCategoryById, "/business_categories/<int:id>")


################ PRODUCTS ################

# GET
class Products(Resource):
    def get(self):
        products = [product.to_dict(
            only=(
                # "product_name",
                # "product_description",
                "product_img",
                # "product_price",
            )
        ) for product in Product.query.all()]
        response = make_response(
            products,
            200
        )
        return response
# POST

    def post(self):
        try:
            data = request.get_json()
            print(data)
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
# GET
class ProductsByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            {"error": "Product not found"},
            404
        product_dict = product.to_dict()
        response = make_response(
            product_dict,
            200
        )
        return response
    # POST
    # PATCH

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

    # DELETE
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            make_response(
                {"error": "product not foun"},
                404
            )
        db.session.delete(product)
        db.session.commit()


api.add_resource(ProductsByID, '/product/<int:id>')

#GET /products_by_bis/<int:business>
class ProductsByBis(Resource):
    def get(self, business):
        products = [product.to_dict(
            only=(
                "product_name",
                # "product_description",
                # "product_img",
                "product_price",
            )
        ) for product in Product.query.filter_by(business_id=business).all()]
        response = make_response(
            products,
            200
        )
        return response
    
api.add_resource(ProductsByBis, "/products_by_bis/<int:business>")

#GET /products_by_bis/<int:business>
class ProductsByCat(Resource):
    def get(self, category):
        products = [product.to_dict(
            only=(
                "product_name",
                # "product_description",
                # "product_img",
                "product_price",
            )
        ) for product in Product.query.filter_by(product_category_id=category).all()]
        response = make_response(
            products,
            200
        )
        return response
    
api.add_resource(ProductsByCat, "/products_by_cat/<int:category>")


######### ATTRIBUTES ################
# GET /attributes


class Attributes(Resource):
    def get(self):
        # 1 query
        ats = Attribute.query.all()
        if not ats:
            return {"error": "Business not found."}, 404
        # 2 dict aka res into JSON obj
        ats_dict = [at.to_dict(
            only=("attribute_name", "product_id", "id",)
        ) for at in ats]
        # 3 res
        res = make_response(
            ats_dict,
            200
        )
        return res

# POST /attributes
    def post(self):
        # 1 set data as JSON
        data = request.get_json()
        # 2 create instance
        new_at = Attribute(
            attribute_name=data.get('attribute_name')
        )
        # 3 add/commit to database
        db.session.add(new_at)
        db.session.commit()

        # 4 dict aka res into JSON obj
        new_at_dict = new_at.to_dict()

        # 5 res
        res = make_response(
            new_at_dict,
            201
        )
        # 6 return res
        return res


# add route
api.add_resource(Attributes, "/attributes")

# GET /attributes/<int:id>


class AttributeById(Resource):
    def get(self, id):
        # 1 query
        one_at = Attribute.query.filter_by(id=id).first()
        if not one_at:
            return {"error": "Attribute not found."}, 404
        # 2 dict aka res into JSON obj
        one_at_dict = one_at.to_dict(
            only=("attribute_name", "product_id", "id",)
        )
        res = make_response(
            one_at_dict,
            200
        )
        return res

# DELETE /attributes/<int:id>
    def delete(self, id):
        # 1 get by id
        one_at = Attribute.query.filter_by(id=id).first()
        if not one_at:
            return {"error": "Attribute not found."}, 404
        # 2 delete from database
        db.session.delete(one_at)
        db.session.commit()

        return make_response({}, 204)


# add route
api.add_resource(AttributeById, "/attributes/<int:id>")

################ PRODUCT CATEGORIES ################

# GET /product_categories


class ProductCategories(Resource):
    # NO MAX RECURSION
    # FULLY FUNCTIONAL
    def get(self):
        # 1 query
        pcs = ProductCategory.query.all()
        if not pcs:
            return {"error": "Product Category not found."}, 404
        # 2 dict
        pcs_dict = [pc.to_dict() for pc in pcs]
        # 3 res
        res = make_response(
            pcs_dict,
            200
        )
        return res


# POST /product_categories
# NOT NEEDED; NO USER NEEDS TO POST; ONLY DEVS
# AVAILABLE FOR TESTING PURPOSES
    # def post(self):
    #     # 1 set data as JSON
    #     data = request.get_json()
    #     # 2 create instance
    #     new_product = ProductCategory(
    #         category_name=data.get('category_name')
    #     )
    #     # add/commit to db
    #     db.session.add(new_product)
    #     db.session.commit()

    #     # 4 dict aka res into JSON obj
    #     new_product_dict = new_product.to_dict()

    #     # 5 res
    #     res = make_response(
    #         new_product_dict,
    #         201
    #     )
    #     # 6 return res
    #     return res


api.add_resource(ProductCategories, "/product_categories")

# GET /product_categories/<int:id>


class ProductCategoryById(Resource):
    def get(self, id):
        # 1 query
        one_pc = ProductCategory.query.filter_by(id=id).first()
        if not one_pc:
            return {"error": "Product Category not found."}, 404
        # 2 dict
        one_pc_dict = one_pc.to_dict()
        # res
        res = make_response(
            one_pc_dict,
            200
        )
        return res

# DO WE NEED PATCH FOR THIS MODEL??
# PATCH /product_categories/<int:id>
    # def patch(self, id):
    #     #1 query
    #     #2 data to JSON
    #     #3 edit
    #     #add/commit to db
    #     #return res


# DELETE /product_categories/<int:id>
# NOT NEEDED; NO USER NEEDS TO POST; ONLY DEVS
# AVAILABLE FOR TESTING PURPOSES
    # def delete(self, id):
    #     # 1 query
    #     pc = ProductCategory.query.filter_by(id=id).first()
    #     if not pc:
    #         return {'error': "Product Category not found."}, 404
    #     # delete/commit from/to db
    #     db.session.delete(pc)
    #     db.session.commit()
    #     # return res
    #     return make_response({}, 204)


api.add_resource(ProductCategoryById, "/product_categories/<int:id>")

################ INVENTORY ################




################ REVIEWS ################
class Reviews(Resource):
    def get(self, product_id):
        try:
            reviews = Review.query.filter_by(product_id=product_id).all()
            review_list = []
            for review in reviews:
                review_info = {
                    'review_id': review.id,
                    'buyer_id': review.buyer_id,
                    'buyer_name': review.buyer.name,
                    'rating': review.rating,
                    'review_text': review.review,
                    'created_at': review.created_at
                }
                if review.updated_at:
                    review_info['updated_at'] = review.updated_at.isoformat()
                if review.review_img:
                    review_info['review_img'] = review.review_img

                review_list.append(review_info)
            return review_list, 200
        except Exception as e:
            return {'error': 'An error occurred while fetching the reviews', 'Message': {e}}, 500

    @login_required
    def post(self, product_id):
        try:
            buyer_id = current_user.id
            data = request.get_json()
            rating = int(data.get('rating'))
            review_text = data.get('review_text')
            if data['review_img']:
                try:
                    review_img = data['review_img']
                    with open(review_img, 'rb') as img:
                        image_data = img.read()
                        encoded_image = base64.b64encode(image_data)
                except Exception as e:
                    return {'Error': 'error while processing image', 'Message': {e}}, 500

            review = Review(
                buyer_id=buyer_id,
                product_id=product_id,
                review=review_text,
                rating=rating
            )
            if encoded_image:
                review['review_img'] = encoded_image

            db.session.add(review)
            db.session.commit()

            review_info = {
                'review_id': review.id,
                'buyer_id': review.buyer_id,
                'buyer_name': review.buyer.name,
                'rating': review.rating,
                'review_text': review.review,
                'created_at': review.created_at
            }
            if review.updated_at:
                review_info['updated_at'] = review.updated_at.isoformat()
            if review.review_img:
                review_info['review_img'] = review.review_img

            return review_info, 201

        except Exception as e:
            return {'error': 'An error occurred while creating review', 'Message': {e}}, 500


api.add_resource(Reviews, '/review/<product_id>')

# Buyer specific reviews

class BuyerReview(Resource):
    @login_required
    def patch(self, review_id):
        try:
            buyer_id = current_user.id
            review_to_edit = Review.query.filter_by(id=review_id, buyer_id=buyer_id).first()

            if review_to_edit:
                data = request.get_json()
                rating = data.get('rating')
                review = data.get('review')

                review_to_edit.rating = rating
                review_to_edit.review = review
                review.updated_at = datetime.datetime.now()

                db.session.commit()

                review_info = {
                    'review_id': review_to_edit.id,
                    'buyer_id': review_to_edit.buyer_id,
                    'rating': review_to_edit.rating,
                    'review': review_to_edit.review,
                    'created_at': review.created_at.isoformat() if review.created_at else None
                }

                if review.updated_at:
                    review_info['updated_at'] = review.updated_at.isoformat()
                return review_info, 200
            else:
                return {'Error': 'Review not found'}, 404
        except Exception as e:
            return {'Error': 'An error occurred while updating review', 'Message': {e}}, 500
    
    @login_required
    def delete(self, review_id):
        try:
            buyer_id = current_user.id
            review = Review.query.filter_by(id=review_id, buyer_id=buyer_id).first()

            if review:
                db.session.delete(review)
                db.session.commit()
                return {}, 204
            else:
                return {'Error': 'Review not found'}, 404
        except Exception as e:
            return {'Error': 'An error occured while deleting review', 'Message': {e}}, 500
        
api.add_resource(BuyerReview, '/buyer/reviews/<review_id>')


################ SALE HISTORY ################
#GET - doing by User since this should be applicable for both sellers and buyers
class SaleHistoryByUser(Resource):
    def get(self):
        current_user = User.get_current_user()
        if not current_user:
                {"error": "Unauthorized Access"},
                404

        sale_histories = SaleHistory.query.join(
            "order"
        ).join(
            "business"
        ).filter(Order.user_id == current_user.id).all()

        if not sale_histories:
            {"error": "No sale history found for this user"},
            404

        response = make_response("Sale history retrieved successfully", 200)
        return response
    def patch(self, order_id):
        current_user = User.get_current_user()  
        if not current_user:
                {"error": "User not found"},
                404

        order = Order.query.filter_by(id=order_id).first()
        if not order:
                {"error": "Order not found"},
                404
        new_status_id = request.json.get("status_id")
        if not new_status_id:
                "Missing status_id in request data",
                404

        try:
            new_status = Order_Status.query.get(new_status_id)
            if not new_status:
                {"error": "Invalid ID"},
                404

            order.status = new_status
            db.session.commit()  

            response = make_response("Order status updated successfully", 200)
        return response

api.add_resource(SaleHistoryByUser, '/salehistorybyuser/<int:id>')


################ ORDERS ################

#GET /orders_by_buyer/
class OrderByBuyer(Resource):
    def get(self):
        buyer = current_user.id
        orders = [order.to_dict(
            only= (
                "buyer_id",
                )
        ) for order in Order.query.filter_by(buyer_id=buyer).all()]
        response = make_response(
            orders,
            200
        )
        return response
    
api.add_resource(OrderByBuyer, "/orders_by_buyer")

#GET /buyers_specific_orders
class BuyersSpecificOrder(Resource):
    def get(self, order_id):
        try:
            buyer_id = current_user.id
            order = Order.query.filter_by(id=order_id, buyer_id=buyer_id).first()
            if order:
                order_items = [
                    {
                        "product_id": item.product_id,
                        "product_name": item.product.name,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order.order_items
                ]
                order_info = {
                    "order_id": order.id,
                    "total_price": order.total_price,
                    "order_items": order_items,
                    "order_status": order.status_id
                }
                return order_info, 200
            else:
                return {"error": "order not found"}, 400
        except Exception as e:
            return {"error": "an error occurred while processing", "Message": {e}}, 500
    
api.add_resource(BuyersSpecificOrder, "/buyers_specific_orders/<int:order>")

################ ORDER ITEMS ################
# GET
# FULLY FUNCTIONAL


class OrderItems(Resource):
    def get(self):
        orderItems = [orderItem.to_dict()
                      for orderItem in Order_Item.query.all()]
        response = make_response(
            orderItems,
            200
        )
        return response


api.add_resource(OrderItems, '/orderitems')

################ ORDER STATUS ################
# GET


################ SHOPIFY INFO ################
# GET


class ShopifyInfo(Resource):
    def get(self):
        shopifyInfo = [shopifyInfos.to_dict()
                       for shopifyInfos in ShopifyInfo.query.all()]
        response = make_response(
            shopifyInfo,
            200
        )
        return response


api.add_resource(ShopifyInfo, '/shopifyinfo')

################ PAYMENT ################
# GET


class Payment(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        response = make_response(
            payments,
            200
        )
        return response


api.add_resource(Payment, '/payment')

################ MESSAGING ################

# GET /messages

# NOT COMPLETE, CHECK POST, OTHERWISE FULLY FUNCTIONAL


class Messages(Resource):
    def get(self):
        ms = Message.query.all()
        if not ms:
            return {"error": "Message not found."}, 404
        ms_dict = [m.to_dict() for m in ms]
        res = make_response(
            ms_dict,
            200
        )
        return res

# POST /messages
    def post(self):

        data = request.get_json()

        new_msg = Message(
            content=data.get('content'),
            read_by_buyer=data.get('read_by_buyer'),
            read_by_seller=data.get('read_by_seller'),
            attachments=data.get('attachments')
            # conversations=data.get('conversations'),
        )
        db.session.add(new_msg)
        db.session.commit()

        new_msg_dict = new_msg.to_dict()

        res = make_response(
            new_msg_dict,
            201
        )
        return res


api.add_resource(Messages, "/messages")

# GET /messages/<int:id>


class MessageById(Resource):
    def get(self, id):
        m = Message.query.filter_by(id=id).first()

        if not m:
            return {"error": "Message not found."}, 404

        m_dict = m.to_dict()

        res = make_response(
            m_dict,
            200
        )
        return res

# PATCH /messages/<int:id>

# DELETE /messages/<int:id>
    def delete(self, id):
        m = Message.query.filter_by(id=id).first()
        if not m:
            return {"error": "Message not found."}, 404
        db.session.delete(m)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(MessageById, "/messages/<int:id>")

################ MESSAGE RECIPIENT ################


################ ORDER HISTORY ################
# list of all
# see one
#


################ ADDRESS ################

# GET /addresses
# FUNCTIONALLY COMPLETE
class Addresses(Resource):
    @login_required
    def get(self):
        try:
            buyer_id = current_user.id
            addresses = Address.query.filter_by(buyer_id=buyer_id).all()
            address_list = []
            for address in addresses:
                address_info = {
                    'id': address.id,
                    'address_line_one': address.address_line_one,
                    'address_line_two': address.address_line_two,
                    'city': address.city,
                    'state': address.state,
                    'zipcode':address.zip,
                    'type': address.address_type
                }
                address_list.append(address_info)
            return address_list, 200
        except Exception as e:
            return {'Error': 'There was an error getting the address', 'Message':{e}}, 500

# POST /addresses
    @login_required
    def post(self):
        try:
            data = request.json()
            buyer_id = current_user.id
            address = Address(
                buyer_id=buyer_id,
                address_line_one=data['address_line_one'],
                address_line_two=data['address_line_two'],
                city=data['city'],
                state=data['state'],
                zip=data['zip'],
                address_type=data['address_type']
            )
            db.session.add(address)
            db.session.commit()

            address_info = {
                    'id': address.id,
                    'address_line_one': address.address_line_one,
                    'address_line_two': address.address_line_two,
                    'city': address.city,
                    'state': address.state,
                    'zipcode':address.zip,
                    'type': address.address_type
                }
            return address_info, 201
        except Exception as e:
            return {'error': 'An error occurred while creating the address', "message": str(e)}, 500

api.add_resource(Addresses, "/addresses")

# GET /addresses/<int:id>

class AddressById(Resource):
    
# PATCH /addresses/<int:id>
    @login_required
    def patch(self, address_id):
        try:
            buyer_id = current_user.id
            data = request.get_json()

            address = Address.query.filter_by(id=address_id, buyer_id=buyer_id).first()

            if not address:
                return {'error':'address not found'}, 404
            
            for attr in data:
                setattr(address, attr, data[attr])
            db.session.add(address)
            db.session.commit()

            return address.to_dict(), 200
        except Exception as e:
            return {'Error':'An error occurred while updating the address', 'message': {e}}, 500
        
    @login_required
    def delete(self, address_id):
        try:
            buyer_id = current_user.id
            address = Address.query.filter_by(id=address_id, buyer_id=buyer_id).first()

            if not address:
                return {"Error":"Address not found"}, 404
            
            db.session.delete(address)
            db.session.commit()

            return {}, 204
        except Exception as e:
            return {'Error':'An error occured while deleting the address'}, 500


api.add_resource(AddressById, "/addresses/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
