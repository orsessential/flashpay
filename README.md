<h2>FlashPay</h2>
simple mini wallet service using django rest framework

============================

<h3>running at:</h3>
    http://127.0.0.1:8000/


<h3>Assets postman collection</h3>
In assets folder

<h3>function:</h3>

* initialize wallet account
* view balance/amount wallet
* deposit balance
* withdrawl balance
* enable wallet 
* disable wallet
* feature (separate api for generate token)

============================

<h3>Package:</h3>

Django                        2.2.3
django-model-utils            4.1.1
djangorestframework           3.10.0 
djangorestframework-simplejwt 4.8.0
decorator                     5.0.9
decorator                     5.0.9
pytz                          2019.1

<h3>Setting Environment Project</h3>

    pip3 install -r requirements.txt
    ./manage.py migrate
    manage.py runserver
    manage.py migrate --run-syncdb
.. code-block:: bash


