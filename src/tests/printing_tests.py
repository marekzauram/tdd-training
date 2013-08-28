import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display
from sales_system import ProductCatalogue

class PrintingTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.printer = Printer()
        
    def test_print_receipt_one_item(self):
        self.sales_system = SalesSystem(self.display, self.printer, ProductCatalogue([{'price': 10.00, 'tax': 'G', 'barcode': '777'}]))
        self.sales_system.on_barcode('777')
        self.sales_system.on_print()
        self.assertEquals(self.printer.content,
            '777 10.00 G'    + '\n' +
            'Subtotal 10.00' + '\n' +
            'GST 0.80'       + '\n' +
            'PST 0.00'       + '\n' +
            'Total: 10.80'   + '\n'
        )
        
    def test_print_receipt_zero_items(self):
        products = [
            {'price': 20.00, 'tax': 'G',  'barcode': '6666'},
        ]
        self.sales_system = SalesSystem(self.display, self.printer, ProductCatalogue(products))
        self.sales_system.on_print()
        self.assertEquals(self.printer.content,
            'Subtotal 0.00' + '\n' +
            'GST 0.00'      + '\n' +
            'PST 0.00'      + '\n' +
            'Total: 0.00'   + '\n'
        )

    def test_print_receipt_three_items(self):
        products = [
            {'price': 20.00, 'tax': 'G',  'barcode': '6666'},
            {'price': 10.00, 'tax': 'GP', 'barcode': '5555'}
        ]
        self.sales_system = SalesSystem(self.display, self.printer, ProductCatalogue(products))
        self.sales_system.on_barcode('6666')
        self.sales_system.on_barcode('6666')
        self.sales_system.on_barcode('5555')
        self.sales_system.on_print()
        self.assertEquals(self.printer.content,
            '6666 20.00 G'    + '\n' +
            '6666 20.00 G'    + '\n' +
            '5555 10.00 GP'   + '\n' +
            'Subtotal 50.00'  + '\n' +
            'GST 4.00'        + '\n' +
            'PST 0.50'        + '\n' +
            'Total: 54.50'    + '\n'
        )

    def test_reset_by_printing(self):
        products = [
            {'price': 20.00, 'tax': 'G',  'barcode': '6666'},
        ]
        self.sales_system = SalesSystem(self.display, self.printer, ProductCatalogue(products))
        self.sales_system.on_barcode('6666')
        self.sales_system.on_print()
        self.sales_system.on_print()
        self.assertEquals(self.printer.content,
            'Subtotal 0.00' + '\n' +
            'GST 0.00'      + '\n' +
            'PST 0.00'      + '\n' +
            'Total: 0.00'   + '\n'
        )
    
    def test_printout(self):
        self.printer.content = 'i must be deleted after printout'
        self.printer.print_out(False)
        self.assertEquals(self.printer.content, '')
        
if __name__ == '__main__':
    unittest.main()
