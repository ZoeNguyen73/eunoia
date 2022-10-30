from enum import Enum

class ListingStatuses(Enum):
  ACTIVE = 'active'
  CONFIRMED = 'confirmed'
  INACTIVE = 'inactive'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls] 