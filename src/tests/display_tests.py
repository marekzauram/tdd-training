import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display

class DisplayTests(unittest.TestCase):
    def test_display_item(self):
        display = Display()
        display.display_item(25.1, 'G')
        self.assertEquals('EUR 25.10 G', display.text)
    
    def test_display_total(self):
        display = Display()
        display.display_total(33.334)
        self.assertEquals('Total: EUR 33.33', display.text)

    def test_printout(self):
        display = Display()
        display.text = 'i must be deleted after printout'
        display.print_out(False)
        self.assertEquals(display.text, '')
        
if __name__ == '__main__':
    unittest.main()
