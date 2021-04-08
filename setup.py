import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mew',
    version='0.0.1',
    author="Ravenclaw",
    author_email="arpan29@gmail.com",
    description="A Django Quickstart Package",
    url="https://github.com/arpan29/mew",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Django==2.2.20',
        'djangorestframework==3.10.3',
        'django-filter==2.2.0',
        'requests==2.22.0',
        'django-cors-headers==3.1.1',
        'pylint==2.4.3',
        'pylint-django==2.0.13',
        'google-api-python-client==1.8.0',
        'google-auth-httplib2==0.0.3',
        'google-auth-oauthlib==0.4.1',
        'jsonschema==3.1.1',
    ],
    dependency_links=[],
    scripts=['bin/mew'],
)
