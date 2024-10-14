from odoo import models, fields, api
from odoo.exceptions import UserError
from lxml import etree

class QWebTutorial(models.Model):
    _name = 'qweb.tutorial'
    _description = 'QWeb Tutorial'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model', ondelete='cascade')
    template_code = fields.Text(string='QWeb Template Code')
    domain = fields.Char(string='Domain', help="Domain for selecting records")
    rendered_html = fields.Html(string='Rendered HTML')
    pdf_attachment_id = fields.Binary(string='PDF Attachment')
    record_limit = fields.Integer(string='Record Limit', default=10)


    def _compute_rendered_html(self):
        for record in self:
            if record.template_code and record.model_id:
                try:
                    model = self.env[record.model_id.model]
                    # Застосовуємо домен, якщо він є
                    domain = eval(record.domain) if record.domain else []
                    limit = self.record_limit or 10
                    example_records = model.search(domain, limit=limit)

                    data = {
                        'docs': example_records,
                        'model': model,  # Додайте модель до контексту
                        'record': record,  # Додайте поточний запис до контексту
                    }

                    # Створення etree елемента з коду шаблону
                    template_code = f"<t t-name='custom_template'>{record.template_code}</t>"
                    template_element = etree.fromstring(template_code)

                    # Рендеринг шаблону
                    qweb = self.env['ir.qweb']
                    rendered_html = qweb._render(template_element, data)

                    record.rendered_html = rendered_html.decode('utf-8') if isinstance(rendered_html, bytes) else rendered_html

                except Exception as e:
                    raise UserError(f"Error rendering QWeb template: {str(e)}")
            else:
                record.rendered_html = ''

    def action_render_qweb(self):
        self._compute_rendered_html()

    def action_render_qweb_new_window(self):
        self.ensure_one()
        self._compute_rendered_html()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/qweb_tutorial/render_new_window/{self.id}',
            'target': 'new',
        }

