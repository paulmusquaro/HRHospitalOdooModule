from odoo import models, fields, api
from datetime import date

class Patient(models.Model):
    """
    Represents a hospital patient.

    Patients are individuals who receive care and attend visits.
    This model stores personal details, birth date, emergency contact,
    and provides computed fields like full name and age.

    Inherits from hr.hospital.person to reuse personal details (first name, last name, phone, etc.).
    """
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    personal_doctor_id = fields.Many2one('hr.hospital.doctor', string='Personal Doctor')
    birth_date = fields.Date(string="Birth Date")
    passport_data = fields.Char(string="Passport Information")
    contact_person = fields.Char(string="Emergency Contact")

    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    diagnosis_ids = fields.One2many(
        'hr.hospital.diagnosis',
        'patient_id_related',
        string="Diagnosis History",
        compute='_compute_diagnosis_ids',
        store=False
    )

    @api.depends()
    def _compute_diagnosis_ids(self):
        """
        Compute and assign all diagnoses related to the patient.

        The relation is indirect: through hr.hospital.visit
        and linked diagnosis records where patient_id is involved.
        """
        for patient in self:
            diagnoses = self.env['hr.hospital.diagnosis'].search([
                ('visit_id.patient_id', '=', patient.id)
            ])
            patient.diagnosis_ids = diagnoses

    @api.depends('birth_date')
    def _compute_age(self):
        """
        Compute patient's age based on their birth date.

        If birth date is not set, age will be zero.
        """
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
        """
        Compute full name of the patient using first and last name.
        """
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    def action_open_visits(self):
        """
        Open a list view of all visits for this patient.

        Returns:
            dict: An ir.actions.act_window to display visits in list and form view.
        """
        self.ensure_one()
        return {
            'name': 'Patient Visits',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_visit(self):
        """
        Open a form to create a new visit for the patient.

        Returns:
            dict: An ir.actions.act_window to open the new visit form with patient pre-filled.
        """
        self.ensure_one()
        return {
            'name': 'New Visit',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_patient_id': self.id,
            },
            'target': 'current',
        }

