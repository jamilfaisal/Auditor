class Course:

    def __init__(self, courseId: int, org: str, orgName: str, courseTitle: str, courseCode: str, section: str,
                 breadthCategory: str, distributionCategory: str, meetings: dict, weekday: str, hour: str):
        self.courseId = courseId
        self.org = org
        self.orgName = orgName
        self.courseTitle = courseTitle
        self.courseCode = courseCode
        self.section = section
        if breadthCategory == "":
            self.breadthCategory = "None"
        else:
            self.breadthCategory = breadthCategory
        self.distributionCategory = distributionCategory
        self.meetings = self.filter_meetings(meetings, weekday, hour)

    # TODO: Optimize this function by adding new columns to dataset in CourseDataCollector
    def filter_meetings(self, meetings, weekday, hour):
        filtered_meetings = []
        for lecture in meetings:
            # TODO: Remove once tutorials are removed from dataset
            if not lecture.startswith("LEC"):
                continue
            for meeting_day_code in meetings[lecture]["schedule"]:
                start_time = meetings[lecture]["schedule"][meeting_day_code]["meetingStartTime"]
                meetingDay = meetings[lecture]["schedule"][meeting_day_code]["meetingDay"]
                assignedRoom1 = meetings[lecture]["schedule"][meeting_day_code]["assignedRoom1"]
                assignedRoom2 = meetings[lecture]["schedule"][meeting_day_code]["assignedRoom1"]
                if start_time == hour and meetingDay == weekday and (assignedRoom1 != "" or assignedRoom2 != ""):
                    actualEnrolment = meetings[lecture]["actualEnrolment"]
                    enrollmentCapacity = meetings[lecture]["enrollmentCapacity"]
                    instructors = meetings[lecture]["instructors"]
                    meetingEndTime = meetings[lecture]["schedule"][meeting_day_code]["meetingEndTime"]
                    assignedRooms = self.get_assigned_rooms(assignedRoom1, assignedRoom2)
                    filtered_meetings.append(Meeting(lecture, actualEnrolment, enrollmentCapacity, instructors,
                                                     meetingDay, start_time, meetingEndTime, assignedRooms))
        return filtered_meetings

    def format_course(self):
        result = """
        =====================================================
        **{}: {}**
        {}
        Breadth: {}
        Distribution: {}
        Meetings:""".format(self.courseCode, self.courseTitle, self.orgName, self.breadthCategory,
                            self.distributionCategory)
        for meeting in self.meetings:
            result += meeting.format_meeting()
        return result

    @staticmethod
    def get_assigned_rooms(assignedRoom1, assignedRoom2):
        if assignedRoom1 == "":
            assignedRooms = assignedRoom2
        elif assignedRoom2 == "":
            assignedRooms = assignedRoom1
        elif assignedRoom1 == assignedRoom2:
            assignedRooms = assignedRoom1
        else:
            assignedRooms = [assignedRoom1, assignedRoom2]
        return assignedRooms


class Meeting:

    def __init__(self, lectureCode, actualEnrolment, enrollmentCapacity, instructors, meetingDay, meetingStartTime,
                 meetingEndTime, assignedRooms):
        self.lectureCode = lectureCode
        self.actualEnrolment = actualEnrolment
        self.enrollmentCapacity = enrollmentCapacity
        self.instructors = instructors
        self.meetingDay = meetingDay
        self.meetingStartTime = meetingStartTime
        self.meetingEndTime = meetingEndTime
        self.assignedRooms = assignedRooms

    def format_meeting(self):
        result = """
        {}: {}, {}-{}, Room: {}""".format(self.lectureCode, self.meetingDay, self.meetingStartTime,
                                          self.meetingEndTime, self.assignedRooms)
        return result
