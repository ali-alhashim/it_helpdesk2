from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

class ItRequest(models.Model):
    _name = 'it.request'
    _inherit = ['mail.thread']
    _description = 'for IT Requests'
    
    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id)
    department_manager_id = fields.Many2one('hr.employee', string="Department Manager", compute="_compute_department_manager", store=True)
    it_manager_id = fields.Many2one('hr.employee', string="IT Manager", compute="_compute_it_manager", store=True)
    
    state = fields.Selection([
                                ('draft', 'Draft'),
                                ('department_manager_approval', 'Waiting for Department Manager Approval'),
                                ('it_manager_approval', 'Waiting for IT Manager Approval'),
                                ('approved', 'Approved'),
                                ('rejected', 'Rejected'),
                            ], default='draft', string="Status", tracking=True)
    request_type = fields.Selection([
        ('desktop_pc', 'Desktop PC'),
        ('laptop', 'Laptop'),
        ('printer', 'Printer'),
        ('ink', 'Ink'),
        ('monitor', 'Monitor'),
        ('other', 'Other')
    ], string='Request Type', required=True, tracking=True)

    justification = fields.Text(string='Justification', tracking=True)

    @api.constrains('request_type', 'justification')
    def _check_justification(self):
        for record in self:
            if record.request_type == 'other' and not record.justification:
                raise ValidationError('Justification is required for "Other" request type.')
            
    
    @api.depends('employee_id')
    def _compute_department_manager(self):
        self.department_manager_id = self.employee_id.parent_id

    
    @api.depends('employee_id')
    def _compute_it_manager(self):
        it_manager = self.env['hr.employee'].search([('job_title', '=', 'IT Manager')], limit=1)
        self.it_manager_id = it_manager



    
    def action_submit(self):
        self.state = 'department_manager_approval'

    def action_department_manager_approve(self):
        if self.env.user.employee_id == self.department_manager_id:
            self.state = 'it_manager_approval'
        else:
            raise UserError('Only the Department Manager can approve this request.')

    def action_it_manager_approve(self):
        if self.env.user.employee_id == self.it_manager_id:
            self.state = 'approved'
        else:
            raise UserError('Only the IT Manager can approve this request.')

    def action_reject(self):
        if self.env.user.employee_id in [self.department_manager_id, self.it_manager_id]:
            self.state = 'rejected'
        else:
            raise UserError('Only a manager can reject this request.')

