from odoo import models, _
from odoo.addons.account.models.chart_template import template

class L10nCRTemplate(models.AbstractModel):
    _name = 'l10n_cr_custom.chart.template'
    _inherit = 'account.chart.template'

    @template('cr_custom')
    def _get_cr_custom_template_data(self):
        # Minimal template data; code_digits set to 7 based on provided CoA
        return {
            'name': _('Costa Rica - Custom'),
            'visible': True,
            'code_digits': '7',
            'property_account_receivable_id': 'cr_coa_1040101',
            'property_account_payable_id': 'cr_coa_2010101', 
        }

    @template('cr_custom', 'res.company')
    def _get_cr_custom_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cr',
            }
        }
