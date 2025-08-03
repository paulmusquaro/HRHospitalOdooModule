from odoo import models
from datetime import datetime

class ReportDoctorTemplate(models.AbstractModel):
    _name = 'report.hr_hospital.report_doctor_template'  # важливо: має співпадати з report_name у XML
    _description = 'Doctor Report'

    def _get_report_values(self, docids, data=None):
        print("⚠️ _get_report_values called!")  # DEBUG
        docs = self.env['hr.hospital.doctor'].browse(docids)
        latest_visits = {}
        for doctor in docs:
            for visit in doctor.visit_ids:
                pid = str(visit.patient_id.id)
                latest_visits[pid] = visit
        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M')
        return {
            'doc_ids': docids,
            'doc_model': 'hr.hospital.doctor',
            'docs': docs,
            'latest_visits': latest_visits,
            'company': self.env.company,
            'now': formatted_now,
        }