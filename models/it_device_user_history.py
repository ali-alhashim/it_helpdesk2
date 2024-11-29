from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ItDeviceUserHistory(models.Model):
    _name = 'it.device.user.history'
    _description    = 'IT Device User History'
    _inherit        = ['mail.thread']
    _rec_name       = "reference"
    _order = 'start_date desc'
    device_id       = fields.Many2one('it.device', string='Device')
    user_id         = fields.Many2one('hr.employee', string='User')
    start_date      = fields.Date(string='Start Date', tracking=True)
    end_date        = fields.Date(string='End Date', tracking=True)
    state           = fields.Selection([('new','New'),('used','Used'), ('old','Old'),('damaged','Damaged'),('lost','Lost')], default='new', tracking=True)
    note            = fields.Text(string = "note", tracking=True)

    reference       = fields.Char(string="Reference", default='New', copy=False)

    device_type     = fields.Selection(related='device_id.type', string='Device Type', store=True)
    arabic_name     = fields.Char(related='user_id.arabic_name', string='Arabic Name')

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                # Generate a new reference using the sequence
                vals['reference'] = self.env['ir.sequence'].next_by_code('it.asset.code') or 'New'
                
                # Ensure the reference is unique in the current environment (to handle edge cases)
                if self.search([('reference', '=', vals['reference'])]):
                    raise UserError('The reference generated is duplicated. Please try creating the record again.')
                    # get last reference and add +1 then try

        return super(ItDeviceUserHistory, self).create(vals_list)
    
    
    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise ValidationError("End Date must be after Start Date.")