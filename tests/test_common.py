from odoo.tests.common import TransactionCase, new_test_user
from datetime import datetime, timedelta
import uuid


class HospitalCommon(TransactionCase):
    """
    Common test setup for HR Hospital module.

    Provides shared test data, reusable records, and users with specific
    access groups (doctor, intern, manager, admin, patient).

    Inherited by other test classes to reduce code duplication.
    """

    @classmethod
    def setUpClass(cls):
        """
        Create demo users, medical entities and link them appropriately.

        This includes:
        - Users for each group (doctor, intern, etc.)
        - One specialty (Cardiology)
        - One doctor and one intern (linked via mentor)
        - One patient (linked to doctor)
        - One disease
        - One planned visit for intern and patient
        """
        super().setUpClass()

        cls.spec_cardio = cls.env['hr.hospital.specialty'].create({
            'name': 'Cardiology',
        })

        cls.user_doctor = new_test_user(
            cls.env, login=f'doctor_{uuid.uuid4().hex[:6]}',
            groups='hr_hospital.group_doctor')
        cls.user_intern = new_test_user(
            cls.env, login=f'intern_{uuid.uuid4().hex[:6]}',
            groups='hr_hospital.group_intern')
        cls.user_manager = new_test_user(
            cls.env, login=f'manager_{uuid.uuid4().hex[:6]}',
            groups='hr_hospital.group_manager')
        cls.user_admin = new_test_user(
            cls.env, login=f'admin_{uuid.uuid4().hex[:6]}',
            groups='hr_hospital.group_admin')
        cls.user_patient = new_test_user(
            cls.env, login=f'patient_{uuid.uuid4().hex[:6]}',
            groups='hr_hospital.group_patient')

        cls.doctor = cls.env['hr.hospital.doctor'].sudo().create({
            'first_name': 'Alice', 'last_name': 'Mentor',
            'specialty_id': cls.spec_cardio.id,
            'user_id': cls.user_doctor.id,
        })
        cls.intern = cls.env['hr.hospital.doctor'].sudo().create({
            'first_name': 'Bob', 'last_name': 'Intern',
            'is_intern': True,
            'mentor_id': cls.doctor.id,
            'specialty_id': cls.spec_cardio.id,
            'user_id': cls.user_intern.id,
        })
        cls.patient = cls.env['hr.hospital.patient'].sudo().create({
            'first_name': 'John', 'last_name': 'Patient',
            'personal_doctor_id': cls.doctor.id,
            'user_id': cls.user_patient.id,
        })
        cls.disease = cls.env['hr.hospital.disease'].create({'name': 'Flu'})
        cls.visit = cls.env['hr.hospital.visit'].sudo().create({
            'doctor_id': cls.intern.id,
            'patient_id': cls.patient.id,
            'planned_datetime': datetime.now() + timedelta(days=1),
        })

    def setUp(self):
        """
        Instance-level setup: map shared class-level data
        into instance attributes for use in each test.
        """
        super().setUp()
        for name in (
            'user_doctor', 'user_intern', 'user_manager', 'user_admin',
            'user_patient', 'doctor', 'intern', 'patient', 'disease', 'visit'
        ):
            setattr(self, name, getattr(self.__class__, name))
