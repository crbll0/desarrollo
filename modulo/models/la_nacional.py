# -*- coding: utf-8 -*-

#from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


#_logger = logging.getLogger(__name__)


class RealEstateCustomDocNacional(models.Model):
    _name = "real.estate.custom.doc_lanacional"
    _description = "Real Estate Custom Documentation La Nacional"

    nombres = fields.Char(string='Nombres')
    apellidos = fields.Char(string='Apellidos')
    apodo = fields.Char(string='Apodo')
    fecha_de_nacimiento = fields.Char(string='Fecha de Nacimiento')
    sexo = fields.Selection([
            ('m', 'M'),
            ('f', 'F'),
        ], string="Sexo")
    cedula = fields.Char(string='No.Cedula (solo dominicanos)')
    pasaporte = fields.Char(string='No. Pasaporte(s) (si aplica)')
    vencimiento = fields.Char(string='Fecha(s) de Vencimiento (si aplica)')
    cods = fields.Char(string='Cods.Pais Emision (Si aplica)')
    pais = fields.Char(string='Pais de Nacimiento')
    resid_o_ciud = fields.Char(string='Solo residentes o ciudadanos de EEUU')
    no_ss = fields.Char(string='No.Seguridad Social')
    nac_adquirida = fields.Char(string='Nacionalidad Adquirida (si aplica)')
    estado_civil = fields.Char(string='Estado Civil')
    profesion_ocup = fields.Char(string='Profesion u Ocupacion')
    empleador = fields.Char(string='Empleador o Negocio')
    posicion = fields.Char(string='Posicion o Cargo')
    ingreso = fields.Char(string='Fecha de Ingreso/Inicio Labores')
    ingresos_mens = fields.Char(string=u'Ingresos Mensuales RD$')
    pensionado = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Pensionado")
    ha_sido_funcionario = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Ha sido funcionario del Gobierno?")
    es_pariente_de = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Es pariente de un Funcionario del Gobierno?")

    otros_ingresos = fields.Char(string='Otros Ingresos')
    proveniencia_de = fields.Char(string='Provenientes de Otros Ingresos')

    calle = fields.Char(string='Calle')
    no = fields.Char(string='No.')
    edif = fields.Char(string='Edif.')
    apto = fields.Char(string='Apto.')
    sector = fields.Char(string='Sector')
    ciudad = fields.Char(string='Ciudad')
    pais = fields.Char(string='Pais')
    telefono = fields.Char(string='Telefono Residencia (incluir codigo de area)')
    celular = fields.Char(string='Telefono Celular (incluir codigo de area)')
    email = fields.Char(string='Correo Electronico')
    proyecto = fields.Char(string='Nombre del Proyecto')
    inmobiliaria = fields.Char(string='Unidad Inmobiliaria')
    valor = fields.Char(string='Valor del inmueble')
    financiamiento = fields.Char(string='Monto del Financiamiento')
    plazo = fields.Char(string='Plazo del Financiamiento')

    nombre = fields.Char(string='Nombre')
    direccion = fields.Char(string='Direccion')
    telefono = fields.Char(string='Telefono')

    nombre1 = fields.Char(string='Nombre')
    direccion1 = fields.Char(string='Direccion')
    telefono1 = fields.Char(string='Telefono')

    nombre2 = fields.Char(string='Nombre')
    direccion2 = fields.Char(string='Direccion')
    telefono2 = fields.Char(string='Telefono')

    documentos_anexos = fields.Selection([
            ('copia de doc identidad', 'Copia del Documento de Identidad (Mayores de 18 años'),
            ('carta laboral', 'Carta Laboral'),
            ('reporte buro', 'Reporte Buro de Credito'),
        ], string="Documentos Anexos")

    calificacion_fatca = fields.Selection([
            ('fatca', 'FATCA'),
            ('no fatca', 'No FATCA'),
            ('recalcitrante', 'Recalcitrante'),
            ('en evaluacion', 'En evaluacion'),
        ], string="Calificacion FATCA")

    entrevista = fields.Char(string='Entrevista')

    firma_cliente = fields.Char(string='Firma Cliente')
    identificacion = fields.Char(string='No. Identificacion')
    fecha = fields.Date(string='Fecha')
