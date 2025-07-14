from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one('hr.hospital.visit', string="Visit", required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string="Disease", required=True)
    description = fields.Text(string="Treatment Notes")
    approved = fields.Boolean(string="Approved by Mentor")

    @api.constrains('approved')
    def _check_approval_rights(self):
        for rec in self:
            if rec.visit_id.doctor_id.is_intern and not rec.approved:
                raise ValidationError("Diagnosis by intern must be approved by mentor.")