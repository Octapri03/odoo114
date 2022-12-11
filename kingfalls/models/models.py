# -*- coding: utf-8 -*-


from email.policy import default
from odoo import models, fields, api


class player(models.Model):
    _name = 'kingfalls.player'
    _description = 'player of the game'

    name = fields.Char(Required=True)
    comarca = fields.Many2one('kingfalls.comarca')
    bando = fields.Many2one('kingfalls.bando')
    poblacion = fields.Integer(default = 100)
    guardias = fields.Integer(default = 10)
    dinero = fields.Integer(default = 1000)
    aliados = fields.Many2many('kingfalls.ciudad', compute='lista_aliados')

    @api.depends('bando')
    def lista_aliados(self):
        for c in self:
            c.aliados = self.env['kingfalls.ciudad'].search([( "bando.name", "=", c.bando.name )])
            print(c.aliados)
            print(c.bando)

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
            dinero = player.dinero + 500

            player.write({
                "dinero": dinero
            })

class ciudad(models.Model):
    _name = 'kingfalls.ciudad'
    _description = 'ciudad'

    name = fields.Char(Required=True)
    descripcion = fields.Char()
    comarca = fields.Many2one('kingfalls.comarca')
    bando = fields.Many2one('kingfalls.bando')
    image = fields.Image(max_width = 500, max_height = 500)
    poblacion = fields.Integer(default = 100)
    guardias = fields.Integer(default = 10)
    defensa = fields.Selection([('1', "Alta"), ('2', "Media"), ('3', "Baja")], default = '3')

class bando(models.Model):
    _name = 'kingfalls.bando'
    _description = 'bando'

    name = fields.Char(Required=True)
    descripcion = fields.Char(Required=True)
    image = fields.Image(max_width = 250, max_height = 250)

class comarca(models.Model):
    _name = 'kingfalls.comarca'
    _description = 'comarca'

    name = fields.Char(Required=True)
    descripcion = fields.Char(Required=True)
    image = fields.Image(max_width = 250, max_height = 250)

class raid(models.Model):
    _name = 'kingfalls.raid'
    _description = 'raids'

    name = fields.Char(Required=True)
    descripcion = fields.Char()
    image = fields.Image(max_width = 500, max_height = 500)
    amenaza = fields.Selection([('1', "Alta"), ('2', "Media"), ('3', "Baja")], default='1')



class monstruos(models.Model):
    _name = 'kingfalls.monstruos'
    _description = 'raids'

    name = fields.Char(Required=True)
    descripcion = fields.Char()
    image = fields.Image(max_width = 500, max_height = 500)
    fuerza = fields.Integer()
    vida = fields.Integer(default = 50)
    aguante = fields.Integer(default = 75)
    nivel = fields.Integer(default = 1)   


    


     
