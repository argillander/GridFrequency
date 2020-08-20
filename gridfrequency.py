""" GridFrequency obtains the current frequency of the Swedish power grid.
See https://www.svk.se/drift-av-stamnatet/kontrollrummet/


Author: Joakim Argillander [http://github.com/argillander]
"""
import requests as req
import json
import time
import math

URL = "http://driftsdata.statnett.no/restapi/Frequency/BySecondWithXY?FromInTicks={}&ToInTicks={}"
URL2 = "https://www.svk.se/Proxy/Proxy/?a=http://driftsdata.statnett.no/restapi/Frequency/BySecondWithXY?FromInTicks={" \
      "}&ToInTicks={} "

""" API URL. Unofficial URL as reverse-engineered from the Swedish National Grid's data aggregation website """


def getCurrentTimeStamp():
    return math.floor(time.time() * 1000.0)


def getCurrentFrequency(last_time_stamp=0):
    """
    Retrieves current frequency of the national grid. Parameter last_last_time_stamp optional.
    If omitted or set to 0, returns all possible frequency measurements
    """
    f_url = URL.format(last_time_stamp, getCurrentTimeStamp())
    res = req.get(f_url)
    if res.ok:
        js = json.loads(res.content)
        arr = js["Measurements"]
        cur_phase = arr[len(arr) - 1]
        return cur_phase[0], cur_phase[1]
    else:
        print("ERR: " + res.content)


def pollGridFrequency(callback=None, poll_period=0.5, notify_only_if_freq_changed=True):
    """
    Returns new grid frequency with callback
    """
    last_freq = 0
    last_time_stamp = 0
    while True:
        last_time_stamp, cur_freq = getCurrentFrequency(last_time_stamp)
        if (not notify_only_if_freq_changed) or (cur_freq != last_freq):
            last_freq = cur_freq
            if not callback:
                print("Current grid frequency: {} Hz".format(cur_freq))
            else:
                callback(cur_freq)
        time.sleep(poll_period)


# --- EXAMPLE USAGE BELOW ---

# pollGridFrequency(notify_only_if_freq_changed=False)
""" Polls every 0.5s [default], only printing result [default]. Calls callback only if value changed [default]"""

# pollGridFrequency(my_callback, 0.1)
""" Polls with custom callback function my_callback taking ONE argument (frequency). I.e. my_callback(freq) is called. 
Custom refresh rate """

#pollGridFrequency(None, 1, False)
""" No callback (prints values only), polling every 2s and returning values regardless of whether they have changed. """

# print("This is freq: " + str(getCurrentFrequency()[1]))
""" Single-capture frequency. """



if __name__ == "__main__":
    try:
        pollGridFrequency(None, 1, False)
        # pollGridFrequency(notify_only_if_freq_changed=False)
        # pollGridFrequency(my_callback, 0.1)
        # print("This is freq: " + str(getCurrentFrequency()[1]))

    except(KeyboardInterrupt):
        print("Exiting GridFrequency Demo...")
        exit(0)
