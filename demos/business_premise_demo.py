from datetime import datetime, timedelta

from furs_fiscal.api import FURSBusinessPremiseAPI, TYPE_MOVABLE_PREMISE_A


# Path to our .p12 cert file
P12_CERT_PATH = 'demo_podjetje.p12'
# Password for out .p12 cert file
P12_CERT_PASS = 'Geslo123#'


class BusinessPremiseDemo():

    def register_immovable_business_premise(self):
        """
        We will register a following business premise

        Name: BP105
        Address: Trzaska cesta 24A, Ljubljana, 1000 Ljubljana

        """

        # Let's initiate FURS Business Premise API for the Development server with request timeout of 1.0 second
        api = FURSBusinessPremiseAPI(p12_path=P12_CERT_PATH,
                                     p12_password=P12_CERT_PASS,
                                     production=False,
                                     request_timeout=2.0)

        # Registering business unit is easy ...
        s = api.register_immovable_business_premise(tax_number=10039856,  # TaxNumber of our Company
                                                    premise_id='BP105',  # Name of our Business Premise - printed on Invoice
                                                    real_estate_cadastral_number=112,  # Cadastral data
                                                    real_estate_building_number=11,  # Cadastral data
                                                    real_estate_building_section_number=1,  # Cadastral data
                                                    street='Trzaska cesta',
                                                    house_number='24',
                                                    house_number_additional='A',  # Set as None if you don't have it
                                                    community='Ljubljana',  # This is actually the city name...
                                                    city='Ljubljana',  # Name of the Post Office
                                                    postal_code='1000',  # Postal code
                                                    validity_date=datetime.now() - timedelta(days=60),  # Date when we opened premise
                                                    software_supplier_tax_number=24564444,  # TaxNumber of SW Supplier
                                                    foreign_software_supplier_name=None,  # If SW Supplier does not have Slovenian Tax Number pass in the supplier name
                                                    special_notes='No notes',
                                                    close=False)  # If you want to add a special note for FURS. Generaly just leave empty

        if s:
            print("Immovable Success!")

    def register_movable_business_premise(self):
        """
        Let's register a Movable Business Premise.

        Movable business premises are one of three types:
         - Type "A": Movable object such as vehicle, movable stand etc.
         - Type "B": Object at permanent location such as news stand, market stand etc.
         - Type "C": Individual electronic device in cases when the company does not use other business premises

        """
        # Let's initiate FURS Business Premise API for the Development server with request timeout of 1.0 second
        api = FURSBusinessPremiseAPI(p12_path=P12_CERT_PATH,
                                     p12_password=P12_CERT_PASS,
                                     production=False,
                                     request_timeout=1.0)

        # Registering business unit is easy ...
        s = api.register_movable_business_premise(tax_number=10039856,  # TaxNumber of our Company
                                                  premise_id='BP101',  # Name of our Business Premise - printed on Invoice
                                                  movable_type=TYPE_MOVABLE_PREMISE_A,
                                                  validity_date=datetime.now() - timedelta(days=60),  # Date when we opened premise
                                                  software_supplier_tax_number=24564444,  # TaxNumber of SW Supplier
                                                  foreign_software_supplier_name=None,  # If SW Supplier does not have Slovenian Tax Number pass in the supplier name
                                                  special_notes='No')  # If you want to add a special note for FURS. Generaly just leave empty

        if s:
            print("Movable Success!")


if __name__ == "__main__":
    demo = BusinessPremiseDemo()
    demo.register_immovable_business_premise()
    demo.register_movable_business_premise()
