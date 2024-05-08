from ingredient_parser import parse_ingredient
from recipe_scrapers import scrape_me
from termcolor import colored, cprint
from simple_term_menu import TerminalMenu
from utils import convert_to_pint_unit, pluralize, singularize
from ingredient_categorizer import categorize_ingredient
from pint import Unit

DEBUG_MODE = True

STOP_INPUTS = ['', None, ' ', 'stop', 'exit', 'quit']

# the order I go thru my grocery store!
GROCERY_STORE_ORDER = [
  'you_probably_have', 
  'produce', 
  'meat', 
  'seafood', 
  'pantry',
  'baking',
  'dairy', 
  'bread', 
  'frozen',
]

# feedback colors
ERR = 'red'
WARN = 'yellow'
INFO = 'cyan'
GOOD = 'green'

# order the categorized export
# move categorizer into main file for submit
# write some tests

def main():
  OPTIONS = [
    "Add ingredients from recipe to shopping list (by URL, works with most recipe pages)", 
    "Add items to shopping list", 
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
    
  terminal_menu = TerminalMenu(OPTIONS)

  shopping_list = ShoppingList()

  while(True):
    terminal_menu = TerminalMenu(OPTIONS, status_bar="Items: " + str(shopping_list.length) + " | Recipes: " + str(len(shopping_list.recipes)))
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
      add_recipe_by_url(shopping_list)
    elif menu_entry_index == 1:
      add_items_to_list(shopping_list)
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
    self._items = list(map(lambda x: Ingredient(x), items))
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
    return categories

  def string_categorized_items(self):
    categories = self.categorized_items()
    lines = []
    for category, items in categories.items():
      lines.append(f'{category.upper()}:')
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

  # add an item to the shopping list
  # returns 0 if successful, 1 if existing item was added to, 
  # 2 if existing item was not added to, 3 if item was not parsed
  def add_item(self, item, coeff = 1):
    # change this I think - don't want it to choke on empty strings
    if not item:
      raise TypeError("No item to add.")
    try:
      new_item = Ingredient(item.strip())
    # bringing together all potential parsing errors
    except Exception as e:
      raise ParseException(f"Couldn't parse that item - {item}.")
    if coeff != 1:
      # choosing not to choke on coeff not working right - yet
      # eventually exception handling raised out of class methods
      try:
        new_item = new_item * coeff
      except Exception as e:
        cprint(e, 'red')
    existing_item = self.existing_item(new_item)
    if existing_item:
      return 1
    self._items.append(new_item)
    return 0
 
  # if ingredient with same name exists, attempt to add them
  # return 0 if there is no existing item
  # return 1 if existing item was added to, 2 if existing item was not added to
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
    None
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
class Ingredient:
  """
  A class to represent an ingredient.

  Given a string (hopefully an ingredient string), it will parse the string using the ingredient_parser library, provide some simple ways to interact with that parsed data. It will also categorize the ingredient using the ingredient_categorizer.

  Parameters
  ----------
  text : str
    The ingredient string to parse and categorize.
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
    if self.preparation:
      text = text + ' (' + self.preparation + ')'
    return text

  # longterm TODO: account for change to singular/plural of units and ingredients
  # longterm TODO: smarter units - conversion, preferred unit for shopping, etc
  # overload the * operator to multiply the quantity of the ingredient
  # TypeError if the multiplier is not a number
  # Returns the ingredient as is if it has no quantity to multiply
  def __mul__(self, other):
    if type(other) != int and type(other) != float:
      raise TypeError("Can only multiply an Ingredient by a number.")
    if self.amount:
      if self.quantity:
        coeff = float(other)
        self.quantity = str(f'{(float(self.quantity) * coeff):.2g}')
        self._modified = True
    return self

  # overload the + operator to add the quantity of the ingredient
  # relies on both ingredients having compatible pint.Units OR both having the same string unit
  # resulting ingredient will have the unit of the first ingredient
  def __add__(self, other):
    if type(other) != Ingredient:
      raise TypeError("Can only add an Ingredient to an Ingredient.")
    if singularize(self.name) != singularize(other.name):
      raise ValueError("Can only add ingredients with the same name.")
    if not self.quantity or not other.quantity:
      raise ValueError("Both ingredients must have a quantity to add them.")
    if type(self.unit) == Unit and type(other.unit) == Unit:
      if self.unit.is_compatible_with(other.unit):
        a = self.unit * float(self.quantity)
        b = other.unit * float(other.quantity)
        self.quantity = str((a + b).magnitude)
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

  # this assumes there's only one useful amount - might need to change
  @property
  def amount(self):
    if self._parsed.amount:
      return self._parsed.amount[0]
    return None

  @property
  def unit(self):
    if self.amount:
      return self.amount.unit
    return None

  @property
  def quantity(self):
    if self.amount:
      return self.amount.quantity
    return None

  @quantity.setter
  def quantity(self, value):
    if self.amount and self.quantity:
      self._parsed.amount[0].quantity = f'{float(value):.2g}'
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
    servings_text = colored(" " + scraper.yields() + " ", GOOD, attrs=['reverse', 'blink'])
    print(f'Mmmm, {scraper.title()}. It looks like this recipe yields {servings_text}. Do you modify the yield (ie double, halve, etc) ')
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
    print(f'\n{shopping_list}\n')

def export_list(shopping_list):
  if shopping_list.length == 0:
    print("Nothing to export! See ya!")
    return
  filename = 'shopping_list.txt'
  with open(filename, 'w') as file:
    file.write('Shopping List\n')
    file.write('=============\n')
    file.write(shopping_list.string_categorized_items())
    file.write('\n\nRecipes:\n')
    for recipe in shopping_list.recipes:
      file.write(str(recipe) + '\n')
    cprint(f"Exported {shopping_list.length} item long list to {filename}.", GOOD)

if __name__ == "__main__":
  main()