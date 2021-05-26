import datetime
import time
import uuid
import flask
import io
import csv
import os
import math
import base64

from app.main import db
from app.main.model.product import Product
from app.main.model.unit import Unit
from app.main.model.product_category import ProductCategory
from app.main.model.manufacturer import Manufacturer
from app.main.model.supplier import Supplier

from flask import redirect, url_for, Response
from sqlalchemy import desc, asc
from io import TextIOWrapper
from werkzeug.utils import secure_filename


def save_product(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = ['Product name must not be null!']

    if data['product_image'] == "":
        errors['product_image'] = ['Product image must not be null!']

    if data['product_category_id'] == "":
        errors['product_category_id'] = [
            'Product category id must not be null!']

    if data['unit_id'] == "":
        errors['unit_id'] = ['Product unit id must not be null!']

    if data['manufacturer_id'] == "":
        errors['manufacturer_id'] = [
            'Product manufacturer id must not be null!']

    if data['supplier_id'] == "":
        errors['supplier_id'] = ['Product supplier id must not be null!']

    # Check if foregin key is valid or not
    unit = Unit.query.filter_by(id=data['unit_id']).first()
    if not unit:
        errors['unit_id'] = ["Unit ID does not exist!"]

    product_category = ProductCategory.query.filter_by(
        id=data['product_category_id']).first()
    if not product_category:
        errors['product_category_id'] = ["Product category ID does not exist!"]

    manufacturer = Manufacturer.query.filter_by(
        id=data['manufacturer_id']).first()
    if not manufacturer:
        errors['manufacturer_id'] = ["Manufacturer ID does not exist!"]

    supplier = Supplier.query.filter_by(
        id=data['supplier_id']).first()
    if not supplier:
        errors['supplier_id'] = ["Supplier ID does not exist!"]

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new product!',
            'errors': errors
        }
        return response_object, 200
    else:
        product = Product.query.filter_by(name=data['name']).first()
        if product:
            errors['name'] = 'Product name is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a product!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_product = Product(
                name=data['name'],
                description=data['description'],
                product_image=upload_image_with_base64(data['product_image']),
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow(),
                product_category_id=data['product_category_id'],
                unit_id=data['unit_id'],
                manufacturer_id=data['manufacturer_id'],
                supplier_id=data['supplier_id']
            )
            save_changes(new_product)

            output = {}
            output['id'] = str(new_product.id)
            output['name'] = new_product.name
            output['description'] = new_product.description
            output['product_image'] = new_product.product_image
            output['unit_id'] = str(new_product.unit_id)
            output['product_category_id'] = str(
                new_product.product_category_id)
            output['manufacturer_id'] = str(new_product.manufacturer_id)
            output['supplier_id'] = str(new_product.supplier_id)
            output['created_on'] = str(new_product.created_on)
            output['updated_on'] = str(new_product.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new product is created successfully!',
                'data': output
            }
            return response_object, 201


def get_all_products_with_pagination(args):
    # Query Params
    page_size = 10
    current_page = 1
    next_page = False
    key_word = None
    sort_field = None
    sort_order = -1

    # Check query param value
    if "page_size" in args:
        page_size = int(args['page_size'])
    if "current_page" in args:
        current_page = int(args['current_page'])
    if "key_word" in args:
        key_word = args['key_word'].lower()
    if "sort_field" in args:
        sort_field = args['sort_field']
    if "sort_order" in args:
        sort_order = int(args['sort_order'])

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        products = Product.query.order_by(Product.created_on.desc())
    else:
        if sort_order == -1:
            products = Product.query.order_by(desc(sort_field))
        else:
            products = Product.query.order_by(asc(sort_field))

    products_on_page = products.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(products.count() / page_size)

    if math.ceil(products.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for product in products_on_page:
        product_category = ProductCategory.query.filter_by(
            id=product.product_category_id).first()
        unit = Unit.query.filter_by(
            id=product.unit_id).first()
        manufacturer = Manufacturer.query.filter_by(
            id=product.manufacturer_id).first()
        supplier = Supplier.query.filter_by(
            id=product.supplier_id).first()

        # Sort by keyword
        if (key_word is not None):
            if (key_word in product.name.lower()) or (
                    key_word in product.description.lower()) or (
                        key_word in product_category.name.lower()) or (
                            key_word in unit.name.lower()) or (
                                key_word in manufacturer.name.lower()) or (
                                    key_word in supplier.name.lower()):
                product_data = {}
                product_data['id'] = str(product.id)
                product_data['name'] = product.name
                product_data['description'] = product.description
                product_data['product_image'] = product.product_image
                product_data['product_category'] = {}
                product_data['product_category']['id'] = str(
                    product_category.id)
                product_data['product_category']['name'] = product_category.name
                product_data['unit'] = {}
                product_data['unit']['id'] = str(unit.id)
                product_data['unit']['name'] = unit.name
                product_data['manufacturer'] = {}
                product_data['manufacturer']['id'] = str(manufacturer.id)
                product_data['manufacturer']['name'] = manufacturer.name
                product_data['supplier'] = {}
                product_data['supplier']['id'] = str(supplier.id)
                product_data['supplier']['name'] = supplier.name
                product_data['created_on'] = str(product.created_on)
                product_data['updated_on'] = str(product.updated_on)

                output.append(product_data)
        else:
            product_data = {}
            product_data['id'] = str(product.id)
            product_data['name'] = product.name
            product_data['description'] = product.description
            product_data['product_image'] = product.product_image
            product_data['product_category'] = {}
            product_data['product_category']['id'] = str(product_category.id)
            product_data['product_category']['name'] = product_category.name
            product_data['unit'] = {}
            product_data['unit']['id'] = str(unit.id)
            product_data['unit']['name'] = unit.name
            product_data['manufacturer'] = {}
            product_data['manufacturer']['id'] = str(manufacturer.id)
            product_data['manufacturer']['name'] = manufacturer.name
            product_data['supplier'] = {}
            product_data['supplier']['id'] = str(supplier.id)
            product_data['supplier']['name'] = supplier.name
            product_data['created_on'] = str(product.created_on)
            product_data['updated_on'] = str(product.updated_on)

            output.append(product_data)

    data = {}
    data['products'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all products',
        'data': data
    }
    return response_object, 200


def update_product(id, data):
    product = Product.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not product:
        errors['id'] = ["Product ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update product's information!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == "":
            errors['name'] = ['Product name must not be null!']

        if data['product_image'] == "":
            errors['product_image'] = ['Product image must not be null!']

        if data['product_category_id'] == "":
            errors['product_category_id'] = [
                'Product category id must not be null!']

        if data['unit_id'] == "":
            errors['unit_id'] = ['Product unit id must not be null!']

        if data['manufacturer_id'] == "":
            errors['manufacturer_id'] = [
                'Product manufacturer id must not be null!']

        if data['supplier_id'] == "":
            errors['supplier_id'] = ['Product supplier id must not be null!']

        # Check if foregin key is valid or not
        unit = Unit.query.filter_by(id=data['unit_id']).first()
        if not unit:
            errors['unit_id'] = ["Unit ID does not exist!"]

        product_category = ProductCategory.query.filter_by(
            id=data['product_category_id']).first()
        if not product_category:
            errors['product_category_id'] = [
                "Product category ID does not exist!"]

        manufacturer = Manufacturer.query.filter_by(
            id=data['manufacturer_id']).first()
        if not manufacturer:
            errors['manufacturer_id'] = ["Manufacturer ID does not exist!"]

        supplier = Supplier.query.filter_by(
            id=data['supplier_id']).first()
        if not supplier:
            errors['supplier_id'] = ["Supplier ID does not exist!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update product's information!",
                'errors': errors
            }
            return response_object,  200
        else:
            if data['name'] != product.name:
                # Check if product name is existed or not
                updated_product = Product.query.filter_by(
                    name=data['name']).first()
                if updated_product:
                    errors['name'] = ["Product name is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update product's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    product.name = data['name']

            if data['description'] != product.description:
                is_updated = True
                product.description = data['description']

            if data['product_image'] != product.product_image:
                is_updated = True
                product.product_image = data['product_image']

            if data['product_category_id'] != str(product.product_category_id):
                is_updated = True
                product.product_category_id = data['product_category_id']

            if data['unit_id'] != str(product.unit_id):
                is_updated = True
                product.unit_id = data['unit_id']

            if data['manufacturer_id'] != str(product.manufacturer_id):
                is_updated = True
                product.manufacturer_id = data['manufacturer_id']

            if data['supplier_id'] != str(product.supplier_id):
                is_updated = True
                product.supplier_id = data['supplier_id']

            if is_updated is True:
                product.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            product_data = {}
            product_data['id'] = str(product.id)
            product_data['name'] = product.name
            product_data['description'] = product.description
            product_data['product_image'] = product.product_image
            product_data['product_category'] = {}
            product_data['product_category_id'] = str(product_category.id)
            product_data['product_category_name'] = product_category.name
            product_data['unit'] = {}
            product_data['unit_id'] = str(unit.id)
            product_data['unit_name'] = unit.name
            product_data['manufacturer'] = {}
            product_data['manufacturer_id'] = str(manufacturer.id)
            product_data['manufacturer_name'] = manufacturer.name
            product_data['supplier'] = {}
            product_data['supplier_id'] = str(supplier.id)
            product_data['supplier_name'] = supplier.name
            product_data['created_on'] = str(product.created_on)
            product_data['updated_on'] = str(product.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated product information!",
                'data': product_data
            }
            return response_object, 200


def get_all_products():
    products = Product.query.all()
    output = []

    for product in products:

        unit = Unit.query.filter_by(id=product.unit_id).first()

        product_category = ProductCategory.query.filter_by(
            id=product.product_category_id).first()

        manufacturer = Manufacturer.query.filter_by(
            id=product.manufacturer_id).first()

        supplier = Supplier.query.filter_by(
            id=product.supplier_id).first()

        product_data = {}
        product_data['id'] = str(product.id)
        product_data['name'] = product.name
        product_data['description'] = product.description
        product_data['product_image'] = product.product_image
        product_data['product_category'] = {}
        product_data['product_category']['id'] = str(product_category.id)
        product_data['product_category']['name'] = product_category.name
        product_data['unit'] = {}
        product_data['unit']['id'] = str(unit.id)
        product_data['unit']['name'] = unit.name
        product_data['manufacturer'] = {}
        product_data['manufacturer']['id'] = str(manufacturer.id)
        product_data['manufacturer']['name'] = manufacturer.name
        product_data['supplier'] = {}
        product_data['supplier']['id'] = str(supplier.id)
        product_data['supplier']['name'] = supplier.name
        product_data['created_on'] = str(product.created_on)
        product_data['updated_on'] = str(product.updated_on)

        output.append(product_data)

    data = {}
    data['products'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all products',
        'data': data
    }
    return respone_object, 200


def get_product(id):
    errors = {}
    product = Product.query.filter_by(id=id).first()

    if not product:
        errors['id'] = ["Product ID does not exist"]
        response_object = {
            'status': 'FAILED',
            'message': 'Can not get product information',
            'errors': errors
        }
        return response_object, 200

    unit = Unit.query.filter_by(id=product.unit_id).first()

    product_category = ProductCategory.query.filter_by(
        id=product.product_category_id).first()

    manufacturer = Manufacturer.query.filter_by(
        id=product.manufacturer_id).first()

    supplier = Supplier.query.filter_by(
        id=product.supplier_id).first()

    product_data = {}
    product_data['id'] = str(product.id)
    product_data['name'] = product.name
    product_data['description'] = product.description
    product_data['product_image'] = product.product_image
    product_data['product_category'] = {}
    product_data['product_category']['id'] = str(product_category.id)
    product_data['product_category']['name'] = product_category.name
    product_data['unit'] = {}
    product_data['unit']['id'] = str(unit.id)
    product_data['unit']['name'] = unit.name
    product_data['manufacturer'] = {}
    product_data['manufacturer']['id'] = str(manufacturer.id)
    product_data['manufacturer']['name'] = manufacturer.name
    product_data['supplier'] = {}
    product_data['supplier']['id'] = str(supplier.id)
    product_data['supplier']['name'] = supplier.name
    product_data['created_on'] = str(product.created_on)
    product_data['updated_on'] = str(product.updated_on)

    respone_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting information of product',
        'data': product_data
    }
    return respone_object, 200


def delete_product(id):
    errors = {}
    product = Product.query.filter_by(id=id).first()

    if not product:
        errors['id'] = ["Product ID does not exist!"]
        respone_object = {
            'status': 'FAILED',
            'message': 'Can not delete product!',
            'errors': errors
        }
        return respone_object, 200
    else:
        db.session.delete(product)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted product!'
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def download_csv():
    output = io.StringIO()
    writter = csv.writer(output)

    ''' First line '''
    head_line = ['id', 'name', 'description', 'price',
                 'product_category_id', 'unit_id', 'manufacturer_id']
    writter.writerow(head_line)

    products = Product.query.all()

    for product in products:
        row = [str(product.id), product.name, product.description, str(product.price), str(
            product.product_category_id), str(product.unit_id, str(product.manufacturer_id))]
        writter.writerow(row)

    output.seek(0)

    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=product_report.csv"})


def upload_csv(data):
    csv_file = TextIOWrapper(data, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        new_product = Product(
            name=row[1],
            description=row[2],
            price=row[3],
            public_id=str(uuid.uuid4()),
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow(),
            product_category_id=row[4],
            unit_id=row[5],
            manufacturer_id=row[6]
        )
        save_changes(new_product)

    respone_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully created a new product!',
    }
    return respone_object, 201


def upload_image(image):
    errors = {}
    # if user does not select file, browser also
    # submit an empty part without filename
    if image.filename == '':
        errors['file_name'] = ['File name must not be null!']
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to upload product image',
            'errors': errors
        }
        return response_object, 200

    # Check request content-length
    # if not allowed_image_size(content_length):
    #     errors['file_size'] = ['File size is not allowed']
    #     response_object = {
    #         'status': 'FAILED',
    #         'message': 'Failed to upload product image',
    #         'errors': errors
    #     }
    #     return response_object, 200

    if image and allowed_image_type(image.filename):
        file_name = secure_filename(image.filename)
        # Modify the file name before saving to db
        new_file_name = generate_product_imgae_filename(file_name)
        UPLOAD_FOLDER = 'static'
        image.save(os.path.join(UPLOAD_FOLDER, new_file_name))
        response_object = {
            'status': 'SUCCESS',
            'message': 'Sucessfully saved image!',
            'url': 'http://localhost:5000/static/'+new_file_name
        }
        return response_object, 201
    else:
        errors['file_name'] = ['File name is not allowed!']
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to upload product image',
            'errors':  errors
        }
        return response_object, 200


def allowed_image_type(filename):
    '''['png', 'jpg', 'jpeg', 'gif']'''
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image_size(content_length):
    '''5 MB size is allowed'''
    MAX_IMAGE_FILESIZE = 5 * 1024 * 1024
    if content_length <= MAX_IMAGE_FILESIZE:
        return True
    else:
        return False


def generate_product_imgae_filename(product_id):
    # image_type = filename.rsplit('.', 1)[1].lower()
    ts = round(time.time())
    product_image_name = str(ts) + ".png"
    return product_image_name


def upload_image_with_base64(base64_string, product_id):
    # Convert base64_string to image file
    imgdata = base64.b64decode(base64_string)

    # Saving image data to public folder
    UPLOAD_FOLDER = 'static'
    filename = generate_product_imgae_filename(product_id)
    with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
        f.write(imgdata)
    image_result = 'http://localhost:5000/static/'+filename
    return image_result
