from odoo import models, fields

class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    parent_id = fields.Many2one('hr.hospital.disease', string="Parent Disease")
    child_ids = fields.One2many('hr.hospital.disease', 'parent_id', string="Sub Diseases")
