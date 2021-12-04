from datetime import datetime, timedelta
from enum import Enum
import pandas as pd

from Course import Course

"""Data for Retrieving Time Information"""
# Order matters for lookup (based on Python's convention for weekday (Ex: 0 -> Monday, etc...)
weekday_translate = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


class Section(Enum):
    FALL = "F"
    WINTER = "S"
    SUMMER = None


section_translate = {
    "Jan": Section.WINTER,
    "Feb": Section.WINTER,
    "Mar": Section.WINTER,
    "Apr": Section.WINTER,
    "May": Section.SUMMER,
    "Jun": Section.SUMMER,
    "Jul": Section.SUMMER,
    "Aug": Section.SUMMER,
    "Sep": Section.FALL,
    "Oct": Section.FALL,
    "Nov": Section.FALL,
    "Dec": Section.FALL
}

"""Functions for Retrieving Time Information"""


def get_relevant_time_information():
    now = datetime.now()
    # Weekday
    weekday = get_weekday(now)
    # Section
    section = get_section(now)
    # Next nearest hour
    next_nearest_hour = get_next_nearest_hour(now)
    return weekday, section, next_nearest_hour


def get_weekday(time: datetime):
    weekday = time.weekday()
    return weekday_translate[weekday]


def get_section(time: datetime):
    month_name = time.strftime("%b")
    return section_translate[month_name]


def get_next_nearest_hour(time: datetime):
    next_nearest_hour_time = time.replace(second=0, microsecond=0, minute=0, hour=time.hour) + \
                             timedelta(hours=time.minute // 30)
    return next_nearest_hour_time.strftime("%H:%M")


"""Functions for filtering UofT database"""


def filter_database(dataset: pd.DataFrame, weekday: str, section: str, hour: str):
    # Filter by section
    dataset = dataset.drop(dataset[(dataset.section != section) & (dataset.section != 'Y')].index)
    # Filter by times
    dataset = dataset[dataset.apply(lambda row: check_weekday_and_hour(row, weekday, hour), axis=1)]
    return dataset


def check_weekday_and_hour(row, weekday, hour):
    result = False
    for time in row["meeting_times"]:
        if time[0] == weekday and time[1] == hour:
            return True
    return result


def filter_courses(database: pd.DataFrame, weekday: str, hour: str):
    courses = []
    for index, row in database.iterrows():
        course = Course(row["courseId"], row["org"], row["orgName"], row["courseTitle"], row["code"],
                        row["section"], row["breadthCategories"], row["distributionCategories"],
                        dict(row["meetings"]), weekday, hour)
        # Final filter for courses with no valid meetings
        if len(course.meetings) != 0:
            courses.append(course)
    return courses
