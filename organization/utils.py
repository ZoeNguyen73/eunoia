from enum import Enum

class OrganizationTypes(Enum):
  CHARITY = 'Charity'
  DONOR = 'Donor'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class OrganizationStatuses(Enum):
  PENDING = 'pending'
  ACTIVE = 'active'
  DEACTIVATED = 'deactivated'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]