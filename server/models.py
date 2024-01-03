from config import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates 
from sqlalchemy.ext.associationproxy import associationproxy
from sqlalchemy.ext.hybrid import hybrid_proprty
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin, LoginManager
import re
from datetime import datetime


############### Models ##############

############ SELLER -Val ############

class Seller(db.Model, SerializerMixin, UserMixin):
    __tablename__ = "sellers"

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    business_id=db.Column(db.Integer, db.ForeignKey("businesses.id"))

    seller_name=db.Column(db.String)
    seller_email=db.Column(db.String)
    seller_username=db.Column(db.String)
    seller_password=db.Column(db.String)
    seller_img=db.Column(db.String)
    
    #RELATIONSHIP
    
    #one seller has many businesses; many businesses belong to one seller
    
    # seller_business=db.relationship(
        
    # )
    
    #VALIDATION
    @validates('seller_email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email
        
    
    # password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+={}[\]:;<>,.?~\\/-])[a-zA-Z0-9!@#$%^&*()_+={}[\]:;<>,.?~\\/-]{8,}$')

    # def is_password_valid(password):
    #      return bool(password_pattern.match(password))
    
    @validates ('password')
    def validate_password(self, key, password):
            
            if len(password) < 8:
                 raise ValueError('Password must be at least 8 characters long.')
            # elif (not is_password_valid(password)):
            #      raise ValueError('Password must contain atleast one capital, one special character and one number')
            # elif not re.search('[!@#$%^&*]', password):
            #      raise ValueError('Password must contain at least one special character.')
            return password

    #SERIALIZE RULES







############ BUSINESS -Val ############
    
class Business(db.Model, SerializerMixin):
    __tablename__ = "businesses"

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    bis_category_id=db.Column(db.Integer)
    seller_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)

    business_name=db.Column(db.String)
    business_address=db.Column(db.String)
    business_img=db.Column(db.String)
    business_banner_img=db.Column(db.String)
    business_desc=db.Column(db.String)

    #RELATIONSHIP

    #one seller has many businesses; many businesses belong to one seller
    #seller relationship

    #one business has many categories; one category has many businesses
    #business_category relationship

    #one business has many products; many products have one business 
    #business_products relationship



    #VALIDATION


    #SERIALIZE RULES







############ BUSINESS CATEGORIES -Val ############
    
class BusinessCategory(db.Model, SerializerMixin):
    __tablename__ = "business_categories"

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    
    #FOREIGN KEY
    business_id=db.Column(db.Integer, db.ForeignKey("businesses.id"))

    category_name=db.Column(db.String)
    
    #RELATIONSHIP
    
    #one business has many categories; one category has many businesses
    #category relationship 

    #VALIDATION
    
    
    #SERIALIZE RULES




################# PRODUCTS - Steve ##################

class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id= db.Column(db.Integer, primary_key=True)
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at= db.Column(db.DateTime, onupdate=db.func.now())
    product_name= db.Column(db.String, nullable=False)
    product_description= db.Column(db.String, nullable=False)
    product_img= db.Column(db.LargeBinary, nullable=False)
    product_price= db.Column(db.Float, nullable=False)

    #FOREIGN KEY
    seller_id= db.Column(db.Integer, db.ForeignKey("sellers.id"))
    business_id= db.Column(db.Integer, db.ForeignKey("businesses.id"))

    #RELATIONSHIP

    #one business has many products; many products have one business 
    #business relationship
    
    #one product belongs to many categories; one category has many products
    #product_category relationship
    
    #one product has many attributes; many attributes belong to a product
    #product_attributes relationship
    
    #one instance of inventory belongs to one product; one product has one instance of inventory
    #product_inventory relationship
    
    #many reviews belong to one product; one product has many reviews
    #reviews relationship





################# ATTRIBUTES #################
class Attribute(db.Model, SerializerMixin):
    __tablename__ = "attributes"

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    #FOREIGN KEY
    product_id=db.Column(db.Integer, db.ForeignKey("products.id"))

    #array to allow front end dropdown menu with attribute info
    attribute_name=db.Column(db.ARRAY(db.String))

    #RELATIONSHIP
    
    #one product has many attributes; many attributes belong to a product
    #product relationship
    
    #one attribute belongs to one inventory; one inventory belongs to one attribute
    #inventory relationship
    
    
    #VALIDATION


    #SERIALIZER RULES

################# PRODUCT CATEGORIES #################
class ProductCategory(db.Model, SerializerMixin):
    __tablename__='product_categories'
    
    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())

    #FOREIGN KEY
    product_id=db.Column(db.Integer, db.ForeignKey("products.id"))

    #array to allow front end category selection
    category_name=db.Column(db.db.ARRAY(db.String))
    
    #RELATIONSHIP

    #one product belongs to many categories; one category has many products
    #products
    

    #VALIDATION



    #SERIALIZER RULES



    
         



################# INVENTORY #################
class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventories'

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    product_quntity= db.Column(db.Integer, nullable=False)

    #FOREIGN KEYS
    product_id=db.Column(db.Integer, db.ForeignKey("products.id"))

    #RELATIONSHIPS
    
    #one instance of inventory belongs to one product; one product has one instance of inventory
    #product relationship
    
    #one attribute belongs to one inventory; one inventory belongs to one attribute
    #attributes relationship

    #SERIALIZE RULES








################# REVIEWS ##################
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id=db.Colum(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now())
    review=db.Column(db.String, nullable=False)
    rating=db.Column(db.Integer, nullable=False)
    review_img=db.Column(db.LargeBinary, nullable=False)

    #FOREIGN KEY
    
    product_id=db.Column(db.Integer, db.ForeignKey("products.id"))
    buyer_id=db.Column(db.Integer, db.ForeignKey("buyers.id"))

    #RELATIONSHIP
    

################# SALEHISTORY #################
class SaleHistory(db.Model, SerializerMixin):
    __tablename__ = "sale_histories"
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #FOREIGN KEY
    seller_id=db.Column(db.Integer, db.ForeignKey("sellers.id"))

    #RELATIONSHIP

    #one sale belongs to one order; one order belongs to one sale
    #order 

    #VALIDATION


    #SERIALIZE RULES


################# ORDERS ###################
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    total_price = db.Column(db.Float, nullable=False)
    status_id = db.Column(db.String, db.ForeignKey('order_statuses.id'))
    
    # relationship

################# ORDERITEMS ################
class Order_Item(db.Model, SerializerMixin):
    __tablename__ = 'orderitems'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

class Order_Status(db.Model, SerializerMixin):
    __tablename__ = 'order_statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    serialize_rules = ("-orders",)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

################# SHOPIFYINFO ##################
class ShopifyInfo(db.Model, SerializerMixin):
    __tablename__="shopify_infos"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #FOREIGN KEY
    seller_id=db.Column(db.Integer, db.ForeignKey("sellers.id"))

    shopify_auth_token=db.Column(db.Integer)




     
################# PAYMENT ####################
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #RELATIONSHIPS
    
################# MESSAGING- STEVE ##################
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    content= db.Column(db.String)
    read_by_buyer= db.Column(db.Boolean)
    read_by_seller= db.Column(db.Boolean)
    attachments= db.Column(db.LargeBinary)
    conversations= db.Column(db.String)
    
    #FOREIGN KEYS
    seller_id= db.Column(db.Integer, db.ForeignKey("sellers.id"))
    buyer_id= db.Column(db.Integer, db.ForeignKey("buyer.id"))


################# ORDERHISTORY ################
class OrderHistory(db.Model, SerializerMixin):
    __tablename__ = "order_histories"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #FOREIGN KEY
    buyer_id=db.Column(db.Integer, db.ForeignKey("buyers.id"))
    

################# ADDRESS #################
class Address(db.Model, SerializerMixin):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    address_line_one=db.Column(db.String)
    address_line_two=db.Column(db.String)
    postal_code=db.Column(db.Integer)
    address_type=db.Column(db.String)

   
    



################# BUYER - Evan ####################

class Buyer(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'buyer'
     
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    # reviews_id = db.Column(db.Integer, db.ForeignKey('reviews.id))
    buyer_name = db.Column(db.String, nullable=False)
    buyer_email = db.Column(db.String, nullable=False)
    buyer_username = db.Column(db.String, nullable=False)
    buyer_password = db.Column(db.String, nullable=False)
    buyer_image = db.Column(db.LargeBinary)

    # Relationships

    # Serialize Rules

    # Validations
    @validates('seller_email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email

