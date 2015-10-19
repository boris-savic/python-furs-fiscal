import pytz
import uuid
import datetime

from base_api import FURSBaseAPI

TYPE_MOVABLE_PREMISE_A = 'A'
TYPE_MOVABLE_PREMISE_B = 'B'
TYPE_MOVABLE_PREMISE_C = 'C'

REGISTER_BUSINESS_UNIT_PATH = 'v1/cash_registers/invoices/register'


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
        real_estate_bp = message['BusinessPremiseRequest']['BusinessPremise']['BPIdentifier']['RealEstateBP']

        real_estate_bp['PropertyID'] = {
            'CadastralNumber': real_estate_cadastral_number,
            'BuildingNumber': real_estate_building_number,
            'BuildingSectionNumber': real_estate_building_section_number
        }

        self._send_request(path=REGISTER_BUSINESS_UNIT_PATH, data=message)

        return True

    def register_movable_business_premise(self):
        # TODO - define parameters, build JSON, call FURSBaseAPI
        raise NotImplemented()

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
                'BPIdentifier': {
                    'RealEstateBP': {
                        'Address': {
                            'Street': kwargs['street'],
                            'HouseNumber': kwargs['house_number'],
                            'HouseNumberAdditional': kwargs['house_number_additional'],
                            'Community': kwargs['community'],
                            'City': kwargs['city'],
                            'PostalCode': kwargs['postal_code']
                        }
                    }
                }
            }
        }

        if kwargs['house_number_additional'] == '' or kwargs['house_number_additional'] is None:
            data['BusinessPremiseRequest']['BusinessPremise']\
                ['BPIdentifier']['RealEstateBP']['Address'].pop('HouseNumberAdditional')

        return data



class FURSInvoiceAPI(FURSBaseAPI):

    def get_protected_id(self, *args, **kwargs):
        # TODO - define parameters, docstring
        return self.get_zoi(*args, **kwargs)

    def get_unique_invoice_id(self, *args, **kwargs):
        # TODO - define parameters, docstring
        return self.get_eor(*args, **kwargs)

    def get_zoi(self, *args, **kwargs):
        # TODO - define parameters
        raise NotImplemented()

    def get_eor(self, *args, **kwargs):
        # TODO - define parameters, build JSON, call FURSBaseAPI
        raise NotImplemented()
