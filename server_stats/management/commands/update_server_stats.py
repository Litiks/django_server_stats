from django.core.management.base import NoArgsCommand
from django.db import connection, transaction

from server_stats.models import QueryStat

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        #for details, see:  https://docs.djangoproject.com/en/dev/topics/db/sql/#executing-custom-sql-directly
        cursor = connection.cursor()
        cursor.execute("SHOW GLOBAL status like 'Queries'")
        text,nqueries = cursor.fetchone()
        print nqueries
        QueryStat(queries=nqueries).save()



