from django.test import TestCase

# Create your tests here.

"""
require 'test_helper'
require 'nokogiri'

module NomadicCrawler
    class CurriculumParserTest < ActiveSupport::TestCase
        def setup
            course_info = {year: 2018, semester: 6, course_code: "002551", course_division: 1}
            cyberlecture_info = {year: 2018, semester: 6, course_code: "002060", course_division: 1}
            @curriculum_parser   = CurriculumParser.new(**course_info)
            @cyberlecture_parser = CurriculumParser.new(**cyberlecture_info)
        end

        test '생성자가 제대로 돌아감' do
            assert_equal @curriculum_parser.year,        2018
            assert_equal @curriculum_parser.semester,    6
            assert_equal @curriculum_parser.course_code, "002551"
        end

        test '강의 제목/강의실이 틀리지 않음' do 
            @curriculum_parser.request_for_course
            assert_equal @curriculum_parser.parsed_information[:title], "논리와사고"
            assert_equal @curriculum_parser.parsed_information[:classrooms], "C809"
        end        

        test '사이버강좌는 강의실이 없음' do
            @cyberlecture_parser.request_for_course
            assert_empty @cyberlecture_parser.parsed_information[:classrooms]
        end
    end
end
"""

"""
require 'test_helper'
require 'selenium-webdriver'
require 'nokogiri'

module NomadicCrawler
    class CrawlerTest < ActiveSupport::TestCase
        def setup
            @crawler = Crawler.new(ENV['TARGET_SITE'])
        end

        test 'fill in the form' do
            @crawler.fill_in_the_form

            assert true # 최근 학기를 선택했는지
            assert true # 언제 입학했는지 체크
            assert true # 어떤 종류의 학생인지 체크
        end

        test 'Check if Successfully parsed' do
            @crawler.fill_in_the_form

            result = @crawler.parse_abstruse_link "javascript:gocn4001(1,2,'A101',0)"
            assert_equal result[:p_campus], 1
            assert_equal result[:p_gubun], 2
            assert_equal result[:p_dept], "A101"
            assert_equal result[:p_grade], 0
        end        

        test 'Get Latest Semester' do
            @crawler.fill_in_the_form

            courses = @crawler.request_latest_semester_curriculum
            assert_not_empty courses
        end

        test '강의 목록을 제대로 긁어왔는지 검사' do
            semester_info = {
                p_yy: 2018,
                p_hakgi: 6,
                p_campus: 1,
                p_gubun: 1,
                p_dept: "0001",
                p_grade: 16,
                p_abeek: 1,
                p_2014: "on",
                p_2016: 2016
            }

            assert_equal @crawler.crawl_courses_list(semester_info).size, 3
        end
    end
end
"""
