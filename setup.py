from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1.3'

install_requires = [
    'DataSounds',
    'numpy'
]

setup(name='OceanSound',
    version=version,
    description="Get the music from oceancolor images, through MODIS satellite",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
    ],
    keywords='music oceanography data',
    author='Arnaldo Russo , Luiz Irber',
    author_email='arnaldo@datasounds.org, luiz@datasounds.org',
    url='https://github.com/DataSounds/OceanSound',
    license='PSF',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
#    entry_points={
#        'console_scripts':
#            ['cnv=cnv:main']
#    },
    platforms='any',
#    scripts=["bin/cnvdump"],
)
