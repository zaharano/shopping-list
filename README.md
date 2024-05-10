# Shopping List
#### Video Demo: 
https://youtu.be/eQPkCT_uGz8
### Description:
This command-line application assembles a shopping list from the ingredient lists on recipe webpages, as well as from manual user input. Ingredient sentences, whether from websites or the user, are parsed into structured data using NLP (natural language processing, see `ingredient_parser_nlp` below), which allows the app to add together amounts (even if they are in different units!) of ingredients duplicated across recipes, multiply the yield of a recipe to a desired size, and attempt to categorize and sort ingredients based on where they'll be in a grocery store.

### Choices
I didn't start with things in a object-oriented class-based structure, but quickly found that that method of organization helped me greatly once I started to implement it. There are classes for ShoppingList, Recipe, and ShoppingIngredient, each with a few properties and methods. The ShoppingIngredient class has overloaded addition and multiplication operators, allowing two ingredients to be added together directly or an ingredient to be multiplied by a coefficient directly. 

Initially I had pieces of UI sprinkled into the classes, so for instance there was a method on ShoppingList to generate a selectable list of all of that lists ingredients (which is used in a few different tasks). I eventually decided that it made more sense to keep the classes as purely about holding and manipulating their own data as possible (making them more portable or usable by different methods of interface) and switched as much UI stuff as possible to external functions. This also lead to me to think more about errors and the handling thereof - how it's useful to set up exceptions within the class when something goes wrong, and then the 'higher level' functions doing the UI consume those exceptions and print out the information - and ideally not stop the program in doing so, but just provide the feedback.

I regret not focusing from the start on making everything a bit more 'functional programming' style. Specifically there are oddities because the overloaded addition and multiplication are mutating existing instances of an Ingredient rather than creating a new one, which makes for some unintended behavior in certain circumstances. Something to refactor.

The categorizer is basically just a dictionary of huge lists of ingredients. I built it not having any real idea of how well it was going to work. I've set up some minimal processing of ingredient strings (like splitting phrases by `' or '` and checking each string split out this way, checking trying to singularize everything, stripping out unhelpful characters) but for the most part we are just asking if `'flour' == 'flour'`. It feels inelegant but is honestly pretty effective. I've definitely missed large swathes ingredients, but I'm not trying to spend too much time making this categorization method too exhaustive - because there's definitely much better, future-proof, and more powerful ways to approach this with a database of known ingredients, with aliases, then comparisons involving confidence values, probably something about a root noun pulled from the ingredient phrase being looked up, etc etc. It's all just beyond the scope of this project.

### Libraries
This app relies a great deal upon some impressive libraries, that are doing a lot of the heavy lifting! Many thanks to their authors and maintainers.

[`ingredient_parser_nlp`](https://ingredient-parser.readthedocs.io/en/latest/) is the star here, a library that uses a technique called Conditional Random Fields to process ingredient lines into structured data where the string `1 cup flour, sifted` becomes a labelled object where that `1` can be multiplied or added to, that `cup` can be converted to another unit, and `flour` can be looked up for categorization. The model used by the parser is dependant upon a great deal of manually tagged and structured data, taken from a few different sources.

[`recipe_scrapers`](https://pypi.org/project/recipe-scrapers/) library is used to scrape recipe info from well-known recipe pages. This is an implementation of the popular library `beautiful_soup` with defined scraping templates for major recipe sites, and a generic 'best-guess' template if a specific one isn't available.

[`Pint`](https://pint.readthedocs.io/en/stable/) provides a way to convert and compare compatible units with one another.

`Inflect` handles singularizing/pluralizing terms when amounts change.

### Shortcomings
NLP is hard. The ingredient parser does a pretty darn good job, considering the challenges involved. But even with perfectly parsed data, working with data processed from natural language is still full of pitfalls. There are all kinds of ways in which you will not get optimal results from this app, far too many issues for me to list, but here's a few:

* The choice to display PREPARATION and COMMENT in a shopping list wasn't easy. These are often information that has to do with mis en place or the cook and so is very extraneous to shopping. But they CAN be essential to know a preferred type of thing to buy, or they can be important context like how `1 tbsp garlic` seems silly but `1 tbsp garlic, minced` makes sense. But there's no easy way to determine when information is valuable for shopping or not.

* There's the simple matter of cases like `chickpeas` are the same as `garbanzo beans` but my simple string comparison for names will not catch this. Ideally we have a robust database of ingredients with more associated data like aliases (enabling much better categorization too), but that gets well beyond the scope of this project!

* This app will not add `1 cup flour` and `200 grams flour` because these are different types of units. Cups are a measure of volume, grams a measure of weight (or mass!) The fact is that it is possible to guesstimate a conversion and that would be useful (bakers will often convert to mass as a matter of course, as its a more exact way to measure ingredients) but building out all the various conversions is beyond the scope here (each ingredient will have its own volume to mass ratio and another great case for a db of ingredients). In fact an argument can be made that everything dry should be converted to weight because a. It's a more exact measure and b. It's how things are measured in a store, where you buy pounds and ounces of most things that aren't liquids. And all liquid volumes should be converted to fl. oz. as you never see 'cups' or 'tbsp' on a package at the store so they might be silly to keep in context of a shopping list.

* Those PREPARATION and COMMENT phrases, which we hope to be pulled out and tagged separately, can still make things hard to work with. For instance `onions` will often have the unit `cups` because they have the preparation `chopped` where cups makes sense. But this is less informative in the context of shopping, and then if recipes are added that just list `1 onion` these cannot be combined with the chopped onion cups, and so will be dropped.

This app was my first step working with recipe data like this, and the experience is helping me start to build a more robust web app that does some of this extra work and more!