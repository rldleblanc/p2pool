from setuptools import setup, find_packages
from setuptools.extension import Extension
from glob import glob
from p2pool import __version__

ltc_scrypt_module = Extension('p2pool.pow.ltc_scrypt',
                              sources = ['p2pool/pow/scryptmodule.c',
                                         'p2pool/pow/scrypt.c'])

setup(
    name='P2Pool',
    version=__version__,
    description='Peer-to-peer Bitcoin mining pool',
    long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    author='Forrest Voight <forrest@forre.st>, Jonathan Toomim <j@toom.im>, Robert LeBlanc <robert@leblancnet.us>',
    url='https://github.com/jtoomim/p2pool.git',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Twisted',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Other/Nonlisted Topic',
        ],
    packages=find_packages(),
    python_requires='~=3.5',
    install_requires=[
        'twisted',
        ],
    entry_points={
        'console_scripts': [
            'run_p2pool.py=p2pool.main:run',
            ],
        },
    ext_modules=[ltc_scrypt_module],
    include_package_data=True,
    data_files=[
        ('', ['VERSION']),
        ('web-static', glob('web-static/*')),
        ],
    )
