from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    status = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='planned')

    planned_datetime = fields.Datetime(string="Planned Date & Time")
    actual_datetime = fields.Datetime(string="Actual Visit Time")

    doctor_id = fields.Many2one('hr.hospital.doctor', string="Doctor")
    patient_id = fields.Many2one('hr.hospital.patient', string="Patient")
    diagnosis_ids = fields.One2many('hr.hospital.diagnosis', 'visit_id', string="Diagnoses")
    notes = fields.Text(string='Notes')

    @api.constrains('actual_datetime', 'doctor_id', 'status')
    def _check_visit_constraints(self):
        for rec in self:
            if rec.status == 'done':
                if self.env.context.get('no_check_edit'):
                    continue
                raise ValidationError("You cannot change completed visit.")

    @api.constrains('doctor_id', 'patient_id', 'planned_datetime')
    def _check_duplicate_visit(self):
        for rec in self:
            same_day_start = rec.planned_datetime.date()
            visits = self.search([
                ('id', '!=', rec.id),
                ('doctor_id', '=', rec.doctor_id.id),
                ('patient_id', '=', rec.patient_id.id),
                ('planned_datetime', '>=', same_day_start),
                ('planned_datetime', '<', same_day_start + timedelta(days=1))
            ])
            if visits:
                raise ValidationError("This patient is already scheduled with this doctor on this day.")

    def unlink(self):
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError("You cannot delete visits with diagnoses.")
        return super().unlink()