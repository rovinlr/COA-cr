from odoo import fields, models


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

    def _run_report(self, detailed=False):
        self.ensure_one()
        moves = self._get_moves()
        action_xmlid = 'l10n_cr_custom_19_v1.action_report_sales_purchase'
        if detailed:
            action_xmlid = 'l10n_cr_custom_19_v1.action_report_sales_purchase_detail'
        action = self.env.ref(action_xmlid)
        context = dict(self.env.context)
        context.update({'report_detail': detailed})
        data = {'report_detail': detailed}
        return action.with_context(context).report_action(moves, data=data)

    def action_print_summary(self):
        return self._run_report(detailed=False)

    def action_print_detail(self):
        return self._run_report(detailed=True)
