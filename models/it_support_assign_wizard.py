from odoo import models, fields, api

class ITSupportAssignWizard(models.TransientModel):
    _name = 'it.support.assign.wizard'
    _description = 'Assign IT Support'

    user_id = fields.Many2one('res.users', string='Assign to', required=True, domain=lambda self: [('groups_id', 'in', self.env.ref('it_helpdesk2.group_it_support').id)])

    def action_assign(self):
        self.ensure_one()
        ticket_id = self.env.context.get('active_id')
        ticket = self.env['it.ticket'].browse(ticket_id)
        if ticket:
            ticket.write({
                'handled_by': self.user_id.id,
                'status': 'in_progress',
            })
        return {'type': 'ir.actions.act_window_close'}
