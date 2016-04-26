import pytz
import hashlib
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
                                            special_notes='No notes',
                                            close=False):
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
        :param close (boolean), If you want to close business unit. Default is False
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
                                          special_notes='No notes',
                                          close=True):
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
        :param close (boolean), If you want to close business unit. Default is False
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
            "DateTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
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
        if kwargs.get('close', False):
            data['BusinessPremiseRequest']['BusinessPremise']['ClosingTag'] = 'Z'

        return data


class FURSInvoiceAPI(FURSBaseAPI):

    def __init__(self, low_tax_rate=9.5, high_tax_rate=22, *args, **kwargs):
        """
        Initialize the class with current active tax rates in Slovenia.

        :param low_tax_rate: (float) - Defaults to 9.5 for 9.5%
        :param high_tax_rate:  (float) - Defaults to 22 for 22%
        :param args:
        :param kwargs:
        :return:
        """
        FURSBaseAPI.__init__(self, *args, **kwargs)
        self.low_tax_rate = low_tax_rate
        self.high_tax_rate = high_tax_rate

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

    def prepare_printable(self, tax_number, zoi, issued_date, timezone='Europe/Ljubljana'):
        """
        Get Data Record for QR Code/Code 128/PDF417 that should be placed at the bottom of the Invoice.

        :param tax_number:
        :param zoi:
        :param issued_date:
        :return: (string) Data Record
        """
        if issued_date.tzinfo:
            tz = pytz.timezone(timezone)
            issued_date = issued_date.astimezone(tz)

        zoi_base10 = str(int(zoi, 16)).zfill(39)
        date_str = issued_date.strftime('%y%m%d%H%M%S')

        data = zoi_base10+str(tax_number)+date_str
        control = str(sum(map(int, data)) % 10)

        return data+control

    def get_invoice_eor(self,
                        zoi,
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
        """
        Obtain EOR from FURS. Will build the request and call the FURS API.

        :param zoi:
        :param tax_number:
        :param issued_date:
        :param invoice_number:
        :param business_premise_id:
        :param electronic_device_id:
        :param invoice_amount:
        :param low_tax_rate_base:
        :param low_tax_rate_amount:
        :param high_tax_rate_base:
        :param high_tax_rate_amount:
        :param other_taxes_amount:
        :param exempt_vat_taxable_amount:
        :param reverse_vat_taxable_amount:
        :param non_taxable_amount:
        :param special_tax_rules_amount:
        :param payment_amount:
        :param customer_vat_number:
        :param returns_amount:
        :param operator_tax_number: (int) - Tax number of the register operator
        :param foreign_operator: (boolean) - Set to True if register operator does not have Slovenian TAX number
        :param subsequent_submit: (boolean) - Set to True if you're reissuing the request to FURS
        :param reference_invoice_number: (string) - Required if we're issuing Storno
        :param reference_invoice_business_premise_id: (string) - Required if we're issuing Storno
        :param reference_invoice_electronic_device_id: (string) - Required if we're issuing Storno
        :param reference_invoice_issued_date: (datetime) - Required if we're issuing Storno
        :param numbering_structure: (string) - defaults to B - numbering is defined by the Register, C for central numbering
        :param special_notes:
        :return: eor (string) - Invoice UniqueID from FURS
        """
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

        message['InvoiceRequest']['Invoice']['TaxesPerSeller'].append(tax_spec)

        if customer_vat_number:
            message['InvoiceRequest']['Invoice']['CustomerVATNumber'] = customer_vat_number

        if returns_amount:
            message['InvoiceRequest']['Invoice']['ReturnsAmount'] = returns_amount

        if operator_tax_number:
            message['InvoiceRequest']['Invoice']['OperatorTaxNumber'] = operator_tax_number

        if foreign_operator:
            message['InvoiceRequest']['Invoice']['ForeignOperator'] = True

        if subsequent_submit:
            message['InvoiceRequest']['Invoice']['SubsequentSubmit'] = True

        if reference_invoice_number:
            reference_invoice = [{
                'ReferenceInvoiceIdentifier': {
                    'BusinessPremiseID': reference_invoice_business_premise_id,
                    'ElectronicDeviceID': reference_invoice_electronic_device_id,
                    'InvoiceNumber': reference_invoice_number
                },
                'ReferenceInvoiceIssueDateTime': reference_invoice_issued_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }]

            message['InvoiceRequest']['Invoice']['ReferenceInvoice'] = reference_invoice

        response = self._send_request(path=INVOICE_ISSUE_PATH, data=message)

        return response['InvoiceResponse']['UniqueInvoiceID']

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
            "DateTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        return header

    @staticmethod
    def _build_common_message_body(*args, **kwargs):
        data = dict()
        data['InvoiceRequest'] = {
            'Header': FURSInvoiceAPI._prepare_invoice_request_header(),
            'Invoice': {
                'TaxNumber': kwargs['tax_number'],
                'IssueDateTime': kwargs['issued_date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            }
        }

        return data


    def get_sales_book_invoice_eor(self,
                        tax_number,
                        issued_date,
                        invoice_number,
                        business_premise_id,
                        set_number,
                        serial_number,
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
                        reference_invoice_number=None,
                        reference_invoice_business_premise_id=None,
                        reference_invoice_electronic_device_id=None,
                        reference_invoice_issued_date=None,
                        reference_sales_book_number=None,
                        reference_sales_book_issued_date=None,
                        special_notes=''):
        """
        Obtain EOR from FURS. Will build the request and call the FURS API.

        :param tax_number:
        :param issued_date:
        :param invoice_number:
        :param business_premise_id:
        :param set_number:
        :param serial_number:
        :param invoice_amount:
        :param low_tax_rate_base:
        :param low_tax_rate_amount:
        :param high_tax_rate_base:
        :param high_tax_rate_amount:
        :param other_taxes_amount:
        :param exempt_vat_taxable_amount:
        :param reverse_vat_taxable_amount:
        :param non_taxable_amount:
        :param special_tax_rules_amount:
        :param payment_amount:
        :param customer_vat_number:
        :param returns_amount:
        :param operator_tax_number: (int) - Tax number of the register operator
        :param reference_invoice_number: (string) - Required if we're issuing Storno
        :param reference_invoice_business_premise_id: (string) - Required if we're issuing Storno
        :param reference_invoice_electronic_device_id: (string) - Required if we're issuing Storno
        :param reference_invoice_issued_date: (datetime) - Required if we're issuing Storno
        :param special_notes:
        :return: eor (string) - Invoice UniqueID from FURS
        """
        # build the base message body
        message = self._build_common_sales_book_message_body(**locals())

        tax_spec = {'SellerTaxNumber': operator_tax_number}
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

        message['InvoiceRequest']['SalesBookInvoice']['TaxesPerSeller'].append(tax_spec)

        if customer_vat_number:
            message['InvoiceRequest']['SalesBookInvoice']['CustomerVATNumber'] = customer_vat_number

        if returns_amount:
            message['InvoiceRequest']['SalesBookInvoice']['ReturnsAmount'] = returns_amount


        if reference_invoice_number:
            reference_invoice = [{
                'ReferenceInvoiceIdentifier': {
                    'BusinessPremiseID': reference_invoice_business_premise_id,
                    'ElectronicDeviceID': reference_invoice_electronic_device_id,
                    'InvoiceNumber': reference_invoice_number
                },
                'ReferenceInvoiceIssueDateTime': reference_invoice_issued_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }]
            message['InvoiceRequest']['SalesBookInvoice']['ReferenceInvoice'] = reference_invoice

        if reference_sales_book_number:
            reference_sales_book = [{
                'ReferenceSalesBook': {
                    'ReferenceSalesBookIdentifier': reference_sales_book_number,
                    'ReferenceSalesBookIssueDate': reference_sales_book_issued_date,
                },
                'ReferenceInvoiceIssueDateTime': reference_invoice_issued_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }]
            message['InvoiceRequest']['SalesBookInvoice']['ReferenceSalesBook'] = reference_sales_book

        response = self._send_request(path=INVOICE_ISSUE_PATH, data=message)

        return response['InvoiceResponse']['UniqueInvoiceID']


    @staticmethod
    def _build_common_sales_book_message_body(*args, **kwargs):
        data = dict()
        data['InvoiceRequest'] = {
            'Header': FURSInvoiceAPI._prepare_invoice_request_header(),
            'SalesBookInvoice': {
                'TaxNumber': kwargs['tax_number'],
                'IssueDate': kwargs['issued_date'].strftime("%Y-%m-%d"),
                'SalesBookIdentifier': {
                    'InvoiceNumber': kwargs['invoice_number'],
                    'SetNumber': kwargs['set_number'],
                    'SerialNumber': kwargs['serial_number'],
                },
                'BusinessPremiseID': kwargs['business_premise_id'],
                'InvoiceAmount': kwargs['invoice_amount'],
                'PaymentAmount': kwargs['payment_amount'] if kwargs['payment_amount'] else kwargs['invoice_amount'],
                'TaxesPerSeller': [],
            }
        }

        return data
