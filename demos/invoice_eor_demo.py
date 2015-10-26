from datetime import datetime
from decimal import Decimal

from furs_fiscal.api import FURSInvoiceAPI


# Path to our .p12 cert file
P12_CERT_PATH = 'demo_podjetje.p12'
# Password for out .p12 cert file
P12_CERT_PASS = 'Geslo123#'


class InvoiceEORDemo():

    def demo_eor(self):
        """
        """

        # First we'll need to initialize FURSInvoice APi - so that it loads all the certs
        api = FURSInvoiceAPI(p12_path=P12_CERT_PATH,
                             p12_password=P12_CERT_PASS,
                             production=False,
                             request_timeout=1.0)

        date_issued = datetime.now()
        # let's get that ZOI
        zoi = api.calculate_zoi(tax_number=10039856,  # Issuer Tax Number
                                issued_date=date_issued,  # DateTime of the Invoice
                                invoice_number='11',  # Invoice Number - Sequential
                                business_premise_id='BP101',  # Business premise ID
                                electronic_device_id='B1',  # Electronic Device ID
                                invoice_amount=Decimal('19.15'))  # Invoice Amount

        print("ZOI: " + zoi)

        # get EOR code from FURS
        eor = api.get_invoice_eor(zoi=zoi,
                                  tax_number=10039856,
                                  issued_date=date_issued,
                                  invoice_number='11',
                                  business_premise_id='BP101',
                                  electronic_device_id='B1',
                                  invoice_amount=66.71,
                                  low_tax_rate_base=35.14,
                                  low_tax_rate_amount=3.34,
                                  high_tax_rate_base=23.14,
                                  high_tax_rate_amount=5.09,
                                  operator_tax_number=12345678)

        print("EOR: " + eor)

if __name__ == "__main__":
    demo = InvoiceEORDemo()
    demo.demo_eor()
