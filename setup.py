from setuptools import setup

setup(
  name = 'furs_fiscal',
  packages = ['furs_fiscal'],
  version = '0.4.0',
  description = 'Python library for simplified communication with FURS (Financna uprava Republike Slovenije).',
  author = 'Boris Savic',
  author_email = 'boris70@gmail.com',
  url = 'https://github.com/boris-savic/python-furs-fiscal',
  download_url = 'https://github.com/boris-savic/python-furs-fiscal/tarball/0.4.0',
  keywords = ['FURS', 'fiscal', 'fiscal register', 'davcne blagajne'],
  classifiers = [],
  package_data={'furs_fiscal': ['certs/*.pem']},
  install_requires=[
        'pytz==2017.2',
        'requests==2.13.0',
        'python-jose==0.5.4',
        'pyOpenSSL==17.0.0',
    ]
)