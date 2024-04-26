from ingredient_parser import parse_ingredient
import argparse, uuid

import json

parser = argparse.ArgumentParser(
  description="Parse an entire list of ingredients into structured data",
)

parser.add_argument('-f', help='a filename to parse (.txt)')

args = parser.parse_args()

def parse_list(s):
  processed = []
  for line in s:
    processed.append({
      '_id': uuid.uuid4(),
      'type': 'holder',
      'ingredient': parse_line(line)
    })
  return processed

def parse_line(s):
  # Clean lines of \n, leading or trailing space. Other sanitation?
  return parse_ingredient(s.replace('\n', '').strip())

def parse_file(f):
  with open(f, 'r') as file:
    return parse_list(file.readlines())

# just a placeholder function
def do_something_with_ingredients(parsed_ingredients):
  with open('output.txt', 'w') as file:
    for p in parsed_ingredients:
      file.write(json.dumps(p['ingredient'].__dict__, indent=2))
  # for p in parsed_ingredients:
  #   for a in p['ingredient'].amount:
  #     print(a.quantity, a.unit, p['ingredient'].name.text)

if args.f:
  parsed_ingredients = parse_file(args.f)
  do_something_with_ingredients(parsed_ingredients)
  
