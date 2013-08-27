import unittest


class SalesSystem(object):
    def __init__(self, display, printer, product_map):
        self.display   = display
        self.printer   = printer
        self.total     = 0
        self.total_tax_g = 0
        self.total_tax_p = 0
        self.basket    = []
        self.product_map = product_map

    def on_barcode(self, barcode):
        if '' == barcode:
            self.display.text = 'Scanning error: empty barcode'
            return

        product = None
        for x in self.product_map:
            if x['barcode'] == barcode:
                product = x
                break
        if product == None:
            self.display.text = 'Price not found for barcode "%s"' % barcode
        else:
            self.basket.append(product)
        
            self.total       = self.total + product['price']
            self.total_tax_g = self.total_tax_g + self.get_tax_amount(product['price'], product['tax'].replace('P',''))
            self.total_tax_p = self.total_tax_p + self.get_tax_amount(product['price'], product['tax'].replace('G',''))
            
            self.display.display_item(product['price'], product['tax'])
    
    def get_tax_amount(self, amount, tax):
        if tax == 'GP':
            return amount * 0.13
        elif tax == 'P':
            return amount * 0.05
        elif tax == 'G':
            return amount * 0.08
        else:
            return amount * 0.00

    def on_total(self):
        self.display.display_total(self.total + self.total_tax_g + self.total_tax_p)
    
    def on_print(self):
        lines = ''
        for product in self.basket:
            lines = lines + '%(barcode)s %(price).02f %(tax)s' % (product) + '\n'
            
        self.printer.content = (
            lines +
            'Subtotal %.02f' % (self.total,) + '\n' +
            'GST %.02f' % (self.total_tax_g) + '\n' +
            'PST %.02f' % (self.total_tax_p) + '\n' +
            'Total: %.02f' % (self.total + self.total_tax_g + self.total_tax_p) + '\n'
        )

class Printer(object):
    def __init__(self):
        self.content = None
        
class Display(object):
    def __init__(self):
        self.text = None
        
    def display_item(self, price, tax):
        self.text = 'EUR %.02f %s' % (price, tax,)

    def display_total(self, total):
        self.text = 'Total: EUR %.02f' % (total,)

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

if __name__ == '__main__':
    unittest.main()
