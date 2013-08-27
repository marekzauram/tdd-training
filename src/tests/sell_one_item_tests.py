import unittest


class SalesSystem(object):
    def __init__(self, display, printer, barcode_to_price_map):
        self.display   = display
        self.printer   = printer
        self.total     = 0
        self.total_tax = 0
        self.barcode_to_price_map = barcode_to_price_map

    def on_barcode(self, barcode):
        if '' == barcode:
            self.display.text = 'Scanning error: empty barcode'
            return

        if barcode not in self.barcode_to_price_map:
            self.display.text = 'Price not found for barcode "%s"' % barcode
        else:
            item = self.barcode_to_price_map[barcode]
            
            self.total     = self.total + item['price']
            self.total_tax = self.total_tax + self.get_tax_amount(item['price'], item['tax'])
            
            self.display.display_item(item['price'], item['tax'])
    
    def get_tax_amount(self, amount, tax):
        if tax == 'GP':
            return amount * 0.13
        else:
            return amount * 0.08

    def on_total(self):
        self.display.display_total(self.total + self.total_tax)

class Printer(object):
    pass
        
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
        self.sales_system = SalesSystem(self.display, self.printer, { '123': {'price': 7.95, 'tax': 'G'}, '321': {'price': 10.00, 'tax': 'GP'}})

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
        self.sales_system = SalesSystem(self.display, self.printer, { '123': {'price': 7.95, 'tax': 'G'}, '321': {'price': 10.00, 'tax': 'GP'}})

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
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'G'), 0.80);

    def test_gp_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'GP'), 1.30);

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
    def test_print_receipt(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
