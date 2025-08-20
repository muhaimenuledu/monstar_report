from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_custom_invoice_lines(self):
        """Return the invoice lines as a list for custom QWeb rendering"""
        lines_list = []
        for line in self.invoice_line_ids:
            lines_list.append({
                'product': line.product_id.name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'tax': line.tax_ids.name,
                'subtotal': line.price_subtotal,
            })
        return lines_list
