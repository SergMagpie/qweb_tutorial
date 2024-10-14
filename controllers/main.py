from odoo import http
from odoo.http import request
from lxml import etree

class QWebTutorialController(http.Controller):

    @http.route('/qweb_tutorial/render', type='http', auth='public', website=True, csrf=False)
    def render_qweb(self, **kw):
        model_name = kw.get('model_name', '')
        template_code = kw.get('template_code', '')
        rendered_html = ''

        if model_name and template_code:
            try:
                model = request.env[model_name]
                records = model.search([])

                data = {
                    'docs': records,
                }

                # Create an etree element from the template code
                template_element = etree.fromstring(f"""
                <templates>
                    <t t-name="custom_template">{template_code}</t>
                </templates>
                """)

                qweb = request.env['ir.qweb']
                rendered_html = qweb._render(template_element, data)
            except Exception as e:
                rendered_html = f"<div style='color: red;'>Error: {str(e)}</div>"

        return request.make_response(rendered_html)

    @http.route('/qweb_tutorial/render_new_window/<int:record_id>', type='http', auth='public', website=True, csrf=False)
    def render_qweb_new_window(self, record_id, **kw):
        record = request.env['qweb.tutorial'].browse(record_id)
        if not record.exists():
            return request.not_found()

        record._compute_rendered_html()

        # Use a basic QWeb template for proper formatting
        qweb_template = """
        <t t-name="qweb_tutorial.render_template">
            <html>
                <head>
                    <link rel="stylesheet" href="/web/static/lib/bootstrap/dist/css/bootstrap.css"/>
                    <link rel="stylesheet" href="/web/static/src/css/webclient.css"/>
                </head>
                <body>
                    <div class="container">
                        <t t-raw="content"/>
                    </div>
                </body>
            </html>
        </t>
        """
        template_element = etree.fromstring(qweb_template)
        qweb = request.env['ir.qweb']
        rendered_html = qweb._render(template_element, {'content': record.rendered_html})

        return request.make_response(rendered_html)
