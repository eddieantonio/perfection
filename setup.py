from distutils.core import setup
from perfection import __version__ as VERSION

setup(
    name='perfection',
    version=VERSION,
    url='https://github.com/eddieantonio/perfection',
    license='MIT',
    author='Eddie Antonio Santos',
    author_email='easantos@ualberta.ca',
    description='Perfect hashing utilities for Python',
    long_description=open('README.rst').read(),
    packages=['perfection',],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    download_url = 'https://github.com/eddieantonio/perfection/tarball/v1.0.1',
)
