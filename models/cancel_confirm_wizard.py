from odoo import models, fields, api

class CancelConfirmWizard(models.TransientModel):
    _name = 'cancel.confirm.wizard'
    _description = 'Cancel Confirmation Wizard'

    ticket_id = fields.Many2one('it.ticket', string='Ticket', required=True)

    def action_confirm_cancel(self):
        self.ticket_id.status = 'canceled'
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
