from datetime import datetime
from django.db import models
from auth.models import User

class PageViewLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255, default='')
    view_name = models.CharField(max_length=255, default='')
    gen_time = models.BigIntegerField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    ip = models.CharField(max_length=20, default='')
    
    def __unicode__(self):
        return u'%s' % self.url
        
    def gen_time_in_seconds(self):
        return "%s seconds" % (self.gen_time / 1000000.0)
        
class QueryStat(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    queries = models.IntegerField()
    
class BenchmarkMilestone(models.Model):
    datetime = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=255, help_text="Briefly describe the change")
    
    def __unicode__(self):
        return self.name
        