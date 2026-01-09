from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class plato_sme(models.Model):
    _name = 'gestion_restaurante_sme.plato_sme'
    _description = 'gestion_restaurante_sme.plato_sme'

    codigo = fields.Char(compute="_get_codigo")

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Introduzca el nombre del plato")
    description = fields.Text(
        string="Descripción",
        help="Breve descripción del plato")

    precio = fields.Float(
        string="Precio",
        required=True,
        help="Precio del plato")

    tiempo_preparacion = fields.Integer(
        string="Tiempo de preparación",
        help="Tiempo de preparación en minutos")

    disponible = fields.Boolean(
        string="Disponible",
        default=True)

    categoria = fields.Selection([
        ("entrante", "Entrante"),
        ("principal", "Principal"),
        ("postre", "Postre"),
        ("bebida", "Bebida")
    ],
    string="Categoria",
    help="Categoria del plato")

    precio_con_iva = fields.Float(compute="_compute_precio_con_iva")

    descuento = fields.Float(
        string="Descuento (%)",
        help="Descuento en porcentaje"
        )

    precio_final = fields.Float(
        compute="_precio_final",
        store=True
    )

    menu = fields.Many2one(
        'gestion_restaurante_sme.menu_sme',
        string="Menu",
        ondelete="set null",
        help="Menu del plato")

    rel_ingredientes = fields.Many2many(
        comodel_name="gestion_restaurante_sme.ingrediente_sme",
        relation="relacion_platos_ingredientes",
        column1="rel_platos",
        column2="rel_ingredientes",
        string="Ingredients",
        help="Ingredientes del plato")

    


    

    def _compute_precio_con_iva(self):
        for plato in self:
            if not plato.precio:
                plato.precio_con_iva = 0.0
            else:
                plato.precio_con_iva = plato.precio * 1.10




    def _get_codigo(self):
        for plato in self:
            
            # Verificamos que tenga sprint asignado
            if not plato.categoria:
                plato.codigo = "PLT_"+str(plato.id)

                # Generamos el código
            plato.codigo = str(plato.categoria[:3]).upper() + "_" + str(plato.id)


    @api.depends('precio', 'descuento')
    def _precio_final(self):
        for plato in self:
            if plato.descuento:
                plato.precio_final = plato.precio *  1 - (plato.descuento / 100)
            else:
                plato.precio_final = plato.precio
                




            

class menu_sme(models.Model):
    _name = 'gestion_restaurante_sme.menu_sme'
    _description = 'gestion_restaurante_sme.menu_sme'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Introduzca el nombre del Menu")
    description = fields.Text(
        string="Descripción",
        help="Breve descripción del Menu")

    fecha_inicio = fields.Date(
        string="Fecha inicio",
        help="Fecha de inicio del menu",
        required=True)

    fecha_fin = fields.Date(
        string="Fecha fin",
        help="Fecha de fin del menu")

    activo = fields.Boolean(
        string="Activo",
        help="Si el menu esta activo o no")

    platos = fields.One2many(
        'gestion_restaurante_sme.plato_sme',
        'menu',
        string="Platos",
        help="Platos incluidos en el menu")

    precio_total = fields.Float(
        string="Precio total",
        compute="_compute_precio_total",
        store=True,
        )

    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            precios = menu.platos.mapped('precio_final')
            menu.precio_total = sum(precios)

    
class ingrediente_sme(models.Model):
    _name = 'gestion_restaurante_sme.ingrediente_sme'
    _description = 'gestion_restaurante_sme.ingrediente_sme'

    name = fields.Char(
        string="Nombre",
        help="Nombre del ingrediente",
        required=True)

    es_alergeno = fields.Boolean(
        string="Alergeno",
        help="indica si el ingrediente es alergeno")


    description = fields.Text(
        string="Descripción",
        help="Descripción del ingrediente")

    rel_platos = fields.Many2many(
        comodel_name="gestion_restaurante_sme.plato_sme",
        relation="relacion_platos_ingredientes",
        column1="rel_ingredientes",
        column2="rel_platos",
        string="Plato",
        help="platos que contienen el ingrediente")

    


    