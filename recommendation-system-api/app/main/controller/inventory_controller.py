from flask import request
from flask_restx import Resource

from ..util.dto import InventoryDto
from ..service.inventory_service import get_all_inventory, get_by_id_inventory


api = InventoryDto.api


@api.route('/')
class InventoryList(Resource):
    @api.doc('List all inventory list')
    def get(self):
        """List all inventory"""
        return get_all_inventory()


@api.route('/<id>')
class Inventory(Resource):
    def get(self, id):
        return get_by_id_inventory(id)
