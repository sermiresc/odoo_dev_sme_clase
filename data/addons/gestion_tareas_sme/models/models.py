from odoo import models, fields, api


class gestion_tareas_sme(models.Model):
    _name = 'gestion_tareas_sme.gestion_tareas_sme'
    _description = 'gestion_tareas_sme.gestion_tareas_sme'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")

    date_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea")

    date_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")

    date_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")

    ended = fields.Boolean(
        string="Finalizado", 
        help="Indica si la tarea ha sido finalizada o no")

    sprint = fields.Many2one(
        'gestion_tareas_sme.sprints_sme', 
        string='Sprint relacionado', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')

    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_sme.tecnologias_sme',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')

class sprints_sme(models.Model):
    _name = 'gestion_tareas_sme.sprints_sme'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del sprint")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción del sprint")

    date_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del sprint")

    date_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización del sprint")

    tasks = fields.One2many(
        'gestion_tareas_sme.gestion_tareas_sme', 
        'sprint', 
        string='Tareas del Sprint')

class tecnologias_sme(models.Model):
    _name = 'gestion_tareas_sme.tecnologias_sme'
    _description = 'Modelo de Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología")

    rel_tareas = fields.Many2many(
        comodel_name='gestion_tareas_sme.gestion_tareas_sme',
        relation='relacion_tareas_tecnologias',
        column1='rel_tecnologias',
        column2='rel_tareas',
        string='Tareas')

        


