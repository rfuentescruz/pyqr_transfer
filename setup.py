from setuptools import setup, find_packages

setup(
    name='pyqr_transfer',
    version='0.1.0',
    description='Transfer files from your computer to a mobile device via QR codes',
    author='Rolando Cruz <rolando.cruz21@gmail.com>',

    packages=find_packages(),

    install_requires=[
        'pyqrcode >= 1.2.1, < 2.0'
    ],
    entry_points={
        'console_scripts': ['qr-transfer=pyqr_transfer.cli:main']
    }
)
