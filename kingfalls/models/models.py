# -*- coding: utf-8 -*-


from email.policy import default
from odoo import models, fields, api


class player(models.Model):
    _name = 'kingfalls.player'
    _description = 'player of the game'

    name = fields.Char(Required=True)
    contrasena = fields.Integer()
    vida = fields.Integer(default = 100)
    aguante = fields.Integer(default = 100)
    nivel = fields.Integer(default = 1)
    avatar = fields.Image(max_width = 250, max_height = 250)


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


    


     
