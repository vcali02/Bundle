from app import app
from models import db, Seller, Business, BusinessCategory, Product, Attribute, ProductCategory, Inventory, Review, SaleHistory, Order, Order_Item, Order_Status, ShopifyInfo, Payment, Message, OrderHistory, Address, Buyer 
import pickle
from flask_bcrypt import Bcrypt
import random
import ipdb
import json
import os

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

    seller = [{'seller_name': 'Evan Roberts', 'seller_email': 'evanroberts@email.com', 'seller_username': 'EvanRoberts', 'seller_password': 'password', 'seller_img': image_data}]

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

def seed_business():
    try:
        image_path = os.path.join("images", "illustration.png")
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        image_path_2 = os.path.join('images', 'chocowoco.png')
        with open(image_path_2, 'rb') as image_file_2:
            image_data_2 = image_file_2.read()

        business = [
            {
                "bis_category_id":1,
                'seller_id':1,
                'business_name':'Chocotonic',
                'business_img': image_data,
                'business_banner_img': image_data_2,
                'business_desc': 'we sell chocolate :)'
            }
        ]

        for business_data in business:
            business_obj = Business(
                bis_category_id=business_data['bis_category_id'],
                seller_id=business_data['seller_id'],
                business_name=business_data['business_name'],
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
                new_product = Product(
                    product_name=product_name,
                    product_description='Yummy Chocolate',
                    product_img=image_data,
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
    "milk chocolate": [5, 6, 7],
    "dark chocolate": [1, 4], 
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

if __name__ == '__main__':
    with app.app_context():
        # seed_business_category()
        # seed_product_category()
        # seed_test_seller()
        # seed_business()
        # seed_product()
        # seed_inventory()
        # seed_attributes()
        pass