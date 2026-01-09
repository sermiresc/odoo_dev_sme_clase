from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class gestion_tareas_sme(models.Model):
    _name = 'gestion_tareas_sme.gestion_tareas_sme'
    _description = 'gestion_tareas_sme.gestion_tareas_sme'


    # En el modelo tareas_sergio


    codigo = fields.Char(compute="_get_codigo")

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

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")

    fecha_fin = fields.Datetime(
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

    def _get_codigo(self):
        for tarea in self:
            try:
                # Verificamos que tenga sprint asignado
                if not tarea.sprint:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")

                # Generamos el código
                tarea.codigo = str(tarea.sprint.name).upper() + "_" + str(tarea.id)

            except Exception as e:
                raise ValidationError(f"Error al generar el código: {str(e)}")

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

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio del sprint")

    tasks = fields.One2many(
        'gestion_tareas_sme.gestion_tareas_sme', 
        'sprint', 
        string='Tareas del Sprint')
    duracion = fields.Integer(
        string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")

    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        for sprint in self:
            try:
                if sprint.fecha_ini and sprint.duracion and sprint.duracion > 0:
                    sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
                else:
                    sprint.fecha_fin = sprint.fecha_ini
            except Exception as e:
                raise UserError(f"Error al generar el codigo: {str(e)}")

    @api.constrains('fecha_ini', 'fecha_fin')
    def _check_fechas(self):
        for sprint in self:
            if sprint.fecha_fin and sprint.fecha_ini:
                if sprint.fecha_fin < sprint.fecha_ini:
                    raise ValidationError(
                        "La fecha de fin no puede ser anterior a la fecha de inicio."
                    )
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

        


