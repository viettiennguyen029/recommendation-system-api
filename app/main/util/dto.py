from flask_restx import Namespace, fields, marshal
import json


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(
            required=True, description='User email address'),
        'username': fields.String(
            required=True, description='User username'),
        'password': fields.String(
            required=True, description='User password'),
        'public_id': fields.String(
            description='User Identifier'),
        'phone_number': fields.String(
            required=True, description='User phone number'),
        'full_name': fields.String(
            required=True, description='User full name'),
        'gender': fields.String(
            required=True, description='User gender'),
        'date_of_birth': fields.String(
            required=True, description='User date of birth'),
        'avatar': fields.String(
            required=True, description='User avatar'),
        'admin': fields.String(
            description='Is user an administrator?')
    })


class AuthDto:
    api = Namespace('auth', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(
            required=True, description='The username'),
        'password': fields.String(
            required=True, description='The user password ')
    })


class ProductCategoryDto:
    api = Namespace('product_category',
                    description='Product category related operations')
    product_category = api.model('product_category', {
        'name': fields.String(
            required=True, description='Product category name'),
        'description': fields.String(
            description='Product category description')
    })


class ManufacturerDto:
    api = Namespace(
        'manufacturer', description='Manufacturer related operations')
    manufacturer = api.model('manufacturer', {
        'name': fields.String(
          required=True, description='Manufacturer name'),
        'description': fields.String(
          description='Manufacturer description'),
        'address': fields.String(
          required=True, description='Manufacturer address'),
        'email': fields.String(
          required=True, description='Manufacturer email'),
        'phone_number': fields.String(
          required=True, description='Manufacturer phone number'),
        'fax_number': fields.String(
          required=True, description='Manufacturer fax number')
    })


class SupplierDto:
    api = Namespace(
        'supplier', description='Suplier related operations')
    supplier = api.model('supplier', {
        'name': fields.String(
          required=True, description='Suplier name'),
        'description': fields.String(
          description='Suplier description'),
        'address': fields.String(
          required=True, description='Suplier address'),
        'email': fields.String(
          required=True, description='Suplier email'),
        'phone_number': fields.String(
          required=True, description='Suplier phone number'),
        'fax_number': fields.String(
          required=True, description='Suplier fax number')
    })


class ProductDto:
    api = Namespace('product', description='Product related operations')
    product = api.model('product', {
        'name': fields.String(
            required=True, description='Product name'),
        'description': fields.String(
            description='Product description'),
        'product_image': fields.String(
            required=True, description='Product image'),
        'product_category_id': fields.String(
            description='Product Category ID'),
        'unit_id': fields.String(
            description='Unit ID'),
        'supplier_id': fields.String(
            description='Supplier ID'),
        'manufacturer_id': fields.String(
            description='Manufacturer ID')
    })


class UnitDto:
    api = Namespace('unit', description='Unit related operations')
    unit = api.model('unit', {
        'name': fields.String(
            required=True, description='Unit name'),
        'description': fields.String(
            description='Unit description')
    })


class ProductPriceHistoryDto:
    api = Namespace(
        'product_price_history', description='Product price history related operations')
    product_price_history = api.model('product_price_history', {
        'effective_date': fields.String(
            required=True, description='Product price updated date'),
        'original_price': fields.String(
            required=True, description='Product original price'),
        'sale_price': fields.String(
            required=True, description='Product sale price'),
        'product_id': fields.String(
            required=True, description='Product ID')
    })


class ProducDataDto:
    api = Namespace(
        'product_data', description='Product price history and product information')
    product_data = api.model('product_data', {
        'name': fields.String(
            required=True, description='Product name'),
        'description': fields.String(
            description='Product description'),
        'product_image': fields.String(
            required=True, description='Product image'),
        'product_category_id': fields.String(
            description='Product Category ID'),
        'unit': fields.String(allow_null=False),
        'supplier_id': fields.String(
            description='Supplier ID'),
        'manufacturer_id': fields.String(
            description='Manufacturer ID'),
        'original_price': fields.String(
            required=True, description='Product original price'),
        'sale_price': fields.String(
            required=True, description='Product sale price'),
        'effective_date': fields.String(
            required=True, description='Product price updated date')
    })


class RecommendedListDto:
    api = Namespace(
        'recommended_list', description='Recommended list related operations')
    recommended_list = api.model('recommended_list', {
        'title': fields.String(
            required=True, description='Recommended list name'),
        'description': fields.String(
            description='Recommended list description'),
        'total_products': fields.String(
            required=True, description='Recommended list total products'),
        'time_span': fields.String(
            required=True, description='Recommended list time span'),
    })


class RecommendedListDataDto:
    api = Namespace(
        'recommended_list_data', description='Recommended list data related operations')
    recommended_list_data = api.model('recommended_list', {
        'title': fields.String(
            required=True, description='Recommended list name'),
        'description': fields.String(
            description='Recommended list description'),
        'total_products': fields.String(
            required=True, description='Recommended list total products'),
        'time_span': fields.String(
            required=True, description='Recommended list time span'),
        'recommended_list_items': fields.String(
            required=True, description='Recommended list items'),
    })


class RecommendedListItemDto:
    api = Namespace(
        'recommended_list_item', description='Recommended item related operations')
    recommended_list_item = api.model('recommended_list_item', {
        'quantity': fields.String(
            required=True, description='Recommended quantity'),
        'min_quantity': fields.String(
            required=True, description='Recommended min quantity'),
        'max_quantity': fields.String(
            required=True, description='Recommended max quantity'),
        'revenue': fields.String(
            required=True, description='Recommended revenue'),
        'min_revenue': fields.String(
            required=True, description='Recommended min revenue'),
        'max_revenue': fields.String(
            required=True, description='Recommended max revenue'),
        'accuracy': fields.String(
            required=True, description='Recommended accuracy'),
        'priority': fields.String(
            required=True, description='Recommended priority'),
        'original_price': fields.String(
            required=True, description="Recommended product's original price"),
        'sale_price': fields.String(
            required=True, description="Recommended product's sale price"),
        'profit_rate': fields.String(
            required=True, description="Recommended product's profit rate"),
        'inware_amount': fields.String(
            required=True, description="Recommended product's profit rate"),
        'min_inware_amount': fields.String(
            required=True, description="Recommended product's profit rate"),
        'max_inware_amount': fields.String(
            required=True, description="Recommended product's profit rate"),
        'product_id': fields.String(
            required=True, description='Recommended product ID'),
        'recommended_list_id': fields.String(
            required=True, description='Recommended list ID'),
    })


class OtherFeeDto:
    api = Namespace(
        'other_fees', description='Other fee related operations')
    other_fee = api.model('other_fee', {
        'started_on': fields.String(
          required=True, description='Other fee started on'),
        'ended_on': fields.String(
          required=True, description='Other fee ended on'),
        'amount': fields.String(
          required=True, description='Other fee amount')
    })


# class transaction_listDto:
#     api = Namespace(
#         'transaction_list', description='transaction_list related operations')
#     transaction_list = api.model('transaction_list', {
#         'customer_id': fields.String(
#           required=True, description='transaction_list customer id'),
#         'total_amount': fields.String(
#           required=True, description='transaction_list total amount'),
#         'transaction_list_date': fields.String(
#           required=True, description='transaction_list date')
#     })


class TransactionListDataDto:
    api = Namespace(
        'transaction_list_data', description='transaction_list related operations')
    transaction_list_data = api.model('transaction_list', {
        'customer_id': fields.String(
          required=True, description='transaction_list customer id'),
        'total_amount': fields.String(
          description='transaction_list total amount'),
        'transaction_list_date': fields.String(
          required=True, description='transaction_list date'),
        'transaction_list_items': fields.String(
          required=True, description='transaction_list items')
    })


# class TransactionDto:
#     api = Namespace(
#         'transaction', description='Transaction')
#     transaction = api.model('transaction', {
#         'product_id': fields.String(
#           required=True, description='Product id'),
#         'transaction_list_id': fields.String(
#           required=True, description='transaction_list id'),
#         'quantity': fields.String(
#           required=True, description='Product quantity')
#     })


class InwareListDto:
    api = Namespace(
        'inware_list', description='Inware list related operations')
    inware_list = api.model('inware_list', {
        'name': fields.String(
          required=True, description='Inware_list name'),
        'description': fields.String(
          description='Inware_list description'),
        'record_date': fields.String(
          description='Inware_list record date')
    })


class InwareListItemDto:
    api = Namespace(
        'inware_list_item', description='Inware item related operations')
    inware_list_item = api.model('inware_list_item', {
        'inware_list_id': fields.String(
          required=True, description='Inware_list id'),
        'product_id': fields.String(
          description='Product id'),
        'price': fields.String(
          description='Product Inware price'),
        'quantity': fields.String(
          description='Product Inware quantity'),
    })


class InwareDataDto:
    api = Namespace(
        'inware_data', description='Inware list related operations')
    inware_data = api.model('inware_data', {
        'name': fields.String(
          required=True, description='Inware_list name'),
        'notes': fields.String(
          description='Inware list notes'),
        'record_date': fields.String(
          description='Inware_list record date')
    })


class SettingsDto:
    api = Namespace(
        'settings', description='Personal settings')
    settings = api.model('settings', {
        'user_public_id': fields.String(),
        'full_name': fields.String(),
        'email': fields.String(),
        'phone_number': fields.String(),
        'fax_number': fields.String(),
        'address': fields.String(),
        'billing_address': fields.String(),
    })


class InventoryDto:
    api = Namespace(
        'inventory', description='Product inventory')
    inventory = api.model('inventory', {
        'quantity': fields.String(required=True),
        'time_span': fields.String(required=True),
        'product_id': fields.String(required=True),
    })
