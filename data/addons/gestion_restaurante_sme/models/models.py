from odoo import models, fields, api


class plato_sergi(models.Model):
    _name = 'gestion_restaurante_sme.gestion_restaurante_sme'
    _description = 'gestion_restaurante_sme.gestion_restaurante_sme'

    name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

