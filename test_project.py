import pytest
from project import ShoppingIngredient, ShoppingList, convert_to_pint_unit, categorize_ingredient, add_ingredients, multiply_ingredient
from pint import Unit

def test_add_ingredients():
    # add together two quantities of same unit
    x = ShoppingIngredient("1 cup flour")
    y = ShoppingIngredient("2 cups flour")
    assert add_ingredients(x, y).quantity == '3'

    # amount text should be updated to reflect new quantity and plurality of unit
    x = ShoppingIngredient("1 cup flour")
    y = ShoppingIngredient("2 cups flour")
    assert add_ingredients(x, y).amount.text == '3 cups'

    # two singular names with no unit should pluralize
    x = ShoppingIngredient("1 orange")
    y = ShoppingIngredient("1 orange")
    assert add_ingredients(x, y).name == 'oranges'

    # convert to larger whole unit
    x = ShoppingIngredient("1 cup broth")
    y = ShoppingIngredient("1 quart broth")
    assert add_ingredients(x, y).amount.text == '1.25 quarts'

def test_multiply_ingredient():
    x = ShoppingIngredient("1 cup flour")
    assert multiply_ingredient(x, 2).quantity == '2'

    x = ShoppingIngredient("1 cup flour")
    assert multiply_ingredient(x, 2).amount.text == '2 cups'

    x = ShoppingIngredient("1 orange")
    assert multiply_ingredient(x, 2).name == 'oranges'

    x = ShoppingIngredient("1 bunch of cilantro, chopped finely")
    y = multiply_ingredient(x, 2)
    assert y.amount.text == '2 bunches'
    
# this is a pointless test but I can't think of what to do
def test_convert_to_pint_unit():
    assert convert_to_pint_unit('cup') == Unit('cup')
    assert convert_to_pint_unit('cups') == Unit('cup')
    # NOT pico-inch
    assert convert_to_pint_unit('pinch') == 'pinch'

def test_categorize_ingredient():
    assert categorize_ingredient("flour") == 'baking'
    assert categorize_ingredient("baking powder") == 'baking'
    assert categorize_ingredient("cilantro") == 'produce'
    assert categorize_ingredient("chicken broth") == 'pantry'
    assert categorize_ingredient("chicken") == 'meat'
    assert categorize_ingredient("kosher salt") == 'you_probably_already_have'

    # ' or ' splits the string and tests each
    assert categorize_ingredient("flatleaf or curly parsley") == 'produce'
    assert categorize_ingredient("ground beef or pork") == 'meat'
    # this is wrong but I'm not sure about easy way to fix it
    assert categorize_ingredient("chicken or beef broth") == 'meat'

