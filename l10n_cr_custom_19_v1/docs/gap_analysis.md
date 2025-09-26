# Gap analysis vs. Odoo official `l10n_cr`

This note summarizes the key elements that prevent the custom package from behaving like the official Costa Rican localization shipped with Odoo (commit `a8bfd12e25a453bb8845ae8813c53704766e8d82`).

## Manifest dependencies and data files

* The module currently depends only on `account`, so core localizations such as `l10n_latam_base`, `l10n_latam_invoice_document`, or reporting helpers are never installed. The official module requires several of these add-ons before the chart template is usable. 【F:l10n_cr_custom_19_v1/__manifest__.py†L3-L22】
* Only CSV templates and a couple of report/view definitions are loaded. There are no XML records to expose the chart template, taxes, or fiscal positions to the chart installation wizard, so the data never becomes available even though the CSV files exist in `data/template`. 【F:l10n_cr_custom_19_v1/__manifest__.py†L13-L21】

## Chart template implementation

* The python template (`models/template_cr.py`) defines the high-level `account.chart.template`, a few journals, and default company values, but it never feeds the account, tax, tax group, or fiscal position records contained in the CSV exports. As a result, the chart wizard cannot create the actual accounting data. 【F:l10n_cr_custom_19_v1/models/template_cr.py†L1-L70】
* To mirror the official module you must either (a) port the XML data files (`account_chart_template_data.xml`, `account_tax_data.xml`, `account_fiscal_position_data.xml`, …) and their dependencies, or (b) extend the python template to parse and inject the CSV exports for accounts, account groups, taxes, tax repartition lines, and fiscal positions.

## Recommended next steps

1. Import the missing dependencies from the official manifest and ensure they are listed in `depends`.
2. Restore the XML data files that bind the CSV templates to actual models, or programmatically load the CSV contents through the `@template` API.
3. Add noupdate data (tax tags, fiscal position mappings, default taxes) and test the installation on a fresh database using the standard chart template installation wizard.
