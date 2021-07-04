import json
import os
import sys
import urllib
from urllib.parse import urlencode
import datetime
import requests

USERNAME = os.getenv('USERNAME', None)
PASSWORD = os.getenv('PASSWORD', None)
CLUB_ID = os.getenv('CLUB_ID', None)
TRAINING_NAME = os.getenv('TRAINING_NAME', None)

HEADERS = {
    'content-type': 'application/json',
    'platform': 'members',
    'with-cookie': 'true',
    'Accept': '*/*',
    'version-check-bypass': 'true',
}


def get_auth_cookie():
    """
    Login on clubconnect.fr and get an auth cookie
    :return: cookie
    """
    data = {"email": USERNAME,
            "password": PASSWORD}
    data_encoded = json.dumps(data)
    response = requests.post('https://members.clubconnect.fr/api/mobile/session',
                             headers=HEADERS,
                             data=data_encoded)
    if response.status_code != 201:
        print("Authentication failed")
        sys.exit(0)
    print("Authentication ok")
    return response.cookies


def get_two_next_training_date():
    """
    return a dict with next Monday and Thursday training

    E.g
    {'monday': 'Mon Jul 05 2021', 'thursday': 'Thu Jul 08 2021'}
    :return:
    """
    returned_dict = dict()
    today = datetime.date.today()

    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    print("Next Monday: {}".format(next_monday))
    formatted_next_monday = next_monday.strftime("%a %b %d %Y")
    returned_dict["monday"] = formatted_next_monday

    next_thursday = today + datetime.timedelta(days=3-today.weekday(), weeks=1)
    print("Next Thursday: {}".format(next_thursday))
    formatted_next_thursday = next_thursday.strftime("%a %b %d %Y")
    returned_dict["thursday"] = formatted_next_thursday
    return returned_dict


def get_trainings_id_from_date(cookies, date):
    date_min_with_time = "{} 00:00:00 GMT+0200".format(date)
    date_max_with_time = "{} 23:59:59 GMT+0200".format(date)
    date_min_encoded = urllib.parse.quote(date_min_with_time)
    date_max_encoded = urllib.parse.quote(date_max_with_time)
    url = "https://members.clubconnect.fr/api/mobile/seance?clubs={}&date_min={}&date_max={}"
    url_with_encoded_parameters = url.format(CLUB_ID, date_min_encoded, date_max_encoded)
    response = requests.get(url_with_encoded_parameters,
                            headers=HEADERS,
                            cookies=cookies)
    payload = response.json()

    # try to find the right training from the name:
    for course in payload:
        if course["name"] == TRAINING_NAME:
            return course
    return None


def book_course(cookie, course):
    if not course["bookable"]["enabled"]:
        print("Training is not bookable")
        return

    if "booking" in course:
        if not course["booking"]["waiting"]:
            print("Training already booked for date '{}'".format(course["dates"]["starts"]["iso"]))
            return

    data = {
        "seance": {
            "id": course["id"]
        },
        "waiting": False
    }

    data_encoded = json.dumps(data)
    response = requests.post("https://members.clubconnect.fr/api/mobile/booking",
                             headers=HEADERS,
                             data=data_encoded,
                             cookies=cookie)
    if response.status_code != 201:
        print("Booking failed for date {}".format(course["dates"]["starts"]["iso"]))
        return
    print("Training successfully booked for date {}".format(course["dates"]["starts"]["iso"]))


def main():
    cookie = get_auth_cookie()
    next_dates = get_two_next_training_date()
    next_monday_course = get_trainings_id_from_date(cookies=cookie,
                                                    date=next_dates["monday"])
    book_course(cookie, next_monday_course)

    next_thursday_course = get_trainings_id_from_date(cookies=cookie,
                                                      date=next_dates["thursday"])
    book_course(cookie, next_thursday_course)


if __name__ == '__main__':
    main()
