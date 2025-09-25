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
                'bank_account_code_prefix': '1010101',
                'cash_account_code_prefix': '1010301',
                'transfer_account_code_prefix': '1020401',
                'account_default_pos_receivable_account_id': 'cr_coa_1040201',
                'income_currency_exchange_account_id': 'cr_coa_4410101',
                'expense_currency_exchange_account_id': 'cr_coa_5410301',
                'account_sale_tax_id': 'cr_tax_iva_13_bienes_v_sale',
                'account_purchase_tax_id': 'cr_tax_iva_13_bienes_c_purchase',
                'income_account_id': 'cr_coa_4110101',
                'expense_account_id': 'cr_coa_5110101',
            }
        }
