from os.path import dirname, join
from setuptools import setup


readme_path = join(dirname(__file__), 'README.md')

with open(readme_path) as readme_file:
    readme = readme_file.read()


setup(
    name='aiookru',
    version='0.0.1',
    author='Konstantin Togoi',
    author_email='konstantin.togoi@protonmail.com',
    url='https://github.com/KonstantinTogoi/aiookru',
    description='ok.ru Python REST API wrapper',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='BSD',
    packages=['aiookru'],
    install_requires='aiohttp>=3.0.0',
    tests_require=['pytest', 'pytest-asyncio', 'pytest-localserver'],
    keywords=['ok.ru api asyncio'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
