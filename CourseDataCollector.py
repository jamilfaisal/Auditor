import requests
import os
import pandas as pd
import numpy as np
from config import settings


class CourseDataCollector:
    url = settings.latest_url
    year = settings.year
    meeting_days_valid_values = ["MO", "TU", "WE", "TH", "FR"]

    # TODO: Set this equal to ["00:00", "01:00", ..., "12:00", "13:00", ..., "23:00"]
    # start_times_valid_values = []

    def __init__(self, org=None, code=None, section=None, studyyear=None, daytime=None, weekday=None, prof=None,
                 breadth=None, waitlist=None, available=None, fyfcourse=None, title=None):
        self.org = org
        self.code = code
        self.section = section
        self.studyyear = studyyear
        self.daytime = daytime
        self.weekday = weekday
        self.prof = prof
        self.breadth = breadth
        self.waitlist = waitlist
        self.available = available
        self.fyfcourse = fyfcourse
        self.title = title

    def get_data(self):
        params = {
            "org": self.org,
            "code": self.code,
            "section": self.section,
            "studyyear": self.studyyear,
            "daytime": self.daytime,
            "weekday": self.weekday,
            "prof": self.prof,
            "breadth": self.breadth,
            "deliverymode": "CLASS",
            "online": None,
            "waitlist": self.waitlist,
            "available": self.available,
            "fyfcourse": self.fyfcourse,
            "title": self.title
        }
        r = requests.get(self.url, params=params)
        # Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()).T

        # Transform dataframe
        self.transform_dataset(df)

        # Save dataframe as json
        file_path = os.path.join("course_data", self.year + ".json")
        df.to_json(file_path)

    def transform_dataset(self, df):
        # Add new column of list of days of meetings
        df["meeting_times"] = df.apply(lambda row: self.extract_meeting_days_and_start_times(row), axis=1)
        # Filter out courses with no times
        df.dropna(subset=["meeting_times"], inplace=True)
        # Sort by course code
        df.sort_values("code", inplace=True)

    def extract_meeting_days_and_start_times(self, row):
        times = []
        lectures = row.get("meetings")
        for lecture in lectures:
            # Exclude non-lectures
            # TODO: Remove tutorials from dataset
            if not lecture.startswith("LEC"):
                continue
            for meeting_day_code in lectures[lecture]["schedule"]:
                meet_day = lectures[lecture]["schedule"][meeting_day_code]["meetingDay"]
                start_time = lectures[lecture]["schedule"][meeting_day_code]["meetingStartTime"]
                if meet_day in self.meeting_days_valid_values and start_time is not None:
                    times.append((meet_day, start_time))
        if len(times) == 0:
            return np.NaN
        return list(set(times))
