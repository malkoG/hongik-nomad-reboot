import os

from lxml import html
from urllib.parse import urlencode

class CurriculumParser:
    
    def __init__(self, **options):
        self.year               = options['year']
        self.semester           = options['semester']
        self.course_code        = options['course_code']
        self.course_division    = options['course_division']
        self.is_vacation        = False
        self.parsed_information = None

        query_dict = {
            'yy': self.year,
            'hakgi': self.semester, 
            'haksu': self.course_code,
            'bunban': self.course_division,
        }

        self.source = "{}?{}".format(CURRICULUM_SITE_BASE, urlencode(query_dict))

    def request_for_course(self):
        self.is_vacation = self.semester > 2
        res      = requests.get(self.source) 
        dom_tree = html.fromstring(res.text)

        self.parsed_information = _parse_syllabus(doc)

    def _parse_syllabus(self, dom_tree):
        title      = dom_tree.xpath("/html/body/table[1]/tr[2]/td[2]/text()[1]").strip()
        instructor = dom_tree.xpath("/html/body/table[1]/tr[5]/td[2]").strip()
        classrooms = dom_tree.xpath("/html/body/table[1]/tr[4]/td[4]").strip()
        schedule   = dom_tree.xpath("/html/body/table[1]/tr[3]/td[6]").strip()

        return {
            'title': title,
            'course_code': self.course_code,
            'is_vacation': self.is_vacation,
            'classrooms': classrooms,
            'instructor': instructor,
            'schedule': schedule,
        }