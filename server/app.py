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


## START ############## LOGIN / USER ################

#### SELLER ####
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
                ipdb.set_traceback()
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
    def get(self):
        # 1 query
        bs = Business.query.all()
        if not bs:
            return {"error": "Business not found."}, 404
        # 2 dict aka res into JSON obj
        b_dict = [b.to_dict() for b in bs]
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
            business_desc=data.get('business_desc'),
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


################ BUSINESS CATEGORIES ################

# GET /business_categories
class BusinessCategories(Resource):
    def get(self):
        # 1 query
        bcs = Business.query.all()
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

# POST /business_categories
    def post(self):
        # 1 set data as JSON
        data = request.get_json()
        # 2 create instance
        new_bis_cat = BusinessCategory(
            category_name=data.get('cat')
        )
        # 3 add to db
        db.session.add(new_bis_cat)
        db.session.commit()

        # 4 dict aka res into JSON obj
        new_bis_cat_dict = new_bis_cat.to_dict()

        # 5 res to JSON obj
        res = make_response(
            new_bis_cat_dict,
            201
        )
        return res


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

# PATCH /business_categories/<int:id>

    def patch(self, id):
        # 1 query by id
        bc = BusinessCategory.query.filter_by(id=id).first()

        # 2 get data from request in JSON format
        data = request.get_json()

        # 3 update values in the model
        for attr in data:
            setattr(bc, attr, data.get(attr))

        # 4 update the database
        db.session.add(bc)
        db.session.commit()

        # 5 return res
        return make_response(bc.to_dict(), 200)


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
        products = [product.to_dict() for product in Product.query.all()]
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
            abort(404, "Product not found")
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

######### ATTRIBUTES ################


################ PRODUCT CATEGORIES ################

# GET /product_categories
class ProductCategories(Resource):
    def get(self):
        # 1 query
        pcs = ProductCategory.query.all()
        if not pcs:
            return {"error": "Product Category not found."}, 404
        # 2 dict
        pcs_dict = [pc.to_dict for pc in pcs]
        # 3 res
        res = make_response(
            pcs_dict,
            200
        )
        return res


# POST /product_categories

    def post(self):
        # 1 set data as JSON
        data = request.get_json()
        # 2 create instance
        new_product = ProductCategory(
            category_name=data.get(['product_category'])
        )
        # add/commit to db
        db.session.add(new_product)
        db.session.commit()

        # 4 dict aka res into JSON obj
        new_product_dict = new_product.to_dict()

        # 5 res
        res = make_response(
            new_product_dict,
            201
        )
        # 6 return res
        return res


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

    def delete(self, id):
        # 1 query
        pc = ProductCategory.query.filter_by(id=id).first()
        if not pc:
            return {'error': "Product Category not found."}, 404
        # delete/commit from/to db
        db.session.delete(pc)
        db.session.commit()
        # return res
        return make_response({}, 204)

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
                review = review_text,
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

################ REVIEWSBYID ################

# GET


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
    # POST
    # PATCH

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

    # DELETE
    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            make_response(
                {"error": "review not found"},
                404
            )
        db.session.delete(review)
        db.session.commit()


api.add_resource(ReviewsByID, '/review/<int:id>')


################ SALE HISTORY ################

################ ORDERS ################
# GET
class Orders(Resource):
    def get(self):
        orders = [order.to_dict() for order in User.query.all()]
        response = make_response(
            orders,
            200
        )
        return response


api.add_resource(Orders, '/orders')
################ ORDERSBYID ################
# GET


class OrderByID(Resource):
    def get(self, id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            abort(404, "order not found")
        order_dict = order.to_dict()
        response = make_response(
            order_dict,
            200
        )
        return response
    # PATCH

    def patch(self, id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            return make_response({'error': 'order not found'}, 404)
        data = request.get_json()
        for attr in data:
            setattr(order, attr, data[attr])
        db.session.add(order)
        db.session.commit()

        return make_response(order.to_dict(), 202)
    # DELETE

    def delete(self, id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            make_response(
                {"error": "order not found"},
                404
            )
        db.session.delete(order)
        db.session.commit()

        order = Order.query.filter_by(id=id).first()
        if not order:
            make_response(
                {"error": "order not found"},
                404
            )
        db.session.delete(order)
        db.session.commit()


api.add_resource(OrderByID, '/order/<int:id>')

################ ORDER ITEMS ################
# GET


class OrderItems(Resource):
    def get(self):
        orderItems = [orderItem.to_dict()
                      for orderItem in OrderItem.query.all()]
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
            attachments=data.get(['attachments']),
            conversations=data.get('conversations'),
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


################ ORDER HISTORY ################
# list of all
# see one
#


################ ADDRESS ################

# GET /addresses
class Addresses(Resource):
    def get(self):
        # 1 query
        ads = Address.query.all()
        # 2 dict
        ads_dict = [ads.to_dict() for ad in ads]
        # res
        res = make_response(
            ads_dict,
            200
        )
        return res

# POST /addresses
    def post(self):
        # 1 set data as JSON
        data = request.get_json()
        # 2 create instance
        new_ad = Business(
            address_line_one=data.get('address_line_one'),
            address_line_two=data.get('address_line_two'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            address_type=data.get('address_type'),
        )
        # 3 add/commit to database
        db.session.add(new_ad)
        db.session.commit()

        # 4 dict aka res into JSON obj
        new_ad_dict = new_ad.to_dict()

        # 5 res
        res = make_response(
            new_ad_dict,
            201
        )
        # 6 return res
        return res


api.add_resource(Addresses, "/addresses")

# GET /addresses/<int:id>


class AddressById(Resource):
    def get(self, id):
        # 1 query
        ad = Address.query.filter_by(id=id).first()
        if not ad:
            return {"error": "Address not found."}, 404
        # 2 dict
        ad_dict = ad.to_dict()
        # res
        res = make_response(
            ad_dict,
            200
        )
        return res


# PATCH /addresses/<int:id>

    def patch(self, id):
        ad = Address.query.filter_by(id=id).first()
        data = request.to_json()
        if not ad:
            return make_response({'error': 'address not found'},
                                 404
                                 )
        data = request.get_json()
        for attr in data:
            setattr(ad, attr, data[attr])
        db.session.add(ad)
        db.session.db.session.commit()

        return make_response(ad.to_dict(), 202)

# DELETE /addresses/<int:id>
    def delete(self, id):
        ad = Address.query.filter_by(id=id).first()
        if not ad:
            return {"error": "Address not found."}, 404
        db.session.delete(ad)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(AddressById, "/addresses/<int:id>")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
