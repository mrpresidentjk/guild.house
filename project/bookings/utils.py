# -*- coding: utf-8 -*-
from . import settings
import datetime


def generate_times():
    time_list = []
    interval = settings.BOOKING_INTERVAL
    this_time = datetime.datetime.combine(datetime.date.today(),
                                          settings.BOOKING_TIMES[0])-interval

    while this_time<=datetime.datetime.combine(datetime.date.today(),
            settings.BOOKING_TIMES[1])-interval:
            this_time = this_time+interval
            time_list.append("{}:{:0>2}".format(this_time.hour,
                                                this_time.minute))
    return time_list
