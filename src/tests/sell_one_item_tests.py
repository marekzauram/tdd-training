import unittest


class SalesSystem(object):
    def __init__(self, display):
        self.display = display

    def on_barcode(self, barcode):

        barcode_to_price_map = {
            '321': "EUR 10.00",
            '123': "EUR 7.95",
        }

        self.display.text = barcode_to_price_map[barcode]


class Display(object):
    def __init__(self):
        self.text = None


class SellOneItemTests(unittest.TestCase):
    def test_price_found(self):
        display = Display()
        sales_system = SalesSystem(display)

        sales_system.on_barcode("123")

        self.assertEquals("EUR 7.95", display.text)

    def test_another_price_found(self):
        display = Display()
        sales_system = SalesSystem(display)

        sales_system.on_barcode("321")

        self.assertEquals("EUR 10.00", display.text)


if __name__ == "__main__":
    unittest.main()
