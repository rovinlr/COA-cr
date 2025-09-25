from collections import defaultdict

from odoo import fields, models


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

        company = self.env.company
        company_currency = company.currency_id

        today = fields.Date.context_today(self)

        def _tax_report_values(moveset):
            summary = defaultdict(lambda: {
                'tax_id': False,
                'tax_name': '',
                'base': 0.0,
                'tax': 0.0,
                'total': 0.0,
            })
            details = []

            for move in moveset:
                tax_lines = move.line_ids.filtered('tax_line_id')
                for line in tax_lines:
                    tax = line.tax_line_id
                    base_amount = company_currency.round(line.tax_base_amount or 0.0)
                    tax_amount = company_currency.round(line.balance or 0.0)
                    total_amount = base_amount + tax_amount

                    entry = summary[tax.id]
                    entry['tax_id'] = tax.id
                    entry['tax_name'] = tax.display_name or tax.name
                    entry['base'] += base_amount
                    entry['tax'] += tax_amount
                    entry['total'] += total_amount

                    details.append({
                        'document': move.name or move.ref or '',
                        'date': fields.Date.to_date(move.invoice_date or move.date),
                        'tax_name': entry['tax_name'],
                        'base': base_amount,
                        'tax': tax_amount,
                        'total': total_amount,
                    })

            summary_list = sorted(summary.values(), key=lambda item: item['tax_name'] or '')
            details.sort(key=lambda item: (item['date'] or today, item['document']))

            totals = {
                'base': sum(item['base'] for item in summary_list),
                'tax': sum(item['tax'] for item in summary_list),
            }
            totals['total'] = totals['base'] + totals['tax']

            return {
                'summary': summary_list,
                'details': details,
                'totals': totals,
            }

        sale_data = _tax_report_values(sale_moves)
        purchase_data = _tax_report_values(purchase_moves)

        grand_totals = {
            'base': sale_data['totals']['base'] + purchase_data['totals']['base'],
            'tax': sale_data['totals']['tax'] + purchase_data['totals']['tax'],
        }
        grand_totals['total'] = grand_totals['base'] + grand_totals['tax']

        show_details = bool(self.env.context.get('report_detail') or (data or {}).get('report_detail'))

        return {
            'doc_ids': relevant_moves.ids,
            'doc_model': 'account.move',
            'docs': relevant_moves,
            'sale_moves': sale_moves,
            'purchase_moves': purchase_moves,
            'sale_summary': sale_data['summary'],
            'purchase_summary': purchase_data['summary'],
            'sale_totals': sale_data['totals'],
            'purchase_totals': purchase_data['totals'],
            'sale_details': sale_data['details'],
            'purchase_details': purchase_data['details'],
            'grand_totals': grand_totals,
            'show_details': show_details,
            'company': company,
            'company_currency': company_currency,
        }
