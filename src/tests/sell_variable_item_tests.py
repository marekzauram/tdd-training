import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display
from sales_system import ProductCatalogue

class SellVariableItemTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.printer = Printer()
        products = [
            {'price': 7.95, 'tax': 'G', 'barcode': '123'},
            {'price': 10.00, 'tax': 'GP', 'barcode': '321'}
        ]
        self.sales_system = SalesSystem(self.display, self.printer, ProductCatalogue(products))

    def test_empty_total(self):
        self.sales_system.on_total()
        self.assertEquals('Total: EUR 0.00', self.display.text)

    def test_two_item_sale(self):
        self.sales_system.on_barcode('321')
        self.assertEquals('EUR 10.00 GP', self.display.text) # 1.30  tax
        self.sales_system.on_barcode('123')
        self.assertEquals('EUR 7.95 G', self.display.text)   # 0.636 tax 
        self.sales_system.on_total()
        self.assertEquals('Total: EUR 19.89', self.display.text)  # rounded up
        
if __name__ == '__main__':
    unittest.main()
