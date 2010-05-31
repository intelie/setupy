import sys
argv = sys.argv
sys.argv = [argv[0]]
import unittest
from setupy import ini_parse


class TestIniParser(unittest.TestCase):
    section = 'mysqld'
    option = 'default-storage-engine'
    value = 'InnoDB'

    def do_test(self, input_, output):
        real_output = ini_parse(input_, self.section, self.option, self.value)
        self.assertEqual(output, real_output)


    def test_empty_file(self):
        input_ = ''
        output = '\n[mysqld]\ndefault-storage-engine = InnoDB'
        self.do_test(input_, output)


    def test_file_with_only_one_empty_section(self):
        input_ = '[mysqld]'
        output = '[mysqld]\ndefault-storage-engine = InnoDB'
        self.do_test(input_, output)


    def test_file_with_only_one_section(self):
        input_ = '[mysqld]\nae = bc\nqwe'
        output = '[mysqld]\ndefault-storage-engine = InnoDB\nae = bc\nqwe'
        self.do_test(input_, output)


    def test_file_with_two_sections(self):
        input_ = '[bla]\na = b\nc\n\n[mysqld]\ne = f\nsadf'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf'
        self.do_test(input_, output)
        
    
    def test_file_with_three_sections_with_required_on_the_middle_and_dont_have_required_option(self):
        input_ = '[bla]\na = b\nc\n\n[mysqld]\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        self.do_test(input_, output)


    def test_file_with_three_sections_with_required_on_the_middle_and_have_required_option(self):
        input_ = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = MyISAM\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        self.do_test(input_, output)


    def test_try_to_read_a_section_that_does_not_exist_and_get_None(self):
        input_ = ''
        output = None
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_try_to_read_a_section_that_exists_but_option_dont_and_get_None(self):
        input_ = '[mysqld]\nsome-option = some-value'
        output = None
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_when_read_a_section_and_option_that_exist_should_return_correct_value(self):
        input_ = '[%s]\n%s = %s' % (self.section, self.option, self.value)
        output = self.value
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_when_read_a_section_and_option_that_exist_should_return_correct_value_using_no_spaces_between_option_and_value(self):
        input_ = '[%s]\n%s=%s' % (self.section, self.option, self.value)
        output = self.value
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_when_read_a_section_and_option_in_mysql_cnf_format_that_exist_should_return_True(self):
        input_ = '[%s]\n%s' % (self.section, self.option)
        output = True
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_when_read_a_section_and_option_in_mysql_cnf_format_that_exist_should_return_True_in_multisection_file(self):
        input_ = '[bar]\nfoo = baz\n[%s]\n%s\n[foo]\nbar = baz' % \
                 (self.section, self.option)
        output = True
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


    def test_when_read_a_section_and_option_in_mysql_cnf_format_that_exist_should_return_True_in_multisection_file_and_multioption_section(self):
        input_ = '[bar]\nfoo = baz\n[%s]\nbar = baz\n%s\ncruft = kruft\n[foo]\nbar = baz' % \
                 (self.section, self.option)
        output = True
        self.assertEqual(ini_parse(input_, self.section, self.option), output)


unittest.main()
