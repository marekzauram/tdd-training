import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display

class TaxTests(unittest.TestCase):
    def test_g_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'G'), 0.80)

    def test_gp_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'GP'), 1.30)

    def test_p_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, 'P'), 0.50)

    def test_zero_tax(self):
        self.assertEquals(SalesSystem(None, None, None).get_tax_amount(10.00, ''), 0.00)

if __name__ == '__main__':
    unittest.main()
