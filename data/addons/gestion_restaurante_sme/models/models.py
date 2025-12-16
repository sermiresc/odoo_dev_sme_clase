from odoo import models, fields, api


class plato_sme(models.Model):
    _name = 'gestion_restaurante_sme.plato_sme'
    _description = 'gestion_restaurante_sme.plato_sme'

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

    


    