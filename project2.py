from ingredient_parser import parse_ingredient
from recipe_scrapers import scrape_me
from termcolor import colored, cprint
from simple_term_menu import TerminalMenu

class ShoppingList:
  def __init__(self, items = []):
    self._items = items
    self._recipes = []
    
  def __str__(self):
    lines = []
    for item in self._items:
      lines.append(str(item))
    return '\n'.join(lines)

  def length(self):
    return len(self._items)

  def add_item(self, item):
    if not item:
      return
    try:
      new_item = Ingredient(item.strip())
    except:
      cprint(f"Couldn't parse that - ({item}). Please try again.", 'red')
      return
    if self.existing_item(new_item):
      return
    self._items.append(new_item)
 
  # if ingredient with same name exists, add the quantity (or use the new amount there is none)
  # TODO: account for singular/plural of units and ingredients
  # longterm TODO: convert units if they don't match
  # longterm TODO: account for different ways of writing the same ingredient
  def existing_item(self, new_item):
    for i in self._items:
      if i.name == new_item.name:
        if i.amount and new_item.amount:
          if i.amount.unit != new_item.amount.unit:
            cprint(f"Units don't match for {i.name.text} - {i.amount.unit} and {new_item.amount.unit}. This program doesn't support conversion yet. Keeping existing amount - you can manually add this item again using the same unit to add more to your list!", 'red')
            return
          i.amount.quantity += new_item.amount.quantity
        elif i.amount:
          return
        elif new_item.amount:
          i.amount = new_item.amount
        return
    return False

  def add_single_item(self, item):
    if not item:
      cprint("You didn't enter an item!", 'red')
      return
    self.add_item(item)
    cprint(f"Added item. The shopping list now has {self.length()} items.", 'green')

  def remove_item(self, index):
    try:
      del self._items[int(index)]
    except:
      cprint("Couldn't remove that item. Please try again.", 'red')
      return
    cprint(f"Removed item. The shopping list now has {self.length()} items.", 'green')

  def remove_items(self):
    while True:
      if self.length() == 0:
        cprint("The shopping list is empty!", 'red')
        return
      print('Select item to remove:')
      index = self.item_select()
      if index == -1:
        return
      self.remove_item(index)

  def item_select(self):
    names = [str(item) for item in self._items]
    item_menu = TerminalMenu([*names, "Back"])
    menu_entry_index = item_menu.show()
    if menu_entry_index == len(names):
      return -1
    return menu_entry_index

  def add_recipe(self, url):
    try:
      scraper = scrape_me(url)
    except:
      cprint("Sorry, I couldn't find that recipe. Please try another URL.", 'red')
      return
    # TODO: account for absent yields
    servings_text = colored(" " + scraper.yields() + " ", 'green', attrs=['reverse', 'blink'])
    check = input(f'Mmmm, {scraper.title()}. It looks like this recipe yields {servings_text}. Do you want to halve or double the recipe? ')
    self._recipes.append({'scraper': scraper, 'url': url, 'check': check})
    for ingredient in scraper.ingredients():
      self.add_item(ingredient)
    cprint(f"Added items from recipe. The shopping list now has {self.length()} items.", 'green')
  def export_list(self, filename):
    with open(filename, 'w') as file:
      file.write('Shopping List\n')
      file.write('=============\n\n')
      file.write('Items:\n')
      file.write(self.__str__())
      file.write('\n\nRecipes:\n')
      for recipe in self._recipes:
        file.write(recipe['scraper'].title() + '\n')
        file.write('\t' + recipe['url'] + '\n')
      cprint(f"Exported {self.length()} items to {filename}.", 'green')

# TODO: figure out if I can extend ParsedIngredient class from the lib?
class Ingredient:
  def __init__(self, text):
    self._sentence = text
    self._parsed = parse_ingredient(text)
    # init category

  def __str__(self):
    text = self.name
    if self.amount:
      text = text + ', ' + self.amount.text
    if self.preparation:
      text = text + ' (' + self.preparation + ')'
    return text

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

# add ingredient list from file

# def main():
#   tester = parse_ingredient('1/4 cup flour')
#   print(tester)

def main():
  shopping_list = ShoppingList()
  OPTIONS = [
    "Add ingredients from recipe to shopping list (by URL, works with most recipe pages)", 
    "Add a single item to the shopping list", 
    "Remove items from the shopping list",
    "View current shopping list", 
    "Export list and quit",
  ]
  termal_menu = TerminalMenu(OPTIONS)
  while(True):
    menu_entry_index = termal_menu.show()
    if menu_entry_index == 0:
      url = input("Enter the URL of the recipe: ")
      shopping_list.add_recipe(url)
    elif menu_entry_index == 1:
      item = input("Enter the item to add: ")
      shopping_list.add_single_item(item)
    elif menu_entry_index == 2:
      shopping_list.remove_items()
    elif menu_entry_index == 3:
      if shopping_list.length() == 0:
        print("The shopping list is empty!")
      else:
        print(f'\n{shopping_list}\n')
    elif menu_entry_index == 4:
      if shopping_list.length() == 0:
        print("Nothing to export! See ya!")
        break
      shopping_list.export_list('shopping_list.txt')
      break

if __name__ == "__main__":
  main()
