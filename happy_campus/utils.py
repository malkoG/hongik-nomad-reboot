"""
require "nokogiri"

module NomadicCrawler
  class CurriculumParser
    attr_accessor :year, :semester, :course_code, :course_division, :is_vacation, :parsed_information

    def initialize(**options)
      @year               = options[:year]
      @semester           = options[:semester]
      @course_code        = options[:course_code]
      @course_division    = options[:course_division]
      @is_vacation        = false
      @parsed_information = nil

      query  = { yy: @year, hakgi: @semester, haksu: @course_code, bunban: @course_division }.to_query
      @source = "#{ENV['CURRICULUM_SITE_BASE']}?#{query}"
    end

    def request_for_course
      @is_vacation = @semester > 2
      doc = Nokogiri.HTML(open(@source))
      
      @parsed_information = parse_syllabus(doc)
    end

    protected
      def parse_syllabus(doc)
        title      = doc.xpath("/html/body/table[1]/tr[2]/td[2]/text()[1]").text.strip
        instructor = doc.xpath("/html/body/table[1]/tr[5]/td[2]").text.strip
        classrooms = doc.xpath("/html/body/table[1]/tr[4]/td[4]").text.strip
        schedule   = doc.xpath("/html/body/table[1]/tr[3]/td[6]").text.strip

        return { 
          title: title, 
          course_code: @course_code,
          is_vacation: @is_vacation, 
          classrooms: classrooms, 
          instructor: instructor, 
          schedule: schedule
        } 
      end
  end
end
"""

"""
require "selenium-webdriver"
require "nokogiri"
require "scanf"

module NomadicCrawler
  class Crawler
    SLEEP_TIME=2

    attr_reader :target_site
    attr_accessor :driver, :year, :semester

    def initialize(target_site)
      @target_site = target_site

      options = Selenium::WebDriver::Chrome::Options.new
      options.add_argument('--headless')
      @driver = Selenium::WebDriver.for :chrome, options: options
      
      @driver.navigate.to @target_site
    end

    def fill_in_the_form
      select_tag = Selenium::WebDriver::Support::Select.new(@driver.find_element tag_name: 'select')
      select_tag.select_by(:index, 1)
      year, semester = select_tag.selected_options[0].property(:value).scanf "%4d%1d"

      checkbox_xpath = '//*[@id="select_abeek"]/tbody/tr[2]/td/form/input[2]'
      checkbox    = @driver.find_element xpath: checkbox_xpath
      checkbox.click
      sleep(SLEEP_TIME)

      radio_xpath  = '//*[@id="select_abeek"]/tbody/tr[2]/td/form/input[4]'
      radio_button = @driver.find_element xpath: radio_xpath
      radio_button.click
      sleep(SLEEP_TIME)

      @year = year
      @semester = semester
    end

    def crawl_courses_list(course_category_info)
      courses_list = []
      
      response = HTTParty.post(ENV['COURSE_LIST_SITE'], query: course_category_info)
      html_doc = Nokogiri.HTML(response.body)
      course_codes_list = html_doc.css("#select_list tr > td:nth-child(#{((11..13).include? course_category_info[:p_grade]) ? 6 : 5})").map do |html|
        course_id = html.text.strip
        return {} if course_id.empty? 
        course_code, course_division = course_id.split '-'
        { course_code: course_code, course_division: course_division }
      end

      return course_codes_list
    end

    def parse_abstruse_link(text)
      campus, category, department, grade = text.scanf "javascript:gocn4001(%d,%d,'%[^']',%d)"
      return {
        p_yy: @year,
        p_hakgi: @semester,
        p_campus: campus,
        p_gubun: category,
        p_dept: department,
        p_grade: grade,
        p_abeek: 1,
        p_2014: "on",
        p_2016: 2016
      }
    end

    def request_latest_semester_curriculum
      submit_xpath = '//*[@id="select_abeek"]/tbody/tr[2]/td/form/input[7]'
      submit_button = @driver.find_element xpath: submit_xpath
      submit_button.click

      sleep(SLEEP_TIME)

      element = @driver.find_element id: 'table_seoul'
      html_doc = Nokogiri.HTML(@driver.page_source)
      course_category_parameters = html_doc.css("#table_seoul > tbody > tr > td > a").map do |html|
        parse_abstruse_link html.attr('href')
      end      

      courses_list = []
      course_category_parameters.each do |course_category|
        crawled_list = crawl_courses_list(course_category)
        courses_list.concat crawled_list
      end
      
      course_informations = courses_list.map do |course|
        course_summary_info = { 
          year: @year,
          semester: @semester,
          course_code: course[:course_code], 
          course_division: course[:course_division]
        }
        
        @parser = CurriculumParser.new(**course_summary_info)
        @parser.request_for_course
      end

      result = course_informations.map(&:to_s)
      result.each { |s| puts s }
      result = result.join('\n')
      path = Rails.root+"/tmp/courses.txt"
      File.open path, "w" do |f|
        f.write result
      end

      return course_informations
    end
  end
end
"""
