from flask_restx import Api
from flask import Blueprint
from flask_cors import CORS

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.unit_controller import api as unit_ns
from .main.controller.product_category_controller\
    import api as product_category_ns
from .main.controller.manufacturer_controller import api as manufacturer_ns
from .main.controller.supplier_controller import api as supplier_ns
from .main.controller.product_controller import api as product_ns
from .main.controller.other_fee_controller import api as other_fee_ns
from .main.controller.recommended_list_data_controller \
    import api as recommended_list_data_ns
from .main.controller.product_price_history_controller\
    import api as product_price_history_ns
from .main.controller.product_data_controller import api as product_data_ns
from .main.controller.transaction_list_data_controller \
    import api as transaction_list_data_ns
from .main.controller.inware_list_controller import api as inware_list_ns
from .main.controller.inware_list_item_controller \
    import api as inware_list_item_ns
from .main.controller.inware_data_controller import api as inware_list_data_ns
from .main.controller.inventory_controller import api as inventory_ns
from .main.controller.settings_controller import api as settings_ns


blueprint = Blueprint('api', __name__)
CORS(blueprint)

api = Api(blueprint,
          title='Recommendation System API',
          version='1.0',
          description='The official API for the recommendation system'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(unit_ns, path='/unit')
api.add_namespace(product_category_ns, path='/product-category')
api.add_namespace(manufacturer_ns, path='/manufacturer')
api.add_namespace(supplier_ns, path='/supplier')
api.add_namespace(product_ns, path='/product')
api.add_namespace(product_price_history_ns, path='/product-price-history')
api.add_namespace(other_fee_ns, path='/others-fee')
api.add_namespace(recommended_list_data_ns, path='/recommended-list-data')
api.add_namespace(product_data_ns, path='/product-data')
api.add_namespace(transaction_list_data_ns, path='/transaction-list-data')
api.add_namespace(inware_list_data_ns, path='/inware-list-data')
api.add_namespace(inware_list_item_ns, path='/inware-item')
api.add_namespace(inware_list_ns, path='/inware-list')
api.add_namespace(inventory_ns, path='/inventory')
api.add_namespace(settings_ns, path='/settings')
