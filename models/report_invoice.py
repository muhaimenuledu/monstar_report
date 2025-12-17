# -*- coding: utf-8 -*-
import json
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_custom_invoice_lines(self):
        """Return invoice lines as list for custom QWeb rendering (optional helper)."""
        lines_list = []
        for line in self.invoice_line_ids:
            lines_list.append({
                "product": line.product_id.name,
                "quantity": line.quantity,
                "price_unit": line.price_unit,
                "tax": ", ".join(line.tax_ids.mapped("name")) if line.tax_ids else "",
                "subtotal": line.price_subtotal,
            })
        return lines_list

    def _get_report_paid_credit_lines(self):
        """
        Return reconciled entries shown in Odoo UI totals area (payments + credit notes)
        using invoice_payments_widget (JSON).
        """
        self.ensure_one()
        result = []

        widget_raw = getattr(self, "invoice_payments_widget", False)
        if not widget_raw:
            return result

        try:
            widget = json.loads(widget_raw) if isinstance(widget_raw, str) else widget_raw
        except Exception:
            return result

        content = widget.get("content") or []
        if not content:
            return result

        # Build lines in the same order as Odoo shows them
        for item in content:
            # item keys typically: date, amount, currency_id, move_id, ref, name, journal_name, account_payment_id, etc.
            move_id = item.get("move_id")
            payment_id = item.get("account_payment_id")

            related_move = self.env["account.move"].browse(move_id) if move_id else self.env["account.move"]
            is_credit_note = bool(
                related_move
                and related_move.exists()
                and related_move.move_type in ("out_refund", "in_refund")
                and not payment_id
            )

            date_str = item.get("date")  # usually 'YYYY-MM-DD'
            amount = item.get("amount", 0.0)

            currency = self.currency_id
            currency_id = item.get("currency_id")
            if currency_id:
                currency = self.env["res.currency"].browse(currency_id) or self.currency_id

            label = f"Credit Note on {date_str}" if is_credit_note else f"Paid on {date_str}"

            result.append({
                "label": label,
                "date": date_str,
                "amount": amount,
                "currency": currency,
                "type": "credit_note" if is_credit_note else "payment",
                "move_id": move_id,
                "account_payment_id": payment_id,
            })

        return result
