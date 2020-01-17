import pytz

from datetime import datetime
from decimal import Decimal

from furs_fiscal.api import FURSInvoiceAPI, TaxesPerSeller

# Path to our .p12 cert file
P12_CERT_PATH = 'demo_podjetje.p12'
# Password for out .p12 cert file
P12_CERT_PASS = 'Geslo123#'


class InvoiceEORDemo():

    def demo_eor(self):
        """
        This demo shows how you should report your invoice to the FURS.
        """

        # First we'll need to initialize FURSInvoice APi - so that it loads all the certs
        api = FURSInvoiceAPI(p12_path=P12_CERT_PATH,
                             p12_password=P12_CERT_PASS,
                             production=False,
                             request_timeout=1.0)

        date_issued = datetime.now(tz=pytz.UTC)
        # let's get that ZOI
        zoi = api.calculate_zoi(tax_number=10039856,  # Issuer Tax Number
                                issued_date=date_issued,  # DateTime of the Invoice
                                invoice_number='11',  # Invoice Number - Sequential
                                business_premise_id='BP105',  # Business premise ID
                                electronic_device_id='B1',  # Electronic Device ID
                                invoice_amount=Decimal('19.15'))  # Invoice Amount

        print("ZOI: " + zoi)

        # Construct TaxesPerSeller object - for each seller.
        # In most cases there will be just one seller - the one that issues the invoice
        # For some cases - you may need to include more sellers. In that case
        #                  do not forget to set seller_tax_number for the other sellers.
        #                  you don't need to set it for your company - but you do for others.
        seller_one = TaxesPerSeller(other_taxes_amount=None,
                                    exempt_vat_taxable_amount=None,
                                    reverse_vat_taxable_amount=None,
                                    non_taxable_amount=None,
                                    special_tax_rules_amount=None,
                                    seller_tax_number=None)

        seller_one.add_vat_amount(tax_rate=22, tax_base=23.14, tax_amount=5.09)
        seller_one.add_vat_amount(tax_rate=9.5, tax_base=35.14, tax_amount=3.34)
        # 5% vat - for books etc...
        seller_one.add_vat_amount(tax_rate=5, tax_base=10, tax_amount=0.5)

        # get EOR code from FURS
        eor = api.get_invoice_eor(zoi=zoi,
                                  tax_number=10039856,
                                  issued_date=date_issued,
                                  invoice_number='11',
                                  business_premise_id='BP105',
                                  electronic_device_id='B1',
                                  invoice_amount=66.71,
                                  taxes_per_seller=[seller_one],
                                  operator_tax_number=12345678,
                                  reference_invoice_number=['10', '11'],
                                  reference_invoice_business_premise_id=['BP105', 'BP105'],
                                  reference_invoice_electronic_device_id=['B1', 'B1'],
                                  reference_invoice_issued_date=[date_issued, date_issued]
                                  )

        print("EOR: " + eor)


if __name__ == "__main__":
    demo = InvoiceEORDemo()
    demo.demo_eor()
