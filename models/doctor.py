from odoo import models, fields, api
from lxml import etree

class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    specialty_id = fields.Many2one('hr.hospital.specialty', string="Specialty")
    is_intern = fields.Boolean(string="Intern")
    mentor_id = fields.Many2one('hr.hospital.doctor', string="Mentor", domain="[('is_intern','=',False)]")
    intern_ids = fields.One2many('hr.hospital.doctor', 'mentor_id', string="Interns")
    visit_ids = fields.One2many('hr.hospital.visit', 'doctor_id', string="Visits")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in doc.xpath("//field[@name='mentor_id']"):
                field.set('attrs', '{"invisible": [["is_intern", "=", False]]}')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
