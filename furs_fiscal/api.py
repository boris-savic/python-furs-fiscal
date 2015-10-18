from base_api import FURSBaseAPI


class FURSBusinessPremiseAPI(FURSBaseAPI):
    def register_immovable_business_premise(self, tax_number, premise_id, real_estate_cadastral_number,
                                            real_estate_building_number, real_estate_building_section_number,
                                            street, house_number, house_number_additional,
                                            community, city, postal_code, validity_date, software_supplier_tax_number,
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
        :param validity_date: (datetime object) Datetime object representing the date when the premise started issuing invoices
        :param software_supplier_tax_number: (int) Tax number of the software supplier. E.g. "10039856"
        :param special_notes: (string) If you need to send any special notes to FURS. Default is ""
        :return:
        """
        # TODO - build JSON, call FURSBaseAPI. Define return object
        raise NotImplemented()

    def register_movable_business_premise(self):
        # TODO - define parameters, build JSON, call FURSBaseAPI
        raise NotImplemented()


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
