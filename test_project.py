import pytest
from project import Ingredient, ShoppingList

def test_ingredient_addition():
    x = Ingredient("1 cup flour")
    y = Ingredient("2 cups flour")
    assert (x + y).quantity == '3'

def test_ingredient_addition_amount_text():
    x = Ingredient("1 cup flour")
    y = Ingredient("2 cups flour")
    assert (x + y).amount.text == '3 cups'

def test_ingredient_addition_name_pluralize():
    x = Ingredient("1 orange")
    y = Ingredient("2 oranges")
    assert (x + y).name == 'oranges'

def test_ingredient_multiplication():
    x = Ingredient("1 cup flour")
    assert (x * 2).quantity == '2'

def test_ingredient_multiplication_amount_text():
    x = Ingredient("1 cup flour")
    assert (x * 2).amount.text == '2 cups'

def test_ingredient_multiplication_name_pluralize():
    x = Ingredient("1 orange")
    assert (x * 2).name == 'oranges'