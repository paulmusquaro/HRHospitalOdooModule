from odoo import models, fields, api
from lxml import etree

class Doctor(models.Model):
    """
    Represents a medical doctor within the hospital system.

    A doctor can be either a licensed specialist or an intern.
    Interns are linked to a mentor doctor. The model also includes a computed
    full name, list of supervised interns, and visit history.

    Inherits from hr.hospital.person to reuse common personal details such as name, gender, phone, etc.
    """
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    specialty_id = fields.Many2one('hr.hospital.specialty', string="Specialty")
    is_intern = fields.Boolean(string="Intern")
    mentor_id = fields.Many2one('hr.hospital.doctor', string="Mentor", domain="[('is_intern','=',False)]")
    intern_ids = fields.One2many('hr.hospital.doctor', 'mentor_id', string="Interns")
    visit_ids = fields.One2many('hr.hospital.visit', 'doctor_id', string="Visits")
    interns_names = fields.Char(string="Interns' names", compute='_compute_interns_names', store=True)

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """
        Compute the full name of the doctor based on first and last names.
        """
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    @api.depends('intern_ids.name')
    def _compute_interns_names(self):
        """
        Compute a comma-separated string of the names of all assigned interns.
        """
        for rec in self:
            rec.interns_names = ', '.join(rec.intern_ids.mapped('name') or [])

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """
        Customize the form view to conditionally hide the mentor field
        when the doctor is not marked as an intern.

        This enhances usability by hiding irrelevant fields.
        """
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in doc.xpath("//field[@name='mentor_id']"):
                field.set('attrs', '{"invisible": [["is_intern", "=", False]]}')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
