from odoo import models, fields, api

class SolutionInputWizard(models.TransientModel):
    _name = 'solution.input.wizard'
    _description = 'Solution Input Wizard'

    ticket_id = fields.Many2one('it.ticket', string='Ticket', required=True)
    solution = fields.Text(string='Solution', required=True)

    def action_confirm_solution(self):
        self.ticket_id.solution = self.solution
        self.ticket_id.status = 'done'
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
