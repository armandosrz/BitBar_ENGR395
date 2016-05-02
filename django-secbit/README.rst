=====
Secu
=====

Polls is a simple Django app to transfer currency and
create your own user profiles.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "secu" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'secu',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^secu/', include('secu.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
