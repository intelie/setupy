import unittest
from setupy import ini_parse


class TestIniParser(unittest.TestCase):
    section = 'mysqld'
    option = 'default-storage-engine'
    value = 'InnoDB'

    def do_test(self, input, output):
        real_output = ini_parse(input, self.section, self.option, self.value)
        self.assertEqual(output, real_output)


    def test_empty_file(self):
        input = ''
        output = '\n[mysqld]\ndefault-storage-engine = InnoDB'
        self.do_test(input, output)


    def test_file_with_only_one_empty_section(self):
        input = '[mysqld]'
        output = '[mysqld]\ndefault-storage-engine = InnoDB'
        self.do_test(input, output)


    def test_file_with_only_one_section(self):
        input = '[mysqld]\nae = bc\nqwe'
        output = '[mysqld]\ndefault-storage-engine = InnoDB\nae = bc\nqwe'
        self.do_test(input, output)


    def test_file_with_two_sections(self):
        input = '[bla]\na = b\nc\n\n[mysqld]\ne = f\nsadf'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf'
        self.do_test(input, output)
        
    
    def test_file_with_three_sections_with_required_on_the_middle_and_dont_have_required_option(self):
        input = '[bla]\na = b\nc\n\n[mysqld]\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        self.do_test(input, output)


    def test_file_with_three_sections_with_required_on_the_middle_and_have_required_option(self):
        input = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = MyISAM\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        output = '[bla]\na = b\nc\n\n[mysqld]\ndefault-storage-engine = InnoDB\ne = f\nsadf\n\n[qwe]\nasdf = 123'
        self.do_test(input, output)


if __name__ == '__main__':
    unittest.main()
