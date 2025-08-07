from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    """
    Represents a medical diagnosis made during a hospital visit.

    Each diagnosis is linked to a specific patient visit and includes details such as the diagnosed disease,
    treatment description, and mentor approval (if required). Diagnoses are created by doctors and may require
    approval if the doctor is an intern.

    Fields like doctor, patient, and visit date are inherited from the related visit for consistency.
    """
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


    @api.depends('visit_id.patient_id')
    def _compute_patient(self):
        """
        Compute the related patient based on the selected visit.

        This method ensures that the 'patient_id_related' field reflects the patient assigned
        to the corresponding hospital visit, maintaining data consistency across models.
        """
        for rec in self:
            rec.patient_id_related = rec.visit_id.patient_id

    @api.constrains('approved')
    def _check_approval_rights(self):
        """
        Ensure mentor approval is provided for diagnoses created by interns.

        Business rule: If the doctor who created the diagnosis is marked as an intern,
        the 'approved' checkbox must be enabled by their mentor. Otherwise, a ValidationError is raised
        to prevent saving the record.
        """
        for rec in self:
            if rec.visit_id.doctor_id.is_intern and not rec.approved:
                raise ValidationError("Diagnosis by intern must be approved by mentor.")