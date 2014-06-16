from datetime import datetime, timedelta
import operator

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.db import models

from django.contrib.auth.decorators import login_required
from manage_structure.decorators import staff_required
from server_stats.models import *
from master.http import Http403
from server_stats.forms import BenchmarkMilestoneForm

@login_required
@staff_required
def index(request, num=None, units=None):
    user = request.user
    if num and units:
        kwargs = {
            units:int(num),
        }
        delta = timedelta(**kwargs)
    else:
        delta = timedelta(hours=24)
    yesterday = datetime.now() - delta
    
    #compile the top 10 pages, 
    pages = PageViewLog.objects.filter(datetime__gt=yesterday)
    #top 10 users
    top_pages = {}
    top_users = {}
    slowest_pages = {}
    users_with_errors = {}
    for page in pages:
        if not top_pages.has_key(page.url):
            top_pages[page.url] = 0
        top_pages[page.url] += 1
        
        t = page.gen_time / 1000000.0
        if not slowest_pages.has_key(page.url):
            slowest_pages[page.url] = t
        elif t > slowest_pages[page.url]:
            slowest_pages[page.url] = t
        
        if not top_users.has_key(page.user):
            top_users[page.user] = 0
        top_users[page.user] += 1
        
        if page.status_code == 500:
            if not users_with_errors.has_key(page.user):
                users_with_errors[page.user] = 0
            users_with_errors[page.user] += 1
        
    sorted_top_pages = sorted(top_pages.iteritems(), key=operator.itemgetter(1))
    sorted_top_users = sorted(top_users.iteritems(), key=operator.itemgetter(1))
    sorted_slowest_pages = sorted(slowest_pages.iteritems(), key=operator.itemgetter(1))
    sorted_users_with_errors = sorted(users_with_errors.iteritems(), key=operator.itemgetter(1))
    sorted_top_pages.reverse()
    sorted_top_users.reverse()
    sorted_slowest_pages.reverse()
    sorted_users_with_errors.reverse()
    
    context = {
        'yesterday':yesterday,
        'sorted_top_pages':sorted_top_pages[:10],
        'total_pages':len(sorted_top_pages),
        'sorted_top_users':sorted_top_users[:10],
        'total_users':len(sorted_top_users),
        'sorted_slowest_pages':sorted_slowest_pages[:10],
        'sorted_users_with_errors':sorted_users_with_errors,
    }
    return render_to_response( 'server_stats/index.html' , RequestContext(request, context))
    
@login_required
@staff_required
def benchmark(request, num=None, units=None):
    user = request.user
    if num and units:
        kwargs = {
            units:int(num),
        }
        delta = timedelta(**kwargs)
    else:
        delta = timedelta(hours=24)
    yesterday = datetime.now() - delta
    
    #compile stats 
    pages = PageViewLog.objects.filter(datetime__gt=yesterday)
    
    #find and tally unique views
    vs = PageViewLog.objects.all().values('view_name').distinct()
    views = []
    totals = []
    for v in vs:
        n = v['view_name']
        if not n:
            continue
        views.append({
            'name': n,
            'total': PageViewLog.objects.filter(view_name=n).count(),
            'milestones':[],
        })
        
    #group by milestone
    milestones = []
    ms = BenchmarkMilestone.objects.filter(datetime__gt=yesterday).order_by('datetime')
    prev_ms = BenchmarkMilestone.objects.filter(datetime__lte=yesterday).order_by('-datetime')
    if prev_ms:
        milestones.append(prev_ms[0])
    for m in ms:
        milestones.append(m)
        
    for i,m in enumerate(milestones):
        msvs = pages.filter(datetime__gt=m.datetime)
        try:
            next = milestones[i+1]
        except IndexError:
            pass
        else:
            msvs = msvs.filter(datetime__lt=next.datetime)
        score = 0
        total = 0
        page_total = 0
        for view in views:
            qs = msvs.filter(view_name=view['name'])
            page_count = qs.count()
            
            #find the average gen_time for this view, for this milestone
            vs = qs.aggregate(avg=models.Avg('gen_time'))
            avg = float(vs['avg'] or 0)
            avg = avg / 1000000.0
            
            if page_count:
                #find the median
                i = int(page_count * .5)
                log = qs.order_by('gen_time')[i]
                median = log.gen_time / 1000000.0
                
                #find the 90th percentile
                i = int(page_count * .9)
                log = qs.order_by('gen_time')[i]
                ninetieth = log.gen_time / 1000000.0
                
                #find the 95th percentile
                i = int(page_count * .95)
                log = qs.order_by('gen_time')[i]
                ninety_fifth = log.gen_time / 1000000.0
                
            else:
                median = None
                ninetieth = None
                ninety_fifth = None
            
            avg_change = None
            median_change = None
            ninetieth_change = None
            ninety_fifth_change = None
            if view['milestones']:
                last = view['milestones'][-1]
                last_avg = last['average'][0]
                if avg and last_avg:
                    avg_change = 100*((avg - last_avg)/last_avg)
                last_median = last['median'][0]
                if median and last_median:
                    median_change = 100*((median - last_median)/last_median)
                last_ninetieth = last['ninetieth'][0]
                if ninetieth and last_ninetieth:
                    ninetieth_change = 100*((ninetieth - last_ninetieth)/last_ninetieth)
                last_ninety_fifth = last['ninety_fifth'][0]
                if ninety_fifth and last_ninety_fifth:
                    ninety_fifth_change = 100*((ninety_fifth - last_ninety_fifth)/last_ninety_fifth)
                    
            view['milestones'].append({
                'average':(avg or None, avg_change, page_count),
                'median':(median or None, median_change, page_count),
                'ninetieth':(ninetieth or None, ninetieth_change, page_count),
                'ninety_fifth':(ninety_fifth or None, ninety_fifth_change, page_count),
            })
            score += avg * view['total']
            total += view['total']
            page_total += page_count
            
        #generate cumulative score
        #formula: cumulative score = ((group1.average_time * group1.num_global) + (...)) / total_global
        t = score/total
        change = None
        if totals:
            last = totals[-1][0]
            if last:
                change = 100*((t - last)/last)
        totals.append((t,change,page_total))

    context = {
        'yesterday':yesterday,
        'milestones':milestones,
        'views':views,
        'totals':totals,
    }
    return render_to_response( 'server_stats/benchmark.html' , RequestContext(request, context))
    
@login_required
@staff_required
def edit_milestone(request, mid=None):
    if mid:
        milestone = get_object_or_404(BenchmarkMilestone, pk=mid)
    else:
        milestone = BenchmarkMilestone()
        
    if request.POST:
        form = BenchmarkMilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('server_stats-benchmark'))
    else:
        form = BenchmarkMilestoneForm(instance=milestone)
    
    context = {
        'form':form,
    }
    return render_to_response( 'server_stats/edit_milestone.html' , RequestContext(request, context))
@login_required
@staff_required
def ux_chart(request, num=None, units=None):
    """ display a google motion chart to help review user experience over time """
    if num and units:
        kwargs = {
            units:int(num),
        }
        delta = timedelta(**kwargs)
    else:
        delta = timedelta(hours=24)
    yesterday = datetime.now() - delta
    resolution = 1
    if delta.total_seconds() > 1000:
        resolution = 60
    if delta.total_seconds()/60 > 1000:
        resolution = 3600
    if delta.total_seconds()/3600 > 1000:
        resolution = 86400
    
    #compile stats
    pages = PageViewLog.objects.filter(datetime__gt=yesterday)
    milestones = list(BenchmarkMilestone.objects.all().order_by('-datetime'))
    
    data = []
    for page in pages:
        milestone = None
        for m in milestones:
            if m.datetime < page.datetime:
                milestone = m
                break

        #determine timeline number
        #timeline number is a numerical indicator of time since start (based on the pre-determined resolution)
        d = page.datetime - yesterday
        timeline_number = int(d.total_seconds() / resolution)
        
        data.append({
            'user':page.user,
            'timeline':timeline_number,
            'datetime':page.datetime, #time (or time since registration)
            'url':page.url,
            'view_name':page.view_name,
            'gen_time':page.gen_time,
            'milestone':milestone,
        })
            
    context = {
        'yesterday':yesterday,
        'data':data,
    }
    return render_to_response( 'server_stats/ux_chart.html' , RequestContext(request, context))
    
@login_required
@staff_required
def initial_ux_chart(request, num=None, units=None):
    """ display a google motion chart to help review user experience over time """
    if num and units:
        kwargs = {
            units:int(num),
        }
        delta = timedelta(**kwargs)
    else:
        delta = timedelta(hours=24)
    yesterday = datetime.now() - delta
    #find users who registered within this timeframe
    users = User.objects.filter(date_joined__gte=yesterday)
    
    #compile stats
    milestones = list(BenchmarkMilestone.objects.all().order_by('-datetime'))
    
    data = {}
    for user in users:
        pages = PageViewLog.objects.filter(user = user).order_by('datetime')[:50]
        for i, page in enumerate(pages):
            milestone = None
            for m in milestones:
                if m.datetime < page.datetime:
                    milestone = m
                    break
                    
            if i not in data:
                data[i] = {}
            if page.view_name not in data[i]:
                data[i][page.view_name] = {
                    'view_name':page.view_name,
                    'timeline':i, #this is the i'th page loaded
                    'total_gen_time':0,
                    'average_gen_time':0,
                    'count':0,
                }
                
            data[i][page.view_name]['total_gen_time'] += page.gen_time
            data[i][page.view_name]['count'] += 1
            data[i][page.view_name]['average_gen_time'] = data[i][page.view_name]['total_gen_time'] / data[i][page.view_name]['count']
        
    for i, d in data.items():
        total_gen_time = 0
        count = 0
        for details in d.values():
            total_gen_time += details['total_gen_time']
            count += details['count']
        data[i]['all_views'] = {
            'view_name':'all_views',
            'timeline':i,
            'total_gen_time':total_gen_time,
            'average_gen_time': total_gen_time / count,
            'count':count,
        }
        
    new_data = []
    for d in data.values():
        for e in d.values():
            new_data.append(e)
            
    context = {
        'yesterday':yesterday,
        'data':new_data,
    }
    return render_to_response( 'server_stats/initial_ux_chart.html' , RequestContext(request, context))
    
#eof
