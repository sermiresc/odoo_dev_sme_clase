# from odoo import http


# class GestionRestauranteSme(http.Controller):
#     @http.route('/gestion_restaurante_sme/gestion_restaurante_sme', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurante_sme/gestion_restaurante_sme/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurante_sme.listing', {
#             'root': '/gestion_restaurante_sme/gestion_restaurante_sme',
#             'objects': http.request.env['gestion_restaurante_sme.gestion_restaurante_sme'].search([]),
#         })

#     @http.route('/gestion_restaurante_sme/gestion_restaurante_sme/objects/<model("gestion_restaurante_sme.gestion_restaurante_sme"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurante_sme.object', {
#             'object': obj
#         })

