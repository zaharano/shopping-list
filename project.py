from ingredient_parser import parse_ingredient
from recipe_scrapers import scrape_me
from termcolor import colored, cprint
from simple_term_menu import TerminalMenu
from utils import convert_to_pint_unit, pluralize, singularize
from ingredient_categorizer import categorize_ingredient
from pint import Unit
import copy

DEBUG_MODE = False

STOP_INPUTS = ['', None, ' ', 'stop', 'exit', 'quit']

# the order I go thru my grocery store!
GROCERY_STORE_ORDER = [
  'you_probably_already_have', 
  'produce', 
  'meat', 
  'seafood', 
  'pantry',
  'baking',
  'dairy_and_eggs', 
  'bread', 
  'frozen',
  'misc'
]

# feedback colors
ERR = 'red'
WARN = 'yellow'
INFO = 'cyan'
GOOD = 'green'

def main():
  OPTIONS = [
    "Add items to shopping list", 
    "Add ingredients from recipe to shopping list (by URL, works with most recipe pages)", 
    "Remove items from the shopping list",
    "View current shopping list", 
    "Export list and quit",
  ]
  DEBUG_OPTIONS = [
    "Print an item's parsed data (for debugging)"
  ]

  # DEBUG MODE set at top of this file
  if DEBUG_MODE:
    OPTIONS += DEBUG_OPTIONS

  shopping_list = ShoppingList()

  while(True):
    terminal_menu = TerminalMenu(
      OPTIONS, 
      status_bar="Items: " + str(shopping_list.length) + " | Recipes: " + str(len(shopping_list.recipes)), 
      status_bar_style=("bg_gray", "fg_green")
    )
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
      add_items_to_list(shopping_list)
    elif menu_entry_index == 1:
      add_recipe_by_url(shopping_list)
    elif menu_entry_index == 2:
      remove_items_from_list(shopping_list)
    elif menu_entry_index == 3:
      view_list(shopping_list)
    elif menu_entry_index == 4:
      export_list(shopping_list)
      return 0

    # DEBUG OPTIONS
    elif menu_entry_index == 5:
      select = item_select(shopping_list.items)
      if select == -1:
        continue
      print(shopping_list._items[select].parsed)
      print(shopping_list._items[select])
      
    elif menu_entry_index == None:
      cprint("Exiting...", GOOD)
      break

class ShoppingList:
  '''
  A class to represent a shopping list.

  The shopping list is a collection of ingredients and recipes. It provides methods to add and remove items, and to categorize the items.

  Parameters
  ----------
  items : list, optional
    A list of strings to initialize the shopping list with. Default is an empty list.
  '''
  def __init__(self, items = []):
    if type(items) != list:
      raise TypeError("Items must be a list.")
    if not all(isinstance(x, str) for x in items):
      raise TypeError("Items must be a list of strings.")
    self._items = list(map(lambda x: ShoppingIngredient(x), items))
    self._recipes = []
    
  def __str__(self):
    lines = []
    for item in self._items:
      lines.append(str(item))
    return '\n'.join(lines)

  def categorized_items(self):
    categories = {}
    for item in self._items:
      if item.category not in categories:
        categories[item.category] = []
      categories[item.category].append(item)
    sorted_categories = {}
    for category in GROCERY_STORE_ORDER:
      if category in categories:
        sorted_categories[category] = categories[category]
    return sorted_categories

  def string_categorized_items(self):
    categories = self.categorized_items()
    lines = []
    for category, items in categories.items():
      lines.append(f'{category.upper().replace('_', ' ')}:')
      for item in items:
        lines.append(str(item))
      lines.append('')
    return '\n'.join(lines)

  @property
  def items(self):
    return self._items

  @property
  def recipes(self):
    return self._recipes

  @property
  def length(self):
    return len(self._items)

  def add_item(self, item, coeff = 1):
    '''
    Given a string, parse it into an Ingredient object and add it to the list of items. If an item with the same name already exists in the list, attempt to add the new item to the existing item. Return a result code.

    Parameters:
    ----------
    item : str
      the string for the new item to add to the shopping list
    coeff : int, optional
      a coefficient by which to multiply the quantity of the item. Default is 1.

    Returns:
    -------
    int
      1 if the item is added to an existing item, 0 if it is appended to the list of items
    '''
    if not item:
      raise TypeError("No item to add.")
    try:
      new_item = ShoppingIngredient(item.strip())
    # bringing together all potential parsing errors
    except Exception as e:
      raise ParseException(f"Couldn't parse that item - {item}.")
    if coeff != 1:
      new_item = new_item * coeff
    existing_item = self.existing_item(new_item)
    if existing_item:
      return 1
    self._items.append(new_item)
    return 0
 
  # longterm TODO: account for different ways of writing the same ingredient
  def existing_item(self, new_item):
    '''
    Given a parsed Ingredient object, check if an item with the same name exists in the list of items. If it does, attempt to add the new item to the existing item. Return a result code.

    Parameters:
    ----------
    new_item : Ingredient
      the new item to check against the existing items

    Returns:
    -------
    bool
      True if the item was added to an existing item, False if it was not
    '''
    for i in self._items:
      if singularize(i.name) == singularize(new_item.name):
        i = i + new_item
        return True
    return False
    
  def remove_item(self, index):
    '''
    Given an index, remove the item at that index from the list of items.

    Parameters:
    ----------
    index : int
      The index of the item to remove from the _items list.

    Returns:
    -------
    None
    '''
    if index >= 0 and index < len(self._items):
      del self._items[int(index)]
    else:
      raise ValueError("Invalid delete index.")

  def add_recipe(self, recipe):
    '''
    Given a Recipe object, append it to the list of recipes, and add its ingredients to the list of items.

    If a recipe with the same title already exists, don't append it to the list of recipes (but still add its ingredients to the shopping list).

    Parameters:
    ----------
    recipe : Recipe
      The recipe to add to the shopping list.

    Returns:
    -------
    int
      1 if there were issues adding some ingredients from the recipe, 0 if there were no issues
    '''
    exists = False
    issues = False
    for existing_recipe in self._recipes:
      if existing_recipe.title == recipe.title:
        exists = True
    if not exists:
      self._recipes.append(recipe)
    for ingredient in recipe.ingredients:
      if ingredient:
        try:
          self.add_item(ingredient, recipe.coeff)
        except Exception as e:
          cprint(e, 'red')
          issues = True
    if issues:
      return 1
    return 0

class Recipe:
  def __init__(self, title, ingredients, yields, url, data = None, coeff = 1):
    self._title = title
    self._ingredients = ingredients
    if coeff != 1:
      self._yields = yields + f' ({coeff}x ingredients)'
    else:
      self._yields = yields
    self._url = url
    self._data = data
    self._coeff = coeff

  def __str__(self):
    lines = [self.title + ' | ' + self.yeilds, self.url]
    return '\n'.join(lines)

  @property
  def title(self):
    return self._title

  @property
  def ingredients(self):
    return self._ingredients

  @property
  def yeilds(self):
    return self._yields

  @property
  def url(self):
    return self._url

  @property
  def data(self):
    return self._data

  @property
  def coeff(self):
    return self._coeff

# TODO: figure out if I can extend ParsedIngredient class from the lib?
class ShoppingIngredient:
  """
  A class to represent an ingredient.

  Given a string (hopefully an ingredient string, of the sort you'd typically find in the ingredients list on a recipe, which contains some or all of the tokens QUANTITY, UNIT, INGREDIENT, PREPARATION, COMMENT), upon initialization the string will be parsed using the ingredient_parser library and the parsed data is saved privately. The unit will be converted to a Pint unit, if the unit is found in the Pint unit registry. Pint units have a host of useful features including easy conversion to compatible units. The ingredient will also be categorized using the ingredient_categorizer.
  
  The class provides many properties to access the parsed data, with one property (quantity) being settable, which will also reset the amount text to account for the new quantity. The class also provides overloaded operators for multiplication and addition, which will multiply the quantity of the ingredient by a number or add the quantity of another ingredient to this ingredient, respectively. These operators mutate the first object in place - they do not return a fresh object. I will probably change this soon. There is also a string overload to format the ingredient for printing in a shopping list.

  Parameters
  ----------
  text : str
    The ingredient string to parse and categorize.

  Operators
  ---------
  * : Multiply the quantity of the ingredient by a number. Returns the ingredient as is if it has no quantity to multiply.
  + : Attempt to add the quantity of another ingredient to this ingredient. Names must match, and units must be compatible, which is done either via pint Unit compatability or string matching. The existing ingredient will have its quantity and unit updated to reflect the sum. If two ingredients with compatible but not equal Pint units are added, the unit that results in  the smaller whole magnitude (>= 1) will be used for the sum.
  """
  def __init__(self, text):
    self._sentence = text
    self._parsed = parse_ingredient(text)
    self._category = categorize_ingredient(self.name)
    self._modified = False
    # convert unit to pint unit for easy conversion and comparison
    try:
      if self._parsed.amount:
        self._parsed.amount[0].unit = convert_to_pint_unit(self._parsed.amount[0].unit)
    except Exception as e:
      cprint(e, ERR)

  # string overload formats the ingredient
  def __str__(self):
    text = self.name
    if self.amount:
      text = text + ', ' + self.amount.text
    if self.preparation or self.comment or self.amount_two:
      paren_text = []
      if self.preparation:
        paren_text.append(self.preparation)
      if self.amount_two:
        paren_text.append(self.amount_two.text)
      if self.comment:
        # remove parens from comments where they have been retained
        paren_text.append(self.comment.replace('(', '').replace(')', ''))
      text = text + ' (' + ", ".join(paren_text) + ')'
    return text

  # longterm TODO: smarter units - conversion, preferred unit for shopping, etc
  # Returns the ingredient as is if it has no quantity to multiply
  def __mul__(self, other):
    if type(other) != int and type(other) != float:
      raise TypeError("Can only multiply an Ingredient by a number.")
    if self.amount:
      if self.quantity:
        coeff = float(other)
        self.quantity = str(f'{(float(self.quantity) * coeff):.3g}')
        self._modified = True
    return self

  def __add__(self, other):
    # TODO: implement this so that it returns a new object, not mutate the existing one
    # new_ingredient = copy.deepcopy(self)
    if type(other) != ShoppingIngredient:
      raise TypeError("Can only add an Ingredient to an Ingredient.")
    if singularize(self.name) != singularize(other.name):
      raise ValueError("Can only add ingredients with the same name.")
    if not self.quantity or not other.quantity:
      raise ValueError("Both ingredients must have a quantity to add them.")
    if other.amount_two:
      raise ValueError("Can't add ingredient with secondary amounts. This will be implemented in the future.")
    if type(self.unit) == Unit and type(other.unit) == Unit:
      if self.unit.is_compatible_with(other.unit):
        a = self.unit * float(self.quantity)
        b = other.unit * float(other.quantity)
        c = a + b
        if c.magnitude > c.to(other.unit).magnitude and c.to(other.unit).magnitude >= 1:
          self.unit = copy.deepcopy(other.unit)
          self.quantity = str(c.to(other.unit).magnitude)
        else:
          self.quantity = str(c.magnitude)
      else:
        raise ValueError(f"Can't add ingredients with incompatible units. Attempted to add {self.unit} and {other.unit} for {self.name}. Such conversions will be implemented in the future.")
    elif type(self.unit) == str and type(other.unit) == str:
      if self.unit == other.unit:
        self.quantity = str(float(self.quantity) + float(other.quantity))
    elif not self.unit and not other.unit:
      self.quantity = str(float(self.quantity) + float(other.quantity))
    else:
      raise ValueError(f"Can't add ingredients with incompatible units. Attempted to add {self.unit} and {other.unit} for {self.name}. Such conversions will be implemented in the future.")
    return self

  @property
  def name(self):
    return self._parsed.name.text

  @property
  def sentence(self):
    return self._sentence

  # assumes no more than two amounts
  # and that the second one doesn't change when multiplying etc
  @property
  def amount(self):
    if self._parsed.amount:
      return self._parsed.amount[0]
    return None

  # seen this used for sizing pieces of meat, good info for parenthetical
  @property
  def amount_two(self):
    if len(self._parsed.amount) > 1:
      return self._parsed.amount[1]
    return None

  @property
  def unit(self):
    if self.amount:
      return self.amount.unit
    return None

  # this needs to be better. handle different things. setting an amount should be one big setter i think.
  @unit.setter
  def unit(self, value):
    if self.amount:
      self._parsed.amount[0].unit = value
      self._modified = True

  @property
  def quantity(self):
    if self.amount:
      return self.amount.quantity
    return None

  @quantity.setter
  def quantity(self, value):
    if self.amount and self.quantity:
      self._parsed.amount[0].quantity = f'{float(value):.3g}'
      new_text = []
      new_text.append(self.quantity)
      if self.unit:
        new_text.append(pluralize(str(self.unit), float(self.quantity)))
      else:
        self._parsed.name.text = pluralize(self.name, float(self.quantity))
      self._parsed.amount[0].text = ' '.join(new_text)
      self._modified = True


  @property
  def preparation(self):
    if self._parsed.preparation:
      return self._parsed.preparation.text
    return None

  @property
  def category(self):
    return self._category

  @property
  def comment(self):
    if self._parsed.comment:
      return self._parsed.comment.text
    return None

  @property
  def parsed(self):
    return self._parsed

# this is probably not necessary - but wanted to collect all the parsing errors in one place
class ParseException(Exception):
  pass

def item_select(items):
  names = [str(item) for item in items]
  item_menu = TerminalMenu([*names, "Back"])
  menu_entry_index = item_menu.show()
  if menu_entry_index == len(names):
    return -1
  return menu_entry_index

# Add ingredients from recipe to shopping list
# requests URL, scrapes recipe, adds ingredients to shopping list
def add_recipe_by_url(shopping_list):
  url = input("Enter the URL of the recipe: ")
  if url in STOP_INPUTS:
    return
  try: 
    scraper = scrape_me(url)
  except: 
    cprint("Couldn't find or parse the recipe at that URL. Please try a different one!", ERR)
    return
  coeff = 1
  if scraper.yields() != None:
    title_text = colored(scraper.title(), GOOD, attrs=['reverse'])
    servings_text = colored(scraper.yields(), GOOD, attrs=['reverse'])
    print(f'Mmmm, {title_text}. It looks like this recipe yields {servings_text}.\nWould you like to modify the yield (ie double, halve, etc) ')
    coeff_menu = TerminalMenu(['No change', 'Halve', 'Double', 'Triple', 'Custom'])
    coeffs = [1, 0.5, 2, 3]
    coeff_index = coeff_menu.show()
    if coeff_index < 4:
      coeff = coeffs[coeff_index]
    elif coeff_index == 4:
      while True:
        try:
          coeff = float(input("Enter the desired multiplier: "))
          if coeff <= 0:
            raise ValueError
          if coeff == 1:
            cprint("No change made.", GOOD)
          if coeff > 100:
            raise ValueError
          break
        except:
          cprint("Not a valid coefficient. Enter a number more than zero and less than 100.", ERR)
  new_recipe = Recipe(scraper.title(), scraper.ingredients(), scraper.yields(), url, scraper, coeff)
  result = shopping_list.add_recipe(new_recipe)
  if result == 1:
    cprint(f"There were issues adding some ingredients from the recipe. The shopping list now has {shopping_list.length} items", WARN)
  else:
    cprint(f"Added items from recipe. The shopping list now has {shopping_list.length} items.", GOOD)

def add_items_to_list(shopping_list):
  while(True):
    item = input("Enter an item to add (enter nothing to stop adding items): ")
    if item in STOP_INPUTS:
      break
    try:
      shopping_list.add_item(item)
      cprint(f"Added item. The shopping list now has {shopping_list.length} items.", GOOD)
    except Exception as e:
      cprint(e, ERR)

def remove_items_from_list(shopping_list):
  while True:
    if shopping_list.length == 0:
      cprint("The shopping list is empty!", ERR)
      break
    print('Select item to remove:')
    index = item_select(shopping_list.items)
    if index == -1:
      break
    try:
      shopping_list.remove_item(index)
      cprint(f"Removed item. The shopping list now has {shopping_list.length} items.", GOOD)
    except Exception as e:
      cprint(e, ERR)
      break

def view_list(shopping_list):
  if shopping_list.length == 0:
    print("The shopping list is empty!")
  else:
    print(f'\n{shopping_list.string_categorized_items()}\n')

def export_list(shopping_list):
  if shopping_list.length == 0:
    print("Nothing to export! See ya!")
    return
  filename = 'shopping_list.txt'
  with open(filename, 'w') as file:
    file.write('Shopping List\n')
    file.write('=============\n')
    file.write(shopping_list.string_categorized_items())
    if shopping_list.recipes:
      file.write('\n\nRecipes:\n')
      for recipe in shopping_list.recipes:
        file.write(str(recipe) + '\n')
    cprint(f"Exported {shopping_list.length} item long list to {filename}.", GOOD)

# these are here to create tests for cs50p submit
def add_ingredients(ingredient1, ingredient2):
  return ingredient1 + ingredient2

def multiply_ingredient(ingredient, coeff):
  return ingredient * coeff

if __name__ == "__main__":
  main()