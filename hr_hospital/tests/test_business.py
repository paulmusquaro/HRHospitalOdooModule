from datetime import datetime, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import tagged

from .test_common import HospitalCommon


@tagged("-at_install", "post_install")
class TestBusinessLogic(HospitalCommon):
    """
    Business logic tests for the HR Hospital module.

    This class contains test cases for domain logic, constraints, and
    business methods of the custom hospital management module.

    It inherits test fixtures from `HospitalCommon`.
    """

    def test_doctor_names(self):
        """
        Test that doctor full name and intern names are correctly computed.
        """
        self.assertEqual(self.doctor.name, "Alice Mentor")
        self.assertEqual(self.doctor.interns_names, "Bob Intern")

    def test_patient_age(self):
        """
        Test that patient age is correctly calculated from birth date.
        """
        self.patient.birth_date = datetime(2000, 1, 1)
        self.patient._compute_age()
        self.assertGreater(self.patient.age, 20)

    def test_duplicate_visit(self):
        """
        Ensure that a doctor cannot have two visits with the same patient
        on the same day — constraint should raise ValidationError.
        """
        with self.assertRaises(ValidationError):
            self.env["hr.hospital.visit"].create(
                {
                    "doctor_id": self.intern.id,
                    "patient_id": self.patient.id,
                    "planned_datetime": self.visit.planned_datetime
                    + timedelta(hours=2),
                }
            )

    def test_done_visit_write(self):
        """
        Ensure that once a visit is marked 'done', no updates are allowed
        without `no_check_edit` context.
        """
        self.visit.with_context(no_check_edit=True).write({"status": "done"})
        fresh_visit = self.visit.browse(self.visit.id)
        with self.assertRaises(ValidationError):
            fresh_visit.write({"doctor_id": self.doctor.id})

    def test_intern_diagnosis_needs_approval(self):
        """
        Ensure that diagnoses created by interns must be approved.
        Constraint should raise ValidationError if not approved.
        """
        with self.assertRaises(ValidationError):
            self.env["hr.hospital.diagnosis"].create(
                {
                    "visit_id": self.visit.id,
                    "disease_id": self.disease.id,
                    "approved": False,
                }
            )

    def test_unlink_with_diagnosis(self):
        """
        Test that visits with linked diagnoses cannot be deleted.
        """
        self.env["hr.hospital.diagnosis"].create(
            {
                "visit_id": self.visit.id,
                "disease_id": self.disease.id,
                "approved": True,
            }
        )
        with self.assertRaises(ValidationError):
            self.visit.unlink()

    def test_patient_doctor_update_wizard(self):
        """
        Test that the patient-doctor wizard correctly assigns
        a doctor to the selected patients.
        """
        wiz = self.env["hr.hospital.patient.doctor.wizard"].create(
            {
                "doctor_id": self.doctor.id,
                "patient_ids": [(6, 0, [self.patient.id])],
            }
        )
        wiz.action_update_doctor()
        self.assertEqual(self.patient.personal_doctor_id.id, self.doctor.id)

    def test_diagnosis_report_wizard_domain(self):
        """
        Test that the diagnosis report wizard builds the expected domain
        based on selected doctors, diseases, and dates.
        """
        wiz = self.env["hr.hospital.diagnosis.report.wizard"].create(
            {
                "doctor_ids": [(6, 0, [self.intern.id])],
                "disease_ids": [(6, 0, [self.disease.id])],
                "date_from": datetime.today().date(),
            }
        )
        action = wiz.get_diagnosis_records()
        self.assertIn(("visit_id.doctor_id", "in", [self.intern.id]), action["domain"])
        self.assertIn(("disease_id", "in", [self.disease.id]), action["domain"])
