from datetime import datetime
from server_stats.models import PageViewLog

class PageViewLogMiddleware(object):
    def process_request(self, request):
        self.stime = datetime.now()
        self.view_name = ''
        return None
        
    def process_view(self, request, view_func, *args, **kwargs):
        self.view_name = view_func.__name__
        return None

    def process_response(self,request,response):
        if hasattr(self,'stime'):
            etime = datetime.now()
            gen_time = etime - self.stime
            gen_time = (gen_time.seconds*1000000) + gen_time.microseconds
        else:
            gen_time = None
            
        try:
            id = int(request.user.id)
        except:
            #we don't care about unauthed requests
            pass
        else:
            ip = request.META['REMOTE_ADDR']
            if request.META.get('HTTP_CF_CONNECTING_IP'):
                ip = request.META['HTTP_CF_CONNECTING_IP']
            try:
                pvl = PageViewLog(
                    user = request.user,
                    url = request.META.get('PATH_INFO'),
                    gen_time = gen_time,
                    view_name = getattr(self,'view_name',''),
                    status_code = response.status_code,
                    ip = ip,
                ).save()
            except:
                pass
        
        return response


