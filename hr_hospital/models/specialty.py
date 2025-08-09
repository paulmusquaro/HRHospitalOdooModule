from odoo import models, fields


class Specialty(models.Model):
    """
    Represents a medical specialty that a doctor can have.

    Examples of specialties include Cardiology, Neurology, Pediatrics, etc.
    Doctors can be assigned to a specialty using the `specialty_id` field
    in the `hr.hospital.doctor` model.

    This model allows for categorizing doctors by their field of medical expertise.
    """
    _name = 'hr.hospital.specialty'
    _description = 'Medical Specialty'

    name = fields.Char(string="Name", required=True, translate=True)