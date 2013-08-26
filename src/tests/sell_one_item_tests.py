import unittest


class SalesSystem(object):
    def __init__(self, display, barcode_to_price_map):
        self.display = display
        self.barcode_to_price_map = barcode_to_price_map

    def on_barcode(self, barcode):
        if '' == barcode:
            self.display.text = 'Scanning error: empty barcode'
            return

        if barcode not in self.barcode_to_price_map:
            self.display.text = 'Price not found for barcode "%s"' % barcode
        else:
            self.display.text = self.barcode_to_price_map[barcode]


class Display(object):
    def __init__(self):
        self.text = None


class SellOneItemTests(unittest.TestCase):
    def setUp(self):
        self.display = Display()
        self.sales_system = SalesSystem(self.display, { '123': "EUR 7.95", '321': "EUR 10.00" })

    def test_price_found(self):
        sales_system = SalesSystem(self.display, { '123': "EUR 7.95" })
        sales_system.on_barcode("123")
        self.assertEquals("EUR 7.95", self.display.text)

    def test_price_found_among_many(self):
        sales_system = SalesSystem(self.display, { '123': "EUR 87123.12", '321': "EUR 10.00", '787': "EUR 981.92" })
        sales_system.on_barcode("321")
        self.assertEquals("EUR 10.00", self.display.text)

    def test_price_not_found(self):
        sales_system = SalesSystem(self.display, { "anything but unknown-barcode": "EUR 786.23"})
        sales_system.on_barcode("unknown-barcode")
        self.assertEquals('Price not found for barcode "unknown-barcode"', self.display.text)

    def test_empty_barcode(self):
        sales_system = SalesSystem(self.display, None)
        sales_system.on_barcode("")
        self.assertEquals('Scanning error: empty barcode', self.display.text)


if __name__ == "__main__":
    unittest.main()
