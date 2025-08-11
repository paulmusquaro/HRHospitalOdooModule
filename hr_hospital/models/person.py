from odoo import fields, models


class Person(models.AbstractModel):
    """
    Abstract model for storing basic personal information.

    This model is intended to be inherited by models such as Patient and Doctor
    to avoid duplication of commonly used fields such as names, contact information,
    and a reference to the related system user.

    Note:
        As an abstract model (`_name`, not `_inherit`), no table is created in the database.
    """

    _name = "hr.hospital.person"
    _description = "Abstract Person Model"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    phone = fields.Char(string="Phone")
    photo = fields.Image(string="Photo")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    user_id = fields.Many2one(
        "res.users",
        string="Related User",
        ondelete="set null",
        index=True,
        help="The Odoo user that represents this person",
    )
