# django-arena

Flexible forum application for django 1.5+

## Dependencies

[TODO: Add list of django apps required by arena]

## Quick start

1. Add "arena" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'arena',
    )

2. Include the arena URLconf in your project urls.py like this:

    url(r'^forum/', include('arena.urls')),

3. Run `python manage.py syncdb` to create the arena models. arena also have
   south migration files; so if you're using it, you can instead run
   `python manage.py migrate arena`to create the models.

4. Start the development server and visit admin panel to create forums (you'll
   need the Admin app enabled).

5. Visit /forums to create forum threads and participate in forums.

## License

django-arena is licensed under the terms of the Apache License, version 2.0.
For more information, see LICENSE file.