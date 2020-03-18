from flask import Blueprint, current_app, jsonify
from flask_restful import Api

from data_subscriptions.api.resources import NonsubscribableDataset

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(
    NonsubscribableDataset, "/nonsubscribable_datasets/<string:dataset_id>"
)
