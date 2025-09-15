# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Control de despacho
    transport_company_id = fields.Many2one(
        'res.partner',
        string='Empresa de Transporte',
        help='Empresa encargada del transporte de la mercadería',
        domain=[('is_company', '=', True)]
    )
    
    transport_phone = fields.Char(
        string='Celular',
        help='Número de contacto del transportista'
    )
    
    vehicle_plate = fields.Char(
        string='Placa del Vehículo',
        help='Placa del vehículo utilizado para el transporte'
    )

    # DOCUMENTACIÓN ENVIADA DEL PRODUCTO
    declaration_sworn = fields.Boolean(
        string='Declaración Jurada',
        default=False,
        help='Indica si se envió la declaración jurada'
    )
    
    certificate_microbiological = fields.Boolean(
        string='Certificados Microbiológicos, Físico y Organoléptico',
        default=False,
        help='Indica si se envió los certificados en mención'
    )
    
    shipping_guide = fields.Boolean(
        string='Guía de Remisión',
        default=False,
        help='Indica si se envió la guía de remisión'
    )
    
    other_documents = fields.Text(
        string='Otros Documentos',
        help='Notas adicionales sobre otros documentos enviados'
    )

    # Relación One2many con los controles de temperatura
    temperature_control_ids = fields.One2many(
        'stock.temperature.control', 
        'picking_id', 
        string='Control de Temperatura'
    )
    
    @api.model
    def create(self, vals):
        """Crear registros de temperatura automáticamente al crear un picking"""
        picking = super(StockPicking, self).create(vals)
        # Solo crear para pickings de tipo outgoing e incoming
        if picking.picking_type_id.code in ['outgoing', 'incoming']:
            self.env['stock.temperature.control'].create_default_records(picking.id)
        return picking
    
    def write(self, vals):
        """Si se cambia el tipo de picking, crear o eliminar registros de temperatura"""
        result = super(StockPicking, self).write(vals)
        
        if 'picking_type_id' in vals:
            for picking in self:
                if picking.picking_type_id.code in ['outgoing', 'incoming']:
                    # Si no tiene registros de temperatura, crearlos
                    if not picking.temperature_control_ids:
                        self.env['stock.temperature.control'].create_default_records(picking.id)
                else:
                    # Si ya no es outgoing/incoming, eliminar registros de temperatura
                    picking.temperature_control_ids.unlink()
        
        return result

    # Control de recepción
    referral_guide = fields.Char(string='Guía de remisión', help='Guía de remisión del proveedor')

    @api.depends('picking_type_code')
    def _compute_is_outgoing(self):
        """Computed field para verificar si es un picking de salida"""
        for record in self:
            record.is_outgoing = record.picking_type_code == 'outgoing'
    
    is_outgoing = fields.Boolean(
        string='Es Entrega',
        compute='_compute_is_outgoing',
        store=True,
        help='Campo computado que indica si es un picking de salida'
    )

    @api.depends('picking_type_code')
    def _compute_is_incoming(self):
        """Computed field para verificar si es un picking de recepción"""
        for record in self:
            record.is_incoming = record.picking_type_code == 'incoming'
    
    is_incoming = fields.Boolean(
        string='Es Recepción',
        compute='_compute_is_incoming',
        store=True,
        help='Campo computado que indica si es un picking de recepción'
    )