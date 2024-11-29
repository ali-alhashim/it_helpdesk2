from odoo import models, fields, api


class ItDevice(models.Model):
    _name = 'it.device'
    _inherit        = ['mail.thread']
    _description = 'IT Device'
    _rec_name = 'serial_number'
    _order = 'acquisition_date desc'
    serial_number = fields.Char(string='Serial Number', required = True, tracking=True)
    
    manufacture   = fields.Char(string="Manufacture")
    model         = fields.Char(string="Model")
    state         = fields.Selection([('new','New'),('used','Used'), ('old','Old'),('damaged','Damaged'),('lost','Lost')], default='new', tracking=True)
    type = fields.Selection([
                          ('laptop', 'Laptop'),
                          ('smart phone', 'Smart Phone'),
                          ('Telphone','Telphone'),
                          ('printer', 'Printer'),
                          ('dot matrix printer','Dot Matrix Printer'),
                          ('switch', 'Switch'),
                          ('hard disk', 'Hard Disk'),
                          ('fax', 'Fax'),
                          ('sold state drive ssd', 'Sold State Drive SSD'),
                          ('monitor', 'Monitor'),
                          ('keyboard and mouse wireless', 'Keyboard and Mouse Wireless'),
                          ('keyboard','Keyboard'),
                          ('mouse','Mouse'),
                          ('desktop pc', 'Desktop PC'),
                          ('all-in-one computer', 'All-In-One Computer'),
                          ('flash memory usb', 'Flash Memory USB'),
                          ('scanner', 'Scanner'),
                          ('copy machine', 'Copy Machine'),
                          ('access point wireless','Access Point Wireless'),
                          ('attendance machine','Attendance Machine'),
                          ('adapter','Adapter'),
                          ('router','Router'),
                          ('tablet','Tablet'),
                          ('cabinet','Cabinet'),
                          ('charger','Charger'),
                          ('external dVd drive','External DVD Drive'),
                          ('graphics card','Graphics Card'),
                          ('id card printer','ID Card Printer'),
                          ('wireless card','Wireless Card'),
                          ('webcam','Webcam'),
                          ('other', 'Other'),
                          
        ], string="Category")
    description   = fields.Text(string="Description")
    purchase_price= fields.Float(string = "Price", tracking=True)
    invoice       = fields.Char(string='invoice')
    purchase_order= fields.Char(string='PO')
    acquisition_date = fields.Date(string='Acquisition Date')

    user_ids = fields.One2many('it.device.user.history', 'device_id', string='User History')



   

    current_user_id = fields.Many2one('hr.employee', string='Current User', compute='_compute_current_user', store=True)
    

    

    @api.depends('user_ids')
    def _compute_current_user(self):
        for device in self:
            user_history = self.env['it.device.user.history'].search([
                ('device_id', '=', device.id)
            ], order='start_date desc', limit=1)
            
            if user_history:
                device.current_user_id = user_history.user_id
            else:
                device.current_user_id = None

    def update_current_user(self):
        for record in self:
            record._compute_current_user()
                