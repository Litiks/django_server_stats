from django.conf.urls.defaults import *

from server_stats.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='server_stats'),
    url(r'^(?P<num>\d+)/(?P<units>.+)/$', index, name='server_stats'),

    #benchmark
    url(r'^benchmark/$', benchmark, name='server_stats-benchmark'),
    url(r'^benchmark/(?P<num>\d+)/(?P<units>.+)/$', benchmark, name='server_stats-benchmark'),

    #edit_milestone
    url(r'^add_milestone/$', edit_milestone, name='server_stats-edit_milestone'),
    url(r'^edit_milestone/(?P<mid>.+)/$', edit_milestone, name='server_stats-edit_milestone'),
    
    #ux_chart
    url(r'^ux_chart/$', ux_chart, name='server_stats-ux_chart'),
    url(r'^ux_chart/(?P<num>\d+)/(?P<units>.+)/$', ux_chart, name='server_stats-ux_chart'),
    
    #initial_ux_chart
    url(r'^initial_ux_chart/$', initial_ux_chart, name='server_stats-initial_ux_chart'),
    url(r'^initial_ux_chart/(?P<num>\d+)/(?P<units>.+)/$', initial_ux_chart, name='server_stats-initial_ux_chart'),
)
