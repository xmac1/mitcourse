import bs4
import argparse
import re

class Course():
    noPattern  = re.compile(r'[A-Z]*(6\.[0-9]*)[A-Z]*')
    namePattern = re.compile(r'\s*([a-zA-Z]|\b)*\n\b*(\(*\))')
    def __init__(self, courseNo, courseName, courseLink=None):
        self.courseNo = courseNo
        self.courseName = courseName
        self.courseLink = courseLink
    def __str__(self):
        return "course no: {1}, course title: {2}".format(self.courseNo, self.courseName)
        

with open('course.html', encoding='utf8') as fd:
    soup = bs4.BeautifulSoup(fd, 'html5lib')




tag : bs4.Tag = soup.find(class_="courseListRow")
courseNumCol : bs4.Tag = tag.find(class_="courseNumCol")
courseNum = courseNumCol.find("a")
courseTitleCol : bs4.Tag = tag.find(class_="courseTitleCol")
courseTitle = courseTitleCol.find("a")
course = Course(courseNo=courseNum.get_text(strip=True), courseName=courseTitle.get_text(strip=True))
print(course)