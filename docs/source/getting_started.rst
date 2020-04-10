Getting Started
===============

Installation
------------

If you use pip, just type

.. code-block:: shell

    $ pip install aiookru

You can install from the source code like

.. code-block:: shell

    $ git clone https://github.com/KonstantinTogoi/aiookru.git
    $ cd aiookru
    $ python setup.py install

Account
-------

To create an app you need to:

1. Sign up in `ok.Ru <https://ok.ru>`_ and link an email to your account to receive emails with app data.
2. Obtain developer rights at https://ok.ru/devaccess.

After obtaining developer rights you will get a link
to add apps or external sites.
Open `Games <https://ok.ru/vitrine>`_ and select "My downloads" on top.

Application
-----------

After signing up visit the OK.Ru REST API
`documentation page <https://apiok.ru/en/>`_
and create a new application: https://apiok.ru/en/dev/app/create.

To use client OAuth authentication it must be enabled in the app settings.

Save **app_id** (aka **application_id**), **app_key** (aka **application_key**)
and **app_secret_key** (aka **application_secret_key**)
for user authorization and executing API requests.

.. code-block:: python

    app_id = 'your_client_id'
    app_key = 'your_private_key'
    app_secret_key = 'your_secret_key'
