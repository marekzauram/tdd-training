from datetime import datetime

class SalesSystem(object):
    def __init__(self, display, printer, product_map):
        self.display     = display
        self.printer     = printer
        self.total       = 0
        self.total_tax_g = 0
        self.total_tax_p = 0
        self.basket      = []
        self.sales       = []
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
    
    def reset(self):
        self.basket      = []
        self.total       = 0
        self.total_tax_g = 0
        self.total_tax_p = 0
    
    def save_sale(self, timestamp = None):
        if timestamp is None:
            timestamp = self.get_current_datetime()
        self.sales.append({
            'date'     : timestamp,
            'subtotal' : self.total,
            'gst'      : self.total_tax_g,
            'pst'      : self.total_tax_p,
            'total'    : self.total + self.total_tax_g + self.total_tax_p
        })
        self.reset()

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
        self.save_sale()
    
    def on_sales_report(self):
        return self.get_sales_report(self.get_current_datetime())
    
    def get_current_datetime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M')
        
    def get_sales_report(self, current_time):
        report = 'Sales report at %s' % current_time + '\n'
        report = report + '"Date", "Subtotal", "GST", "PST", "Total"' + '\n'
        totals = {'subtotal': 0, 'gst': 0, 'pst': 0, 'total': 0}
        for sale in self.sales:
            totals['subtotal'] = totals['subtotal'] + sale['subtotal']
            totals['gst']      = totals['gst']      + sale['gst']
            totals['pst']      = totals['pst']      + sale['pst']
            totals['total']    = totals['total']    + sale['total']
            report += '"%(date)s", "%(subtotal).2f", "%(gst).2f", "%(pst).2f", "%(total).2f"' % (sale) + '\n'
        
        report = report + '"Total", "%(subtotal).2f", "%(gst).2f", "%(pst).2f", "%(total).2f"' % (totals)  + '\n'

        return report
        
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
