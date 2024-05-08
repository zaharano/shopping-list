import inflect
from utils import singularize, pluralize

p = inflect.engine()

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