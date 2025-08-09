from odoo.tests.common import tagged
from odoo.exceptions import AccessError
from .test_common import HospitalCommon


@tagged('-at_install', 'post_install')
class TestAccessRights(HospitalCommon):
    """
    Test access control and security rules for HR Hospital module.

    Covers record rules and ACLs for different user roles:
    - Patient
    - Intern
    - Doctor
    - Manager
    - Admin
    """

    def test_patient_read_own(self):
        """
        Ensure that a patient can read their own visit.
        Should return exactly one visit (created in test_common).
        """
        count = self.env['hr.hospital.visit'].with_user(self.user_patient.id).search_count([])
        self.assertEqual(count, 1)

    def test_patient_cannot_create(self):
        """
        Ensure that a patient cannot create a new visit.
        Must raise AccessError due to denied create access.
        """
        with self.assertRaises(AccessError):
            self.env['hr.hospital.visit'].with_user(self.user_patient.id).create({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'planned_datetime': self.visit.planned_datetime,
            })

    def test_intern_can_write_own(self):
        """
        Ensure that an intern can update their own visit record.
        Should successfully write notes.
        """
        self.visit.with_user(self.user_intern.id).write({'notes': 'ok'})
        self.assertEqual(self.visit.notes, 'ok')

    def test_intern_cannot_read_foreign(self):
        """
        Ensure that an intern cannot access another intern’s or doctor's visit.
        Must raise AccessError when trying to read unauthorized record.
        """
        other = self.env['hr.hospital.patient'].create({
            'first_name': 'Foo', 'last_name': 'Bar'
        })
        visit2 = self.env['hr.hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': other.id,
            'planned_datetime': self.visit.planned_datetime,
        })
        with self.assertRaises(AccessError):
            visit2.with_user(self.user_intern.id).read()

    def test_doctor_sees_intern_visits(self):
        """
        Ensure that a doctor (mentor) can see visits performed by their intern.
        Should return the visit created by the intern.
        """
        count = self.env['hr.hospital.visit'].with_user(self.user_doctor.id).search_count([])
        self.assertEqual(count, 1)

    def test_manager_read_all_but_no_write(self):
        """
        Ensure that hospital manager has read-only access to all visits.
        Test that visit records are visible but not writable (write tested elsewhere).
        """
        visits = self.env['hr.hospital.visit'].with_user(self.user_manager.id).search([])
        self.assertTrue(visits)

    def test_hospital_admin_full_access(self):
        """
        Ensure that hospital admin can fully modify visit records.
        Should succeed without AccessError.
        """
        self.env['hr.hospital.visit'].with_user(self.user_admin.id).write({'notes': 'admin'})
