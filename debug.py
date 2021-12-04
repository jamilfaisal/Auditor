import pandas as pd
from CourseDataCollector import CourseDataCollector
from utils import get_relevant_time_information, filter_database, filter_courses
from timeit import default_timer as timer

# Debug: Test commands in console

# Update command
start = timer()
course_data = CourseDataCollector()
course_data.get_data()
end = timer()
print("Time elapsed for update command:", end-start, " seconds")

# Check command
start = timer()
df = pd.read_json('course_data/2021-2022.json')
weekday, section, hour = get_relevant_time_information()
weekday = "FR"  # MO, TU, WE, TH, FR
hour = "15:00"  # 24-time format
filtered_df = filter_database(df, weekday, section.value, hour)
courses = filter_courses(filtered_df, weekday, hour)
if len(courses) == 0:
    print("No lectures found...")
for course in courses:
    print(course.format_course())
end = timer()
print("Time elapsed for check command:", end-start, " seconds")
print("Number of courses found:", len(courses), " courses")
