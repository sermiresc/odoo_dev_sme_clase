from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

# HISTORIAS DE USUARIO ********************************************
class historias_sme(models.Model):
    _name = 'gestion_tareas_sme.historias_sme'
    _description = 'gestion_tareas_sme.historias_sme'


    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la historia")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción de la historia")

    proyecto = fields.Many2one(
        'gestion_tareas_sme.proyectos_sme', 
        string='Proyecto', 
        ondelete='set null', 
        help='Proyecto al que pertenece esta tarea')

    tareas = fields.One2many(
        'gestion_tareas_sme.gestion_tareas_sme', 
        'historia', 
        string='tareas de la historia')

    tecnologias = fields.Many2many(
        "gestion_tareas_sme.tecnologias_sme",
        compute="_compute_tecnologias",
        string="Tecnologias Utilizadas"
    )

    @api.depends('tareas', 'tareas.rel_tecnologias')
    def _compute_tecnologias(self):
        for historia in self:
            tecnologias_acumuladas = self.env['gestion_tareas_sme.tecnologias_sme']

            for tarea in historia.tareas:
                tecnologias_acumuladas = tecnologias_acumuladas + tarea.rel_tecnologias
            
            
            historia.tecnologias = tecnologias_acumuladas

    


# TAREAS_SERGI ***************************************************
class proyectos_sme(models.Model):
    _name = 'gestion_tareas_sme.proyectos_sme'
    _description = 'gestion_tareas_sme.proyectos_sme'


    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre del proyecto")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción del proyecto")
    
    activo = fields.Boolean(
        string='Estado del proyecto',
        default= True
    )

    historias = fields.One2many(
        'gestion_tareas_sme.historias_sme', 
        'proyecto', 
        string='historias de usuario del proyecto')

    sprints = fields.One2many(
        'gestion_tareas_sme.sprints_sme',
        'proyecto',
        string='Sprint de los proyectos')

    

    

# TAREAS_SERGI ***************************************************
class gestion_tareas_sme(models.Model):
    _name = 'gestion_tareas_sme.gestion_tareas_sme'
    _description = 'gestion_tareas_sme.gestion_tareas_sme'

    # ATRIBUTOS TAREAS *******************************************

    codigo = fields.Char(compute="_get_codigo")

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    description = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")

    # def _get_date_actual(self):
    #     return datetime.now()

    date_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea",
        default=lambda self: datetime.now())

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

#    sprint = fields.Many2one(
#       'gestion_tareas_sme.sprints_sme', 
#       string='Sprint relacionado', 
#       ondelete='set null', 
#       help='Sprint al que pertenece esta tarea')

    sprint = fields.Many2one(
        'gestion_tareas_sme.sprints_sme', 
        string='Sprint Activo', 
        compute='_compute_sprint', 
        store=True) 

    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_sme.tecnologias_sme',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')

    historia = fields.Many2one(
        'gestion_tareas_sme.historias_sme', 
        string='historia de usuario', 
        ondelete='set null', 
        help='Historias de usuario de la tarea')

    

    proyecto = fields.Many2one(
        'gestion_tareas_sme.proyectos_sme',
        string='proyecto de usuario',
        ondelete="set null",
        help='Proyecto de los usuario',
        related="historia.proyecto",
        readonly=True
    )

    def _get_proyecto_activo(self):
        return self.env['gestion_tareas_sme.proyectos_sme'].search(
            [('activo','=',True)],
            limit=1, order='create_date desc')
            
    proyecto_default = fields.Many2one(
        'gestion_tareas_sme.proyectos_sme',
        string='proyecto default',
        default=_get_proyecto_activo
    )

    responsable = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user.id)


    desarrollador_ids = fields.Many2one(
        'res.partner',
        string='Desarrollador',
        help='Desarrollador asignado a la tarea'
    )

    # METODOS TAREAS *******************************************


    @api.depends('historia', 'historia.proyecto')
    def _compute_sprint(self):
        for tarea in self:
            tarea.sprint = False

            # Verificar que la tarea tiene historia y proyecto
            if tarea.historia and tarea.historia.proyecto:
                # Buscar sprints del proyecto
                sprints = self.env['gestion_tareas_sme.sprints_sme'].search([
                    ('proyecto.id', '=', tarea.historia.proyecto.id)
                ])

                # Buscar el sprint activo (fecha_fin > ahora) 
                # de entre todos los sprints asociados al proyecto
                # en teoría solo hay un sprint activo, por eso es el que no ha vencido
                for sprint in sprints:
                    if (isinstance(sprint.fecha_fin, datetime) and 
                            sprint.fecha_ini <= datetime.now() and   
                            sprint.fecha_fin > datetime.now()):
                        tarea.sprint = sprint.id
                        break



    @api.depends('sprint', 'sprint.name')
    def _get_codigo(self):
        for tarea in self:
            try:
                # Verificamos que tenga sprint asignado
                if not tarea.sprint:
                    _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                    tarea.codigo = "TSK_"+str(tarea.id)
                else:
                    # Generamos el código
                    tarea.codigo = str(tarea.sprint.name[:3]).upper() + "_" + str(tarea.id)
                    
                _logger.debug(f"Codigo generado: {tarea.codigo}")

            except Exception as e:
                _logger.error(f"Error generando codigo para tarea {tarea.id}: {str(e)}")
                raise ValidationError(f"Error al generar el código: {str(e)}")


# SPRINTS_SERGI ************************************************
class sprints_sme(models.Model):
    _name = 'gestion_tareas_sme.sprints_sme'
    _description = 'Modelo de Sprints para Gestión de Proyectos'

    #ATRIBUTOS SPRINTS *****************************************
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
        string="Duración (dias)", 
        default=14,
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin', 
        store=True,
        string="Fecha Fin")

    proyecto = fields.Many2one(
        'gestion_tareas_sme.proyectos_sme',
        string='Proyecto',
        ondelete='set null',
        help='Proyecto de los sprints'
    )
    

    # METODOS SPRINTS ***************************************

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


# TECNOLOGIAS_SERGI *******************************************
class tecnologias_sme(models.Model):
    _name = 'gestion_tareas_sme.tecnologias_sme'
    _description = 'Modelo de Tecnologías'

    # ATRIBUTOS TECNOLOGIAS ***********************************

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

    desarrolladores_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_dev_tec',
        column2='desarrollador_id',
        column1='tecnologia_id',
        string='Desarrolladores'
    )
        

# TECNOLOGIAS_SERGI *******************************************
class desarrolladores_sme(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    es_desarrollador = fields.Boolean(
        string='Es desarrollador',
        default=False
    )

    tecnologias_ids = fields.Many2many (
        comodel_name='gestion_tareas_sme.tecnologias_sme',
        relation='rel_dev_tec',
        column1='desarrollador_id',
        column2='tecnologia_id',
        string='Tecnologias'
    )


    @api.onchange('es_desarrollador')
    def _onchange_es_desarrollador(self):
        # Buscar la categoría "Desarrollador"
        categorias = self.env['res.partner.category'].search([('name', '=', 'Desarrollador')])

        if len(categorias) > 0:
            # Si existe, usar la primera encontrada
            category = categorias[0]
        else:
            # Si no existe, crearla
            category = self.env['res.partner.category'].create({'name': 'Desarrollador'})

        # Asignar la categoría al contacto
        self.category_id = [(4, category.id)]





