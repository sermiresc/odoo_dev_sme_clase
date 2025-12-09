# from odoo import http


# class GestionTareasSme(http.Controller):
#     @http.route('/gestion_tareas_sme/gestion_tareas_sme', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas_sme/gestion_tareas_sme/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas_sme.listing', {
#             'root': '/gestion_tareas_sme/gestion_tareas_sme',
#             'objects': http.request.env['gestion_tareas_sme.gestion_tareas_sme'].search([]),
#         })

#     @http.route('/gestion_tareas_sme/gestion_tareas_sme/objects/<model("gestion_tareas_sme.gestion_tareas_sme"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas_sme.object', {
#             'object': obj
#         })

