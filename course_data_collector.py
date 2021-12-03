import requests
import os


class CourseDataCollector:

    url = "https://timetable.iit.artsci.utoronto.ca/api/20219/courses"
    year = "2021-2022"

    def __init__(self, org=None, code=None, section=None, studyyear=None, daytime=None, weekday=None, prof=None, breadth=None, waitlist=None, available=None, fyfcourse=None, title=None):
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
        file_path = os.path.join("course_data", self.year + ".json")
        with open(file_path, 'wb') as f:
            f.write(r.content)


course_data = CourseDataCollector()
course_data.get_data()
