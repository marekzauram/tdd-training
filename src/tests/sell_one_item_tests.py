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

class SellVariableItemTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.printer = Printer()
        products = [
            {'price': 7.95, 'tax': 'G', 'barcode': '123'},
            {'price': 10.00, 'tax': 'GP', 'barcode': '321'}
        ]
        self.sales_system = SalesSystem(self.display, self.printer, products)

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

class TaxTests(unittest.TestCase):
    def test_g_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'G'), 0.80)

    def test_gp_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'GP'), 1.30)

    def test_p_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'P'), 0.50)

    def test_zero_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, ''), 0.00)

class DisplayTests(unittest.TestCase):
    def test_display_item(self):
        display = Display()
        display.display_item(25.1, 'G')
        self.assertEquals('EUR 25.10 G', display.text)
    
    def test_display_total(self):
        display = Display()
        display.display_total(33.334)
        self.assertEquals('Total: EUR 33.33', display.text)

class PrintingTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.printer = Printer()
        
    def test_print_receipt_one_item(self):
        self.sales_system = SalesSystem(self.display, self.printer, [{'price': 10.00, 'tax': 'G', 'barcode': '777'}])
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
        self.sales_system = SalesSystem(self.display, self.printer, products)
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
        self.sales_system = SalesSystem(self.display, self.printer, products)
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
        self.sales_system = SalesSystem(self.display, self.printer, products)
        self.sales_system.on_barcode('6666')
        self.sales_system.on_print()
        self.sales_system.on_print()
        self.assertEquals(self.printer.content,
            'Subtotal 0.00' + '\n' +
            'GST 0.00'      + '\n' +
            'PST 0.00'      + '\n' +
            'Total: 0.00'   + '\n'
        )

class ReportingTests(unittest.TestCase):
    def test_empty_report(self):
        sales_system = SalesSystem(None, None, None)
        current_time = '2013-01-01 12:13'
        self.assertEquals(sales_system.get_sales_report(current_time),
            'Sales report at %s' % current_time         + '\n' +
            '"Date", "Subtotal", "GST", "PST", "Total"' + '\n' +
            '"Total", "0.00", "0.00", "0.00", "0.00"'   + '\n'
        )

    def test_one_sale_report(self):
        products = [
            {'price': 20.00, 'tax': 'G',  'barcode': '6666'},
        ]
        display = Display()
        printer = Printer()
        current_time = '2013-12-01 12:13'
        sales_system = SalesSystem(display, printer, products)
        sales_system.on_barcode('6666')
        sales_system.save_sale(current_time)
        self.assertEquals(sales_system.get_sales_report(current_time),
            'Sales report at %s' % current_time         + '\n' +
            '"Date", "Subtotal", "GST", "PST", "Total"' + '\n' +
            '"%s", "%.2f", "%.2f", "%.2f", "%.2f"' % (current_time, 20.00, 1.60, 0.0, 21.60) + '\n' +
            '"Total", "20.00", "1.60", "0.00", "21.60"' + '\n'
        )
        
    def test_triple_sale_report(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
