# python-furs-fiscal
Python library for simplified communication with  FURS (Finančna uprava Republike Slovenije).

## Installation

TODO 

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
                                        special_notes='')
```

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

## Support

TODO

