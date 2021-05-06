# -*- coding: utf-8 -*-

#from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


#_logger = logging.getLogger(__name__)


class RealEstateCustomDocPJ(models.Model):
    _name = "real.estate.custom.doc_juridica"
    _description = "Real Estate Custom Documentation PJ"

    nombre_de_la_compania = fields.Char(string=u'Nombre de la compañia')
    rnc_identificacion = fields.Char(string='RNC/Identificacion')
    direccion = fields.Char(string='direccion')
    sector = fields.Char(string='Sector')
    ciudad = fields.Char(string='Ciudad')
    pais = fields.Char(string='Pais')
    repres_legal = fields.Char(string='Nombre del Representante Legal y/o Persona Autorizada')
    posicion = fields.Char(string='Posicion')
    email = fields.Char(string='E-mail')
    website = fields.Char(string='Website')
    telefono = fields.Char(string='Telefono')
    activ_principal_y_secund = fields.Char(string='Actividad principal y/o secundaria del negocio')
    promedio_mensual_de_ventas = fields.Char(string='Promedio Mensual de Ventas')
    fax = fields.Char(string='Fax')

    tipo_de_organizacion_o_empresa = fields.Selection([
            ('sector_publico', 'Sector Publico'),
            ('corporacion_internacional', 'Corporacion Internacional'),
            ('compania_por_acciones', u'Compañia por acciones o sociedad anonima'),
            ('unico_dueno', u'Unico dueño'),
            ('sin_fines_de_lucro', 'Sin fines de lucro'),
            ('sociedad_de_resp_limitada', 'Sociedad de Responsabilidad Limitada'),
        ], string="Tipo de Organizacion o Empresa")
    otros = fields.Char(string='Otros')

    actividades_del_negocio = fields.Char(string='Actividades del Negocio')
    tipo_de_operacion = fields.Char(string='Tipo de Operacion')
    numero_de_empleados = fields.Char(string='Numero de Empleados')
    anos_de_operacion = fields.Char(string='Años de Operacion')
    porcentaje_de_participacion= fields.Char(string='Porcentaje de Participacion en el mercado')
    tamano_del_negocio= fields.Selection([
            ('pequeno', u'pequeño'),
            ('mediano', 'Mediano'),
            ('grande', 'Grande'),
        ], string=u"Tamaño del Negocio")

    capital_social = fields.Char(string='Capital social')
    lugar_de_constitucion = fields.Char(string='Lugar de Constitucion/incorporacion')
    fecha_de_constitucion = fields.Char(string='Fecha de Constitucion')

    indicar_cambios_recientes = fields.Char(string='Indicar cambios recientes (ultimos 18 meses) en la Organizacion: Fusiones,adquisiciones, cambios en la gerencia, otros')

    indicar_otros = fields.Char(string='Indicar cambios recientes o esperados (ultimos 18 meses) en productos o actividades de negocios: apertura de nuevos locales, otros')

    la_organizacion_esta_experimentando_dificultades_financieras = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="La organizacion esta experimentando dificultades financieras, investigacion en la industria/negocio,intervencion del gobierno, inquietud a nivel de reputacion del negocio/gerencia")
    especificar = fields.Char(string='Especificar')

    entidades_ids = fields.One2many('real.estate.custom.doc_juridica_entidades', 'doc_id')

    ultimos_10_anos = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string=u"La organizacion ha pertenecido a otro propietario en los ultimos 10 años? ")
    si_es_negativa = fields.Char(string='Si la respuesta es negativa, favor presentar nomina anterior de accionistas')

    #completar_el_cuadro = fields.Char(string='Completar el siguiente cuadro con informaciones relativas a los accionistas y directivos de la organizacion')

    propietarios_ids = fields.One2many('real.estate.custom.doc_juridica_propietarios', 'doc_id')

    accionistas_ids = fields.One2many('real.estate.custom.doc_juridica_accionistas', 'doc_id')

    suplidores_ids = fields.One2many('real.estate.custom.doc_juridica_suplidores', 'doc_id')

    bancos_ids = fields.One2many('real.estate.custom.doc_juridica_bancos', 'doc_id')

    existe_alguna_figura_publica_o_pep = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Existe alguna Figura Publica o Persona Politicamente Expuesta (PEP), dentro  de la directiva o accionista de la organizacion? ")
    en_caso_de_afirmativo = fields.Char(string='En caso de afirmativo indicar lo siguiente')
    cargo = fields.Char(string='Cargo')
    pais = fields.Char(string='Pais')
    fecha_de_designacion = fields.Char(string='Fecha de Designacion')
    fecha_de_remocion = fields.Char(string='Fecha de Remocion')

    con_el_proposito_de_ley_155_17 = fields.Char(string='Con el proposito de dar cumplimiento a las disposiciones establecidas en la ley 155-17 y sus reglamentos, que rigen la prevencion del lavado de activos y la financiacion al terrorismo en la Republica Dominicana, realizo la siguiente declaracion de fuente de bienes y/o recuersos')
    los_bienes_son_de = fields.Selection([
            ('ingresos comerciales', 'Ingresos Comerciales'),
            ('ahorros de la organizacion', 'Ahorros de la Organizacion'),
        ], string="Los Bienes que poseo han sido adquiridos a traves de")

    los_recursos_que_entregue_son = fields.Selection([
            ('comisiones', 'Comisiones'),
            ('ingresos comerciales', 'Ingresos Comerciales'),
            ('interes y rendimientos', 'Interes y Rendimientos'),
        ], string="Los recursos que entre provienen de las siguientes fuentes")
    otros_especificar= fields.Char(string='Otros Especificar')

    pais_de_origen_recursos = fields.Selection([
            ('republica dominicana', 'Republica Dominicana'),
            ('otro', 'Otro')
        ], string="Pais de origen de los recursos")
    otros_pais_cual= fields.Char(string='Otros Pais, Cual?')

    declaro_que_los_recursos_que_entregue = fields.Char(string='Declaro que los Recursos que entregue no provienen de Actividades licitas contempladas en el Codigo Penal Dominicano o en cualquier otra norma que lo modifique o adicione y la Ley 155-17')

    no_admitire_que_terceros = fields.Char(string='No admitire que terceros efectuen depositos a mis cuentas con recursos provenientes de actividades ilicitas contempladas en el Codigo Penal Dominicano o en cualquier otra norma que lo adicione, ni afectuare transacciones destinadas a tales actividades o a favor de personas relacionadas con las mismas.')

    firma_del_representante_legal = fields.Char(string='Firma del Representante Legal')
    sello_de_la_compania = fields.Char(string='Sello de la Compañia')

    cliente_vinculado = fields.Selection([
            ('si', 'Si'),
            ('no', 'No'),
        ], string="Cliente Vinculado")

    fecha = fields.Char(string='Fecha')
    representante_de_ventas = fields.Char(string='Representante de Ventas')
    oficial_de_cumplimiento = fields.Char(string='Oficial de Cumplimiento')

    directora_general = fields.Char(string='Directora General')


class EntidadesFilial(models.Model):
    _name = "real.estate.custom.doc_juridica_entidades"
    _description = 'Personas Juridicas Entidades'

    doc_id = fields.Many2one("real.estate.custom.doc_juridica")
    name = fields.Char(string=u'Nombre de la Compañia')
    filial = fields.Char(string='Filial')
    subsidiaria = fields.Char(string='Subsidiaria')
    is_ge = fields.Boolean(string="GE")
    is_gf = fields.Boolean(string="GF")
    pais = fields.Char(string='Pais donde realiza operaciones')


class Propietarios(models.Model):
    _name = "real.estate.custom.doc_juridica_propietarios"
    _description = 'Personas Juridicas Propietarios'

    doc_id = fields.Many2one("real.estate.custom.doc_juridica")
    nombre_del_propietario_mayoritario = fields.Char(string='Nombre del propietario Mayoritario')
    entidad = fields.Char(string='Entidad (colocar literal)')
    pais_de_residencia_legal = fields.Char(string='Pais de Residencia legal')
    porcent_accionario = fields.Char(string='% Accionario')


class Accionistas(models.Model):
    _name = "real.estate.custom.doc_juridica_accionistas"
    _description = 'Personas Juridicas Accionistas'

    doc_id = fields.Many2one("real.estate.custom.doc_juridica")
    nombres_y_apellidos = fields.Char(string='Nombre(s) y Apellido (s)')
    cedula = fields.Char(string='Cedula de Identidad y Electoral/No.pasaporte')
    cargo = fields.Char(string='Cargo')
    pais_de_residencia = fields.Char(string='Pais de Residencia')


class Suplidores(models.Model):
    _name = "real.estate.custom.doc_juridica_suplidores"
    _description = 'Personas Juridicas Propietarios'

    doc_id = fields.Many2one("real.estate.custom.doc_juridica")
    nombre = fields.Char(string='Nombre')
    ubicacion = fields.Char(string='Ubicacion')
    telefono = fields.Char(string='telefono')


class InformacionBancaria(models.Model):
    _name = "real.estate.custom.doc_juridica_bancos"
    _description = 'Personas Juridicas Propietarios'

    doc_id = fields.Many2one("real.estate.custom.doc_juridica")
    no_cuenta = fields.Char(string='No.de cuenta')
    banco = fields.Char(string='Banco')
    tipo_de_cuenta = fields.Char(string='Tipo de Cuenta')
