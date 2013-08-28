from datetime import datetime

class Sale(object):
    def __init__(self):
        self.datetime = None
        self.subtotal = 0
        self.gst      = 0
        self.pst      = 0
        self.products = []

    def add_product(self, product, price, gst, pst):
        self.subtotal = self.subtotal + price
        self.gst = self.gst + gst
        self.pst = self.pst + pst
        self.products.append(product)

    def get_total(self):
        return self.subtotal + self.gst + self.pst

class ProductCatalogue(object):
    def __init__(self, product_map):
        self.product_map = product_map

    def find_product(self, barcode):
        product = None
        for x in self.product_map:
            if x['barcode'] == barcode:
                product = x
                break
        return product

class SalesSystem(object):
    def __init__(self, display, printer, product_catalogue):
        self.display     = display
        self.printer     = printer
        self.sales       = []
        self.sale        = Sale()

        self.product_catalogue = product_catalogue
    
    def on_barcode(self, barcode):
        if '' == barcode:
            self.display.text = 'Scanning error: empty barcode'
            return

        product = self.product_catalogue.find_product(barcode)

        if product == None:
            self.display.text = 'Price not found for barcode "%s"' % barcode
        else:
            gst = self.get_tax_amount(product['price'], product['tax'].replace('P',''))
            pst = self.get_tax_amount(product['price'], product['tax'].replace('G',''))

            self.sale.add_product(product, product['price'], gst, pst)
            
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
        self.display.display_total(self.sale.get_total())
    
    def reset(self):
        self.sale = Sale()
    
    def save_sale(self, timestamp = None):
        if timestamp is None:
            timestamp = self.get_current_datetime()
        self.sale.datetime = timestamp
        self.sales.append(self.sale)
        self.reset()

    def on_print(self):
        lines = ''
        for product in self.sale.products:
            lines = lines + '%(barcode)s %(price).02f %(tax)s' % (product) + '\n'
            
        self.printer.content = (
            lines +
            'Subtotal %.02f' % (self.sale.subtotal,) + '\n' +
            'GST %.02f' % (self.sale.gst) + '\n' +
            'PST %.02f' % (self.sale.pst) + '\n' +
            'Total: %.02f' % (self.sale.get_total()) + '\n'
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
            totals['subtotal'] = totals['subtotal'] + sale.subtotal
            totals['gst']      = totals['gst']      + sale.gst
            totals['pst']      = totals['pst']      + sale.pst
            totals['total']    = totals['total']    + sale.get_total()

            report += '"%(datetime)s", "%(subtotal).2f", "%(gst).2f", "%(pst).2f", "%(total).2f"' % (
                {
                    'datetime': sale.datetime,
                    'subtotal': sale.subtotal,
                    'gst':      sale.gst,
                    'pst':      sale.pst,
                    'total':    sale.get_total()
                }
            )  + '\n'
        
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
