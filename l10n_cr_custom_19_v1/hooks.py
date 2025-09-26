from odoo import SUPERUSER_ID, api


def _ensure_chart_template(env):
    registry_model = env.registry.get('account.chart.template')
    if not registry_model:
        return

    env.cr.execute("SELECT to_regclass('account_chart_template')")
    if not env.cr.fetchone()[0]:
        return

    template_model = env['account.chart.template']
    template = env.ref('l10n_cr_custom_19_v1.cr_custom', raise_if_not_found=False)

    country = env.ref('base.cr')
    base_values = {
        'name': 'Costa Rica - Custom',
        'visible': True,
        'code_digits': 7,
        'complete_tax_set': True,
        'country_id': country.id,
    }
    values = {key: value for key, value in base_values.items() if key in template_model._fields}

    if template:
        template.write(values)
    else:
        template = template_model.create(values)
        env['ir.model.data'].create({
            'module': 'l10n_cr_custom_19_v1',
            'name': 'cr_custom',
            'model': 'account.chart.template',
            'res_id': template.id,
            'noupdate': True,
        })

    if 'chart_template_ref' in template._fields and template.chart_template_ref.id != template.id:
        template.write({'chart_template_ref': template.id})


def post_init_hook(env_or_cr, registry=None):
    """Ensure compatibility with both env and cr signatures."""

    if isinstance(env_or_cr, api.Environment):
        env = env_or_cr
    else:
        env = api.Environment(env_or_cr, SUPERUSER_ID, {})

    _ensure_chart_template(env)
