# setup.py

import setuptools


setuptools.setup(
    name='clocks',
    version='0.1.0',
    packages=['common',
              'machine',
              'system'],
    package_dir={'common': 'clocks/common/',
                 'machine': 'clocks/machine/',
                 'system': 'clocks/system/'},
    install_requires=['flake8',
                      'pytest'],
    python_requires='>=3.10',
)
