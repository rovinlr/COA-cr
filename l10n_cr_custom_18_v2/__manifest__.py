{
    "name": "Costa Rica - Contabilidad (Personalizada)",
    "summary": "Paquete de localización CR basado en el formato de Odoo 18 (plantillas).",
    "version": "18.0.1.2.0",
    "category": "Accounting/Localizations/Account Charts",
    'countries': ['cr'],
    'url': 'https://github.com/rovinlr/OCA-cr/tree/main/l10n_cr_custom_18_v2',
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
        "data/account_chart_template_configure_data.xml"
    ],
    "demo": [],
    "installable": True,
    "application": False,
}
