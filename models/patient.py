from odoo import models, fields, api
from datetime import date

class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    personal_doctor_id = fields.Many2one('hr.hospital.doctor', string='Personal Doctor')
    birth_date = fields.Date(string="Birth Date")
    passport_data = fields.Char(string="Passport Information")
    contact_person = fields.Char(string="Emergency Contact")

    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()
