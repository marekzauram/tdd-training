import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display

class SellOneItemTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.printer = Printer()
        
        products = [
            {'price': 7.95, 'tax': 'G', 'barcode': '123'},
            {'price': 10.00, 'tax': 'GP', 'barcode': '321'}
        ]
        self.sales_system = SalesSystem(self.display, self.printer, products)

    def test_price_found(self):
        self.sales_system.on_barcode('123')
        self.assertEquals('EUR 7.95 G', self.display.text)

    def test_another_price_found(self):
        self.sales_system.on_barcode('321')
        self.assertEquals('EUR 10.00 GP', self.display.text)

    def test_price_not_found(self):
        self.sales_system.on_barcode('999')
        self.assertEquals('Price not found for barcode "999"', self.display.text)

    def test_empty_barcode(self):
        self.sales_system.on_barcode('')
        self.assertEquals('Scanning error: empty barcode', self.display.text)
    
if __name__ == '__main__':
    unittest.main()
