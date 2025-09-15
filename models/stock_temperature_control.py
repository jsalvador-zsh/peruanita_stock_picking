from odoo import models, fields, api

class TemperatureControl(models.Model):
    _name = 'stock.temperature.control'
    _description = 'Control de Temperatura y Humedad'
    _order = 'picking_id, stage'

    # Relación con el picking
    picking_id = fields.Many2one('stock.picking', string='Transferencia', required=True, ondelete='cascade')
    
    # Etapa del proceso (para las 3 filas)
    stage = fields.Selection([
        ('loading', 'Al cargar de almacén'),
        ('transport', 'Durante el transporte'),
        ('delivery', 'Al entregar el producto')
    ], string='Etapa', required=True)
    
    # Campos de registro (las 3 columnas)
    time_hour = fields.Datetime(string='Tiempo/Hora', default=fields.Datetime.now)
    temperature = fields.Float(string='T °C', digits=(5, 2))
    humidity = fields.Float(string='% HR', digits=(5, 2))
    
    # Campos adicionales
    responsible_user = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    notes = fields.Text(string='Observaciones')
    
    @api.model
    def create_default_records(self, picking_id):
        """Crear registros por defecto para las 3 etapas"""
        stages = [
            ('loading', 'Al cargar de almacén'),
            ('transport', 'Durante el transporte'),
            ('delivery', 'Al entregar el producto')
        ]
        
        for stage_code, stage_name in stages:
            self.create({
                'picking_id': picking_id,
                'stage': stage_code,
                'time_hour': fields.Datetime.now(),
                'temperature': 0.0,
                'humidity': 0.0,
            })