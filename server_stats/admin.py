from django.contrib import admin
from server_stats.models import *

class PageViewLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'ip', 'gen_time_in_seconds', 'datetime', 'status_code')
    list_filter = ('status_code','view_name')
    search_fields = ('user__username','url','ip')
    
admin.site.register(PageViewLog, PageViewLogAdmin)
admin.site.register(QueryStat)
admin.site.register(BenchmarkMilestone)
