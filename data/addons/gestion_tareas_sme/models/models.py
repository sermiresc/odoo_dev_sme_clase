from odoo import models, fields, api


class gestion_tareas_sme(models.Model):
    _name = 'gestion_tareas_sme.gestion_tareas_sme'
    _description = 'gestion_tareas_sme.gestion_tareas_sme'

    name = fields.Char()
    description = fields.Text()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
     
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

