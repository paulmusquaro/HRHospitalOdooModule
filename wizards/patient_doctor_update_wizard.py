from odoo import fields, models


class PatientDoctorUpdateWizard(models.TransientModel):
    _name = 'hr.hospital.patient.doctor.wizard'
    _description = 'Bulk update personal doctor'

    doctor_id = fields.Many2one('hr.hospital.doctor', required=True)
    patient_ids = fields.Many2many('hr.hospital.patient')

    def action_update_doctor(self):
        for patient in self.patient_ids:
            patient.personal_doctor_id = self.doctor_id