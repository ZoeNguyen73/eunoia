from enum import Enum

class OrderStatuses(Enum):
  OPEN = 'open'
  COMPLETED = 'completed'
  CANCELLED = 'cancelled'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls] 