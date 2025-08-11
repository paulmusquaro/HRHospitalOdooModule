from odoo import fields, models


class PatientDoctorUpdateWizard(models.TransientModel):
    """
    A wizard that allows bulk updating of patients' personal doctors.

    Used by hospital administrators or staff to assign or reassign multiple
    patients to a new doctor in a single operation.
    """

    _name = "hr.hospital.patient.doctor.wizard"
    _description = "Bulk update personal doctor"

    doctor_id = fields.Many2one("hr.hospital.doctor", required=True)
    patient_ids = fields.Many2many("hr.hospital.patient")

    def action_update_doctor(self):
        """
        Perform the doctor assignment to each selected patient.

        Updates the `personal_doctor_id` field of each selected patient with the
        doctor selected in this wizard.
        """
        for patient in self.patient_ids:
            patient.personal_doctor_id = self.doctor_id
