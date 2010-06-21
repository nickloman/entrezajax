from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^examples/elink.html$', 'direct_to_template', {'template' : 'examples/elink.html'}),
    (r'^developer.html$', 'direct_to_template', {'template' : 'developer.html'}),
    (r'^faq.html$', 'direct_to_template', {'template' : 'faq.html'}),
    (r'^implementation.html$', 'direct_to_template', {'template' : 'implementation.html'}),
)

urlpatterns += patterns('',
    (r'^examples/esearch\+esummary.html$', 'infopages.example_views.example_with_term',
       {'template' : 'examples/esearch+esummary.html',
        'default' : 'Venter JC[Auth]'}
    ),
    (r'^examples/espell.html$', 'infopages.example_views.example_with_term',
       {'template' : 'examples/espell.html',
        'default' : 'brest cancar'}
    ),
    (r'^examples/efetch.html$', 'infopages.example_views.example_with_term',
       {'template' : 'examples/efetch.html',
        'default' : 'shigella toxin'}
    ),
    
    url(r'^espell$', 'json_endpoint.views.espell', name='espell'),
    url(r'^einfo$', 'json_endpoint.views.einfo', name='einfo'),
    url(r'^esearch$', 'json_endpoint.views.esearch', name='esearch'),
    url(r'^esummary$', 'json_endpoint.views.esummary', name='esummary'),
    url(r'^efetch$', 'json_endpoint.views.efetch', name='efetch'),
    url(r'^elink$', 'json_endpoint.views.elink', name='elink'),

    url(r'^esearch\+esummary$', 'json_endpoint.views.esearch_and_esummary', name='esearch_and_esummary'),
    url(r'^esearch\+efetch$', 'json_endpoint.views.esearch_and_efetch', name='esearch_and_efetch'),
    url(r'^esearch\+elink$', 'json_endpoint.views.esearch_and_elink', name='esearch_and_elink'),

    url(r'^elink\+esummary$', 'json_endpoint.views.elink_and_esummary', name='elink_and_esummary'),
    url(r'^elink\+efetch$', 'json_endpoint.views.elink_and_efetch', name='elink_and_efetch'),

    url(r'^register', 'devdb.views.register', name='register'),
    
    url(r'^status/memcache', 'infopages.views.memcache'),
    
    url(r'^$', 'infopages.views.frontpage', name='frontpage')
)
