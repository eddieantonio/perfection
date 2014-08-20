from distutils.core import setup

setup(
    name='perfection',
    version='1.0.0',
    url='https://github.com/eddieantonio/perfection',
    license='MIT',
    author='Eddie Antonio Santos',
    author_email='easantos@ualberta.ca',
    description='Perfect hashing utilities for Python',
    long_description=open('README.txt').read(),
    packages=['perfection',],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    download_url = 'https://github.com/eddieantonio/perfection/tarball/v1.0.0',
)
