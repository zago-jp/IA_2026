import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        list = ["", "", "" , ""]
        for i in range(len(list)+1):
            print(i)



if __name__ == '__main__':
    unittest.main()
