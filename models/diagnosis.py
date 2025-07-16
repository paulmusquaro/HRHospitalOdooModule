from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one('hr.hospital.visit', string="Visit", required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string="Disease", required=True)
    description = fields.Text(string="Treatment Notes")
    approved = fields.Boolean(string="Approved by Mentor")
    patient_id_related = fields.Many2one('hr.hospital.patient', string='Patient (Related)', compute='_compute_patient', store=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string="Doctor", related='visit_id.doctor_id', store=True, readonly=True)
    diagnosis_date = fields.Datetime(string="Diagnosis Date", related='visit_id.actual_datetime', store=True, readonly=True)
    notes = fields.Text(string='Visit Notes', related='visit_id.notes', store=True, readonly=True)
    # diagnosis_count = fields.Integer(string="Diagnosis Count", compute='_compute_diagnosis_count', store=True)
    #
    # @api.depends()
    # def _compute_diagnosis_count(self):
    #     for rec in self:
    #         rec.diagnosis_count = 1

    @api.depends('visit_id.patient_id')
    def _compute_patient(self):
        for rec in self:
            rec.patient_id_related = rec.visit_id.patient_id

    @api.constrains('approved')
    def _check_approval_rights(self):
        for rec in self:
            if rec.visit_id.doctor_id.is_intern and not rec.approved:
                raise ValidationError("Diagnosis by intern must be approved by mentor.")