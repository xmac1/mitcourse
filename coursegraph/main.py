import bs4
import argparse
import re
import arango
from functools import total_ordering

@total_ordering
class Version():
    def __init__(self, version):
        s = version.split(' ')
        self._value = version
        length = len(s)
        self._semester = None
        self._year = None
        if length == 2:
            self._semester = s[0]
            self._year = s[1]
        elif length == 3:
            self._semester = s[0]
            self._year = s[2]
    
    @property
    def value(self):
        return self._value
    @property
    def semester(self):
        return self._semester
    @property
    def year(self):
        return self._year
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return self.year > other.year
    def __str__(self):
        return "{0.value!s}".format(self)


class Course():
    noPattern  = re.compile(r'[A-Z]*(6.[A-Z]*[0-9]*)[A-Z]*')
    namePattern = re.compile(r'^([a-zA-Z0-9_:,\+\-\./ ]*)\s*\((.*)\)')
    def __init__(self, courseNo, courseName, courseLink=None, prerequisite=None):
        self.courseNo = Course.noPattern.match(courseNo).group(1)
        match = Course.namePattern.search(courseName)
        self.courseName = match.group(1)
        self.courseLink = courseLink
        self.version = Version(match.group(2))
        self.prerequisite = prerequisite
    def __str__(self):
        return "course no: {0}, course title: {1}, version: {2}".format(self.courseNo, self.courseName, self.version)
        

def get_wishlist(addr="127.0.0.1:8529"):
    client = arango.ArangoClient()
    sys_db = client.db(name='_system', username='root', password='Master@2020')
    if not sys_db.has_database('mit'):
        sys_db.create_database('mit')
    course = sys_db.collection('course')
    mit_db = client.db(name='mit', username='root', password='Master@2020')

    if mit_db.has_collection('mit_course'):
        mit_course = mit_db.collection('mit_course')
    else:
        mit_course = mit_db.create_collection('mit_course')

    d = get_courses('coursegraph/course.html')
    for key in course.keys():
        doc = d.get(key, None)
        if not doc is None:
            mit_course.insert({
                '_id': doc.courseNo,
                'name': doc.courseName,
                'version': doc.version.value,
            })

def get_courses(file):
    with open(file, encoding='utf8') as fd:
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
        if not course.courseNo in courseDict:
            courseDict[course.courseNo] = course
        else:
            if course.version > courseDict[course.courseNo].version:
                courseDict[course.courseNo] = course
        tag = tag.find_next_sibling(class_="courseListRow")
    
    return courseDict

if __name__ == "__main__":
    get_wishlist()