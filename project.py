from ingredient_parser import parse_ingredient
from recipe_scrapers import scrape_me
from termcolor import colored, cprint
from simple_term_menu import TerminalMenu
# from utils import convert_to_pint_unit, pluralize, singularize
# from ingredient_categorizer import categorize_ingredient
from pint import Unit

# for utils.py
import pint
import inflect

# for ingredient_categorizer.py



DEBUG_MODE = True

STOP_INPUTS = ['', None, ' ', 'stop', 'exit', 'quit']

# the order I go thru my grocery store!
GROCERY_STORE_ORDER = [
  'you_probably_already_have', 
  'produce', 
  'meat', 
  'seafood', 
  'pantry',
  'baking',
  'dairy', 
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

# these are here to create tests for cs50p submit
def add_ingredients(ingredient1, ingredient2):
  return ingredient1 + ingredient2

def multiply_ingredient(ingredient, coeff):
  return ingredient * coeff




############################################
# BEGIN UTILS.PY
############################################
p = inflect.engine()

# this is taken from a newer version of the parser - eventually this will just be from that but wanted to get the pint func going
# Plural and singular units
UNITS = {
    "bags": "bag",
    "bars": "bar",
    "baskets": "basket",
    "batches": "batch",
    "blocks": "block",
    "bottles": "bottle",
    "boxes": "box",
    "branches": "branch",
    "bulbs": "bulb",
    "bunches": "bunch",
    "bundles": "bundle",
    "cans": "can",
    "chunks": "chunk",
    "cloves": "clove",
    "clusters": "cluster",
    "cl": "cl",
    "cL": "cL",
    "cm": "cm",
    "cubes": "cube",
    "cups": "cup",
    "cutlets": "cutlet",
    "dashes": "dash",
    "dessertspoons": "dessertspoon",
    "dollops": "dollop",
    "drops": "drop",
    "ears": "ear",
    "envelopes": "envelope",
    "feet": "foot",
    "fl": "fl",
    "g": "g",
    "gallons": "gallon",
    "glasses": "glass",
    "grams": "gram",
    "grinds": "grind",
    "handfuls": "handful",
    "heads": "head",
    "inches": "inch",
    "jars": "jar",
    "kg": "kg",
    "kilograms": "kilogram",
    "knobs": "knob",
    "lbs": "lb",
    "leaves": "leaf",
    "lengths": "length",
    "links": "link",
    "l": "l",
    "liters": "liter",
    "litres": "litre",
    "loaves": "loaf",
    "milliliters": "milliliter",
    "millilitres": "millilitre",
    "ml": "ml",
    "mL": "mL",
    "mm": "mm",
    "mugs": "mug",
    "ounces": "ounce",
    "oz": "oz",
    "packs": "pack",
    "packages": "package",
    "packets": "packet",
    "pairs": "pair",
    "pieces": "piece",
    "pinches": "pinch",
    "pints": "pint",
    "pods": "pod",
    "pounds": "pound",
    "pts": "pt",
    "punnets": "punnet",
    "racks": "rack",
    "rashers": "rasher",
    "recipes": "recipe",
    "rectangles": "rectangle",
    "ribs": "rib",
    "quarts": "quart",
    "sachets": "sachet",
    "scoops": "scoop",
    "segments": "segment",
    "shakes": "shake",
    "sheets": "sheet",
    "shots": "shot",
    "shoots": "shoot",
    "slabs": "slab",
    "slices": "slice",
    "sprigs": "sprig",
    "squares": "square",
    "stalks": "stalk",
    "stems": "stem",
    "sticks": "stick",
    "strips": "strip",
    "tablespoons": "tablespoon",
    "tbsps": "tbsp",
    "tbs": "tb",
    "teaspoons": "teaspoon",
    "tins": "tin",
    "tsps": "tsp",
    "twists": "twist",
    "wedges": "wedge",
    "wheels": "wheel",
}
# Generate capitalized version of each entry in the UNITS dictionary
_capitalized_units = {}
for plural, singular in UNITS.items():
    _capitalized_units[plural.capitalize()] = singular.capitalize()
UNITS = UNITS | _capitalized_units

# Dict mapping certain units to their imperial version in pint
IMPERIAL_UNITS = {
    "cup": "imperial_cup",
    "floz": "imperial_floz",
    "fluid_ounce": "imperial_fluid_ounce",
    "quart": "imperial_quart",
    "pint": "imperial_pint",
    "gallon": "imperial_gallon",
}

UREG = pint.UnitRegistry()

def convert_to_pint_unit(unit: str, imperial_units: bool = False) -> str | pint.Unit:
    """Convert a unit to a pint.Unit object, if possible.
    If the unit is not found in the pint Unit Registry, just return the input unit.

    Parameters
    ----------
    unit : str
        Unit to find in pint Unit Registry
    imperial_units : bool, optional
        If True, use imperial units instead of US customary units for the following:
        fluid ounce, cup, pint, quart, gallon.
        Default is False, which results in US customary units being used.

    Returns
    -------
    str | pint.Unit

    Examples
    --------
    >>> convert_to_pint_unit("")
    ''

    >>> convert_to_pint_unit("oz")
    <Unit('ounce')>

    >>> convert_to_pint_unit("fl oz")
    <Unit('fluid_ounce')>

    >>> convert_to_pint_unit("cup", imperial_units=True)
    <Unit('imperial_cup')>
    """
    if "-" in unit:
        # When checking if a unit is in the unit registry, pint will parse any
        # '-' as a subtraction and attempt to evaluate it, causing an exception.
        # Since no pint.Unit can contain a '-', we'll just return early with
        # the string.
        return unit

    if unit == 'pinch':
      # Pint decides this common cook-ism is pico-inch, which is not what we want
      return unit

    # Define some replacements to ensure correct matches in pint Unit Registry
    replacements = {
        "fl oz": "floz",
        "fluid oz": "fluid_ounce",
        "fl ounce": "fluid_ounce",
        "fluid ounce": "fluid_ounce",
    }
    for original, replacement in replacements.items():
        unit = unit.replace(original, replacement)

    if imperial_units:
        for original, replacement in IMPERIAL_UNITS.items():
            unit = unit.replace(original, replacement)

    # If unit not empty string and found in Unit Registry,
    # return pint.Unit object for unit
    if unit != "" and unit in UREG:
        return pint.Unit(unit)

    return unit


def singularize_unit(unit: str) -> str:
    """Return the singular form of a unit, if it exists in the UNITS dictionary.
    If the unit is not found in the dictionary, just return the input unit.

    Parameters
    ----------
    unit : str
        Unit to singularize

    Returns
    -------
    str

    Examples
    --------
    >>> singularize("cups")
    'cup'

    >>> singularize("pints")
    'pint'

    >>> singularize("g")
    'g'
    """
    return UNITS.get(unit, unit)

def pluralize_unit(unit: str) -> str:
    """Return the plural form of a unit, if it exists in the UNITS dictionary.
    If the unit is not found in the dictionary, just return the input unit.

    Parameters
    ----------
    unit : str
        Unit to pluralize

    Returns
    -------
    str

    Examples
    --------
    >>> pluralize("cup")
    'cups'

    >>> pluralize("pint")
    'pints'

    >>> pluralize("g")
    'g'
    """
    return UNITS.get(unit, unit)

def pluralize(noun: str, count: float | int = 0) -> str:
    """Return the plural form of a noun, from inflect engine, unless count is exactly 1. This logic may need tweaking.

    is it 0.5 oranges or 0.5 orange? 
    half an orange. etc.

    Parameters
    ----------
    noun : str
        Noun to pluralize
    count : float | int, optional
        Number of items, default is 2

    Returns
    -------
    str

    Examples
    --------
    """
    if count == 1:
        return noun
    if p.singular_noun(noun) == False:
        return p.plural(noun, count)
    return noun


def singularize(noun: str) -> str:
    """Return the singular form of a noun, from inflect engine. If inflect engine determines the noun is already singular, return the input noun.

    Parameters
    ----------
    noun : str
        Noun to singularize

    Returns
    -------
    str

    Examples
    --------
    """
    return p.singular_noun(noun) or noun






############################################
# Ingredient Categorizer
############################################

# for now just doing a lookup of these static lists to categorize ingredients
# obviously db later, that can be added to on the fly

### Produce categories
## Fruits
apples = ['apple', 'fuji apple', 'gala apple', 'golden delicious apple', 'granny smith apple', 'honeycrisp apple', 'jonagold apple', 'mcintosh apple', 'red delicious apple']

oranges = ['orange', 'blood orange', 'clementine', 'mandarin orange', 'navel orange', 'tangerine']
lemons = ['lemon', 'meyer lemon']
limes = ['lime', 'key lime']
citrus_juices = ['fresh orange juice', 'fresh lemon juice', 'fresh lime juice', 'orange juice', 'lemon juice', 'lime juice', 'juice of orange', 'juice of lemon', 'juice of lime', 'orange zest', 'lemon zest', 'lime zest']
citrus = [*oranges, *lemons, *limes, *citrus_juices]

grapes = ['grape', 'concord grape', 'cotton candy grape', 'green grape', 'red grape', 'black grape', 'purple grape', 'seedless grape', 'grapefruit', 'red grapefruit', 'white grapefruit']
berries = ['berry', 'blackberry', 'blueberry', 'cranberry', 'raspberry', 'strawberry']
bananas = ['banana', 'plantain']
kiwi = ['kiwi', 'kiwifruit']
tropical = ['mango', 'papaya', 'pineapple', 'coconut']
melons = ['cantaloupe', 'honeydew', 'watermelon']
stone_fruit = ['apricot', 'cherry', 'nectarine', 'peach', 'plum']
fruit = [*apples, *citrus, *grapes, *berries, *bananas, *kiwi, *tropical, *melons, *stone_fruit]

## Vegetables
squashes = ['acorn squash', 'butternut squash', 'delicata squash', 'hubbard squash', 'spaghetti squash', 'yellow squash', 'zucchini']
root_vegetables = ['beet', 'carrot', 'parsnip', 'potato', 'radish', 'rutabaga', 'sweet potato', 'turnip', 'red potato', 'gold potato', 'yukon potato', 'fingerling potato', 'purple potato', 'white potato', 'russet potato', 'new potato', 'baby potato', 'baby red potato', 'baby gold potato', 'baby yukon potato', 'baby fingerling potato', 'baby purple potato', 'baby white potato',]
leafy_greens = ['arugula', 'collard greens', 'kale', 'lettuce', 'spinach', 'swiss chard', 'endive', 'escarole', 'frisee', 'mesclun', 'mizuna', 'mustard greens', 'radicchio', 'sorrel', 'watercress', 'bok choy', 'chinese cabbage', 'napa cabbage', 'savoy cabbage', 'cabbage', ]
cruciferous_vegetables = ['broccoli', 'brussels sprout', 'brussel', 'brussel sprout', 'cabbage', 'cauliflower', 'kohlrabi']
alliums = ['chive', 'garlic', 'leek', 'onion', 'shallot', 'green onion', 'scallion', 'spring onion', 'ramp', 'red onion', 'white onion', 'yellow onion', 'sweet onion', 'pearl onion', 'cippolini onion', 'vidalia onion', 'walla walla onion', 'maui onion', 'elephant garlic', 'garlic scape', 'garlic chive']
other_vegetables = ['celery', 'cucumber', 'eggplant', 'fennel', 'okra', 'pea', 'snap pea', 'snow pea', 'tomato', 'cherry tomato', 'grape tomato', 'heirloom tomato', 'roma tomato', 'beefsteak tomato', 'plum tomato', 'green tomato', 'yellow tomato', 'orange tomato', 'purple tomato', 'white tomato', 'black tomato', 'pink tomato', 'striped tomato', 'corn', 'artichoke', 'asparagus', 'snap bean', 'green bean', 'wax bean', ]
herbs = ['basil', 'cilantro', 'dill', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'thyme']
peppers = ['bell pepper', 'green bell pepper', 'red bell pepper', 'yellow bell pepper', 'orange bell pepper', 'green pepper', 'red pepper', 'orange pepper', 'jalapeno', 'jalapeño', 'jalapeno peppers', 'poblano', 'poblano peppers', 'serrano', 'serrano peppers']
mushrooms = ['button mushroom', 'cremini mushroom', 'portobello mushroom', 'shiitake mushroom']
vegetables = [*squashes, *root_vegetables, *leafy_greens, *cruciferous_vegetables, *alliums, *herbs, *peppers, *mushrooms, *other_vegetables]

### Meat categories
## Poultry
chicken = ['chicken', 'chicken breast', 'breast', 'chicken drumstick', 'drumstick', 'chicken leg', 'chicken thigh', 'thigh', 'chicken wing', 'wing', 'ground chicken', 'whole chicken', 'chicken liver', 'chicken heart', 'chicken gizzard', 'chicken foot', 'chicken feet', 'chicken neck', 'chicken back', 'chicken cutlet', 'cutlet', 'boneless skinless chicken thigh', 'boneless skinless chicken breast', 'bone-in chicken leg', 'bone-in chicken drumstick', 'boneless skinless chicken', 'boneless skinless chicken cutlet', 'boneless skinless cutlet']
processed_chicken = ['chicken sausage', 'chicken nugget', 'chicken tender', 'chicken strip', 'chicken patty']
turkey = ['turkey', 'turkey breast', 'turkey leg', 'turkey wing', 'turkey liver', 'turkey heart', 'turkey gizzard', 'ground turkey', 'whole turkey', 'turkey cutlet']
processed_turkey = ['turkey sausage', 'turkey bacon', 'turkey burger', 'turkey patty', 'turkey tender', 'turkey strip']
duck = ['duck', 'duck breast', 'duck leg', 'duck wing', 'duck liver', 'duck heart', 'duck gizzard']
goose = ['goose', 'goose breast', 'goose leg', 'goose wing', 'goose liver', 'goose heart', 'goose gizzard']
quail = ['quail', 'quail breast', 'quail leg', 'quail wing', 'quail liver', 'quail heart', 'quail gizzard']
poultry = [*chicken, *processed_chicken, *turkey, *processed_turkey, *duck, *goose, *quail]


## Red meat
beef = ['beef', 'beef chuck', 'beef rib', 'beef round', 'beef sirloin', 'beef tenderloin', 'ground beef', 'steak', 'ribeye', 'filet mignon', 'flank steak', 'hanger steak', 'porterhouse', 'skirt steak', 'strip steak', 't-bone steak', 'top sirloin', 'tri-tip']
processed_beef = ['corned beef', 'pastrami']
pork = ['pork', 'pork belly', 'pork chop', 'pork loin', 'pork rib', 'pork shoulder', 'pork sparerib', 'pork tenderloin', 'ground pork']
processed_pork = ['bacon', 'ham', 'pork sausage', 'italian sausage', 'spicy italian sausage', 'sweet italian sausage', 'chorizo', 'kielbasa', 'pepperoni', 'salami', 'summer sausage']
lamb = ['lamb', 'lamb chop', 'lamb leg', 'lamb loin', 'lamb rib', 'lamb shoulder', 'lamb shank', 'ground lamb']
processed_lamb = ['lamb sausage']
veal = ['veal', 'veal chop', 'veal leg', 'veal loin', 'veal rib', 'veal shoulder', 'ground veal']
processed_veal = ['veal sausage']
red_meat = [*beef, *processed_beef, *pork, *processed_pork, *lamb, *processed_lamb, *veal, *processed_veal]

## Game
venison = ['venison', 'ground venison']
game = ['bison', 'ground bison', 'elk', 'moose', 'boar', 'bear', 'caribou', 'reindeer', 'buffalo', 'ostrich', 'emu', 'kangaroo', 'alligator', 'crocodile', 'snake', 'iguana', 'turtle', 'frog']
game_bird = ['partridge', 'pheasant', 'quail', 'squab', 'wild turkey', 'wild duck', 'wild goose', 'wild quail', 'wild pheasant', 'wild partridge', 'wild squab', 'wild game bird']
game_meat = [*venison, *game, *game_bird]

## Seafood
shellfish = ['crab', 'crab meat', 'crabmeat', 'lobster', 'lobster meat', 'lobster tail', 'lobstermeat', 'mussel', 'oyster', 'shrimp', 'escargot', 'clam', 'scallop', 'abalone', 'conch', 'whelk', 'cockle', 'periwinkle', 'geoduck', 'sea urchin', 'uni']
other_seafood = ['squid', 'calamari', 'octopus', 'sea cucumber']
white_fish = ['cod', 'haddock', 'halibut', 'pollock', 'tilapia']
oily_fish = ['mackerel', 'salmon', 'sardine', 'trout']
flat_fish = ['flounder', 'sole']
round_fish = ['bass', 'carp', 'perch', 'pike']
tropical_fish = ['barracuda', 'grouper', 'snapper']
cartilaginous_fish = ['shark', 'ray']
fillet_fish = [*white_fish, *oily_fish, *flat_fish, *round_fish, *tropical_fish]
fish_fillets = [fish + ' fillet' for fish in fillet_fish]
fresh_seafood = [*shellfish, *fillet_fish, *fish_fillets, *cartilaginous_fish]
anchovy = ['anchovy', 'canned anchovy', 'anchovy fillet', 'canned anchovy fillet', 'anchovy paste', 'canned anchovy paste']
# might put 'tuna' in here
canned_fish = ['canned tuna', 'canned salmon', 'canned sardine', 'canned mackerel', 'canned herring', 'canned trout', 'canned fish', 'canned seafood', 'canned shellfish']

## Bread
bread = ['bread', 'baguette', 'biscuit', 'bun', 'cornbread', 'croissant', 'doughnut', 'flatbread', 'focaccia', 'hamburger bun', 'naan', 'pita', 'roll', 'sourdough', 'tortilla', 'white bread', 'whole wheat bread', 'rye bread', 'rye', 'french bread', 'italian bread', 'ciabatta', 'bagel', 'muffin']
pastas = ['pasta', 'angel hair', 'bowtie', 'bucatini', 'fettuccine', 'linguine', 'macaroni', 'orecchiette', 'penne', 'rigatoni', 'spaghetti', 'tortellini']
rices = ['rice', 'arborio', 'arborio rice', 'basmati', 'basmati rice', 'black rice', 'brown rice', 'cargo rice', 'jasmine rice', 'long grain rice', 'short grain rice', 'wild rice']
grains = ['barley', 'buckwheat', 'corn', 'millet', 'oats', 'quinoa', 'rye', 'sorghum', 'wheat']

dairy_milks = ['milk', 'whole milk', 'skim milk', '2% milk', '1% milk', 'half and half', 'cream', 'heavy cream', 'whipping cream', 'light cream', 'half and half', 'buttermilk',]
alternative_milks = ['almond milk', 'cashew milk', 'hemp milk', 'oat milk', 'oat creamer', 'rice milk', 'soy milk']
butter = ['butter', 'unsalted butter', 'salted butter', 'clarified butter', 'ghee', 'margarine', 'shortening',]
yogurt = ['yogurt', 'greek yogurt', 'plain yogurt', 'vanilla yogurt', 'fruit yogurt', 'flavored yogurt', 'full-fat yogurt', 'low-fat yogurt', 'non-fat yogurt', 'skyr', 'kefir', 'labne']
sour_creams = ['sour cream', 'creme fraiche', 'mexican crema', 'sour cream substitute', 'sour cream alternative', ]

cheeses = ['mozzarella', 'burrata', 'bocconcini', 'scamorza', 'american', 'cheddar', 'colby', 'colby-jack', 'jack', 'monterey jack', 'pepper jack', 'swiss', 'gouda', 'havarti', 'muenster', 'provolone', 'grated parmesan', 'parmesan', 'asiago', 'grated pecorino', 'pecorino', 'romano', 'gruyere', 'emmental', 'fontina', 'brie', 'camembert', 'gorgonzola', 'roquefort', 'stilton', 'boursin', 'feta', 'ricotta', 'cotija']
other_cheeses = ['cheese', 'blue cheese', 'goat cheese', 'fior di latte', 'queso oaxaca', 'queso asadero', 'queso quesadilla', 'queso panela', 'queso chihuahua', 'queso menonita', 'queso cotija', 'queso fresco', 'queso blanco', 'cottage cheese', 'farmer cheese', 'paneer', 'cream cheese', 'neufchatel', 'mascarpone', 'queso fresco', 'queso blanco']
# cheeses that can be with or without 'cheese' at the end, then all others
all_cheeses =  cheeses + [c + ' cheese' for c in cheeses] + other_cheeses

eggs = ['egg', 'chicken egg', 'duck egg', 'goose egg', 'quail egg', 'ostrich egg', 'emu egg', 'egg white', 'egg yolk', 'egg substitute', 'egg replacer']

# going to need to use the unit 'can' to determine if it's canned vs dry
# also plurality will be odd I think
beans = ['black bean', 'black beans', 'black-eyed pea', 'cannellini', 'cannelini bean', 'chickpea', 'garbanzo bean', 'great northern', 'kidney', 'lentil', 'lima', 'navy', 'pinto', 'red bean', 'soybean', 'split pea', 'white bean', 'bean', 'canned bean', 'canned black bean', 'canned black-eyed pea', 'canned cannellini', 'canned chickpea', 'canned garbanzo bean', 'canned great northern', 'canned kidney', 'canned lentil', 'canned lima', 'canned navy', 'canned pinto', 'canned red bean', 'canned soybean', 'canned split pea', 'canned white bean',]

### oils and vinegars
oils = ['oil', 'olive oil', 'vegetable oil', 'canola oil', 'coconut oil', 'sesame oil', 'peanut oil', 'sunflower oil', 'safflower oil', 'corn oil', 'soybean oil', 'grapeseed oil', 'avocado oil', 'walnut oil', 'almond oil', 'hazelnut oil', 'palm oil', 'lard', 'shortening', 'margarine', 'butter', 'ghee', 'clarified butter',]
vinegars = ['vinegar', 'balsamic vinegar', 'apple cider vinegar', 'red wine vinegar', 'white wine vinegar', 'rice vinegar', 'sherry vinegar', 'malt vinegar', 'distilled vinegar', 'cane vinegar', 'coconut vinegar', 'date vinegar', 'honey vinegar', 'malt vinegar', 'mango vinegar', 'palm vinegar', 'sugarcane vinegar', 'beer vinegar', 'cider vinegar', 'fruit vinegar', 'herb vinegar', 'spice vinegar', 'wine vinegar',]

### sauces etc
sauces = ['sauce', 'alfredo sauce', 'bbq sauce', 'bechamel sauce', 'chimichurri sauce', 'cocktail sauce', 'cranberry sauce', 'enchilada sauce', 'gravy', 'hollandaise sauce', 'hot sauce', 'marinara sauce', 'pesto', 'salsa', 'soy sauce', 'sweet and sour sauce', 'tahini', 'teriyaki sauce', 'tzatziki', 'worcestershire sauce', 'hoisin sauce', 'oyster sauce', 'fish sauce', 'ponzu', 'tartar sauce', 'remoulade', 'ranch dressing', 'blue cheese dressing', 'thousand island dressing', 'italian dressing', 'vinaigrette', 'ranch', 'blue cheese', 'thousand island', 'italian', 'vinaigrette', 'dressing', 'dip', 'aioli', 'mayo', 'mayonnaise', 'ketchup', 'mustard', 'mustard sauce', 'dijon mustard',]

### nuts
nuts = ['nut', 'almond', 'brazil nut', 'cashew', 'chestnut', 'hazelnut', 'macadamia nut', 'pecan', 'pine nut', 'pistachio', 'walnut', 'peanut',]
nut_butters = ['nut butter', 'almond butter', 'cashew butter', 'hazelnut butter', 'macadamia nut butter', 'pecan butter', 'peanut butter', 'walnut butter', 'pistachio butter', 'sunflower seed butter', 'tahini', 'almond paste', 'marzipan',]

### seeds
seeds = ['sunflower seed', 'pumpkin seed', 'sesame seed', 'chia seed', 'pepita', 'flaxseed', 'hemp seed', 'poppy seed',  'chia', 'flax', 'seed',]

### dried fruits
dried_berries = ['dried berry', 'dried blackberry', 'dried blueberry', 'dried cranberry', 'dried raspberry', 'dried strawberry', 'raisin', 'gold raisin', 'golden raisin', 'dried cherry', 'dried currant', 'dried grape']
dried_fruits = ['dried apricot', 'prune', 'dried plum', 'date', 'mejool date', 'mehjool date', 'medjool date', 'fig', 'dried fig', 'dried peach', 'dried pear', 'dried apple', 'dried banana', 'dried coconut', 'dried mango', 'dried papaya', 'dried pineapple', 'dried kiwi', 'dried stone fruit', 'dried tropical fruit', 'dried fruit',]

### baking
flours = ['flour', 'all-purpose flour', 'bread flour', 'cake flour', 'pastry flour', 'self-rising flour', 'whole wheat flour', 'almond flour', 'coconut flour', 'cornmeal', 'cornstarch', 'oat flour', 'rice flour', 'rye flour', 'semolina', 'spelt flour', 'tapioca flour', 'teff flour', 'wheat flour', 'gluten-free flour', 'gluten free flour', 'gluten free all-purpose flour', 'gluten free bread flour', 'gluten free cake flour', 'gluten free pastry flour', 'gluten free self-rising flour', 'gluten free whole wheat flour', 'gluten free almond flour', 'gluten free coconut flour', 'gluten free cornmeal', 'gluten free cornstarch', 'gluten free oat flour', 'gluten free rice flour', 'gluten free rye flour', 'gluten free semolina', 'gluten free spelt flour', 'gluten free tapioca flour', 'gluten free teff flour', 'gluten free wheat flour',]
sugars = ['sugar', 'brown sugar', 'confectioners sugar', 'powdered sugar', 'granulated sugar', 'caster sugar', 'superfine sugar', 'turbinado sugar', 'demerara sugar', 'muscovado sugar', 'palm sugar', 'coconut sugar', 'date sugar', 'maple sugar', 'molasses', 'honey', 'agave', 'corn syrup', 'golden syrup', 'maple syrup', 'pancake syrup', 'simple syrup', 'syrup', 'treacle', 'treacle syrup', 'treacle sugar', 'treacle molasses', 'treacle honey', 'treacle agave', 'treacle corn syrup', 'treacle golden syrup', 'treacle maple syrup', 'treacle pancake syrup', 'treacle simple syrup', 'treacle syrup', 'treacle treacle', 'treacle',]
leaveners = ['baking powder', 'baking soda', 'cream of tartar', 'yeast', 'instant yeast', 'active dry yeast', 'sourdough starter', 'starter', 'levain', ]
chocolates = ['chocolate', 'bittersweet chocolate', 'semisweet chocolate', 'dark chocolate', 'milk chocolate', 'white chocolate', 'cocoa powder', 'cacao powder', 'cacao nib', 'cacao butter', 'cacao', 'cocoa', 'chocolate chip', 'chocolate chunk', 'chocolate bar', 'chocolate syrup', 'chocolate sauce', 'chocolate spread', 'chocolate frosting', 'chocolate glaze', 'chocolate ganache', 'chocolate mousse', 'chocolate pudding',]
baking = [*flours, *sugars, *leaveners, *chocolates]

### Spices and dried herbs
spices = ['spice', 'allspice', 'anise', 'annatto', 'asafoetida', 'caraway', 'cardamom', 'cayenne', 'celery seed', 'chervil',  'cinnamon', 'ground cinnamon', 'clove', 'ground clove', 'coriander', 'cumin', 'cumin seed', 'ground cumin', 'curry', 'curry powder', 'fennel seed', 'fenugreek seed', 'garlic powder', 'ginger powder', 'ground ginger', 'lavender', 'mustard seed', 'mustard powder', 'nutmeg', 'ground nutmeg', 'paprika', 'black pepper', 'poppy seed', 'rosemary', 'saffron', 'sage', 'savory', 'tarragon', 'thyme', 'turmeric', 'ground turmeric', 'turmeric powder', 'vanilla', 'wasabi', 'zaatar', 'ground fennel', 'ground fennel seed', 'fennel powder']
dried_herbs = ['herb', 'basil', 'bay leaf', 'chervil', 'chive', 'cilantro', 'dill', 'lavender', 'lemon grass', 'marjoram', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'savory', 'tarragon', 'thyme']
peppers = ['black pepper', 'white pepper', 'cayenne pepper', 'chipotle powder', 'ground chili', 'chili powder', 'new mexico chili powder', 'red-pepper', 'red-pepper flakes', 'red pepper flakes']
all_spices = [*spices, *dried_herbs, *peppers]

### Frozen foods
frozen_veggies = ['frozen peas', 'frozen carrots', 'frozen spinach', 'frozen corn', 'frozen lima beans', 'frozen green beans', 'frozen broccoli', 'frozen cauliflower', 'frozen brussels sprouts', 'frozen mixed vegetables', 'frozen stir fry vegetables', 'frozen vegetable medley', 'frozen vegetable blend', 'frozen vegetable mix', 'frozen vegetable', 'frozen veggie', 'frozen veg', 'frozen greens', 'frozen leafy greens', 'frozen root vegetables', 'frozen squash', 'frozen bell pepper', 'frozen vegetable' ]
frozen_fruit = ['frozen fruit', 'frozen berry', 'frozen banana', 'frozen mango', 'frozen pineapple', 'frozen peach', 'frozen apple', 'frozen pear', 'frozen cherry', 'frozen blueberry', 'frozen blackberry', 'frozen raspberry', 'frozen strawberry', 'frozen cranberry', 'frozen grape', 'frozen citrus', 'frozen orange', 'frozen lemon', 'frozen lime', 'frozen grapefruit', 'frozen tangerine', 'frozen kiwi', 'frozen tropical fruit', ]

you_probably_have = ['water', 'salt', 'kosher salt', 'pepper', 'black pepper', 'salt and pepper', 'salt & pepper', 'kosher salt and black pepper']

# dairy, sauces, canned, baking, snacks, beverages, frozen, misc

grocer_categories = {
    'you_probably_already_have': [*you_probably_have],
    'produce': [*fruit, *vegetables],
    'meat': [*poultry, *red_meat, *game_meat,],
    'seafood': [*fresh_seafood],
    'bread': [*bread],
    'dairy': [*dairy_milks, *alternative_milks, *butter, *yogurt, *sour_creams, *all_cheeses, *eggs],
    'pantry': [*pastas, *rices, *grains, *canned_fish, *anchovy, *beans, *vinegars, *oils, *all_spices, *sauces, *nuts, *nut_butters, *seeds, *dried_fruits, *dried_berries],
    'baking': [*baking],
    'frozen': [*frozen_veggies, *frozen_fruit],
}

DROPPED_CHARACTERS = ['(', ')', '[', ']', '{', '}', '<', '>', '!', '@', '#', '$', '%', '^', '&', '*', '_', '+', '=', '|', '\\', '/', '?', ',', '.', ':', ';', '"', "'", '`', '~']

#TODO: cases where unit influences category
#TODO: preferred returns etc etc.
#TODO: categorize an ingredient within an or statement or other detail
# ie '1 cup flour or cornstarch' -> 'pantry' 
# "parmesan or pecorino" -> 'cheese'
# fresh flat-leaf parsley or dill leaves and fine stems -> 'produce'
def categorize_ingredient(ingredient, unit = None):
  ingredient = ingredient.lower()
  for char in DROPPED_CHARACTERS:
    ingredient = ingredient.replace(char, '')
  for category, items in grocer_categories.items():
    if ingredient in items or singularize(ingredient) in items:
      return category
  return 'misc'

# this is probably better, but needs distinction in the data for terms that
# are too broad like 'pepper' with match 'green pepper' and 'red-pepper flakes'
# and screw up the categorization. but this catches the above or statements
# ultimately, going to have to write something that has a confidence value maybe
def categorize_ingredient_broadly(ingredient, unit = None):
  ingredient = ingredient.lower()
  for char in DROPPED_CHARACTERS:
    ingredient = ingredient.replace(char, '')
  for category, items in grocer_categories.items():
    for item in items:
      if item in ingredient or item in singularize(ingredient):
        return category
  return 'misc'






if __name__ == "__main__":
  main()