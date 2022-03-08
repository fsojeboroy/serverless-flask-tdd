from flask import request
from flask_restx import Resource

from apis.schemas import (get_menu_response, get_order_details_response,
                          post_order_request, post_order_response)
from apis.usecases import get_menu, get_order, post_order, process_order
from common.marshall import RequestWrapper


class MenuController(Resource):
    """Controller class for fetching menu resource."""

    @RequestWrapper(
        response_schema=get_menu_response
    )
    def get(self):
        """Query product details from database

        Returns:
            dict: products and its quantity.
        """

        return get_menu()


class OrderController(Resource):
    """Controller class for creating orders resource."""

    @RequestWrapper(
        schema=post_order_request,
        response_schema=post_order_response
    )
    def post(self):
        """Create an order request and sends to message queue"""
        return post_order(request.parsed_obj)


class OrderDetailsController(Resource):
    """Controller class for fetching specific order"""

    @RequestWrapper(
        response_schema=get_order_details_response
    )
    def get(self, order_uuid: str):
        """Look up `order_uuid` in db and returns dictionary of order details.

        Args:
            order_uuid (str): order_uuid of order.
        """

        return get_order(order_uuid)


class OrderProcessorController:
    """Controller class for processing order from sqs.

    Args:
        sqs_event (dict): event object from AWS Lambda trigger.
    """

    def __init__(self, sqs_event: dict):
        self._sqs_event = sqs_event

    def process(self):
        """Consumes message from sqs."""

        process_order(self._sqs_event)
