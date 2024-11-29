from odoo import models, fields, api
import re

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _order = 'barcode desc'
    it_tickets = fields.One2many('it.ticket', 'user_id', string='IT Tickets')
    it_devices = fields.One2many('it.device.user.history', 'user_id', string='IT Devices')
    arabic_name= fields.Char(string='Arabic Name')
    nationality_code = fields.Char(string='Nationality Code')
    certificate = fields.Selection([
        ('diploma', 'Diploma'),
        ('bachelor degree', 'Bachelor Degree'),
        ('high-school or less', 'High-School or Less'),
        ('master degree','Master Degree'),
        ('phd', 'PhD'),  # Added new option
        ('associate degree', 'Associate Degree'),  # Added new option
        ('other', 'Other'),  # Added 'other' if needed
        ('unknown', 'Unknown'),
    ], 'Certificate Level', default='unknown', groups="hr.group_hr_user", tracking=True)

    maritial_code = fields.Char(string='Maritial Code')
    nudoss        = fields.Char(string='Nudoss')

    
    work_contact_id_value = fields.Char(string="Work Contact ID", compute="_compute_work_contact_id_value")

    @api.depends('work_contact_id')
    def _compute_work_contact_id_value(self):
        for record in self:
            record.work_contact_id_value = record.work_contact_id.id if record.work_contact_id else ''

    @api.model
    def _get_next_barcode(self, last_barcode):
        """
        Increment the barcode by 1, assuming the barcode format is a letter followed by digits.
        For example, if the last barcode is 'A1502', the next should be 'A1503'.
        """
        if last_barcode:
            # Extract the numeric part from the end of the barcode
            match = re.match(r"([A-Z]*)(\d+)", last_barcode, re.I)
            if match:
                prefix = match.groups()[0]
                number = match.groups()[1]
                new_number = str(int(number) + 1).zfill(len(number))
                return f"{prefix}{new_number}"
        return 'A0001'  # Fallback if no previous barcode exists

    def generate_random_barcode(self):
        """
        Override the original method to generate a new barcode based on the last barcode in sequence.
        """
        for employee in self:
            # Search for the last barcode with the highest number
            last_employee = self.search([('barcode', '!=', False)], order="barcode desc", limit=1)
            last_barcode = last_employee.barcode if last_employee else None
            new_barcode = self._get_next_barcode(last_barcode)
            employee.barcode = new_barcode