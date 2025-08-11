from odoo import fields, models


class DiagnosisReportWizard(models.TransientModel):
    """
    A wizard model for generating filtered diagnosis reports.

    This wizard allows users to filter diagnosis records based on:
    - Selected doctors
    - Selected diseases
    - Visit date range (from / to)

    It is used to quickly analyze diagnoses via various views:
    tree, form, pivot, graph.
    """

    _name = "hr.hospital.diagnosis.report.wizard"
    _description = "Diagnosis Report Wizard"

    doctor_ids = fields.Many2many("hr.hospital.doctor")
    disease_ids = fields.Many2many("hr.hospital.disease")
    date_from = fields.Date()
    date_to = fields.Date()

    def get_diagnosis_records(self):
        """
        Returns an action that opens a view with filtered diagnosis records
        based on the criteria provided in the wizard.

        Filters applied:
        - Doctor(s)
        - Disease(s)
        - Visit actual date between `date_from` and `date_to`

        :return: dict representing an ir.actions.act_window action
        """
        domain = []
        if self.doctor_ids:
            domain += [("visit_id.doctor_id", "in", self.doctor_ids.ids)]
        if self.disease_ids:
            domain += [("disease_id", "in", self.disease_ids.ids)]
        if self.date_from:
            domain += [("visit_id.actual_datetime", ">=", self.date_from)]
        if self.date_to:
            domain += [("visit_id.actual_datetime", "<=", self.date_to)]

        return {
            "type": "ir.actions.act_window",
            "name": "Filtered Diagnoses",
            "res_model": "hr.hospital.diagnosis",
            "view_mode": "tree,form,pivot,graph",
            "views": [
                (self.env.ref("hr_hospital.view_diagnosis_tree_for_report").id, "tree"),
                (False, "form"),
                (False, "pivot"),
                (False, "graph"),
            ],
            "domain": domain,
            "context": {
                "group_by": "disease_id",
            },
            "target": "current",
        }
