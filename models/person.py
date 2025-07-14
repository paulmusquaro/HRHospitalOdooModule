from odoo import models, fields

class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person Model'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    phone = fields.Char(string="Phone")
    photo = fields.Image(string="Photo")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
