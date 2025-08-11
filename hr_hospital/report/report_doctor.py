from datetime import datetime

from odoo import models


class ReportDoctorTemplate(models.AbstractModel):
    """
    Abstract model for generating doctor reports.

    This report aggregates doctor data and retrieves the latest visit
    per patient associated with the doctor. It is rendered via QWeb
    using the XML template `report_hr_hospital.report_doctor_template`.

    The model name must match the template's `report_xxx` declaration.
    """

    _name = "report.hr_hospital.report_doctor_template"
    _description = "Doctor Report"

    def _get_report_values(self, docids, data=None):
        """
        Provide the data dictionary required by the QWeb report rendering engine.

        Args:
            docids (list): List of doctor record IDs to include in the report.
            data (dict): Additional data passed to the report (unused).

        Returns:
            dict: A dictionary with context values for rendering the report template.
        """
        docs = self.env["hr.hospital.doctor"].browse(docids)
        latest_visits = {}
        for doctor in docs:
            for visit in doctor.visit_ids:
                pid = str(visit.patient_id.id)
                latest_visits[pid] = visit
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M")
        return {
            "doc_ids": docids,
            "doc_model": "hr.hospital.doctor",
            "docs": docs,
            "latest_visits": latest_visits,
            "company": self.env.company,
            "now": formatted_now,
        }
