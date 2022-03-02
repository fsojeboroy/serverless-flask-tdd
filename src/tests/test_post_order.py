from unittest import mock

import pytest
import werkzeug.exceptions

from apis.usecases import post_order, _build_order_message, _validate_order, _is_valid_order, _push_order_to_sqs
from apis.controllers import OrderController

from custom_exceptions import InvalidOrderException


@mock.patch('apis.controllers.post_order')
def test_post_order_controller_should_trigger_post_order_usecase(mock_post_order):
    OrderController().post()
    mock_post_order.assert_called()

# @mock.patch(__name__ + '._validate_order', return_value=True)
# @mock.patch('apis.usecases._build_order_message', return_value=True)
# @mock.patch('apis.usecases._push_order_to_sqs', return_value=True)
# def test_post_order_given_valid_payload_should_trigger_expected_methods(mock_push_order_to_sqs, mock_build_order_message, mock_validate_order):
#     manager = mock.Mock()
#     manager(mock_validate_order)
#     manager(mock_build_order_message)
#     manager(mock_push_order_to_sqs)
#     expected_calls = [mock.call(mock_validate_order), mock.call(mock_build_order_message), mock.call(mock_push_order_to_sqs)]

#     post_order({})

#     manager.assert_has_calls(expected_calls, any_order=False)


@mock.patch('apis.usecases._validate_order', side_effect=InvalidOrderException())
def test_post_order_given_invalid_payload_should_raise_400(mock_validate_order):
    with pytest.raises(werkzeug.exceptions.BadRequest):
        post_order([])

@mock.patch('apis.usecases._is_valid_order', return_value=True)
def test_validate_order_given_valid_payload_should_return_none(mock_is_valid_order):
    expected = None
    actual = _validate_order([])
    assert expected == actual

@mock.patch('apis.usecases._is_valid_order', return_value=False)
def test_validate_order_given_invalid_payload_should_raise_invalid_order_exception(mock_is_valid_order):
    with pytest.raises(InvalidOrderException):
        _validate_order([[]])

@mock.patch('apis.usecases.get_menu',
    return_value=[
        dict(name="Pork chop", quantity=0),
        dict(name="Rice", quantity=1),
        dict(name="Water", quantity=-1)
    ]
)
@pytest.mark.parametrize('order, expected', [
    # product is infinite
    ([dict(name="Water", quantity=2)], True),
    # product is available but does not match case
    ([dict(name="watEr", quantity=2)], True),
    # product is available
    ([dict(name="Water", quantity=2), dict(name="Rice", quantity=1)], True),
    # product does not exist
    ([dict(name="Carbonara", quantity=2)], False),
    # product quantity is not enough
    ([dict(name="Rice", quantity=2)], False),
    # one or more product is invalid
    ([dict(name="Water", quantity=2), dict(name="Pork chop", quantity=2), dict(name="Rice", quantity=2)], False),
    # quantity is not int
    ([dict(name="Water", quantity='invalid')], False),
    # quantity is < 1
    ([dict(name="Water", quantity=0)], False),
    ([dict(name="Water", quantity=-10)], False),
    # empty list
    ([], False),
    # invalid format
    (dict(Water=1), False),
    ([dict(Water=1)], False)
])
def test_is_valid_order_should_return_expected(mock_get_menu, order, expected):
    actual = _is_valid_order(order)
    assert actual == expected

@mock.patch('apis.usecases.uuid4')
def test_build_order_message_should_trigger_generate_order_uuid(mock_generate_order_uuid):
    _build_order_message([])
    mock_generate_order_uuid.assert_called()

@pytest.mark.usefixtures('generate_sqs')
@pytest.mark.parametrize('order_message', [
    dict(order_uuid='abcd1234', items=[dict(name="Water", quantity=2)]),
    dict(order_uuid='abcd1234', items=[dict(name="Water", quantity=2), dict(name="Pork chop", quantity=2), dict(name="Rice", quantity=2)])
])
def test_push_order_to_sqs_should_not_raise_exception(order_message):
    try:
        _push_order_to_sqs(order_message)
    except Exception as exc:
        assert False, f"'_push_order_to_sqs' raised an exception {exc}"
