import unittest

class SalesSystem(object):
    def on_barcode(self, barcode):
        pass


class Display(object):
    def __init__(self):
        self.text = "EUR 7.95"


class SellOneItemTests(unittest.TestCase):
    def test_price_found(self):
        sales_system = SalesSystem()
        display      = Display()
        #
        sales_system.on_barcode("123")
        #
        self.assertEquals("EUR 7.95", display.text)


if __name__ == "__main__":
    unittest.main()
