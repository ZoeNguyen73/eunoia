from enum import Enum

class TimeslotOptions(Enum):
  _12AM = '12am - 2am'
  _2AM = '2am - 4am'
  _4AM = '4am - 6am'
  _6AM = '6am - 8am'
  _8AM = '8am - 10am'
  _10AM = '10am - 12pm'
  _12PM = '12pm - 2pm'
  _2PM = '2pm - 4pm'
  _4PM = '4pm - 6pm'
  _6PM = '6pm - 8pm'
  _8PM = '8pm - 10pm'
  _10PM = '10pm - 12am'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls] 