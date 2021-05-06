from odoo import api, models, fields


class FormDiligence(models.Model):
    _name = 'real.estate.custom.doc.formulario.fideicomitente'
    _description = 'Real Estate formulario de debida diligencia Adquiriente o Inversionista'

    # -- Customer details --
    name = fields.Char(string='Nombres')
    lastname = fields.Char(string='Apellidos')
    email = fields.Char(string='Correo Electronico (E-mail)')
    sex = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    ], string='Sexo', required=True, default='masculino')
    marital = fields.Selection([
        ('casado', 'Casado'),
        ('soltero', 'Soltero'),
    ], string='Estado Civil')
    econ_activity = fields.Char(string='Nombre de la actividad economica')
    work_sector = fields.Selection([
        ('privado', 'Privado'),
        ('publico', 'Publico')
    ], string="Sector (Si es asalariado)")
    birth = fields.Date(string="Fecha de Nacimiento")
    birth_place = fields.Char(string="Lugar de Nacimiento")
    nationality = fields.Char(string="Nacionalidad")

    doc_type = fields.Selection([
        ('cedula', 'Cedula'),
        ('pasaporte', 'Pasaporte')
    ], string="Tipo de documento de identidad")
    id_doc = fields.Char(string="Documento de identidad")
    passports_ids = fields.One2many('real.estate.custom.doc.formulario.passports', 'passport_refs', string="Pasaportes")
    additional_id = fields.Char(string="No. de identidad adicional (Solo extranjeros o doble nacionalidad)")
    social_id = fields.Char(string="No. de seguridad social (Solo residentes y ciudadanos de EE.UU)")

    nation_q = fields.Selection([
        ('si', 'Si'),
        ('no', 'No'),
    ], string="¿Tiene una segunda nacionalidad?", default='no')
    residences_ids = fields.One2many('real.estate.custom.doc.formulario.residences', 'residence_ref', string="Residencias y Ciudadanias")
    residence_q = fields.Selection([
        ('si', 'Si'),
        ('no', 'No')
    ], string="¿Es residente o ciudadano en EE.UU?", default='no')
    usa_resident = fields.Boolean(string="Residente")
    usa_citizen = fields.Boolean(string="Ciudadano")

    address_street = fields.Char(string="Calle actual de domicilio")
    address_no = fields.Char(string="Numero")
    address_bulding = fields.Char(string="Edificio (Si aplica)")
    address_aprtmnt = fields.Char(string="Apartamento/Piso (Si aplica)")
    country = fields.Char(string="Pais")
    city = fields.Char(string="Ciudad/Provincia")
    sector = fields.Char(string="Sector")

    residence_phone = fields.Char(string="Telefono Residencial")
    mobile = fields.Char(string="Telefono movil")
    us_phone = fields.Char(string="Numero telefonico EE.UU (Si aplica)")

    us_accounts = fields.Boolean(string="¿Posee cuentas en EE.UU?")
    us_person = fields.Boolean(string="¿Cuenta con un poder de representacion de un US person?")
    us_transaction = fields.Boolean(string="¿Recibe o envia transferencias hacia EE.UU?")

    fatca_form = fields.Selection([
        ('w8', 'W8'),
        ('w9', 'W9')
    ], string="Formulario FATCA (Solo para personas vinculadas a EE.UU)")

    fatca_date = fields.Date(string="Fecha de formulario FATCA (en caso de ser W8)")

    # -- US address --
    us_address = fields.Char(string="(Si posee direccion en los estados unidos) Estado o Provincia")
    us_address_city = fields.Char(string="Ciudad")
    us_address_sector = fields.Char(string="Sector")
    us_address_postal = fields.Char(string="Codigo Postal")

    # -- Income Declaration --
    patrimony = fields.Float(string="Patrimonio Aproximado")
    income_origin = fields.Selection([
        ('asalariado', 'Asalariado'),
        ('jubilado', 'Jubilado'),
        ('independiente', 'Independiente'),
        ('otros', 'Otros')
    ], string="Origen de ingresos")
    other_income = fields.Char(string="Indique su fuente de ingreso (En caso de seleccionar otros)")
    monthly_income = fields.Float(string="Ingreso Mensual")
    occupation = fields.Char(string="Ocupacion u Cargo")
    company_name = fields.Char(string="Nombre de la Empresa, si aplica")
    company_activity = fields.Char(string="Actividad Economica de le empresa")
    company_address = fields.Char(string="Direccion de la Empresa")
    company_address_no = fields.Char(string="No. local")
    company_building = fields.Char(string="Edificio")
    company_floor = fields.Char(string="Piso")
    company_country = fields.Char(string="Pais")
    company_city = fields.Char(string="Ciudad o Provincia")
    company_sector = fields.Char(string="Sector")
    company_time = fields.Char(string="Tiempo de la Empresa")
    company_phone = fields.Char(string="Telefono")
    company_email = fields.Char(string="Correo Electronico laboral (E-mail)")
    company_postal = fields.Integer(string="Apartado postal")
    company_region = fields.Selection([
        ('norte', 'Norte'),
        ('este', 'Este'),
        ('oeste', 'Oeste'),
        ('dn', 'DN')
    ])

    # -- Other income entries --
    extra_income = fields.Text(
        string="Otras fuentes de ingresos",
        placeholder="Especificar monto y actividad economica"
    )

    # -- Politically Exposed People (PEPs) --
    question_pep = fields.Selection([
        ('si', 'Si'),
        ('no', 'No'),
    ], string="¿Es o ha sido una persona políticamente expuesta y/o figura pública?")

    # -- if above is true --
    gobv_position = fields.Char(string="Cargo, Rango o Posición en Gobierno")
    position_date = fields.Date(string="Fecha desde que ocupa el Cargo")
    gobv_institution = fields.Char(string="Institución a la que pertenece")
    gobv_country = fields.Char(string="Pais")

    question2_pep = fields.Selection([
        ('si', 'Si'),
        ('no', 'No'),
    ], string="¿Tiene algún parentesco y/o vínculo a una persona políticamente expuesta y/o figura pública?")

    # -- if above is true --
    pep_name = fields.Char(string="Nombre de la PEP")
    afinity_lvl = fields.Selection([
        ('hermano/hermana', 'Hermano/Hermana'),
        ('madre/padre', 'Madre/Padre'),
        ('abuelo/abuela', 'Abuelo/Abuela'),
        ('tio/tia', 'Tio/Tia'),
        ('primo/primo', 'Primo/Prima'),
        ('padrino/madrina', 'Padrino/Madrina'),
        ('amigo', 'Amigo')
    ], string="Indicar nivel de vinculo")


    gobv_position2 = fields.Char(string="Cargo, Rango o Posición en Gobierno")
    position_date2 = fields.Date(string="Fecha desde que ocupa el Cargo, Rango o Posición")
    gobv_institution2 = fields.Char(string="Institución a la que pertenece")
    gobv_country2 = fields.Char(string="Pais")

    inter_type = fields.Selection([
       ('fideicomitente', 'Fideicomitente'),
       ('fideicomisario', 'Fideicomisario'),
       ('otro', 'Otro')
   ], string="Tipo de interviniente")

    fideicom_nombre = fields.Char(string="Nombre de Fideicomisio")
    fideicom_type = fields.Char(string="Tipo de Fideicomisio")

    aprox_amount_proj = fields.Float(string="Monto Estimado del proyecto")
    amount_10 = fields.Boolean(string="Menor a 10")
    amount_10_40 = fields.Boolean(string="De 10MM a 40MM")
    amount_40 = fields.Boolean(string="Mayor de 40MM")
    initial_input = fields.Float(string="Aporte inicial o unico")
    input_type = fields.Char(string="Tipo de aporte")

    # -- Volumen inicial y forma de transacciones --
    unique_input = fields.Boolean(string="No aplica, Aporte unico")
    anual_2_3 = fields.Boolean(string="2 a 3 Aportes anuales")
    anual_more = fields.Boolean(string="3 o mas Aportes anuales")

    # -- tipo principal de aporte --
    transaction_cash = fields.Boolean(string="Efectivo")
    transaction_check = fields.Boolean(string="Cheque o Transferencia a cuenta bancaria")
    transaction_input = fields.Boolean(string="Aporte a inmueble")

    channel_transactions_intl_banks = fields.Boolean(string="Transferencias locales/Internacionales a cuentas bancarias")
    channel_deposit_banks = fields.Boolean(string="Deposito en e    fectivo o Cheque directo en cuentas bancarias")

    international_input_q = fields.Selection([
        ('si', 'Si'),
        ('no', 'No')
    ], string="¿Realizara aportes mediante transferencias internacionales a la cuenta bancaria?")
    # Si la respuesta es si entonces...
    international_input_country = fields.Char(string="Si su respuesta es si, Indique el pais de origen")

    negotiation_purpose = fields.Char(string="Proposito de la negociacion")
    funds_origin = fields.Char(string="Origen de fondos")

    # -- Module relations --
    commercial_info = fields.One2many('real.estate.custom.doc.formulario.info', 'comercial_ref',
                                      string="Informacion Comercial")
    banks_ids = fields.One2many('real.estate.custom.doc.formulario.bank.refs', 'bank_refs',
                                string="Referencias de bancos")
    provider_refs = fields.One2many('real.estate.custom.doc.formulario.providers', 'provider_ref',
                                    string="Principales proveedores (Solo Independientes)")
    clients_refs = fields.One2many('real.estate.custom.doc.formulario.clients', 'client_refs',
                                   string="Segmentos de clientes (Solo para independientes)")
    # project_refs = fields.One2many('real.estate.custom.doc.formulario.infop', 'project_ref',
    #                                string="Cuotas del Projecto")
    contacts_ref = fields.Many2one('res.partner', string="Referencias a los formularios")

#
# class PersonalRefs(models.Model):
#     _name = 'real.estate.custom.doc.formulario.info'
#
#     comercial_ref = fields.Many2one(string='Referencias comerciales')
#     name_last = fields.Char(string='Nombre y apellidos')
#     contact_phone = fields.Char(string='Numero de contacto')
#     relation_type = fields.Char(string='Tipo de relacion')
#
#
# class OtherResidences(models.Model):
#     _name = 'real.estate.custom.doc.formulario.residences'
#
#     residence_ref = fields.Many2one(string='Otras nacionalidades o residencias')
#     residence = fields.Boolean(string='Residente')
#     citizen = fields.Boolean(string='Ciudadano')
#     country = fields.Char(string='Indique el pais')
#
#
# class Passports(models.Model):
#     _name = 'real.estate.custom.doc.formulario.passports'
#
#     passport_refs = fields.Many2one(string="Pasaportes")
#     extra_passport = fields.Char(string='Pasaporte extra')
#     passport_nation = fields.Char(string="Pais de Expedicion del pasaporte")
#     passport_date = fields.Date(string="Fecha de Expedicion de pasaporte")
#     passport_expire = fieldsNo.Date(string="Fecha de Vencimiento")
#
#
# class BankRefs(models.Model):
#     _name = 'real.estate.custom.doc.formulario.bank.refs'
#
#     bank_refs = fields.Many2one(string='Bancos de referencia')
#     acc_num = fields.Char(string="Numero de cuenta (Opcional)")
#     acc_type = fields.Char(string="Tipo de cuenta")
#     acc_coin = fields.Char(string="Moneda")
#     acc_opening = fields.Char(string="Fecha de apertura")
#     acc_entity = fields.Char(string="Nombre de entidad de intermediacion financiera")
#     acc_country = fields.Char(string="Pais de origen")
#
#
# class ClientRefs(models.Model):
#     _name = 'real.estate.custom.doc.formulario.clients'
#
#     client_refs = fields.Many2one(string="Referencias de Clientes (Solo para independientes)")
#     names = fields.Char(string="Nombre y apellido/ Nombre de la empresa")
#     contact_num = fields.Char(string="Numero del contacto")
#
#
# class ProvidersRefs(models.Model):
#     _name = 'real.estate.custom.doc.formulario.providers'
#
#     provider_ref = fields.Many2one(string="Proveedores principales")
#     names = fields.Char(string="Nombre y apellido / Nombre de la empresa")
#     contact_num = fields.Char(string="Numero de contacto")
#
#
# class ProjectInfo(models.Model):
#     _name = 'real.estate.custom.doc.formulario.infop'
#
#     project_ref = fields.Many2one(string="Informacion del proyecto")
#     amount = fields.Float(string="Monto")
#     day = fields.Char(string="Dia")
#     month = fields.Char(string="Mes")

