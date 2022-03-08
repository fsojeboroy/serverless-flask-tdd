from marshmallow import validate

from app_context import ma


class _ProductResponse(ma.Schema):
    class Meta:
        ordered = True

    name = ma.String()
    quantity = ma.Integer()


class GetMenuResponse(ma.Schema):
    class Meta:
        ordered = True

    menu = ma.List(ma.Nested(_ProductResponse()))


class PostOrderResponse(ma.Schema):
    class Meta:
        ordered = True

    order_uuid = ma.String()
    items = ma.List(ma.Nested(_ProductResponse()))


class PostOrderRequest(ma.Schema):
    items = ma.List(ma.Nested(_ProductResponse()))


class GetOrderDetailsResponse(PostOrderResponse):
    class Meta:
        ordered = True

    status = ma.String(validate=validate.OneOf(
        ['PENDING', 'COMPLETED', 'FAILED']))


get_menu_response = GetMenuResponse()
post_order_response = PostOrderResponse()
get_order_details_response = GetOrderDetailsResponse()
post_order_request = PostOrderRequest()
