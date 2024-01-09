from config import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin, LoginManager
import re
from datetime import datetime


############### Models ##############

############ SELLER ############

class Seller(db.Model, SerializerMixin, UserMixin):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    seller_name = db.Column(db.String)
    seller_email = db.Column(db.String, unique=True)
    seller_username = db.Column(db.String, unique=True)
    seller_password = db.Column(db.String)
    seller_img = db.Column(db.LargeBinary)

    # RELATIONSHIP

    # one seller has many businesses; many businesses belong to one seller
    seller_business = db.relationship(
        "Business", back_populates="seller"
    )

    # VALIDATION
    @validates('seller_email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email

    # password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+={}[\]:;<>,.?~\\/-])[a-zA-Z0-9!@#$%^&*()_+={}[\]:;<>,.?~\\/-]{8,}$')

    # def is_password_valid(password):
    #      return bool(password_pattern.match(password))

    @validates('password')
    def validate_password(self, key, password):

        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        # elif (not is_password_valid(password)):
        #      raise ValueError('Password must contain atleast one capital, one special character and one number')
        # elif not re.search('[!@#$%^&*]', password):
        #      raise ValueError('Password must contain at least one special character.')
        return password

    # SERIALIZE RULES

    serialize_rules = ('-seller_business', )

    # hashes/encodes the password
    # security
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self.seller_password = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.seller_password, password.encode('utf-8'))

    @validates('seller_name', 'seller_username', 'seller_password')
    def validate_non_empty_fields(self, key, value):
        if value is not None and not value.strip():
            raise ValueError('Field must not be empty.')
        return value


############ BUSINESS ############

class Business(db.Model, SerializerMixin):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bis_category_id = db.Column(db.Integer, db.ForeignKey('business_categories.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'))

    business_name = db.Column(db.String, unique=True)
    business_address = db.Column(db.String)
    business_img = db.Column(db.String)
    business_banner_img = db.Column(db.String)
    business_desc = db.Column(db.String)

    # RELATIONSHIP

    # one seller has many businesses; many businesses belong to one seller
    seller = db.relationship(
        "Seller", back_populates="seller_business"
    )

    # one business has many categories; one category has many businesses
    business_category = db.relationship(
        "BusinessCategory", back_populates="category"
    )

    # one business has many products; many products have one business
    business_products = db.relationship(
        "Product", back_populates="business"
    )

    sale_histories = db.relationship("SaleHistory", back_populates='business')

    # VALIDATION

    # SERIALIZE RULES

    serialize_rules = ('-seller', '-business_category', 'business_products')


############ BUSINESS CATEGORIES ############

class BusinessCategory(db.Model, SerializerMixin):
    __tablename__ = "business_categories"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # FOREIGN KEY
    category_name = db.Column(db.String)

    # RELATIONSHIP

    # one business has many categories; one category has many businesses
    category = db.relationship(
        "Business", back_populates="business_category"
    )

    # VALIDATION

    # SERIALIZE RULES
    serialize_rules = ('-category', )


################# PRODUCTS ##################

class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    product_name = db.Column(db.String, nullable=False)
    product_description = db.Column(db.String, nullable=False)
    product_img = db.Column(db.LargeBinary, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    # FOREIGN KEY
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))

    # RELATIONSHIP

    # one business has many products; many products have one business
    business = db.relationship(
        "Business", back_populates="business_products"
    )

    # one product belongs to many categories; one category has many products
    product_category = db.relationship(
        "ProductCategory", back_populates="products"
    )

    # one product has many attributes; many attributes belong to a product
    product_attributes = db.relationship(
        "Attribute", back_populates="product"
    )

    # one instance of inventory belongs to one product; one product has one instance of inventory
    product_inventory = db.relationship(
        "Inventory", back_populates="product"
    )

    # many reviews belong to one product; one product has many reviews
    reviews = db.relationship(
        "Review", back_populates="product"
    )

    order_items = db.relationship('Order_Item', back_populates="product")

    # SERIALIZE RULES


################# ATTRIBUTES #################
class Attribute(db.Model, SerializerMixin):
    __tablename__ = "attributes"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # FOREIGN KEY
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # array to allow front end dropdown menu with attribute info
    attribute_name = db.Column(db.ARRAY(db.String))

    # RELATIONSHIP

    # one product has many attributes; many attributes belong to a product
    product = db.relationship(
        "Product", back_populates="product_attributes"
    )

    # one attribute belongs to one inventory; one inventory belongs to one attribute
    inventories = db.relationship('Inventory', back_populates='attribute')

    # VALIDATION

    # SERIALIZER RULES


################# PRODUCT CATEGORIES #################
class ProductCategory(db.Model, SerializerMixin):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # array to allow front end category selection
    category_name = db.Column(db.ARRAY(db.String))

    # RELATIONSHIP

    # one product belongs to many categories; one category has many products
    products = db.relationship(
        "Product", back_populates="product_category"
    )

    # VALIDATION

    # SERIALIZER RULES

    serialize_rules = ('-products', )


################# INVENTORY- STEVE DID RELATIONSHIPS #################
class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    product_quantity = db.Column(db.Integer, nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.id'))
    # FOREIGN KEYS
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # RELATIONSHIPS

    # one instance of inventory belongs to one product; one product has one instance of inventory
    product = db.relationship(
        "Product", back_populates="product_inventory"
    )

    # one attribute belongs to one inventory; one inventory belongs to one attribute
    attribute = db.relationship('Attribute', back_populates='inventories')

    # VALIDATION

    @validates('product_quantity')
    def validate_product_quantity(self, key, product_quantity):
        if product_quantity < 0:
            raise ValueError('Can\'t have less than zero')
        return product_quantity

    # SERIALIZE RULES

    serialize_rules = ('-product', 'attribute')


################# REVIEWS ##################
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    review = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_img = db.Column(db.LargeBinary, nullable=True)

    # FOREIGN KEY

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyers.id"))

    # RELATIONSHIP

    # many reviews belong to one product; one product has many reviews
    product = db.relationship(
        "Product", back_populates="reviews"
    )

    # many reviews belong to one buyer; one buyer owns many reviews
    buyer = db.relationship(
        "Buyer", back_populates="reviews"
    )

    # VALIDATION

    @validates('review')
    def validate_review(self, key, review):
        if len(review) > 2500:
            raise ValueError("Review cannot exceed 2500 characters.")
        return review

    @validates('rating')
    def validate_rating(self, key, rating):
        if not rating or rating < 0 or rating > 5:
            raise ValueError(' Invalid rating value, must be between 0 and 5')
        return rating

    # SERIALIZE RULES

################# SALEHISTORY #################


class SaleHistory(db.Model, SerializerMixin):
    __tablename__ = "sale_histories"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # FOREIGN KEY
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    # RELATIONSHIP

    # one sale belongs to one order; one order belongs to one sale
    order = db.relationship(
        "Order", back_populates="sale_history"
    )

    business = db.relationship("Business", back_populates='sale_histories')

    # SERIALIZE RULES


################# ORDERS ###################
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    total_price = db.Column(db.Float, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.id'))

    ############### FOREIGN KEYS ###############
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'))

    # RELATIONSHIP
    sale_history = db.relationship('SaleHistory', back_populates='order')
    # one sale belongs to one order; one order belongs to one sale
    # sale_history relationship

    # one order belongs to one buyer; one buyer owns one order
    buyer = db.relationship(
        "Buyer", back_populates="order"
    )

    # many order items belong to one order; one order owns many order items
    # order_items relationship
    order_items = db.relationship(
        'Order_Item', back_populates='order', cascade='all, delete-orphan')

    status = db.relationship('Order_Status', backref='orders')

    # SERIALIZE RULES


################# ORDERITEMS ################
class Order_Item(db.Model, SerializerMixin):
    __tablename__ = 'orderitems'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # RELATIONSHIP
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')

    # SERIALIZE RULES
    serialize_rules = ('-order', '-product')


######## ORDER STATUS- COMPLETE ########

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

    # SERIALIZE RULES


################# SHOPIFYINFO- LOOK AT SHOPIFY API ##################
class ShopifyInfo(db.Model, SerializerMixin):
    __tablename__ = "shopify_infos"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # FOREIGN KEY
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))

    shopify_auth_token = db.Column(db.Integer)


################# PAYMENT- LOOK AT SHOPIFY API ####################
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


################# MESSAGING- COMPLETE ##################
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    content = db.Column(db.String)
    read_by_buyer = db.Column(db.Boolean)
    read_by_seller = db.Column(db.Boolean)
    attachments = db.Column(db.ARRAY(db.LargeBinary))
    conversations = db.Column(db.String)

    # FOREIGN KEYS
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyers.id"))

    # VALIDATION

    @validates('content')
    def validate_contentl(self, key, content):
        if len(content) > 2500:
            raise ValueError("Message cannot exceed 2500 characters.")
        return content

    @validates('attachments')
    def validate_attachments(self, key, attachments):
        if len(attachments) > 3:
            raise ValueError("You cannot send more than 3 attachments.")
        return attachments


################# ORDERHISTORY- COMPLETE ################
class OrderHistory(db.Model, SerializerMixin):
    __tablename__ = "order_histories"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # FOREIGN KEY
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyers.id"))


################# ADDRESS- COMPLETE #################
class Address(db.Model, SerializerMixin):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'))
    address_line_one = db.Column(db.String, nullable=False)
    address_line_two = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    address_type = db.Column(db.String)

    # Relationship
    # ADDRESSES
    # arg 1= CLASS
    # arg2 = VARIABLE
    buyer = db.relationship('Buyer', back_populates='addresses')

    # IN BUYER TABLE
    # addresses = db.relationship("Address", back_populates="buyer"

    # Serialize Rules
    serialize_rules = ('-buyer',)

    # Validations
    @validates('postal_code')
    def validate_postal_code(self, key, postal_code):
        pattern = r'^\d{5}$'

        if not re.match(pattern, str(postal_code)):
            raise ValueError('Invalid postal code')
        return postal_code

    @validates('state')
    def validate_state(self, key, state):
        valid_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                        'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                        'VA', 'WA', 'WV', 'WI', 'WY']
        if state not in valid_states:
            raise ValueError(
                'Invalid state, please make sure state is abreviated in all caps.')
        return state

    @validates('address_line_1', 'city', 'address_type')
    def validate_non_empty_fields(self, key, value):
        if value is not None and not value.strip():
            raise ValueError('Field must not be empty.')
        return value

################# BUYER - Evan ####################


class Buyer(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'buyers'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    buyer_name = db.Column(db.String, nullable=False)
    buyer_email = db.Column(db.String, nullable=False)
    buyer_username = db.Column(db.String, nullable=False)
    buyer_password = db.Column(db.String, nullable=False)
    buyer_image = db.Column(db.LargeBinary)

    # RELATIONSHIP
    addresses = db.relationship(
        "Address", back_populates="buyer", cascade="all, delete-orphan")

    # association proxy
    # one buyer has products through purchased products

    # many reviews belong to one buyer; one buyer owns many reviews
    reviews = db.relationship(
        "Review", back_populates="buyer"
    )

    # one order belongs to one buyer; one buyer owns one order
    order = db.relationship(
        "Order", back_populates="buyer"
    )

    # SERIALIZE RULES
    serialize_rules = ('-addresses',)
    # VALIDATIONS

    @validates('buyer_email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email

    @validates('username')
    def validate_username(self, key, username):
        if not username and len(username) < 1:
            raise ValueError('Invalid username')
        return username

    # hashing
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self.buyer_password = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.buyer_password, password.encode('utf-8'))

    @validates('buyer_name', 'buyer_username', 'buyer_password')
    def validate_non_empty_fields(self, key, value):
        if value is not None and not value.strip():
            raise ValueError('Field must not be empty.')
        return value
