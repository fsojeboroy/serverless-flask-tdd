from unittest import mock, TestCase

import pytest

from apis.usecases import get_menu
from apis.controllers import MenuController


@mock.patch('apis.controllers.get_menu')
def test_get_menu_controller_should_trigger_get_menu_usecase(mock_get_menu):
    MenuController().get()
    mock_get_menu.assert_called()

@pytest.mark.usefixtures('generate_menu_data')
def test_get_menu_should_return_menu():
    ut = TestCase()
    expected = [
        {"name": "Pork chop", "quantity": 10},
        {"name": "Rice", "quantity": 10},
        {"name": "Chopsuey", "quantity": 0},
        {"name": "Water", "quantity": -1}
    ]
    actual = get_menu()
    ut.assertCountEqual(expected, actual)

