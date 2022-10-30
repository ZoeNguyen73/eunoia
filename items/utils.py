from enum import Enum

class ItemTypes(Enum):
  COOKED_VEGETABLES = 'Cooked vegetables'
  COOKED_MEAT = 'Cooked meat'
  COOKED_FISH = 'Cooked fish'
  CANNED_FOOD = 'Canned food'
  REFRIDGERATED = 'Refridgerated food'
  DIARY = 'Diary'
  VEGETABLES = 'Vegetables'
  MEAT = 'Meat'
  FISH_SEAFOOD = 'Fish and Seafood'
  EGGS = 'Eggs'
  CONDIMENTS = 'Condiments'
  SNACKS = 'Snacks'
  OIL = 'Oil'
  BAKED_GOODS = 'Baked goods'
  JAMS_SPREADS = 'Jams and Spreads'
  FRUITS = 'Fruits'
  BEVERAGES = 'Beverages'
  RICE = 'Rice'
  NOODLES = 'Noodles'
  SEASONINGS = 'Seasonings'
  PASTE_SAUCES = 'Pastes and Sauces'
  CUTLERY = 'Cutlery'
  DRIED_FOOD = 'Dried food'
  VITAMINS_SUPPLEMENTS = 'Vitamins and Supplements'
  MISCELLANEOUS = 'Miscellaneous'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls] 
