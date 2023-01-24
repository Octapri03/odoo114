# -*- coding: utf-8 -*-


from datetime import timedelta, datetime
from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'player of the game'

    name = fields.Char(required=True)
    comarca = fields.Many2one('kingfalls.comarca')
    bando = fields.Many2one('kingfalls.bando', ondelete = "set null")
    poblacion = fields.Integer(default = 100)
    guardias = fields.Integer(default = 10)
    dinero = fields.Integer(default = 1000)
    produccion = fields.Integer(default = 500)
    aliados = fields.Many2many('kingfalls.ciudad', compute='lista_aliados')
    minas = fields.Many2many('kingfalls.mina' , compute='lista_minas')

    @api.depends('bando')
    def lista_aliados(self):
        for c in self:
            c.aliados = self.env['kingfalls.ciudad'].search([( "bando.name", "=", c.bando.name )])
            print(c.aliados)
            print(c.bando)

    @api.depends('dinero')
    def lista_minas(self):
        for c in self:
            c.minas = self.env['kingfalls.mina'].search([( "precio", "<=", c.dinero )])
            print(c.minas)
            print(c.dinero)

    @api.constrains('dinero')
    def _check_dinero(self):
        for player in self:
            if player.name == "":
                raise ValidationError("El name no puede ser nulo")

    @api.onchange('dinero')
    def _onchange_dinero(self):
        for c in self:  
            print("patata")
            if self.dinero == 0:
                return {
                    'warning': {
                    'title': "Quiebra",
                    'message': "Has gastado todo tu dinero",
                    }
                }

    def sumar_guardias(self):
        for b in self:
            if b.dinero >= 1000:
                b.guardias += 10
                b.dinero -= 1000

    @api.model
    def produce(self):  # ORM CRON
        self.search([]).produce_dinero()

    def produce_dinero(self):
        for player in self:
            dinero = player.dinero + player.produccion

            player.write({
                "dinero": dinero
            })

class ciudad(models.Model):
    _name = 'kingfalls.ciudad'
    _description = 'ciudad'

    name = fields.Char(required=True)
    descripcion = fields.Char()
    comarca = fields.Many2one('kingfalls.comarca')
    bando = fields.Many2one('kingfalls.bando', ondelete = "set null")
    image = fields.Image(max_width = 500, max_height = 500)
    poblacion = fields.Integer(default = 100)
    guardias = fields.Integer(default = 10)
    defensa = fields.Selection([('1', "Alta"), ('2', "Media"), ('3', "Baja")], default = '3')

class bando(models.Model):
    _name = 'kingfalls.bando'
    _description = 'bando'

    name = fields.Char(required=True)
    descripcion = fields.Char(required=True)
    image = fields.Image(max_width = 250, max_height = 250)

class comarca(models.Model):
    _name = 'kingfalls.comarca'
    _description = 'comarca'

    name = fields.Char(required=True)
    descripcion = fields.Char(required=True)
    image = fields.Image(max_width = 250, max_height = 250)

class raid(models.Model):
    _name = 'kingfalls.raid'
    _description = 'raids'

    name = fields.Char(required=True)
    descripcion = fields.Char()
    image = fields.Image(max_width = 500, max_height = 500)
    amenaza = fields.Selection([('1', "Alta"), ('2', "Media"), ('3', "Baja")], default='1')
    poder = fields.Integer()

class mina(models.Model):
    _name = 'kingfalls.mina'
    _description = 'minas'

    name = fields.Char(required=True)
    descripcion = fields.Char()
    produccion = fields.Integer()
    precio = fields.Integer()
    image = fields.Image(max_width = 250, max_height = 250)
 
    def comprar_mina(self):
        for b in self:
            player = self.env['res.partner'].browse(self.env.context['ctx_player'])[0]
            player.produccion = player.produccion + b.produccion
            player.dinero = player.dinero - b.precio

class monstruos(models.Model):
    _name = 'kingfalls.monstruos'
    _description = 'raids'

    name = fields.Char(required=True)
    descripcion = fields.Char()
    image = fields.Image(max_width = 500, max_height = 500)
    fuerza = fields.Integer()
    vida = fields.Integer(default = 50)
    aguante = fields.Integer(default = 75)
    nivel = fields.Integer(default = 1)   

class battle(models.Model):
    _name = 'kingfalls.battle'
    _description = 'Batallas'

    name = fields.Char()
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_duracion')
    progress = fields.Float()
    player1 = fields.Many2one('res.partner')
    player2 = fields.Many2one('res.partner')
    winner = fields.Many2one()
    draft = fields.Boolean()

    @api.onchange('player1')
    def onchange_eleccion_player1(self):
        self.name = self.player1.name
        return {
            'domain': {
            'player2': [('id', '!=', self.player1.id)],
            }
        }

    @api.onchange('player2')
    def onchange_player2(self):
        return {
            'domain': {
            'player1': [('id', '!=', self.player2.id)],
            }
        }

    @api.depends('player1', 'player2')
    def _get_duracion(self):
        for b in self:
            if b.player1.comarca != b.player2.comarca:
                time = 5.0
                b.date_end = fields.Datetime.to_string(
                fields.Datetime.from_string(b.date_start) + timedelta(days=time))
            else:
                time = 1.0
                b.date_end = fields.Datetime.to_string(fields.Datetime.from_string(b.date_start) + timedelta(days=time))

    


     
