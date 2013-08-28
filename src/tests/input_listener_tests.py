import unittest
from sales_system import SalesSystem
from sales_system import Printer
from sales_system import Display
from sales_system import InputListener

class FakeSaleSystem():
    def __init__(self):
        self.called_with_barcode = None
        self.called_on_barcode = False
        self.called_on_total = False
        self.called_on_print = False
        
    def on_barcode(self, barcode):
        self.called_with_barcode = barcode
        self.called_on_barcode = True
    
    def on_total(self):
        self.called_on_total = True
    
    def on_print(self):
        self.called_on_print = True
        

class InputListenerTests(unittest.TestCase):
    def setUp(self):
        self.sales_system = FakeSaleSystem()
        self.input_listener = InputListener(self.sales_system)
        pass
    
    def test_barcode(self):
        self.input_listener.on_input('1234')
        self.assertEquals(self.sales_system.called_on_barcode, True)
    
    def test_total(self):
        self.input_listener.on_input('T')
        self.assertEquals(self.sales_system.called_on_total, True)
        
    def test_total(self):
        self.input_listener.on_input('P')
        self.assertEquals(self.sales_system.called_on_print, True)