import datetime
import math
import base64
import os

from sqlalchemy import desc, asc
from app.main import db

from app.main.model.product import Product
from app.main.model.unit import Unit
from app.main.model.product_category import ProductCategory
from app.main.model.manufacturer import Manufacturer
from app.main.model.supplier import Supplier
from app.main.model.product_price_history import ProductPriceHistory

from werkzeug.utils import secure_filename


def get_product_data(id):
    errors = {}
    product = Product.query.filter_by(id=id).first()

    if not product:
        errors['id'] = ["Product ID does not exist"]
        response_object = {
            'status': 'FAILED',
            'message': 'Can not get product data',
            'errors': errors
        }
        return response_object, 200

    unit = Unit.query.filter_by(
        id=product.unit_id).first()

    product_category = ProductCategory.query.filter_by(
        id=product.product_category_id).first()

    manufacturer = Manufacturer.query.filter_by(
        id=product.manufacturer_id).first()

    supplier = Supplier.query.filter_by(
        id=product.supplier_id).first()

    product_price_history = ProductPriceHistory.query.filter_by(
        product_id=id)

    product_prices = {}

    for product_price in product_price_history:
        product_price_key = str(product_price.id)
        product_prices[product_price_key] = {}
        product_prices[product_price_key]['original_price'] = str(
            product_price.original_price)
        product_prices[product_price_key]['sale_price'] = str(
            product_price.sale_price)
        product_prices[product_price_key]['effective_date'] = str(
            product_price.effective_date).split(' ')[0]
        product_prices[product_price_key]['created_on'] = str(
            product_price.created_on)
        product_prices[product_price_key]['updated_on'] = str(
            product_price.updated_on)

    product_data = {}
    product_data['id'] = str(product.id)
    product_data['name'] = product.name
    product_data['description'] = product.description
    # product_data['product_image_base64'] = decode_base64(
    #     product.product_image)
    product_data['product_image'] = product.product_image
    product_data['product_category'] = {}
    product_data['product_category']['id'] = str(product_category.id)
    product_data['product_category']['name'] = product_category.name
    product_data['product_category']['value'] = str(product_category.id)
    product_data['product_category']['label'] = product_category.name
    product_data['unit'] = {}
    product_data['unit']['id'] = str(unit.id)
    product_data['unit']['name'] = unit.name
    product_data['unit']['value'] = str(unit.id)
    product_data['unit']['label'] = unit.name
    product_data['manufacturer'] = {}
    product_data['manufacturer']['id'] = str(manufacturer.id)
    product_data['manufacturer']['name'] = manufacturer.name
    product_data['manufacturer']['value'] = str(manufacturer.id)
    product_data['manufacturer']['label'] = manufacturer.name
    product_data['supplier'] = {}
    product_data['supplier']['id'] = str(supplier.id)
    product_data['supplier']['name'] = supplier.name
    product_data['supplier']['value'] = str(supplier.id)
    product_data['supplier']['label'] = supplier.name
    product_data['created_on'] = str(product.created_on)
    product_data['updated_on'] = str(product.updated_on)
    product_data['product_price_history'] = product_prices

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting product data',
        'data': product_data
    }
    return response_object, 200


def save_product_data(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = ['Product name must not be null!']

    # if data['product_image'] == "":
    #     errors['product_image'] = ['Product image must not be null!']

    if data['product_category']['value'] == "":
        errors['product_category']['value'] = [
            'Product category must not be null!']

    if data['unit']['value'] == "":
        errors['unit']['value'] = ['Product unit must not be null!']

    if data['manufacturer']['value'] == "":
        errors['manufacturer']['value'] = [
            'Product manufacturer must not be null!']

    if data['supplier']['value'] == "":
        errors['supplier']['value'] = ['Product supplier must not be null!']

    '''len_product_price = len(data['product_price_history'])
    if len_product_price == 0:
        errors['product_price_history'] = ['Product price can not be null']'''

    # Check if foregin key is valid or not
    unit = Unit.query.filter_by(id=data['unit']['value']).first()
    if not unit:
        errors['unit']['value'] = ["Unit ID does not exist!"]

    product_category = ProductCategory.query.filter_by(
        id=data['product_category']['value']).first()
    if not product_category:
        errors['product_category']['value'] = [
            "Product category ID does not exist!"]

    manufacturer = Manufacturer.query.filter_by(
        id=data['manufacturer']['value']).first()
    if not manufacturer:
        errors['manufacturer']['value'] = ["Manufacturer ID does not exist!"]

    supplier = Supplier.query.filter_by(
        id=data['supplier']['value']).first()
    if not supplier:
        errors['supplier']['value'] = ["Supplier ID does not exist!"]

    effective_dates = []
    for price in data['product_price_history']:
        # Check duplicates value when a product can not have
        # 2 the same price effective date
        if price['effective_date'] in effective_dates:
            response_object = {
                'status': 'FAILED',
                'message': 'Effective date is duplicated!',
                'errors': {}
            }
            return response_object, 200

        effective_dates.append(price['effective_date'])

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new product data!',
            'errors': errors
        }
        return response_object, 200
    else:
        product = Product.query.filter_by(name=data['name']).first()
        if product:
            errors['name'] = 'Product name is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new product!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_product = Product(
                name=data['name'],
                description=data['description'],
                product_image=data['product_image'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow(),
                product_category_id=data['product_category']['value'],
                unit_id=data['unit']['value'],
                manufacturer_id=data['manufacturer']['value'],
                supplier_id=data['supplier']['value']
            )
            db.session.add(new_product)
            db.session.commit()

            product_prices = {}
            for price in data['product_price_history']:
                new_price_history = ProductPriceHistory(
                    original_price=price['original_price'],
                    sale_price=price['sale_price'],
                    effective_date=datetime.datetime.strptime(
                        price['effective_date'], '%Y-%m-%d'),
                    product_id=new_product.id,
                    created_on=datetime.datetime.utcnow(),
                    updated_on=datetime.datetime.utcnow()
                )
                db.session.add(new_price_history)
                db.session.commit()

                product_price_key = str(new_price_history.id)
                product_prices[product_price_key] = {}
                product_prices[product_price_key]['original_price'] = str(
                    new_price_history.original_price)
                product_prices[product_price_key]['sale_price'] = str(
                    new_price_history.sale_price)
                product_prices[product_price_key]['effective_date'] = str(
                    new_price_history.effective_date)
                product_prices[product_price_key]['created_on'] = str(
                    new_price_history.created_on)
                product_prices[product_price_key]['updated_on'] = str(
                    new_price_history.updated_on)

            unit = Unit.query.filter_by(
                id=new_product.unit_id).first()
            manufacturer = Manufacturer.query.filter_by(
                id=new_product.manufacturer_id).first()
            supplier = Supplier.query.filter_by(
                id=new_product.supplier_id).first()
            product_category = ProductCategory.query.filter_by(
                id=new_product.product_category_id).first()

            output = {}
            output['id'] = str(new_product.id)
            output['name'] = new_product.name
            output['description'] = new_product.description
            output['product_image'] = new_product.product_image
            output['unit'] = {}
            output['unit']['value'] = str(unit.id)
            output['unit']['label'] = unit.name
            output['manufacturer'] = {}
            output['manufacturer']['value'] = str(manufacturer.id)
            output['manufacturer']['label'] = manufacturer.name
            output['supplier'] = {}
            output['supplier']['value'] = str(supplier.id)
            output['supplier']['label'] = supplier.name
            output['product_category'] = {}
            output['product_category']['value'] = str(product_category.id)
            output['product_category']['label'] = product_category.name
            output['created_on'] = str(new_product.created_on)
            output['updated_on'] = str(new_product.updated_on)
            output['product_price_hisory'] = product_prices

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new product data is created successfully!',
                'data': output
            }
            return response_object, 201


def generate_product_image_filename(product_name):
    ts = datetime.datetime.now().timestamp()
    product_image_name = str(ts).split(".", 1)[0] + ".png"
    return product_image_name


def upload_image_with_base64(base64_string, product_name):
    if base64_string == '':
        filename = "no_image.png"
    else:
        # Convert base64_string to image file
        imgdata = base64.b64decode(base64_string)

        # Saving image data to public folder
        PUBLIC_FOLDER = 'static'
        # filename = generate_product_image_filename(product_name)
        filename = product_name + ".png"
        with open(os.path.join(PUBLIC_FOLDER, filename), 'wb') as f:
            f.write(imgdata)
    return filename


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

    if image and allowed_image_type(image.filename):
        file_name = secure_filename(image.filename)
        # Modify the file name before saving to db
        new_file_name = generate_product_image_filename(file_name)
        UPLOAD_FOLDER = 'static'
        image.save(os.path.join(UPLOAD_FOLDER, new_file_name))
        response_object = {
            'status': 'SUCCESS',
            'message': 'Sucessfully saved product image!',
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


def handling_image_response(product_image):
    if product_image == "no_image.png":
        return product_image
    else:
        base64_string_header = "data:image/png;base64,"
        product_image_encoded = base64_string_header + data['product_image']
        return product_image_encoded


def decode_base64(product_image):
    # Open public folder
    PUBLIC_FOLDER = 'static'
    base64_string_header = 'data:image/png;base64,'
    with open(os.path.join(PUBLIC_FOLDER, product_image), 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_image = base64_string_header + encoded_string.decode("utf-8")
    return encoded_image


def url_product_image(product_image):
    public_folder_url = 'http://localhost:5000/static/'
    product_image_url = public_folder_url + product_image
    return product_image_url


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
    if "page" in args:
        current_page = int(args['page'])
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
                # product_data['product_image_base64'] = decode_base64(
                #     product.product_image)
                product_data['product_image'] = url_product_image(
                    product.product_image)
                product_data['product_category'] = {}
                product_data['product_category']['id'] = str(
                    product_category.id)
                product_data['product_category']['name'] = product_category.name
                product_data['product_category']['value'] = str(
                    product_category.id)
                product_data['product_category']['label'] = product_category.name
                product_data['unit'] = {}
                product_data['unit']['id'] = str(unit.id)
                product_data['unit']['name'] = unit.name
                product_data['unit']['value'] = str(unit.id)
                product_data['unit']['label'] = unit.name
                product_data['manufacturer'] = {}
                product_data['manufacturer']['id'] = str(manufacturer.id)
                product_data['manufacturer']['name'] = manufacturer.name
                product_data['manufacturer']['value'] = str(manufacturer.id)
                product_data['manufacturer']['label'] = manufacturer.name
                product_data['supplier'] = {}
                product_data['supplier']['id'] = str(supplier.id)
                product_data['supplier']['name'] = supplier.name
                product_data['supplier']['value'] = str(supplier.id)
                product_data['supplier']['label'] = supplier.name
                product_data['created_on'] = str(product.created_on)
                product_data['updated_on'] = str(product.updated_on)

                output.append(product_data)
        else:
            product_data = {}
            product_data['id'] = str(product.id)
            product_data['name'] = product.name
            product_data['description'] = product.description
            # product_data['product_image_base64'] = decode_base64(
            #     product.product_image)
            product_data['product_image'] = url_product_image(
                product.product_image)
            product_data['product_category'] = {}
            product_data['product_category']['id'] = str(product_category.id)
            product_data['product_category']['name'] = product_category.name
            product_data['product_category']['value'] = str(
                product_category.id)
            product_data['product_category']['label'] = product_category.name
            product_data['unit'] = {}
            product_data['unit']['id'] = str(unit.id)
            product_data['unit']['name'] = unit.name
            product_data['unit']['value'] = str(unit.id)
            product_data['unit']['label'] = unit.name
            product_data['manufacturer'] = {}
            product_data['manufacturer']['id'] = str(manufacturer.id)
            product_data['manufacturer']['name'] = manufacturer.name
            product_data['manufacturer']['value'] = str(manufacturer.id)
            product_data['manufacturer']['label'] = manufacturer.name
            product_data['supplier'] = {}
            product_data['supplier']['id'] = str(supplier.id)
            product_data['supplier']['name'] = supplier.name
            product_data['supplier']['value'] = str(supplier.id)
            product_data['supplier']['label'] = supplier.name
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


def delete_product_data(id):
    errors = {}
    # Delete product price history
    product_price_history = ProductPriceHistory.query.filter_by(
        product_id=id)
    product = Product.query.filter_by(id=id).first()

    if ((not product_price_history) or (not product)):
        errors = ['Product ID is not valid']
        respone_object = {
            'status': 'ERROR',
            'message': 'Can not delete product data!',
            'error:': errors
        }
        return respone_object, 200
    else:
        for price_history in product_price_history:
            db.session.delete(price_history)
            db.session.commit()

        db.session.delete(product)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted product data!'
        }
        return response_object, 200


def update_product_data(id, data):
    product = Product.query.filter_by(id=id).first()
    product_price_hisory = ProductPriceHistory.query.filter_by(product_id=id)
    is_updated = False
    errors = {}

    if not product:
        errors['id'] = ["Product ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': 'Cannot update product data!',
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == "":
            errors['name'] = ['Product name must not be null!']

        if data['product_category']['value'] == "":
            errors['product_category']['value'] = [
                'Product category id must not be null!']

        if data['unit']['value'] == "":
            errors['unit']['value'] = ['Product unit id must not be null!']

        if data['manufacturer']['value'] == "":
            errors['manufacturer']['value'] = [
                'Product manufacturer id must not be null!']

        if data['supplier']['value'] == "":
            errors['supplier']['value'] = [
                'Product supplier id must not be null!']

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update product data!",
                'errors': errors
            }
            return response_object, 200
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

            if data['product_category']['value'] != str(product.product_category_id):
                # Check if foregin key is valid or not
                product_category = ProductCategory.query.filter_by(
                    id=data['product_category']['value']).first()
                if product_category:
                    is_updated = True
                    product.product_category_id = data['product_category']['value']
                else:
                    errors['product_category']['value'] = [
                        "Product category ID does not exist!"]

            if data['unit']['value'] != str(product.unit_id):
                # Check if foregin key is valid or not
                unit = Unit.query.filter_by(id=data['unit']['value']).first()
                if unit:
                    is_updated = True
                    product.unit_id = data['unit']['value']
                else:
                    errors['unit']['value'] = ["Unit ID does not exist!"]

            if data['manufacturer']['value'] != str(product.manufacturer_id):
                # Check if foregin key is valid or not
                manufacturer = Manufacturer.query.filter_by(
                    id=data['manufacturer']['value']).first()
                if manufacturer:
                    is_updated = True
                    product.manufacturer_id = data['manufacturer']['value']
                else:
                    errors['manufacturer']['value'] = [
                        "Manufacturer ID does not exist!"]

            if data['supplier']['value'] != str(product.supplier_id):
                # Check if foregin key is valid or not
                supplier = Supplier.query.filter_by(
                    id=data['supplier']['value']).first()
                if supplier:
                    is_updated = True
                    product.supplier_id = data['supplier']['value']
                else:
                    errors['supplier']['value'] = [
                        "Supplier ID does not exist!"]

            # For loop to update product price history
            product_prices = {}
            db_prices = []
            request_prices = []
            for db_price in product_price_hisory:
                db_prices.append(db_price.effective_date)

            for price in data['product_price_history']:
                # Compare effective_date in request with others in db
                eff_date = datetime.datetime.strptime(
                    price['effective_date'], '%Y-%m-%d')

                request_prices.append(eff_date)
                # If has, compare sale price and original_price
                if (eff_date in db_prices):
                    price_history = ProductPriceHistory.query.filter_by(
                        product_id=id, effective_date=eff_date).first()
                    org_price = int(price['original_price'])
                    s_price = int(price['sale_price'])

                    if org_price != price_history.original_price:
                        price_history.original_price = org_price
                        is_updated = True
                        # print("Original price changed")

                    if s_price != price_history.sale_price:
                        price_history.sale_price = s_price
                        is_updated = True
                        # print("Sale price changed")
                else:
                    # If does not aldready exist, add new
                    is_updated = True
                    new_price_history = ProductPriceHistory(
                        original_price=price['original_price'],
                        sale_price=price['sale_price'],
                        effective_date=eff_date,
                        product_id=id,
                        created_on=datetime.datetime.utcnow(),
                        updated_on=datetime.datetime.utcnow()
                    )
                    db.session.add(new_price_history)
                    # db.session.commit()

            for db_price in product_price_hisory:
                # Check if effective_date is not exist in request, then delete
                if not (db_price.effective_date in request_prices):
                    db.session.delete(db_price)
                    # db.session.commit()
                    is_updated = True

            if is_updated is True:
                product.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            db_prices.clear()
            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated product data!",
            }
            return response_object, 200


def get_all_product_data():
    all_products = Product.query.all()
    output = []

    for product in all_products:
        product_category = ProductCategory.query.filter_by(
            id=product.product_category_id).first()
        unit = Unit.query.filter_by(
            id=product.unit_id).first()
        manufacturer = Manufacturer.query.filter_by(
            id=product.manufacturer_id).first()
        supplier = Supplier.query.filter_by(
            id=product.supplier_id).first()

        product_data = {}
        product_data['id'] = str(product.id)
        product_data['name'] = product.name
        product_data['description'] = product.description
        # product_data['product_image_base64'] = decode_base64(
        #         product.product_image)
        # product_data['product_image_url'] = url_product_image(
        #         product.product_image)
        product_data['product_image'] = product.product_image
        product_data['category_name'] = product_category.name
        product_data['unit_name'] = unit.name
        product_data['supplier_name'] = supplier.name
        product_data['manufacturer_name'] = manufacturer.name
        # product_data['product_category'] = {}
        # product_data['product_category']['id'] = str(product_category.id)
        # product_data['product_category']['name'] = product_category.name
        # product_data['product_category']['value'] = str(
        #     product_category.id)
        # product_data['product_category']['label'] = product_category.name
        # product_data['unit'] = {}
        # product_data['unit']['id'] = str(unit.id)
        # product_data['unit']['name'] = unit.name
        # product_data['unit']['value'] = str(unit.id)
        # product_data['unit']['label'] = unit.name
        # product_data['manufacturer'] = {}
        # product_data['manufacturer']['id'] = str(manufacturer.id)
        # product_data['manufacturer']['name'] = manufacturer.name
        # product_data['manufacturer']['value'] = str(manufacturer.id)
        # product_data['manufacturer']['label'] = manufacturer.name
        # product_data['supplier'] = {}
        # product_data['supplier']['id'] = str(supplier.id)
        # product_data['supplier']['name'] = supplier.name
        # product_data['supplier']['value'] = str(supplier.id)
        # product_data['supplier']['label'] = supplier.name
        product_data['created_on'] = str(product.created_on)
        product_data['updated_on'] = str(product.updated_on)

        output.append(product_data)

    data = {}
    data['product'] = output

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all products',
        'data': data
    }
    return response_object, 200
