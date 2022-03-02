import json
from unittest import mock

import pytest
from py_event_mocks import create_event

from apis.controllers import OrderProcessorController
from apis.usecases import _parse_order_from_sqs_event, _insert_order_to_db

from custom_exceptions import InvalidMessageException


@mock.patch('apis.controllers.process_order')
def test_process_order_controller_should_trigger_process_order_usecase(mock_process_order):
    OrderProcessorController(sqs_event={}).process()
    mock_process_order.assert_called()

# # def test_process_order_given_valid_event_should_trigger_expected_methods(mock_insert_order_to_db, mock_validate_order_from_sqs_event_message, mock_parse_order_from_sqs_event):

@pytest.mark.parametrize('order_message', [
    dict(order_uuid='abcd1234', items=[{"name": "Water", "quantity": 2}]),
    dict(order_uuid='123415', items=[{"name": "xxx", "quantity": 2}])
])
def test_parse_order_from_sqs_event_given_valid_params_should_return_expected(order_message):
    # setup
    event = create_event('aws:sqs')
    event['Records'][0]['body'] = json.dumps(order_message)

    expected = order_message
    actual = _parse_order_from_sqs_event(event)
    assert actual == expected

def create_sqs_event_with_empty_body():
    event = create_event('aws:sqs')
    event['Records'][0]['body'] = ""
    return event
@pytest.mark.parametrize('event', [
    None, [], {},
    create_event('aws:sqs'),
    create_sqs_event_with_empty_body(),
    create_event('aws:sns')
])
def test_parse_order_from_sqs_event_given_invalid_params_should_raise_expected(event):
    with pytest.raises(InvalidMessageException):
        _parse_order_from_sqs_event(event)

@pytest.mark.parametrize('order_message', [
    dict(order_uuid='abcd1234', items=[{"name": "Water", "quantity": 2}]),
    dict(order_uuid='123415', items=[{"name": "xxx", "quantity": 2}])
])
@pytest.mark.usefixtures('create_order_table')
def test_insert_order_to_db_given_valid_params_should_do_expected(order_message):
    try:
        _insert_order_to_db(order_message)
    except Exception as exc:
        assert False, f"'_push_order_to_sqs' raised an exception {exc}"