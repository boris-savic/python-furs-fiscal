import pytz

from datetime import datetime

from furs_fiscal.api import FURSInvoiceAPI


# Path to our .p12 cert file
P12_CERT_PATH = 'demo_podjetje.p12'
# Password for out .p12 cert file
P12_CERT_PASS = 'Geslo123#'


class SalesBookInvoiceEORDemo():

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


        print("Sales book invoice")

        # get EOR code from FURS
        eor = api.get_sales_book_invoice_eor(tax_number=10039856,
                                             issued_date=date_issued,
                                             invoice_number='612',
                                             business_premise_id='BP105',
                                             set_number='03',
                                             serial_number='5001-0001018',
                                             invoice_amount=66.71,
                                             low_tax_rate_base=35.14,
                                             low_tax_rate_amount=3.34,
                                             high_tax_rate_base=23.14,
                                             high_tax_rate_amount=5.09,
                                             operator_tax_number=12345678)

        print("EOR: " + eor)


if __name__ == "__main__":
    demo = SalesBookInvoiceEORDemo()
    demo.demo_eor()
