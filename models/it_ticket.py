from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ItTicket(models.Model):
    _name = 'it.ticket'
    _description = 'IT Ticket'
    _inherit        = ['mail.thread']
    subject = fields.Char(string='Ticket Subject', required=True)
    description = fields.Text(string='Ticket Description')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium', tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted','Submitted'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    ], string='Status', default='draft', tracking=True)
    device_id  = fields.Many2one('it.device', string='Device' , domain="[('id', 'in', device_ids)]")
    device_ids = fields.Many2many('it.device', string='Devices', compute='_compute_device_ids')

    user_id    = fields.Many2one('hr.employee', string='User', default=lambda self: self.env.user.employee_id)
    handled_by = fields.Many2one('res.users', string='Handled By' , tracking=True)
    solution   = fields.Text(string="Solution", tracking=True)

    @api.depends('user_id')
    def _compute_device_ids(self):
        for record in self:
            if record.user_id:
                device_histories = self.env['it.device.user.history'].search([
                    ('user_id', '=', record.user_id.id),
                    ('end_date', '=', False)  # To ensure the device is currently assigned to the user
                ])
                record.device_ids = device_histories.mapped('device_id')
            else:
                record.device_ids = self.env['it.device']

  

   
            
   

    def action_submit(self):
        if self.user_id == self.env.user.employee_id:
            self.status = 'submitted'
        else:
            raise UserError('Only the Creator of Ticket Can Submit.')
        

    def action_assign_it_support(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Assign IT Support',
        'res_model': 'it.support.assign.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'default_ticket_id': self.id,
        }
    }

    def action_cancel(self):
        if self.handled_by == self.env.user:
           return {
                'type': 'ir.actions.act_window',
                'name': 'Confirm Cancel',
                'res_model': 'cancel.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_ticket_id': self.id,
                }
            }
        else:
            raise UserError(f'Only {self.handled_by.name} Can Cancel this Ticket  .')
        
    def action_done(self):
        if self.handled_by == self.env.user:
           return {
                'type': 'ir.actions.act_window',
                'name': 'Provide Solution',
                'res_model': 'solution.input.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_ticket_id': self.id,
                }
            }
        else:
            raise UserError(f'Only {self.handled_by.name} Can Close this Ticket  .')

