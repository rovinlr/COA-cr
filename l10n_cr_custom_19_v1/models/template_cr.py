import csv

from odoo import models, _
from odoo.addons.account.models.chart_template import template
from odoo.modules.module import get_module_resource


def _convert_csv_value(value):
    if value in ("True", "False"):
        return value == "True"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

class L10nCRTemplate(models.AbstractModel):
    _name = 'l10n_cr_custom.chart.template'
    _inherit = 'account.chart.template'

    def _load_template_from_csv(self, relative_path):
        path = get_module_resource('l10n_cr_custom_19_v1', relative_path)
        result = {}
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            current_id = None
            for row in reader:
                record_id = row.get('id') or current_id
                if not record_id:
                    continue
                current_id = record_id
                values = result.setdefault(record_id, {})
                row_cache = {}
                for field_name, raw_value in row.items():
                    if field_name == 'id' or not raw_value:
                        continue
                    self._assign_template_value(values, field_name.split('/'), raw_value, row_cache)
        return result

    def _assign_template_value(self, container, keys, raw_value, row_cache):
        if len(keys) == 1:
            container[keys[0]] = _convert_csv_value(raw_value)
            return

        head, *tail = keys
        if head.endswith('_ids'):
            line_cache = row_cache.get(head)
            if line_cache is None:
                line_cache = {}
                row_cache[head] = line_cache
                container.setdefault(head, []).append(line_cache)
            self._assign_template_value(line_cache, tail, raw_value, {})
            return

        if len(tail) == 1 and tail[0] == 'id':
            container[head] = _convert_csv_value(raw_value)
            return

        sub_container = container.setdefault(head, {})
        self._assign_template_value(sub_container, tail, raw_value, row_cache)

    @template('cr_custom', 'account.chart.template')
    def _get_cr_custom_template_data(self):
        # Minimal template data; code_digits set to 7 based on provided CoA
        return {
            'template_data': {
                'name': _('Costa Rica - Custom'),
                'visible': True,
                'code_digits': '7',
                'country_id': 'base.cr',
                'chart_template_ref': 'cr_custom',

            },
            'property_account_receivable_id': 'cr_coa_1040101',
            'property_account_payable_id': 'cr_coa_2010101',
            'default_sale_journal_id': 'cr_custom_sale_journal',
            'default_purchase_journal_id': 'cr_custom_purchase_journal',

        }

    @template('cr_custom', 'account.group')
    def _get_cr_custom_account_groups(self):
        return self._load_template_from_csv('data/template/account.group-cr_custom.csv')

    @template('cr_custom', 'account.account.template')
    def _get_cr_custom_accounts(self):
        return self._load_template_from_csv('data/template/account.account-cr_custom.csv')

    @template('cr_custom', 'account.tax.group')
    def _get_cr_custom_tax_groups(self):
        return self._load_template_from_csv('data/template/account.tax.group-cr_custom.csv')

    @template('cr_custom', 'account.tax.template')
    def _get_cr_custom_taxes(self):
        return self._load_template_from_csv('data/template/account.tax-cr_custom.csv')

    @template('cr_custom', 'account.fiscal.position.template')
    def _get_cr_custom_fiscal_positions(self):
        return self._load_template_from_csv('data/template/account.fiscal.position-cr_custom.csv')

    @template('cr_custom', 'account.fiscal.position.tax.template')
    def _get_cr_custom_fiscal_position_tax_map(self):
        return self._load_template_from_csv('data/template/account.fiscal.position.tax-cr_custom.csv')

    @template('cr_custom', 'account.journal')
    def _get_cr_custom_account_journals(self):
        return {
            'cr_custom_sale_journal': {
                'name': _('Ventas CR'),
                'type': 'sale',
                'code': 'VCR',
                'default_account_id': 'cr_coa_4110101',
                'payment_debit_account_id': 'cr_coa_1020501',
                'payment_credit_account_id': 'cr_coa_1020501',
            },
            'cr_custom_purchase_journal': {
                'name': _('Compras CR'),
                'type': 'purchase',
                'code': 'PCR',
                'default_account_id': 'cr_coa_5110101',
                'payment_debit_account_id': 'cr_coa_1020601',
                'payment_credit_account_id': 'cr_coa_1020601',
            },
            'cr_custom_currency_exchange_journal': {
                'name': _('Diferencias de cambio'),
                'type': 'general',
                'code': 'EXC',
                'default_account_id': 'cr_coa_4410101',
                'default_debit_account_id': 'cr_coa_5410301',
                'default_credit_account_id': 'cr_coa_4410101',
            },
            'cr_custom_tax_closing_journal': {
                'name': _('Cierre de impuestos'),
                'type': 'general',
                'code': 'TAX',
                'default_account_id': 'cr_coa_2020201',
                'default_debit_account_id': 'cr_coa_2020201',
                'default_credit_account_id': 'cr_coa_2020201',
            },
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
