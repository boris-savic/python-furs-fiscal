from setuptools import setup

setup(
  name = 'furs_fiscal',
  packages = ['furs_fiscal'],
  version = '0.3.0',
  description = 'Python library for simplified communication with FURS (Financna uprava Republike Slovenije).',
  author = 'Boris Savic',
  author_email = 'boris70@gmail.com',
  url = 'https://github.com/boris-savic/python-furs-fiscal',
  download_url = 'https://github.com/boris-savic/python-furs-fiscal/tarball/0.3.0',
  keywords = ['FURS', 'fiscal', 'fiscal register', 'davcne blagajne'],
  classifiers = [],
  package_data={'furs_fiscal': ['certs/*.pem']},
  install_requires=[
        'pytz',
        'requests',
        'python-jose',
        'pyOpenSSL',
        'urllib3',
        'pyasn1',
        'ndg-httpsclient'
    ]
)