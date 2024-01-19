from app import app
from models import db, Seller, Business, BusinessCategory, Product, Attribute, ProductCategory, Inventory, Review, SaleHistory, Order, Order_Item, Order_Status, ShopifyInfo, Payment, Message, MessageRecipient, OrderHistory, Address, Buyer 
import pickle
from flask_bcrypt import Bcrypt
import random
import ipdb
import json
import os
import base64

bcrypt= Bcrypt()

def seed_business_category():
    try:
        bis_category = BusinessCategory(
            category_name = 'test category'
        )
        db.session.add(bis_category)
        db.session.commit()
    except ValueError as e:
            print(f'Unable to seed business category: {e}')

def seed_product_category():
    try:
        product_category = ProductCategory(
            category_name = ['Food and Beverage']
        )
        db.session.add(product_category)
        db.session.commit()
    except Exception as e:
        print(f'Error: {e}')

def seed_test_seller():
    image_path = os.path.join("images", "blank-profile-picture-973460_960_720.png")
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data)

    seller = [{'seller_name': 'Evan Roberts', 'seller_email': 'evanroberts@email.com', 'seller_username': 'EvanRoberts', 'seller_password': 'password', 'seller_img': encoded_image}]

    for seller_data in seller:
        try:
            password_hash = bcrypt.generate_password_hash(seller_data['seller_password']).decode('utf-8')
            seller_obj = Seller(
                seller_name=seller_data['seller_name'],
                seller_email=seller_data['seller_email'],
                seller_username=seller_data['seller_username'],
                seller_password=password_hash,
                seller_img=seller_data['seller_img']
            )
            db.session.add(seller_obj)
            db.session.commit()
        except KeyError as e:
            print(f'KeyError: {e} not found in seller_data: {seller_data}')

def seed_test_buyer():
    image_path = os.path.join("images", "blank-profile-picture-973460_960_720.png")
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data)

    buyer = [{'buyer_name': 'Evan Roberts', 'buyer_email': 'evanroberts@email.com', 'buyer_username': 'EvanRoberts', 'buyer_password': 'password', 'buyer_img': encoded_image}]

    for buyer_data in buyer:
        try:
            password_hash = bcrypt.generate_password_hash(buyer_data['buyer_password']).decode('utf-8')
            buyer_obj = Buyer(
                buyer_name=buyer_data['buyer_name'],
                buyer_email=buyer_data['buyer_email'],
                buyer_username=buyer_data['buyer_username'],
                buyer_password=password_hash,
                buyer_image=buyer_data['buyer_img']
            )
            db.session.add(buyer_obj)
            db.session.commit()
        except KeyError as e:
            print(f'KeyError: {e} not found in buyer_data: {buyer_data}')

def seed_business():
    try:
        image_path = os.path.join("images", "illustration.png")
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data)

        image_path_2 = os.path.join('images', 'chocowoco.png')
        with open(image_path_2, 'rb') as image_file_2:
            image_data_2 = image_file_2.read()
            encoded_image_2 = base64.b64encode(image_data_2)

        business = [
            {
                "bis_category_id":1,
                'seller_id':1,
                'business_name':'Chocotonic',
                'business_state':'NY',
                'business_address':'123 Main Street',
                'business_zip':13478,
                'business_img': encoded_image,
                'business_banner_img': encoded_image_2,
                'business_desc': 'we sell chocolate :)'
            }
        ]

        for business_data in business:
            business_obj = Business(
                bis_category_id=business_data['bis_category_id'],
                seller_id=business_data['seller_id'],
                business_name=business_data['business_name'],
                business_state=business_data['business_state'],
                business_address=business_data['business_address'],
                business_zip=business_data['business_zip'],
                business_img=business_data['business_img'],
                business_banner_img=business_data['business_banner_img'],
                business_desc=business_data['business_desc']
            )
        db.session.add(business_obj)
        db.session.commit()
    except Exception as e:
        print(f'Error: {e}')

def seed_product():
    images_directory = 'images'
    try:
        for filename in os.listdir(images_directory):
            if filename.endswith((".jpg", ".jpeg", ".png")) and filename not in ("illustration.png", "blank-profile-picture-973460_960_720.png", "chocowoco.png"):
                print(f"Processing image: {filename}")
                image_path = os.path.join(images_directory, filename)
                product_name = os.path.splitext(filename)[0].replace('-', ' ').title()
                product_price= 6.00
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    encoded_image = base64.b64encode(image_data)
                new_product = Product(
                    product_name=product_name,
                    product_description='Yummy Chocolate',
                    product_img=encoded_image,
                    product_price=product_price,
                    seller_id=1,
                    business_id=1
                )
                db.session.add(new_product)
                db.session.commit()
    except Exception as e:
        print(f'Error: {e}')

def seed_inventory():
    try:
        products = Product.query.all()
        for product in products:
            for attribute in product.product_attributes:
                inventory = Inventory(
                    product_id=product.id,
                    product_quantity=100,
                    attribute_id=attribute.id,
                )
                product.product_inventory.append(inventory)
        db.session.commit()
    except Exception as e:
        print(f'Error: {e}')

def seed_attributes():
    chocolate_types = {
    "milk chocolate": [4,5,6],
    "dark chocolate": [1,3], 
    "white chocolate": [2]
    }
    for chocolate_type, product_ids in chocolate_types.items():
        for product_id in product_ids:
            print(f'for product {product_id}')
            product = Product.query.get(product_id)
            print(chocolate_type)
            new_attribute = Attribute(
                product_id = product_id,
                attribute_name=[chocolate_type],
                )
            print(product)
            print(new_attribute)
            product.product_attributes.append(new_attribute)
        db.session.commit()

def seed_address():
    print('seed addresses')
    try:
        buyer = Buyer.query.first()

        new_address = Address(
            buyer_id = buyer.id,
            address_line_one="123 Main St",
            address_line_two="Apt 4B",
            city="Anytown",
            state="CA",
            postal_code=95054,
            address_type="shipping"
        )
        buyer.addresses.append(new_address)

        db.session.commit()

        print("Address seeded successfully!")
    except Exception as e:
        print(f"Error seeding address: {e}")
        db.session.rollback()

def seed_order_status():
    print('seeding order status')
    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']

    try:
        for status in statuses:
            new_status = Order_Status(name=status)
            db.session.add(new_status)
        db.session.commit()
        print("Order statuses seeded successfully!")
    except Exception as e:
        print(f"Error seeding order statuses: {e}")
        db.session.rollback()

def seed_order():
    print('seeding order')
    try:
        buyer = Buyer.query.first()
        order = Order(buyer=buyer)
        order.total_price = 21.00
        db.session.add(order)
        db.session.flush()
        product = Product.query.first()
        order_item = Order_Item(order_id=order.id, product=product, quantity=3, price=product.product_price)
        db.session.add(order_item)
        db.session.flush()
        order.order_items.append(order_item)
        order.status_id = 1
        db.session.commit()
        sale_history = SaleHistory(order_id=order.id, business_id=1)
        db.session.add(sale_history)
        db.session.commit()
        print("Order seeded successfully!")
    except Exception as e:
        print(f"Error seeding order: {e}")
        db.session.rollback()

def seed_reviews():
    print('seeding reviews')
    try:
        products = Product.query.limit(3).all()
        buyer = Buyer.query.first()

        for product in products:
            review_text = f"This is a review for {product.product_name}."
            rating = random.randint(1, 5)

            new_review = Review(
                product_id=product.id,
                buyer_id=buyer.id,
                review=review_text,
                rating=rating
            )

            db.session.add(new_review)

        db.session.commit()

        print("Reviews seeded successfully!")
    except Exception as e:
        print(f"Error seeding reviews: {e}")
        db.session.rollback()

def seed_messages():
    print('seeding messages')
    try:
        buyer = Buyer.query.first()
        seller = Seller.query.first()

        message1 = Message(content="Hi, I'm interested in your product!", attachments=None)
        message2 = Message(content="Great! What would you like to know?", attachments=None)
        message3 = Message(content="Can you tell me more about it", attachments=None)

        message1.recipients.append(
        MessageRecipient(user_type="buyer", buyer_id=buyer.id)
        )
        message1.recipients.append(
        MessageRecipient(user_type="seller", seller_id=seller.id)
        )
        message2.recipients.append(
        MessageRecipient(user_type="seller", seller_id=seller.id)
        )
        message2.recipients.append(
        MessageRecipient(user_type="buyer", buyer_id=buyer.id)
        )
        message3.recipients.append(
        MessageRecipient(user_type="buyer", buyer_id=buyer.id)
        )
        message3.recipients.append(
        MessageRecipient(user_type="seller", seller_id=seller.id)
        )

        db.session.add_all([message1, message2, message3])
        db.session.commit()

        print("Message exchanges seeded successfully!")
    except Exception as e:
        print(f"Error seeding messages: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        seed_business_category()
        seed_product_category()
        seed_test_seller()
        seed_test_buyer()
        seed_business()
        seed_product()
        seed_attributes()
        seed_inventory()
        seed_order_status()
        seed_address()
        seed_messages()
        seed_reviews()
        seed_order()
        # pass