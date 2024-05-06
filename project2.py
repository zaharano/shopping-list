from ingredient_parser import parse_ingredient
from recipe_scrapers import scrape_me
from termcolor import colored, cprint
from simple_term_menu import TerminalMenu
from utils import convert_to_pint_unit
from ingredient_categorizer import categorize_ingredient

DEBUG_MODE = True

#TODO: Fix the existing_item method

class ShoppingList:
  def __init__(self, items = []):
    self._items = items
    self._recipes = []
    
  def __str__(self):
    lines = []
    for item in self._items:
      lines.append(str(item))
    return '\n'.join(lines)

  @property
  def items(self):
    return self._items

  @property
  def recipes(self):
    return self._recipes

  def length(self):
    return len(self._items)

  def add_item(self, item, coeff = 1):
    if not item:
      raise TypeError("No item to add.")
    try:
      new_item = Ingredient(item.strip())
    except:
      raise ParseException("Couldn't parse that item. Please try again.")
    # Apply the coefficient if there is one
    if coeff != 1:
      try:
        new_item = new_item * coeff
      except:
        pass
    if self.existing_item(new_item):
      return
    self._items.append(new_item)
 
  # if ingredient with same name exists, add the quantity (or use the new amount there is none)
  # longterm TODO: account for singular/plural of units and ingredients
  # longterm TODO: smarter units - conversion, preferred unit for shopping, etc
  # longterm TODO: account for different ways of writing the same ingredient
  def existing_item(self, new_item):
    for i in self._items:
      if i.name == new_item.name:
        # if they have pint units, try to add them
        # TODO: fix that this is only one confirmed pint unit
        try:
          if i.unit.is_compatible_with(new_item.unit):
            existing = i.unit * float(i.quantity)
            new = new_item.unit * float(new_item.quantity)
            i.quantity = str((existing + new).magnitude)
            return True
        except:
          pass 

        # if they are not pint units, compare the unit strings
        if i.unit and new_item.unit:
          if i.unit == new_item.unit:
            i.quantity = str(float(i.quantity) + float(new_item.quantity))
            return True

        # if there are no units, just add the quantity
        if not i.unit and not new_item.unit:
          i.quantity = str(float(i.quantity) + float(new_item.quantity))
          return True

        cprint(f"Same ingredient but incompatible units {i.name} - {i.unit} and {new_item.unit}. This program doesn't support this conversion. Keeping existing amount - you can manually add this item again using the existing unit to add more to your list!", 'red')
        return True

    return False
    
  def remove_item(self, index):
    try:
      del self._items[int(index)]
    except:
      raise Exception("Couldn't remove that item. Please try again.", 'red')

  def add_recipe(self, recipe):
    # TODO: don't append recipe if it's already there
    self._recipes.append(recipe)
    for ingredient in recipe.ingredients:
      self.add_item(ingredient, recipe.coeff)

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
  def __init__(self, text):
    self._sentence = text
    self._parsed = parse_ingredient(text)
    self._category = categorize_ingredient(self.name)
    # convert unit to pint unit for easy conversion and comparison
    try:
      self._parsed.amount[0].unit = convert_to_pint_unit(self._parsed.amount[0].unit)
    except:
      pass

  def __str__(self):
    text = self.name
    if self.amount:
      text = text + ', ' + self.amount.text
    if self.preparation:
      text = text + ' (' + self.preparation + ')'
    return text

  # overload the * operator to multiply the quantity of the ingredient
  def __mul__(self, other):
    if type(other) != int and type(other) != float:
      raise TypeError("Can only multiply by a number.")
    if self.amount:
      if self.quantity:
        coeff = float(other)
        self.quantity = str(f'{(float(self.quantity) * coeff):.2g}')
    return self

  __rmul__ = __mul__

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
    if self._parsed.amount and self._parsed.amount[0] and self._parsed.amount[0].quantity:
      self._parsed.amount[0].quantity = f'{float(value):.2g}'
      new_text = []
      new_text.append(value)
      if self.amount.unit:
        new_text.append(str(self.amount.unit))
      self._parsed.amount[0].text = ' '.join(new_text)

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
    terminal_menu = TerminalMenu(OPTIONS, status_bar="Items: " + str(shopping_list.length()) + " | Recipes: " + str(len(shopping_list.recipes)))
    menu_entry_index = terminal_menu.show()

    # Add ingredients from recipe to shopping list
    # requests URL, scrapes recipe, adds ingredients to shopping list
    if menu_entry_index == 0:
      url = input("Enter the URL of the recipe: ")
      try: 
        scraper = scrape_me(url)
      except: 
        cprint("Couldn't find or parse the recipe at that URL. Please try a different one!", 'red')
        continue
      coeff = 1
      if scraper.yields() != None:
        servings_text = colored(" " + scraper.yields() + " ", 'green', attrs=['reverse', 'blink'])
        print(f'Mmmm, {scraper.title()}. It looks like this recipe yields {servings_text}. Do you modify the yield (ie double, halve, etc) ')
        coeff_menu = TerminalMenu(['No change', 'Halve', 'Double', 'Triple', 'Custom'])
        coeff_index = coeff_menu.show()
        if coeff_index == 0:
          coeff = 1
        elif coeff_index == 1:
          coeff = 0.5
        elif coeff_index == 2:
          coeff = 2
        elif coeff_index == 3:
          coeff = 3
        elif coeff_index == 4:
          while True:
            try:
              coeff = float(input("Enter the desired multiplier: "))
              if coeff <= 0:
                raise ValueError
              if coeff == 1:
                cprint("No change made.", 'green')
              if coeff > 100:
                raise ValueError
              break
            except:
              cprint("Not a valid coefficient. Enter a number more than zero and less than 100.", 'red')
      new_recipe = Recipe(scraper.title(), scraper.ingredients(), scraper.yields(), url, scraper, coeff)
      shopping_list.add_recipe(new_recipe)
      cprint(f"Added items from recipe. The shopping list now has {shopping_list.length()} items.", 'green')


    elif menu_entry_index == 1:
      while(True):
        item = input("Enter an item to add (enter nothing to stop adding items): ")
        if item == '':
          break
        try:
          shopping_list.add_item(item)
          cprint(f"Added item. The shopping list now has {shopping_list.length()} items.", 'green')
        except TypeError as e:
          cprint(e, 'red')

    elif menu_entry_index == 2:
      while True:
        if shopping_list.length() == 0:
          cprint("The shopping list is empty!", 'red')
          break
        print('Select item to remove:')
        index = item_select(shopping_list.items)
        if index == -1:
          break
        try:
          shopping_list.remove_item(index)
          cprint(f"Removed item. The shopping list now has {shopping_list.length()} items.", 'green')
        except Exception as e:
          cprint(e, 'red')
          break

    elif menu_entry_index == 3:
      if shopping_list.length() == 0:
        print("The shopping list is empty!")
      else:
        print(f'\n{shopping_list}\n')

    elif menu_entry_index == 4:
      if shopping_list.length() == 0:
        print("Nothing to export! See ya!")
        break
      filename = 'shopping_list.txt'
      with open(filename, 'w') as file:
        file.write('Shopping List\n')
        file.write('=============\n\n')
        file.write('Items:\n')
        file.write(str(shopping_list))
        file.write('\n\nRecipes:\n')
        for recipe in shopping_list.recipes:
          file.write(str(recipe) + '\n')
        cprint(f"Exported {shopping_list.length()} item long list to {filename}.", 'green')
      return 0

    # DEBUG OPTIONS
    elif menu_entry_index == 5:
      select = item_select(shopping_list.items)
      if select == -1:
        continue
      print(shopping_list._items[select].parsed)
      print(shopping_list._items[select])

if __name__ == "__main__":
  main()
  # one = Ingredient('1 cup of flour')
  # two = Ingredient('2 cup of flour')

  # thing = float(one.amount.quantity) * one.amount.unit
  # bass = float(two.amount.quantity) * two.amount.unit

  # added = thing + bass

  # print(added.magnitude)
