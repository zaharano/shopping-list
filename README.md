# Shopping List
#### Video Demo: 
### Description:
This command-line appication will assemble a shopping list from the ingredients listed on any number of user-supplied recipe webpage urls as well as any extra manual user input items. Ingredient lines, whether from websites or the user, are parsed into structured data using NLP (natural language processing, see `ingredient_parser_nlp` below), which allows the app to add together amounts of ingredients duplicated across recipes, multiply the yield of a recipe to a desired size, and attempt to categorize and sort ingredients based on where they'll be in a grocery store.

### Choices
I didn't start with things in a object-oriented class-based structure, but quickly found that that method of organization helped me greatly once I started to implement it. So there are data classes for ShoppingList, Recipe, and Ingredient. 

### Libraries
This app relies a great deal upon some impressive libraries, that are doing a lot of the heavy lifting! Many thanks to their authors and maintainers.

`ingredient_parser_nlp` is the star here, a library that uses a technique called Conditional Random Fields to process ingredient lines into structured data where the string `1 cup flour, sifted` becomes a labelled object where that `1` can be multiplied or added to, that `cup` can be converted to another unit, and `flour` can be looked up for categorization. The model used by the parser is dependant upon a great deal of manually tagged and structured data, taken from a few different sources.

`recipe_scrapers` library is used to scrape recipe info from well-known recipe pages. This is an implementation of the popular library `beautiful_soup` with defined scraping templates for major recipe sites, and a generic 'best-guess' template if a specific one isn't available.

`Pint` provides a way to convert and add different compatible units together.

`Inflect` handles singularizing/pluralizing terms when amounts change.

### Road map
This app informs and in some small way will become part of a larger recipe web app. 