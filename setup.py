try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='beereader',
    version='0.1',
    description='lightweight frontend for melkman',
    author='Luke Tucker',
    author_email='ltucker@openplans.org',
    url='http://github.com/jab/beereader',
    install_requires=[
        "Pylons>=0.9.7",
        "melkman",
        "python-dateutil",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'beereader': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'beereader': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = beereader.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
