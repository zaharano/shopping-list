import pytest
from project import ShoppingIngredient, ShoppingList, convert_to_pint_unit, categorize_ingredient, add_ingredients, multiply_ingredient

def test_add_ingredients():
    x = ShoppingIngredient("1 cup flour")
    y = ShoppingIngredient("2 cups flour")
    assert add_ingredients(x, y).quantity == '3'

    x = ShoppingIngredient("1 cup flour")
    y = ShoppingIngredient("2 cups flour")
    assert add_ingredients(x, y).amount.text == '3 cups'

    x = ShoppingIngredient("1 orange")
    y = ShoppingIngredient("2 oranges")
    assert add_ingredients(x, y).name == 'oranges'

def test_multiply_ingredient():
    x = ShoppingIngredient("1 cup flour")
    assert multiply_ingredient(x, 2).quantity == '2'

    x = ShoppingIngredient("1 cup flour")
    assert multiply_ingredient(x, 2).amount.text == '2 cups'

    x = ShoppingIngredient("1 orange")
    assert multiply_ingredient(x, 2).name == 'oranges'

def test_convert_to_pint_unit():
    assert convert_to_pint_unit('cup').unit == pint.Unit('cup')
    assert convert_to_pint_unit().quantity == '0.5'

    x = ShoppingIngredient("1 cup flour")
    assert convert_to_pint_unit(x).amount.text == '0.5 pint'

def test_categorize_ingredient():
    pass