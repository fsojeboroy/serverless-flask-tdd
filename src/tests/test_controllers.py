
from unittest import mock

from apis.controllers import (MenuController, OrderController,
                              OrderDetailsController, OrderProcessorController)


@mock.patch('apis.controllers.get_menu')
def test_get_menu_controller_should_trigger_get_menu_usecase(mock_get_menu):
    MenuController().get()
    mock_get_menu.assert_called()


@mock.patch('apis.controllers.get_order')
def test_get_order_details_controller_should_trigger_get_order_usecase(mock_get_order):
    OrderDetailsController().get('')
    mock_get_order.assert_called()


@mock.patch('apis.controllers.process_order')
def test_process_order_controller_should_trigger_process_order_usecase(mock_process_order):
    OrderProcessorController(sqs_event={}).process()
    mock_process_order.assert_called()


@mock.patch('apis.controllers.post_order')
@mock.patch('apis.controllers.request')
def test_post_order_controller_should_trigger_post_order_usecase(mock_request, mock_post_order):
    OrderController().post.__wrapped__(OrderController())
    mock_post_order.assert_called()
