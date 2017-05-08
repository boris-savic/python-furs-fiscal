import pytz

from datetime import datetime
from decimal import Decimal

from furs_fiscal.api import FURSInvoiceAPI


# Path to our .p12 cert file
P12_CERT_PATH = 'demos/demo_podjetje.p12'
# Password for out .p12 cert file
P12_CERT_PASS = 'Geslo123#'


class InvoiceDemo():

    def demo_zoi(self):
        """
        Obtaining Invoice ZOI - Protective Mark of the Invoice Issuer

        Our Invoice Number on the Receipt is:
        11/BP101/B1

        Where:
         * 11 - Invoice Number
         * BP101 - Business premise ID
         * B1 - Electronic Register ID
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
                                business_premise_id='BP101',  # Business premise ID
                                electronic_device_id='B1',  # Electronic Device ID
                                invoice_amount=Decimal('19.15'))  # Invoice Amount

        print("ZOI: " + zoi)

        # Let's obtain data for Code128/QR/PDF417 that should be placed at the bottom of the Invoice
        print_data = api.prepare_printable(tax_number=10039856,
                                    zoi=zoi,
                                    issued_date=date_issued)

        print("QR/Code128/PDF417 Data: " + print_data)


if __name__ == "__main__":
    demo = InvoiceDemo()
    demo.demo_zoi()
