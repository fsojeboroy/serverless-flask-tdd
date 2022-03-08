from unittest import TestCase

import pytest

from apis.usecases import get_menu


@pytest.mark.usefixtures('generate_menu_data')
def test_get_menu_should_return_menu():
    ut = TestCase()
    expected = [
        {"name": "Pork chop", "quantity": 10},
        {"name": "Rice", "quantity": 10},
        {"name": "Chopsuey", "quantity": 0},
        {"name": "Water", "quantity": -1}
    ]
    actual = get_menu()['menu']
    ut.assertCountEqual(expected, actual)
