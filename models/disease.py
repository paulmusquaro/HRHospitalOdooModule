from odoo import models, fields

class HospitalDisease(models.Model):
    """
    Represents a disease or medical condition used for diagnosis in the hospital system.

    Diseases can be organized in a hierarchical structure using parent-child relationships,
    allowing grouping of similar or related conditions (e.g. 'Infections' → 'Viral Infection' → 'Flu').

    This model is intended to be used when assigning diagnoses to patient visits.
    """
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    parent_id = fields.Many2one('hr.hospital.disease', string="Parent Disease", index=True, ondelete='cascade')
    child_ids = fields.One2many('hr.hospital.disease', 'parent_id', string="Sub Diseases")