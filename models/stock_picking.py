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
        string='Certificado Microbiológico',
        default=False,
        help='Indica si se envió el certificado microbiológico'
    )
    
    certificate_physical = fields.Boolean(
        string='Certificado Físico',
        default=False,
        help='Indica si se envió el certificado físico'
    )
    
    certificate_organoleptic = fields.Boolean(
        string='Certificado Organoléptico',
        default=False,
        help='Indica si se envió el certificado organoléptico'
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