# python-web-homework
for Bionic university
by Petro Yermolenko

* 22I2016 - socket-based web-applications
* 26I2016 - Flask application, decorators, socket-based PseudoFlask
* 2II2016 - Library (SQLite), websockets chat (not ready yet :( )
* 5II2016 - ORM
  * (see https://docs.djangoproject.com/en/1.9/)
  * Pattern: Active-record
  * manage.py migrate - перетв. описів класів у БД
  * see also: DataMapper
  * https://docs.djangoproject.com/en/1.9/topics/db/models/
  * http://tutorial.djangogirls.org/uk/django_orm/index.html
  * Д/З: Flask, SQL-alchemy (повторити все це з ними)
<!--
  C:\Users\oper4\PycharmProjects\python-web-homework\5II2016\library>py -3 manage.
py makemigrations
No changes detected

C:\Users\oper4\PycharmProjects\python-web-homework\5II2016\library>py -3 manage.
py startapp library_app

C:\Users\oper4\PycharmProjects\python-web-homework\5II2016\library>py -3 manage.
py makemigrations
Migrations for 'library_app':
  0001_initial.py:
    - Create model Author
    - Create model Book
    - Create model BookAuthor

C:\Users\oper4\PycharmProjects\python-web-homework\5II2016\library>py -3 manage.
py migrate
Operations to perform:
  Apply all migrations: auth, admin, library_app, contenttypes, sessions
Running migrations:
  Rendering model states... DONE
  Applying library_app.0001_initial... OK
-->
* 12II2016 - WSGI