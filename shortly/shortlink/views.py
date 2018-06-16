from django.shortcuts import render, redirect
from .forms import CreateLinkModelForm
from django.http import HttpResponseRedirect
from .models import Link

def index(request):
    tops = Link.objects.all().order_by('-visited')[:5]
    return render(request, 'shortlink/index.html', {
        'tops': tops,
        'form': CreateLinkModelForm()
    })

def make_short_link(request):
    if request.method == 'POST':
        tops = Link.objects.all().order_by('-visited')[:5]
        form = CreateLinkModelForm(request.POST)
        if form.is_valid():
            try:
                link = Link.objects.get(basic_link=request.POST.get('fulllink'))
            except Link.DoesNotExist as e:
                link = form.save(commit=True)
                link.save()

            return redirect('/short/'+str(link.pk))
    return render(request, 'shortlink/index.html', {
        'form': form,
        'tops': tops
    })


def get_short(request, pk):
    try:
        link = Link.objects.get(pk=pk)
    except Link.DoesNotExist as e:
        print(e)

    return render(request, 'shortlink/get_short.html', {
        'link': link
    })

def follow_short(request, pk):
    try:
        link = Link.objects.get(pk=pk)
        link.visited += 1
        link.save()
    except:
        return render(request, 'shortlink/error.html', {
            'error': "Short link is incorrect"
        })

    return HttpResponseRedirect(link.basic_link)
