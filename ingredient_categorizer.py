
### Produce categories
## Fruits
apples = ['apple', 'fuji apple', 'gala apple', 'golden delicious apple', 'granny smith apple', 'honeycrisp apple', 'jonagold apple', 'mcintosh apple', 'red delicious apple']

oranges = ['orange', 'blood orange', 'clementine', 'mandarin orange', 'navel orange', 'tangerine']
lemons = ['lemon', 'meyer lemon']
limes = ['lime', 'key lime']
citrus = [*oranges, *lemons, *limes]

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
root_vegetables = ['beet', 'carrot', 'parsnip', 'potato', 'radish', 'rutabaga', 'sweet potato', 'turnip']
leafy_greens = ['arugula', 'collard greens', 'kale', 'lettuce', 'spinach', 'swiss chard']
cruciferous_vegetables = ['broccoli', 'brussels sprout', 'cabbage', 'cauliflower', 'kohlrabi']
alliums = ['chive', 'garlic', 'leek', 'onion', 'shallot']
herbs = ['basil', 'cilantro', 'dill', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'thyme']
peppers = ['bell pepper', 'jalapeno', 'jalapeño', 'poblano', 'serrano']
mushrooms = ['button mushroom', 'cremini mushroom', 'portobello mushroom', 'shiitake mushroom']
vegetables = [*squashes, *root_vegetables, *leafy_greens, *cruciferous_vegetables, *alliums, *herbs, *peppers, *mushrooms]

### Meat categories
## Poultry
chicken = ['chicken', 'chicken breast', 'breast', 'chicken drumstick', 'drumstick', 'chicken leg', 'chicken thigh', 'thigh', 'chicken wing', 'wing', 'ground chicken', 'whole chicken', 'chicken liver', 'chicken heart', 'chicken gizzard', 'chicken foot', 'chicken feet', 'chicken neck', 'chicken back', 'chicken cutlet', 'cutlet']
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
bread = ['baguette', 'biscuit', 'bun', 'cornbread', 'croissant', 'doughnut', 'flatbread', 'focaccia', 'hamburger bun', 'naan', 'pita', 'roll', 'sourdough', 'tortilla', 'white bread', 'whole wheat bread']
pastas = ['angel hair', 'bowtie', 'bucatini', 'fettuccine', 'linguine', 'macaroni', 'orecchiette', 'penne', 'rigatoni', 'spaghetti', 'tortellini']
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


# going to need to use the unit 'can' to determine if it's canned vs dry
# also plurality will be odd I think
beans = ['black bean', 'black beans', 'black-eyed pea', 'cannellini', 'cannelini bean', 'chickpea', 'garbanzo bean', 'great northern', 'kidney', 'lentil', 'lima', 'navy', 'pinto', 'red bean', 'soybean', 'split pea', 'white bean', 'bean', 'canned bean', 'canned black bean', 'canned black-eyed pea', 'canned cannellini', 'canned chickpea', 'canned garbanzo bean', 'canned great northern', 'canned kidney', 'canned lentil', 'canned lima', 'canned navy', 'canned pinto', 'canned red bean', 'canned soybean', 'canned split pea', 'canned white bean',]

### oils and vinegars
oils = ['oil', 'olive oil', 'vegetable oil', 'canola oil', 'coconut oil', 'sesame oil', 'peanut oil', 'sunflower oil', 'safflower oil', 'corn oil', 'soybean oil', 'grapeseed oil', 'avocado oil', 'walnut oil', 'almond oil', 'hazelnut oil', 'palm oil', 'lard', 'shortening', 'margarine', 'butter', 'ghee', 'clarified butter',]
vinegars = ['vinegar', 'balsamic vinegar', 'apple cider vinegar', 'red wine vinegar', 'white wine vinegar', 'rice vinegar', 'sherry vinegar', 'malt vinegar', 'distilled vinegar', 'cane vinegar', 'coconut vinegar', 'date vinegar', 'honey vinegar', 'malt vinegar', 'mango vinegar', 'palm vinegar', 'sugarcane vinegar', 'beer vinegar', 'cider vinegar', 'fruit vinegar', 'herb vinegar', 'spice vinegar', 'wine vinegar',]

### Spices and dried herbs
spices = ['spice', 'allspice', 'anise', 'annatto', 'asafoetida', 'caraway', 'cardamom', 'cayenne', 'celery seed', 'chervil', 'ground chili', 'chili powder', 'cinnamon', 'ground cinnamon', 'cloves', 'ground cloves', 'coriander', 'cumin', 'cumin seed', 'ground cumin', 'curry', 'curry powder', 'fennel seed', 'fenugreek seed', 'garlic powder', 'ginger powder', 'ground ginger', 'lavender', 'mustard seed', 'mustard powder', 'nutmeg', 'ground nutmeg', 'paprika', 'black pepper', 'poppy seed', 'rosemary', 'saffron', 'sage', 'savory', 'tarragon', 'thyme', 'turmeric', 'vanilla', 'wasabi', 'zaatar',]
dried_herbs = ['herb', 'basil', 'bay leaf', 'chervil', 'chive', 'cilantro', 'dill', 'lavender', 'lemon grass', 'marjoram', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'savory', 'tarragon', 'thyme']
all_spices = [*spices, *dried_herbs]

you_probably_have = ['salt', 'kosher salt', 'pepper', 'black pepper', 'salt and pepper', 'salt & pepper']

# dairy, sauces, canned, baking, snacks, beverages, frozen, misc

grocer_categories = {
    'produce': [*fruit, *vegetables],
    'meat': [*poultry, *red_meat, *game_meat,],
    'seafood': [*fresh_seafood],
    'bread': [*bread],
    'dairy': [*dairy_milks, *alternative_milks, *butter, *yogurt, *sour_creams, *all_cheeses],
    'pantry': [*pastas, *rices, *grains, *canned_fish, *anchovy, *beans, *vinegars, *oils, *all_spices, ],
}

#TODO: cases where unit influences category
#TODO: preferred returns etc etc.
def categorize_ingredient(ingredient, unit = None):
    for category, items in grocer_categories.items():
      if ingredient in items:
        return category
    return 'misc'