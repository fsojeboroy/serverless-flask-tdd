from unittest import mock

import pytest
import werkzeug.exceptions

from apis.controllers import OrderController
from apis.usecases import get_order

@mock.patch('apis.controllers.get_order')
def test_get_order_controller_should_trigger_get_order_usecase(mock_get_order):
    OrderController().get('')
    mock_get_order.assert_called()

@pytest.mark.parametrize('order_uuid, expected', [
    ('abcd1234', dict(order_uuid='abcd1234', items=[{"name": "Water", "quantity": 2}], status='PENDING')),
    ('123415', dict(order_uuid='123415', items=[{"name": "xxx", "quantity": 2}], status='COMPLETED'))
])
@pytest.mark.usefixtures('generate_order_data')
def test_get_order_from_db_given_valid_order_uuid_should_return_expected(order_uuid, expected):
    actual = get_order(order_uuid)
    assert actual == expected

@pytest.mark.parametrize('order_uuid', [
    None, [1,2,3], {},
    '', 'test'
])
@pytest.mark.usefixtures('generate_order_data')
def test_get_order_from_db_given_invalid_order_uuid_should_raise_404(order_uuid):
    with pytest.raises(werkzeug.exceptions.NotFound):
        get_order(order_uuid)
