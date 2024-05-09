import pytest
from project import Ingredient, ShoppingList, convert_to_pint_unit, categorize_ingredient, add_ingredients, multiply_ingredient

def test_add_ingredients():
    x = Ingredient("1 cup flour")
    y = Ingredient("2 cups flour")
    assert add_ingredients(x, y).quantity == '3'

    x = Ingredient("1 cup flour")
    y = Ingredient("2 cups flour")
    assert add_ingredients(x, y).amount.text == '3 cups'

    x = Ingredient("1 orange")
    y = Ingredient("2 oranges")
    assert add_ingredients(x, y).name == 'oranges'

def test_multiply_ingredient():
    x = Ingredient("1 cup flour")
    assert multiply_ingredient(x, 2).quantity == '2'

    x = Ingredient("1 cup flour")
    assert multiply_ingredient(x, 2).amount.text == '2 cups'

    x = Ingredient("1 orange")
    assert multiply_ingredient(x, 2).name == 'oranges'

def test_convert_to_pint_unit():
    assert convert_to_pint_unit('cup').unit == pint.Unit('cup')
    assert convert_to_pint_unit().quantity == '0.5'

    x = Ingredient("1 cup flour")
    assert convert_to_pint_unit(x).amount.text == '0.5 pint'

def test_categorize_ingredient():
    