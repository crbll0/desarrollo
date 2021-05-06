# -*- coding: utf-8 -*-

#from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


#_logger = logging.getLogger(__name__)


class RealEstateCustomDoc(models.Model):
    _name = "real.estate.custom.doc"
    _description = "Real Estate Custom Documentation"

    primer_nombre = fields.Char(string='1er. Nombre')
    segundo_nombre = fields.Char(string='2do. Nombre')
    primer_apellido = fields.Char(string='1er. Apellido')
    segundo_apellido = fields.Char(string='2do. Apellido')

    tipo_de_documento = fields.Selection([
            ('cedula', 'Cedula'),
            ('pasaporte', 'Pasaporte'),
        ], string="Tipo de Documento")
    documento = fields.Char('No. Documento')
    sexo = fields.Selection([
            ('m', 'M'),
            ('f', 'F'),
        ], string="Sexo")

    estado_civil = fields.Selection([
            ('soltero', 'Soltero'),
            ('casado', 'Casado'),
            ('viudo', 'Viudo'),
            ('divorciado', 'Divorciado'),
            ('union_libre', 'Union libre'),
        ], string="Estado civil")

    nacimiento = fields.Char(string='Fecha de Nacimiento')

    ciudadania_o_res_extranjera = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Posee Ciudadania o Residencia Extranjera?")

    nacionalidad_de_orig = fields.Char(string='Nacionalidad de Origen')
    nacimiento1 = fields.Char(string='Pais de Nacimiento')
    ciudad = fields.Char(string='Ciudad')
    nacionalidad_adquirida = fields.Char(string='Nacionalidad Adquirida')
    dependientes = fields.Char(string='Cantidad de Dependientes')
    soc_security = fields.Char(string='Numero de Social Security o ID (Si Aplica)')

    nivel_academico = fields.Selection([
            ('basico', 'Basico'),
            ('bachiller', 'Bachiller'),
            ('tecnico', 'Tecnico'),
            ('universitario', 'Universitario'),
            ('maestria', 'Maestria'),
            ('sin_estudios', 'Sin Estudios'),
        ], string="Nivel Academico")

    profesion = fields.Char(string='Profesion')
    ocupacion = fields.Char(string='Actividad Economica u Ocupacion')

    direccion = fields.Char(string='Direccion')
    sector = fields.Char(string='Sector')

    domicilio = fields.Selection([
            ('propio', 'Propio'),
            ('alquilado', 'Alquilado'),
        ], string="Domicilio")

    municipio = fields.Char(string='Municipio')
    provincia = fields.Char(string='Provincia')
    pais = fields.Char(string='Pais')
    tel_casa = fields.Char(string='Telefono Casa')
    tel_cel = fields.Char(string='Telefono Celular')
    tel_ofic = fields.Char(string='Tel.Oficina')
    otros = fields.Char(string='Otros')
    e_mail = fields.Char(string='Correo Electronico (e-mail)')


    entrega_correspondencia = fields.Selection([
            ('email', 'Email'),
            ('oficina_imc', 'Oficina IMC'),
        ], string="Entrega de Correspondencia")



    tipo_de_vivienda = fields.Selection([
            ('propia', 'Propia'),
            ('alquilada', 'Alquilada'),
            ('si_no', 'Si/No'),
            ('hipotecada', 'Hipotecada'),
        ], string="Tipo de Vivienda")

    calle = fields.Char(string='Calle')
    no = fields.Char(string='No')
    edificio = fields.Char(string='Edificio')
    apartamento = fields.Char(string='Apartamento')
    codigo_postal = fields.Char(string='Codigo Postal')
    pais_direccion = fields.Char(string='Pais')
    ciudad_direccion = fields.Char(string='Ciudad')
    estado = fields.Char(string='Estado')



    tel_extranjero = fields.Char(string='Telefono Residencial en el Extranjero')
    otro_tel = fields.Char(string='Otro Numero de Telefono')



    nombre = fields.Char(string='Nombre')
    apellidos = fields.Char(string='Apellidos')
    cedula_pasaporte = fields.Char(string='Cedula/Pasaporte')
    nacionalidad = fields.Char(string='Nacionalidad')
    fecha_de_nacimiento = fields.Char(string='Fecha de Nacimiento')
    lugar_de_nacimiento = fields.Char(string='Lugar de Nacimiento')
    ocupacion_conyugue = fields.Char(string='Ocupacion')
    ingresos_anuales = fields.Char(string='Ingresos Anuales')
    telefono = fields.Char(string='Telefono')
    telefono_movil = fields.Char(string='Telefono Movil')
    correo_e_mail = fields.Char(string='Correo (e-mail)')



    actividad_principal = fields.Selection([
            ('no_trabaja', 'No trabaja'),
            ('ama_de_casa', 'Ama de casa'),
            ('estudiante', 'Estudiante'),
            ('pensionado', 'Pensionado'),
            ('profesional independiente', 'Profesional Independiente'),
            ('empleado_privado', 'Empleado Privado'),
            ('empleado_publico', 'Empleado Publico'),
        ], string="Actividad Principal")

    tipo_de_contrato = fields.Selection([
            ('temporal', 'Temporal'),
            ('indefinido', 'Indefinido'),
            ('presta_servicios', 'Presta Servicios'),
        ], string="Tipo de Contrato")

    labora_empresa = fields.Char(string='Nombre de la Empresa')
    labora_cargo_que_ocupa = fields.Char(string='Cargo que ocupa')
    labora_fecha_de_ingreso = fields.Char(string='Fecha de Ingreso')
    labora_direccion = fields.Char(string='Direccion')
    labora_sector = fields.Char(string='Sector')
    labora_municipio = fields.Char(string='Municipio')
    labora_provincia = fields.Char(string='Provincia')
    labora_pais = fields.Char(string='Pais')
    labora_telefono = fields.Char(string='Telefono')
    labora_fax = fields.Char(string='Fax')
    labora_correo = fields.Char(string='Correo Electronico')
    labora_ing_mensuales = fields.Char(string='Ingresos Mensuales')
    labora_ing_extraordinarios = fields.Char(string='Ingresos extraordinarios')
    labora_antiguedad = fields.Char(string='Antiguedad en la Empresa')
    labora_anos = fields.Char(string='anos')
    labora_meses = fields.Char(string='Meses')

    sector_de_la_empresa = fields.Selection([
            ('privado', 'Privado'),
            ('publico', 'Publico'),
        ], string="Sector de la Empresa")

    actividad_principal_de_la_empresa = fields.Selection([
            ('agroindustrial', 'Agroindustrial'),
            ('comercial', 'Comercial'),
            ('turismo', 'turismo'),
            ('construccion', 'Construccion'),
            ('educacion', 'Educacion'),
            ('militar', 'Militar'),
            ('industrial', 'Industrial'),
            ('mobiliaria', 'Mobiliaria'),
            ('salud', 'Salud'),
            ('servicios', 'Servicios'),
            ('otros', 'Otros'),
        ], string="Actividad principal de la Empresa")

    otro_indicar = fields.Char(string='Si es otro indicar cual')

    fuente_de_ingreso = fields.Char(string='Fuente de Ingreso')
    ingresos_mensuales = fields.Char(string='Ingresos Mensuales')
    ingresos_totales = fields.Char(string='Ingresos Totales')


    regimen_al_que_pertenece = fields.Selection([
            ('comun', 'Comun'),
            ('simplificado', 'Simplificado'),
            ('agente', 'Agente de Retencion Si o No'),
        ], string="Regimen al que pertenece")


    es_usted_o_ha_sido_una_persona_pep = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Es usted o ha sido una persona expuesta politicamente (PEP) conforme la definicion en la ley 155-17 contra el lavado de activos y su reglamento de aplicacion")

    cargo = fields.Char(string='Cargo')
    peps_pais = fields.Char(string='Pais')
    fecha_de_designacion = fields.Char(string='Fecha de designacion')
    fecha_de_remocion = fields.Char(string='Fecha de remocion')

    tipo_bienes= fields.Selection([
            ('herencia', 'Herencia'),
            ('ahorros', 'Ahorros'),
            ('no poseo bienes', 'No poseo bienes'),
            ('otros', 'Otros'),
        ], string="Los bienes que poseo han sido adquiridos a traves de")
    especificar = fields.Char(string='Especificar')

    recursos_provienen_de = fields.Selection([
            ('salarios', 'Salarios'),
            ('comisiones', 'Comisiones'),
            ('interes_rendimientos', 'Interes y Rendimientos'),
            ('ventas_netas', 'Ventas Netas'),
        ], string="Los recursos que entregue provienen de las siguientes fuentes")
    especificar2 = fields.Char(string='Especificar')


    pais_de_origen_de_los_recursos = fields.Selection([
            ('rep_dom', 'Republica Dominicana'),
            ('otro', 'Otro Pais'),
        ], string="Pais de origen de los recursos")
    pais_procedencia_recursos = fields.Char(string='Cual?')

    banco_ids = fields.One2many('real.estate.custom.doc.bancos', 'doc_id')

    cant1 = fields.Integer('Cantidad')
    descripcion1 = fields.Char('Descripcion')
    hipoteca1 = fields.Char('Tiene Hipoteca? Si/No')

    cant2 = fields.Integer('Cantidad')
    descripcion2 = fields.Char('Descripcion')
    hipoteca2 = fields.Char('Tiene Hipoteca? Si/No')

    cant3 = fields.Integer('Cantidad')
    descripcion3 = fields.Char('Descripcion')
    hipoteca3 = fields.Char('Tiene Hipoteca? Si/No')

    cant4 = fields.Integer('Cantidad')
    descripcion4 = fields.Char('Descripcion')
    hipoteca4 = fields.Char('Tiene Hipoteca? Si/No')
    cercania_persona_pep = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
    ])
    nombre_del_pep = fields.Char('Nombre')
    parentesco = fields.Char('Parentesco / Afinidad')


class InfoBancos(models.Model):
    _name = 'real.estate.custom.doc.bancos'
    _description = 'Persona Fisica - Bancos'

    doc_id = fields.Many2one('real.estate.custom.doc')
    banco = fields.Char('Banco')
    tipo_cuenta = fields.Char('Tipo de Cuenta')
    moneda = fields.Char('Moneda')
