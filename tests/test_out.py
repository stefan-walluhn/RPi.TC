#import unittest
#from rpitc.io.out import Out
#
#class OutTest(unittest.TestCase):
#
#    def test_out(self):
#        out = Out()
#        self.assertIsInstance(out, Out)
#
#
#if __name__ == "__main__":
#    unittest.main()

from rpitc.io.out import Out

class TestOut:
	def test_init(self):
	    out = Out()
	    assert isinstance(out, Out)
