from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _description = "Motorcycle Registry"
    _rec_name = 'registry_number'
    _sql_constraints = [
        ('vin_unique', 'UNIQUE(vin)', 'VIN already exists.')
    ]

    registry_number = fields.Char(required=True, string="Registry number", 
                                  default='MRN000', copy=False, readonly=True)
    vin = fields.Char('VIN', required=True)
    # first_name = fields.Char(required=True)
    # last_name = fields.Char(required=True)
    image = fields.Image(string="Image")
    current_mileage = fields.Float()
    license_plate = fields.Char('License Plate Number')
    certificate_title = fields.Binary(string='Certificate Title')
    register_date = fields.Date()

    owner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    owner_phone = fields.Char(related='owner_id.phone')
    owner_email = fields.Char(related='owner_id.email')
    
    # Vehicles fields
    brand = fields.Char(compute='_compute_data')
    make = fields.Char(compute='_compute_data')
    model = fields.Char(compute='_compute_data')

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('registry_number', ('MRN000')) == ('MRN000'):
                vals['registry_number'] = self.env['ir.sequence'].next_by_code('registry.number')
        return super().create(vals_list)
    
    # @api.constrains('license_plate', 'vin')
    # def _check_data(self):
    #     for registry in self:
    #         pattern_vin = re.compile("^[A-Z]{4}[0-9]{2}[A-Z,0-9]{2}[0-9]{6}$")
    #         if not(pattern_vin.match(registry.vin)):
    #             raise ValidationError('Follow the VIN format')
    #         pattern_license = re.compile("^[A-Z]{1,4}[0-9]{1,3}[A-Z]{,2}$")
    #         if not(pattern_license.match(registry.license_plate)):
    #             raise ValidationError('Follow the License Plate format')

    @api.constrains('license_plate')
    def _check_license_plate_size(self):
        pattern = '^[A-Z]{1,3}\d{1,4}[A-Z]{0,2}$'
        for registry in self.filtered(lambda r: r.license_plate):
            match = re.match(pattern, registry.license_plate)
            if not match:
                raise ValidationError('Odoopsie! Invalid License Plate')
 
    @api.constrains('vin')
    def _check_vin_pattern(self):
        pattern = '^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{6}$'
        for registry in self.filtered(lambda r: r.vin):
            match = re.match(pattern, registry.vin)
            if not match:
                raise ValidationError('Odoopsie! Invalid VIN')
            if not registry.vin[0:2] == 'KA':
                raise ValidationError('Odoopsie! Only motorcycles from Kauil Motors are allowed')
            
    @api.depends('vin')
    def _compute_data(self):
        for registry in self:
            registry.brand = registry.vin[:2]
            registry.make = registry.vin[2:4]
            registry.model = registry.vin[4:6]

