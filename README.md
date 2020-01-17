# python-furs-fiscal

[![Join the chat at https://gitter.im/boris-savic/python-furs-fiscal](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/boris-savic/python-furs-fiscal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Python library for simplified communication with  FURS (Finančna uprava Republike Slovenije).



## Installation

    $ pip install furs_fiscal

## Quick Start


### Registering Immovable Business Premise

Registering new Business Premises is simple. But you will need to obtain certain information
from your client such as:

 * Real Estate Cadastral Number
 * Real Estate Building Number
 * Real Estate Building Section Number

One thing you should also keep in mind is your premise address - if your premise is located at **Trzaska cesta 24A** you will need to pass house number **24** and additional number **A** as separate parameters.
If your street does not have additional house number/letter just pass None.

```python
from furs_fiscal.api import FURSBusinessPremiseAPI

api = FURSBusinessPremiseAPI(p12_path='my_cert.p12',
                             p12_password='cert_pass',
                             production=True, request_timeout=2.0)

api.register_immovable_business_premise(tax_number=10039856,
                                        premise_id='BP101',
                                        real_estate_cadastral_number=112,
                                        real_estate_building_number=11,
                                        real_estate_building_section_number=1,
                                        street='Trzaska cesta',
                                        house_number='24',
                                        house_number_additional='A',
                                        community='Ljubljana',
                                        city='Ljubljana',
                                        postal_code='1000',
                                        validity_date=datetime.now() - timedelta(days=60),
                                        software_supplier_tax_number=24564444,
                                        foreign_software_supplier_name=None,
                                        special_notes='/')
```

**NOTE**: As of 23.11.2015 FURS does require you to send some kind of Special note to them. Empty string will raise
invalid JSON on their side.

### Registering Movable Business Premise

In order to register Movable Business Premise you will need to define one of three types:

 * **TYPE_MOVABLE_PREMISE_A**: Movable object such as vehicle, movable stand etc.
 * **TYPE_MOVABLE_PREMISE_B**: Object at permanent location such as news stand, market stand etc.
 * **TYPE_MOVABLE_PREMISE_C**: Individual electronic device in cases when the company does not use other business premises


```python
from furs_fiscal.api import FURSBusinessPremiseAPI, TYPE_MOVABLE_PREMISE_A

api = FURSBusinessPremiseAPI(p12_path='my_cert.p12',
                             p12_password='cert_pass',
                             production=True,
                             request_timeout=2.0)

api.register_movable_business_premise(tax_number=10039856,
                                      premise_id='BP102',
                                      movable_type=TYPE_MOVABLE_PREMISE_A,
                                      validity_date=datetime.now() - timedelta(days=60),
                                      software_supplier_tax_number=24564444,
                                      foreign_software_supplier_name=None,
                                      special_notes='')

```

### Calculate Invoice ZOI - Protected ID

At the end of every Invoice your should print ZOI (Protected ID). To obtain it follow the next procedure:

```python
from furs_fiscal.api import FURSInvoiceAPI

api = FURSInvoiceAPI(p12_path='my_cert.p12',
                     p12_password='cert_pass',
                     production=False,
                     request_timeout=1.0)

date_issued = datetime.now()

zoi = api.calculate_zoi(tax_number=10039856,
                        issued_date=date_issued,
                        invoice_number='11',
                        business_premise_id='BP101',
                        electronic_device_id='B1',
                        invoice_amount=Decimal('19.15'))

```

### Generate Data for QR/Code128/PDF417

You're supposed to print QR Code/Code128 or PDF 417 on every invoice after the ZOI. To obtain the data for QR/Code128/PDF417 perform the following method call on **FURSInvoiceAPI** object.

```python
qr_data = api.prepare_printable(tax_number=10039856,
                                zoi=zoi,
                                issued_date=date_issued)
```

### Get EOR From FURS

To obtain FURS EOR code - UniqueID, you'll have to call the following method. It provides several other parameters,
for issuing invoice storno and special tax rules. Please read the full documentation.

```python
# In most cases there will be just one seller - company that issues the invoice
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

eor = api.get_invoice_eor(zoi=zoi,
                          tax_number=10039856,
                          issued_date=date_issued,
                          invoice_number='11',
                          business_premise_id='BP101',
                          electronic_device_id='B1',
                          invoice_amount=66.71,
                          taxes_per_seller=[seller_one],  # NOTE: Must be an array of TaxesPerSeller objects
                          operator_tax_number=12345678)
```

## Contributing

This library should be sufficient to integrate into your software as is, but there is still some work that needs to be done.

You can contribute in one of the following areas:

 * Detailed documentation
 * More examples for various use-cases
 * Support for issuing invoices with multiple seller tax rates
 * Tests - I'll be adding them soon, but I'll be grateful if you'd help
 * Support for Decimal object serialization

## Contact

**Boris Savic**

 * Twitter: [@zitko](https://twitter.com/zitko)
 * Email: boris70@gmail.com





