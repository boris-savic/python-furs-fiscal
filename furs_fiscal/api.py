import hashlib
import pytz
import uuid
import datetime

from base_api import FURSBaseAPI


TYPE_MOVABLE_PREMISE_A = 'A'
TYPE_MOVABLE_PREMISE_B = 'B'
TYPE_MOVABLE_PREMISE_C = 'C'

NUMBERING_STRUCTURE_CENTRAL = 'C'
NUMBERING_STRUCTURE_DEVICE = 'B'

REGISTER_BUSINESS_UNIT_PATH = 'v1/cash_registers/invoices/register'
INVOICE_ISSUE_PATH = 'v1/cash_registers/invoices'


class FURSBusinessPremiseAPI(FURSBaseAPI):
    """
    FURSBusinessPremiseAPI allows you to register business unit to FURS prior to issuing any invoices.
    """
    def register_immovable_business_premise(self,
                                            tax_number,
                                            premise_id,
                                            real_estate_cadastral_number,
                                            real_estate_building_number,
                                            real_estate_building_section_number,
                                            street,
                                            house_number,
                                            house_number_additional,
                                            community,
                                            city,
                                            postal_code,
                                            validity_date,
                                            software_supplier_tax_number=None,
                                            foreign_software_supplier_name=None,
                                            special_notes=''):
        """
        Register immovable business premise to FURS.

        :param tax_number: (int) Tax number of the business. E.g. "10039856"
        :param premise_id: (string) Business Premise Identifier. E.g. "PE12"
        :param real_estate_cadastral_number: (int) Cadastral number of the real estate. E.g. "365"
        :param real_estate_building_number: (int) Cadastral building number. E.g. "12"
        :param real_estate_building_section_number: (int) Cadastral building section number. E.g. "3"
        :param street: (string) Street name of the premise. E.g. "Slovenska cesta"
        :param house_number: (string) House number of the premise. E.g "24"
        :param house_number_additional: (string) Additional house number. Empty string if does not exist. E.g. "B"
        :param community: (sting) Name of the town. E.g "Ljubljana"
        :param city: (string) Name of the post office. E.g. "Ljubljana"
        :param postal_code: (string) Post office number. E.g. "1000"
        :param validity_date: (datetime object) Datetime object representing the date when the premise started
                                                issuing invoices
        :param software_supplier_tax_number: (int) Tax number of the software supplier. E.g. "10039856"
        :param foreign_software_supplier_name: (int) If software supplier is foreign company - does not have
                                                     Slovenian Tax number, then please provide provider name.
        :param special_notes: (string) If you need to send any special notes to FURS. Default is ""
        :return: boolean: Will return True if success or raise an Exception if anything goes wrong

        :raises
            FURSException - FURS server returned an error
            ConnectionTimedOutException - connection timed out
            ConnectionException - Generic exception
        """
        message = FURSBusinessPremiseAPI._build_common_message_body(**locals())

        bpi_identifier = message['BusinessPremiseRequest']['BusinessPremise']['BPIdentifier']

        bpi_identifier['RealEstateBP'] = {
            'Address': {
                'Street': street,
                'HouseNumber': house_number,
                'HouseNumberAdditional': house_number_additional,
                'Community': community,
                'City': city,
                'PostalCode': postal_code
            },
            'PropertyID': {
                'CadastralNumber': real_estate_cadastral_number,
                'BuildingNumber': real_estate_building_number,
                'BuildingSectionNumber': real_estate_building_section_number
            }
        }

        if house_number_additional == '' or house_number_additional is None:
            message['BusinessPremiseRequest']['BusinessPremise']\
                ['BPIdentifier']['RealEstateBP']['Address'].pop('HouseNumberAdditional')

        self._send_request(path=REGISTER_BUSINESS_UNIT_PATH, data=message)

        return True

    def register_movable_business_premise(self,
                                          tax_number,
                                          premise_id,
                                          movable_type,
                                          validity_date,
                                          software_supplier_tax_number=None,
                                          foreign_software_supplier_name=None,
                                          special_notes=''):
        """
        Register movable business unit to FURS.

        :param tax_number: (int) Tax number of the business. E.g. "10039856"
        :param premise_id: (string) Business Premise Identifier. E.g. "PE12"
        :param movable_type: (string) Type of the movable business unit. Values "A", "B" or "C"
        :param validity_date: (datetime object) Datetime object representing the date when the premise started
                                                issuing invoices
        :param software_supplier_tax_number: (int) Tax number of the software supplier. E.g. "10039856"
        :param foreign_software_supplier_name: (int) If software supplier is foreign company - does not have
                                                     Slovenian Tax number, then please provide provider name.
        :param special_notes: (string) If you need to send any special notes to FURS. Default is ""
        :return: boolean: Will return True if success or raise an Exception if anything goes wrong

        :raises
            FURSException - FURS server returned an error
            ConnectionTimedOutException - connection timed out
            ConnectionException - Generic exception
        """
        message = FURSBusinessPremiseAPI._build_common_message_body(**locals())
        bpi_identifier = message['BusinessPremiseRequest']['BusinessPremise']['BPIdentifier']

        bpi_identifier['PremiseType'] = movable_type

        self._send_request(path=REGISTER_BUSINESS_UNIT_PATH, data=message)

        return True

    @staticmethod
    def _prepare_business_premise_request_header():
        header = {
            "MessageID": str(uuid.uuid4()),
            "DateTime": datetime.datetime.now(tz=pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        return header

    @staticmethod
    def _prepare_software_supplier_json(software_supplier_tax_number=None, foreign_software_supplier_name=None):
        if software_supplier_tax_number:
            return {'TaxNumber': software_supplier_tax_number}
        else:
            return {'NameForeign': foreign_software_supplier_name}

    @staticmethod
    def _build_common_message_body(*args, **kwargs):
        data = dict()
        data['BusinessPremiseRequest'] = {
            'Header': FURSBusinessPremiseAPI._prepare_business_premise_request_header(),
            'BusinessPremise': {
                'TaxNumber': kwargs['tax_number'],
                'BusinessPremiseID': kwargs['premise_id'],
                'ValidityDate': kwargs['validity_date'].strftime("%Y-%m-%d"),
                'SpecialNotes': kwargs['special_notes'],
                'SoftwareSupplier': [
                    FURSBusinessPremiseAPI._prepare_software_supplier_json(kwargs['software_supplier_tax_number'],
                                                                           kwargs['foreign_software_supplier_name'])
                ],
                'BPIdentifier': {}
            }
        }

        return data


class FURSInvoiceAPI(FURSBaseAPI):

    def __init__(self, low_tax_rate=9.5, high_tax_rate=22.0, *args, **kwargs):
        """
        Initialize the class with current active tax rates in Slovenia.

        :param low_tax_rate: (float) - Defaults to 9.5 for 9.5%
        :param high_tax_rate:  (float) - Defaults to 22.0 for 22%
        :param args:
        :param kwargs:
        :return:
        """
        self.low_tax_rate = low_tax_rate
        self.high_tax_rate = high_tax_rate

        super(FURSInvoiceAPI, self).__init__(*args, **kwargs)

    def calculate_zoi(self,
                      tax_number,
                      issued_date,
                      invoice_number,
                      business_premise_id,
                      electronic_device_id,
                      invoice_amount):
        """
        Calculate ZOI - Protective Mark of the Invoice Issuer.

        :param tax_number: (int) issuer tax number
        :param issued_date: (datetime) datetime of the invoice issue
        :param invoice_number: (string) invoice sequential number
        :param business_premise_id: (string) business premise id
        :param electronic_device_id: (string) electronic device id
        :param invoice_amount: (Decimal) invoice amount
        :return: (string) ZOI string
        """
        content = "%s%s%s%s%s%s" % (tax_number,
                                    issued_date.strftime('%d-%m-%Y %H:%M:%S'),
                                    invoice_number, business_premise_id, electronic_device_id, invoice_amount)

        return hashlib.md5(self._sign(content=content)).hexdigest()

    def prepare_qr(self, tax_number, zoi, issued_date):
        """
        Get Data Record for QR Code that should be placed at the bottom of the Invoice.

        :param tax_number:
        :param zoi:
        :param issued_date:
        :return: (string) Data Record
        """
        return FURSInvoiceAPI._prepare_zoi_for_print(tax_number=tax_number, zoi=zoi, issued_date=issued_date)

    def prepare_code128(self, tax_number, zoi, issued_date):
        """
        Get Data Record for Code 128 that should be placed at the bottom of the Invoice.

        :param tax_number:
        :param zoi:
        :param issued_date:
        :return: (string) Data Record
        """
        return FURSInvoiceAPI._prepare_zoi_for_print(tax_number=tax_number, zoi=zoi, issued_date=issued_date)

    def prepare_pdf417(self, tax_number, zoi, issued_date):
        """
        Get Data Record for PDF 417 that should be placed at the bottom of the Invoice.

        :param tax_number:
        :param zoi:
        :param issued_date:
        :return: (string) Data Record
        """
        return FURSInvoiceAPI._prepare_zoi_for_print(tax_number=tax_number, zoi=zoi, issued_date=issued_date)

    @staticmethod
    def _prepare_zoi_for_print(tax_number, zoi, issued_date):
        zoi_base10 = str(int(zoi, 16))
        date_str = issued_date.strftime('%y%m%d%H%M%S')

        data = zoi_base10+str(tax_number)+date_str

        control = str(sum(map(int, data)) % 10)

        return data+control

    def get_invoice_eor(self,
                        tax_number,
                        issued_date,
                        invoice_number,
                        business_premise_id,
                        electronic_device_id,
                        invoice_amount,
                        low_tax_rate_base=None,
                        low_tax_rate_amount=None,
                        high_tax_rate_base=None,
                        high_tax_rate_amount=None,
                        other_taxes_amount=None,
                        exempt_vat_taxable_amount=None,
                        reverse_vat_taxable_amount=None,
                        non_taxable_amount=None,
                        special_tax_rules_amount=None,
                        payment_amount=None,
                        customer_vat_number=None,
                        returns_amount=None,
                        operator_tax_number=None,
                        foreign_operator=False,
                        subsequent_submit=False,
                        reference_invoice_number=None,
                        reference_invoice_business_premise_id=None,
                        reference_invoice_electronic_device_id=None,
                        reference_invoice_issued_date=None,
                        numbering_structure=NUMBERING_STRUCTURE_DEVICE,
                        special_notes=''):
        # build the base message body
        message = self._build_common_message_body(**locals())

        tax_spec = {}
        # add tax specification
        if low_tax_rate_base or high_tax_rate_base:
            tax_spec['VAT'] = self._build_tax_specification(low_tax_rate_base=low_tax_rate_base,
                                                            low_tax_rate_amount=low_tax_rate_amount,
                                                            high_tax_rate_base=high_tax_rate_base,
                                                            high_tax_rate_amount=high_tax_rate_amount)

        if non_taxable_amount:
            tax_spec['NontaxableAmount'] = non_taxable_amount
        if reverse_vat_taxable_amount:
            tax_spec['ReverseVATTaxableAmount'] = reverse_vat_taxable_amount
        if exempt_vat_taxable_amount:
            tax_spec['ExemptVATTaxableAmount'] = exempt_vat_taxable_amount
        if other_taxes_amount:
            tax_spec['OtherTaxesAmount'] = other_taxes_amount

        message['Invoice']['TaxesPerSeller'].append(tax_spec)

        if customer_vat_number:
            message['Invoice']['CustomerTaxNumber'] = customer_vat_number

        if returns_amount:
            message['Invoice']['ReturnsAmount'] = returns_amount

        if operator_tax_number:
            message['Invoice']['OperatorTaxNumber'] = operator_tax_number

        if foreign_operator:
            message['Invoice']['ForeignOperator'] = 1

        if subsequent_submit:
            message['Invoice']['SubsequentSubmit'] = 1

        if reference_invoice_number:
            reference_invoice = {
                'ReferenceInvoiceIdentifier': {
                    'BusinessPremiseID': reference_invoice_business_premise_id,
                    'ElectronicDeviceID': reference_invoice_electronic_device_id,
                    'InvoiceNumber': reference_invoice_number
                },
                'ReferenceInvoiceIssuedDateTime': reference_invoice_issued_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }

        self._send_request(path=REGISTER_BUSINESS_UNIT_PATH, data=message)

        return True

    def _build_tax_specification(self,
                                 low_tax_rate_base,
                                 low_tax_rate_amount,
                                 high_tax_rate_base,
                                 high_tax_rate_amount):
        """
        Build the TaxesPerSeller part of the request

        :param low_tax_rate_base:
        :param low_tax_rate_amount:
        :param high_tax_rate_base:
        :param high_tax_rate_amount:
        :return:
        """
        low_tax_spec = {
            'TaxRate': self.low_tax_rate,
            'TaxableAmount': low_tax_rate_base,
            'TaxAmount': low_tax_rate_amount
        }

        high_tax_spec = {
            'TaxRate': self.high_tax_rate,
            'TaxableAmount': high_tax_rate_base,
            'TaxAmount': high_tax_rate_amount
        }

        return filter(lambda x: x['TaxableAmount'] is not None, [low_tax_spec, high_tax_spec])


    @staticmethod
    def _prepare_invoice_request_header():
        header = {
            "MessageID": str(uuid.uuid4()),
            "DateTime": datetime.datetime.now(tz=pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        return header

    @staticmethod
    def _build_common_message_body(*args, **kwargs):
        data = dict()
        data['InvoiceRequest'] = {
            'Header': FURSInvoiceAPI._prepare_invoice_request_header(),
            'Invoice': {
                'TaxNumber': kwargs['tax_number'],
                'IssuedDateTime': kwargs['issued_date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                'NumberingStructure': kwargs['numbering_structure'],
                'InvoiceIdentifier': {
                    'BusinessPremiseID': kwargs['business_premise_id'],
                    'ElectronicDeviceID': kwargs['electronic_device_id'],
                    'InvoiceNumber': kwargs['invoice_number']
                },
                'InvoiceAmount': kwargs['invoice_amount'],
                'PaymentAmount': kwargs['payment_amount'] if kwargs['payment_amount'] else kwargs['invoice_amount'],
                'ProtectedID': kwargs['zoi'],
                'TaxesPerSeller': [],
                'SpecialNotes': kwargs['special_notes']
            }
        }

        return data