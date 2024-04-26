from recipe_scrapers import scrape_me

scraper = scrape_me('https://www.allrecipes.com/recipe/217981/grilled-chicken-with-rosemary-and-bacon/')

# print(scraper.host())
print(scraper.title())
# print(scraper.total_time())
# print(scraper.image())
print(scraper.ingredients())
# print(scraper.ingredient_groups())
print(scraper.instructions())
# print(scraper.instructions_list())
# print(scraper.yields())
# print(scraper.to_json())
# print(scraper.links())
# print(scraper.nutrients())  # not always available
# print(scraper.canonical_url())  # not always available
# print(scraper.equipment())  # not always available