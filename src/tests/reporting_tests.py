import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display

class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.products = [
            {'price': 20.00, 'tax': 'G',  'barcode': '6666'},
            {'price': 10.00, 'tax': 'GP', 'barcode': '5555'},
        ]
        self.display = Display()
        self.printer = Printer()
        self.current_time = '2013-12-01 12:13'
        self.sales_system = SalesSystem(self.display, self.printer, self.products)

    def test_empty_report(self):
        sales_system = SalesSystem(None, None, None)
        current_time = '2013-01-01 12:13'
        self.assertEquals(sales_system.get_sales_report(current_time),
            'Sales report at %s' % current_time         + '\n' +
            '"Date", "Subtotal", "GST", "PST", "Total"' + '\n' +
            '"Total", "0.00", "0.00", "0.00", "0.00"'   + '\n'
        )

    def test_one_sale_report(self):
        self.sales_system.on_barcode('6666')
        self.sales_system.save_sale(self.current_time)
        self.assertEquals(self.sales_system.get_sales_report(self.current_time),
            'Sales report at %s' % self.current_time         + '\n' +
            '"Date", "Subtotal", "GST", "PST", "Total"' + '\n' +
            '"%s", "%.2f", "%.2f", "%.2f", "%.2f"' % (self.current_time, 20.00, 1.60, 0.0, 21.60) + '\n' +
            '"Total", "20.00", "1.60", "0.00", "21.60"' + '\n'
        )
        
    def test_triple_sale_report(self):
        self.sales_system.on_barcode('6666')
        self.sales_system.save_sale(self.current_time)
        self.sales_system.on_barcode('5555')
        self.sales_system.save_sale(self.current_time)
        self.sales_system.on_barcode('5555')
        self.sales_system.save_sale(self.current_time)
        self.assertEquals(self.sales_system.get_sales_report(self.current_time),
            'Sales report at %s' % self.current_time         + '\n' +
            '"Date", "Subtotal", "GST", "PST", "Total"' + '\n' +
            '"%s", "%.2f", "%.2f", "%.2f", "%.2f"' % (self.current_time, 20.00, 1.60, 0.0, 21.60) + '\n' +
            '"%s", "%.2f", "%.2f", "%.2f", "%.2f"' % (self.current_time, 10.00, 0.80, 0.50, 11.30) + '\n' +
            '"%s", "%.2f", "%.2f", "%.2f", "%.2f"' % (self.current_time, 10.00, 0.80, 0.50, 11.30) + '\n' +
            '"Total", "40.00", "3.20", "1.00", "44.20"' + '\n'
        )
        
if __name__ == '__main__':
    unittest.main()
