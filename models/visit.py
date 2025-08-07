from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class HospitalVisit(models.Model):
    """
    Represents a scheduled or completed patient visit in the hospital.

    Each visit is associated with a doctor and a patient and may include one or more diagnoses.
    Visits can have different statuses (planned, done, or cancelled), and include fields for both
    planned and actual visit times.

    Business logic ensures visits cannot be modified once marked as done and prevents duplicates
    for the same doctor-patient-date combination.
    """
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
    visit_count = fields.Integer(string="Visit Count", compute="_compute_count", store=True)

    @api.depends()
    def _compute_count(self):
        """
        Compute a fixed visit count for each record.

        Currently, always sets count to 1. This is a placeholder for possible future logic.
        """
        for rec in self:
            rec.visit_count = 1

    @api.constrains('actual_datetime', 'doctor_id', 'status')
    def _check_visit_constraints(self):
        """
        Prevent editing of visits that are marked as 'done'.

        Raises:
            ValidationError: if someone tries to modify a visit that is already marked as done.
        """
        for rec in self:
            if rec.status == 'done':
                if self.env.context.get('no_check_edit'):
                    continue
                raise ValidationError("You cannot change completed visit.")

    @api.constrains('doctor_id', 'patient_id', 'planned_datetime')
    def _check_duplicate_visit(self):
        """
        Prevent scheduling multiple visits for the same doctor and patient on the same day.

        Raises:
            ValidationError: if a duplicate visit is found.
        """
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
        """
        Prevent deletion of visits that have diagnoses.

        Raises:
            ValidationError: if the visit has linked diagnosis records.
        """
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError("You cannot delete visits with diagnoses.")
        return super().unlink()