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
    diagnosis_ids = fields.One2many(
        'hr.hospital.diagnosis',
        'patient_id_related',
        string="Diagnosis History",
        compute='_compute_diagnosis_ids',
        store=False
    )

    @api.depends()
    def _compute_diagnosis_ids(self):
        for patient in self:
            diagnoses = self.env['hr.hospital.diagnosis'].search([
                ('visit_id.patient_id', '=', patient.id)
            ])
            patient.diagnosis_ids = diagnoses

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

    def action_open_visits(self):
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

