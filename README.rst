==========================================================
HR Hospital ─ Complete Hospital & Residency Management
==========================================================

*For Odoo 17.0 – Community & Enterprise*

HR Hospital is an **all-in-one medical practice module** that streamlines daily
hospital workflow – from outpatient visits to intern supervision – while
remaining light enough for small clinics or university hospitals.

Key Highlights
==============

* **Visits & Scheduling** – plan, perform or cancel patient visits with a built-in
  calendar, status bar and duplicate-visit protection.
* **Diagnoses** – record diseases, treatment notes, mentor approval for intern
  records and rich analytical views (tree / pivot / graph).
* **Residency Supervision** – distinguish **Doctors** vs **Interns**; mentors see
  interns’ visits automatically.
* **Security Out-of-the-box** – five user groups (Patient, Intern, Doctor,
  Manager, Admin) with granular ACLs & record rules.
* **Interactive Wizards** – bulk assign personal doctors and filter diagnoses
  by doctor, disease or date range.
* **PDF Reporting** – *Doctor Report* (latest visits + patient list)
  for printing or email.
* **Demo & Tests** – realistic demo data, 19 unit / security tests.

Installation
============

Prerequisites
-------------

* **Odoo 17.0** running on Python ≥ 3.10
  (Community or Enterprise – no extra modules required)
* Python libs: ``lxml`` (already required by Odoo)

Steps
-----

1. Clone or copy *hr_hospital* into your ``custom_addons`` directory.
2. Update the add-ons path and restart Odoo.
3. Install the module from *Apps* (**activate developer mode** or enable
   «Show Apps Menus»).

Docker / odoo-helper
--------------------

If you rely on `OCA/oca-dev-tools`_ (highly recommended):

*Build + start Odoo 17 in one line*::

    odoo-helper build --odoo-version 17.0
    odoo-helper start -d test_hosp -m hr_hospital --load-demo

.. _OCA/oca-dev-tools: https://github.com/OCA/oca-dev-tools

Running the Automated Test-Suite
================================

Execute **all** module tests (business + security) with coverage:

::

    odoo-helper test -d test_hosp -m hr_hospital --coverage

Afterwards display the percentage of covered lines (only this addon):

::

    coverage report -m --include="custom_addons/hr_hospital/*"

The test layer creates temporary users, visits, diagnoses, etc.—nothing is
written to your real database.

License
=======

This addon is released under the **OPL-1** license (see ``LICENSE``).

Contributing
============

Merge requests, issues or feature ideas are very welcome!
Follow the usual OCA guidelines for coding style, commits and pull requests.

