django_server_stats
===================

A simple app that tracks page views along with some session data (user, view, gen_time, etc..) for later in-depth analysis.


Setup
-----

1.Within settings.py - Add the app to Installed Apps and Middleware::

    # within settings.py:
    INSTALLED_APPS += (
        'server_stats',
    )
    MIDDLEWARE_CLASSES = (
        # be sure to include this AFTER AccountMiddleware
        'server_stats.middleware.PageViewLogMiddleware',
        # and BEFORE other local middleware
    )

2.Sync/Migrate::

    `python manage.py syncdb`
    or
    `python manage.py migrate server_stats`
    
3.Within urls.py - Add a link to the server views (if desired)::

    urlpatterns += patterns('',
        (r'^server_stats/', include('server_stats.urls')),
    )
    

Usage
-----

Allow the site to gather activity, then view the logs within <yoursite>/admin/ or <yoursite>/server_stats/ (if applicable)
