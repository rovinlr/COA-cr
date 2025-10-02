"""Wizard that mirrors the report launcher from ``l10n_cr`` version 19."""

from odoo import fields, models


MODULE_NAME = "l10n_cr_custom_reports"


class TaxReportWizard(models.TransientModel):
    _name = 'l10n.cr.custom.tax.report.wizard'
    _description = 'Asistente de Reporte de Compras y Ventas'

    date_from = fields.Date(string='Fecha desde')
    date_to = fields.Date(string='Fecha hasta')
    target_move = fields.Selection(
        selection=[
            ('posted', 'Publicadas'),
            ('all', 'Todas (Borrador y Publicadas)'),
        ],
        string='Movimientos',
        default='posted',
        required=True,
    )

    def _prepare_domain(self):
        self.ensure_one()
        domain = [
            ('company_id', '=', self.env.company.id),
            (
                'move_type',
                'in',
                ('out_invoice', 'out_refund', 'in_invoice', 'in_refund'),
            ),
        ]
        if self.target_move == 'posted':
            domain.append(('state', '=', 'posted'))
        if self.date_from:
            domain.extend([
                '|',
                ('invoice_date', '>=', self.date_from),
                ('date', '>=', self.date_from),
            ])
        if self.date_to:
            domain.extend([
                '|',
                ('invoice_date', '<=', self.date_to),
                ('date', '<=', self.date_to),
            ])
        return domain

    def _get_moves(self):
        self.ensure_one()
        domain = self._prepare_domain()
        return self.env['account.move'].search(domain, order='invoice_date, date, name')

    def _run_report(self, detailed=False, report_format='html'):
        self.ensure_one()
        moves = self._get_moves()
        action_base = "action_report_sales_purchase_detail" if detailed else "action_report_sales_purchase"
        if report_format == 'html':
            action_xmlid = f"{MODULE_NAME}.{action_base}_html"
        else:
            action_xmlid = f"{MODULE_NAME}.{action_base}"
        action = self.env.ref(action_xmlid)
        context = dict(self.env.context)
        context.update({'report_detail': detailed})
        data = {
            'report_detail': detailed,
            'date_from': fields.Date.to_string(self.date_from) if self.date_from else False,
            'date_to': fields.Date.to_string(self.date_to) if self.date_to else False,
            'target_move': self.target_move,
        }
        return action.with_context(context).report_action(moves, data=data)

    def action_print_summary(self):
        return self._run_report(detailed=False, report_format='html')

    def action_print_detail(self):
        return self._run_report(detailed=True, report_format='html')
