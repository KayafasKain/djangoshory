from django.shortcuts import render, redirect
from  passlib.hash import crypt16 as sha16
from django.http import HttpResponseRedirect
from .models import Link
from .utils import check_url_util as ch_url

def index(request):

    tops = Link.objects.all().order_by('-visited')[:5]
    return render(request, 'shortlink/index.html', {
        'tops': tops
    })

def make_short_link(request):
    if request.method == 'POST' and ch_url.is_valid_url(request.POST.get('fulllink')):
        try:
            link = Link.objects.get(basic_link=request.POST.get('fulllink'))
        except Link.DoesNotExist as e:
            link = Link(basic_link=request.POST.get('fulllink'))
            link.save()

        return redirect('/short/'+str(link.id))
    else:
        return render(request, 'shortlink/error.html', {
            'error': "link is incorrect"
        })

def get_short(request, pk):
    try:
        link = Link.objects.get(id=pk)
    except Link.DoesNotExist as e:
        print(e)

    return render(request, 'shortlink/get_short.html', {
        'link': link
    })

def follow_short(request, pk):
    try:
        link = Link.objects.get(id=pk)
        link.visited += 1
        link.save()
    except:
        return render(request, 'shortlink/error.html', {
            'error': "Short link is incorrect"
        })

    return HttpResponseRedirect(link.basic_link)

def not_found404():
    return render(request, 'shortlink/error.html', {
        'error': "Short link is incorrect"
    })