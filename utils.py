############################################
# BEGIN UTILS.PY
############################################
import pint
import inflect

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
    if singularize(noun) == False:
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