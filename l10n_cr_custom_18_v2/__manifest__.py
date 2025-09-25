{
    "name": "Costa Rica - Contabilidad (Personalizada)",
    "summary": "Paquete de localización CR basado en el formato de Odoo 19 (plantillas).",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    'countries': ['cr'],
    'url': 'https://github.com/rovinlr/OCA-cr/tree/main/l10n_cr_custom_19_v2',
    'author': 'FenixCR Solutions - Rodrigo Lopez R',
    'website': 'https://www.fenixcrsolutions.com',
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/template/account.account-cr.csv",
        "data/template/account.group-cr.csv",
        "data/template/account.tax.group-cr.csv",
        "data/template/account.tax-cr.csv",
        "data/template/account.fiscal.position-cr.csv",
        "report/report_sales_purchase.xml",
        "wizard/tax_report_wizard_views.xml",
    ],
    "qweb": [
        "report/report_sales_purchase_templates.xml"
    ],
    "demo": [],
    "installable": True,
    "application": False,
}
