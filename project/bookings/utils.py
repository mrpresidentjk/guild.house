# -*- coding: utf-8 -*-
from datetime import time, datetime
from .models import Booking
from .settings import DEFAULT_BOOKING_DURATION, UNKNOWN_EMAIL

# Synchronising scrape from Revel to bookings system.
# To be automated daily.


def import_revel_bookings(scrape):

    # Utility functions

    def create_date_from_string(d):
        day, month, year = [int(x) for x in d.split("/")]
        return datetime(year, month, day, 0, 0, 0)

    def create_time_from_string(t):
        hour, minute = [int(x) for x in t.split(":")]
        return time(hour, minute)

    def create_legacy_code(data):
        return "".join(data[0:-1]).replace(" ", "")

    # Confident that they'll do an update one day that will break this.
    # -> Happened Aug 2017

    split_string_start = "Order ID\tStatus\tParty Size\tWait time\tCustomer\tPhone\tNotes & Preferences\r\n"
    split_string_end = "Watch the tutorial"

    data_raw = scrape.split(split_string_start)[-1].split(split_string_end)
    data_list = [x.split("\t") for x in data_raw[0].split("\r\n")]

    # Mapping is as follows:
    """

    ## 0 Reserved On
    ## 1 Reserved For
    # 2 Order ID
    ## 3 Status
    ## 4 Party Size
    # 5 Wait time
    ## 6 Customer
    # 7 Phone
    # 8 Notes & Preferences

    0 updated_at
    1 reserved_date, reserved_time
    2 -
    3 status
    4 party_size
    5 -
    6 name
    7 phone
    8 note
    legacy_code
    """

    success = []
    for data in data_list:
        if not len(data) == 9:
            continue
        obj = Booking()
        obj.created_at = create_date_from_string(data[0])
        reserve_date = data[1].split(" ")[0]
        reserve_time = data[1].split(" ")[1]
        obj.reserved_date = create_date_from_string(reserve_date)
        obj.reserved_time = create_time_from_string(reserve_time)
        obj.status = data[3]
        obj.party_size = int(data[4])
        obj.name = data[6]
        obj.phone = data[7]
        obj.notes = data[8]
        obj.legacy_code = create_legacy_code(data)
        obj.duration = DEFAULT_BOOKING_DURATION
        obj.email = UNKNOWN_EMAIL
        obj.save()
        print(obj)
        success.append(obj)
    return success
