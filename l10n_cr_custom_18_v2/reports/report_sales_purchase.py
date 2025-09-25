from odoo import models


class ReportSalesPurchase(models.AbstractModel):
    _name = 'report.l10n_cr_custom_18_v2.report_sales_purchase'
    _description = 'Reporte de Compras y Ventas'

    def _get_report_values(self, docids, data=None):
        moves = self.env['account.move'].browse(docids)
        relevant_moves = moves.filtered(
            lambda m: m.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
        )

        def _ordered(records):
            return records.sorted(key=lambda m: (m.invoice_date or m.date or False, m.name or m.ref or m.id))

        sale_moves = _ordered(
            relevant_moves.filtered(lambda m: m.move_type in ('out_invoice', 'out_refund'))
        )
        purchase_moves = _ordered(
            relevant_moves.filtered(lambda m: m.move_type in ('in_invoice', 'in_refund'))
        )

        def _totals(recordset):
            return {
                'base': sum(recordset.mapped('amount_untaxed')),
                'tax': sum(recordset.mapped('amount_tax')),
                'total': sum(recordset.mapped('amount_total')),
            }

        company = self.env.company
        company_currency = company.currency_id

        return {
            'doc_ids': relevant_moves.ids,
            'doc_model': 'account.move',
            'docs': relevant_moves,
            'sale_moves': sale_moves,
            'purchase_moves': purchase_moves,
            'sale_totals': _totals(sale_moves),
            'purchase_totals': _totals(purchase_moves),
            'grand_totals': _totals(relevant_moves),
            'company': company,
            'company_currency': company_currency,
        }
