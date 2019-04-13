from distutils.core import setup
from perfection import __version__ as VERSION

from codecs import open

setup(
    name='perfection',
    version=VERSION,
    url='https://github.com/eddieantonio/perfection',
    license='MIT',
    author='Eddie Antonio Santos',
    author_email='easantos@ualberta.ca',
    description='Perfect hashing utilities for Python',
    long_description=open('README.rst',encoding="UTF-8").read(),
    packages=['perfection',],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    download_url = 'https://github.com/eddieantonio/perfection/tarball/v' + VERSION,
)
