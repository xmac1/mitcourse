import bs4
import argparse
import re

class Version():
    def __init__(self, version):
        self.value = version
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        sv = self.value.split(' ')[-1]
        ov = other.value.split(' ')[-1]
        return sv > ov
    def __ge__(self, other):
        sv = self.value.split(' ')[-1]
        ov = other.value.split(' ')[-1]
        return sv >= ov
    def __lt__(self, other):
        sv = self.value.split(' ')[-1]
        ov = other.value.split(' ')[-1]
        return sv < ov
    def __le__(self, other):
        sv = self.value.split(' ')[-1]
        ov = other.value.split(' ')[-1]
        return sv <= ov
    def __str__(self):
        return self.value.split(' ')[-1]
    @property
    def version(self):
        return int(self.value.split(' ')[-1])

class Course():
    noPattern  = re.compile(r'[A-Z]*(6.[A-Z]*[0-9]*)[A-Z]*')
    namePattern = re.compile(r'^([a-zA-Z0-9_:,\+\-\./ ]*)\s*\((.*)\)')
    def __init__(self, courseNo, courseName, courseLink=None):
        self.courseNo = Course.noPattern.match(courseNo).group(1)
        match = Course.namePattern.search(courseName)
        self.courseName = match.group(1)
        self.courseLink = courseLink
        self.version = Version(match.group(2)) 
    def __str__(self):
        return "course no: {0}, course title: {1}, version: {2}".format(self.courseNo, self.courseName, self.version)
        

with open('course.html', encoding='utf8') as fd:
    soup = bs4.BeautifulSoup(fd, 'html5lib')




tag : bs4.Tag = soup.find(class_="courseListRow")
courseDict = {}
while True:
    if tag == None:
        break
    courseNumCol : bs4.Tag = tag.find(class_="courseNumCol")
    courseNum = courseNumCol.find("a")
    courseTitleCol : bs4.Tag = tag.find(class_="courseTitleCol")
    courseTitle = courseTitleCol.find("a")
    course = Course(courseNo=courseNum.get_text(strip=True), courseName=courseTitle.get_text(strip=True))
    print(course)
    tag = tag.find_next_sibling(class_="courseListRow")
    if not course. in courseDict:

    

    