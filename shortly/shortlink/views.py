from django.shortcuts import render, redirect,
from .forms import CreateLinkModelForm
from django.views.generic import ListView, DetailView, RedirectView
from .models import Link

class MainPage(ListView):
    model = Link
    template_name = 'shortlink/index.html'
    context_object_name = 'main'
    form_class = CreateLinkModelForm

    def post(self, request, *args, **kwargs):
        tops = self.model.objects.all().order_by('-visited')[:5]
        form = CreateLinkModelForm(request.POST)
        if form.is_valid():
            try:
                link = self.model.objects.get(basic_link=request.POST.get('basic_link'))
            except self.model.DoesNotExist as e:
                link = form.save(commit=True)
                link.save()

            return redirect('/short/' + str(link.pk))
        return render(request, 'shortlink/index.html', {
            'form': form,
            'tops': tops
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tops'] = self.model.objects.all().order_by('-visited')[:5]
        context['form'] = self.form_class
        return context

main = MainPage.as_view()

class ShortLinkDetail(DetailView):
    template_name = 'shortlink/get_short.html'
    model = Link

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs['pk'])
        try:
            context['link'] = self.model.objects.get(pk=self.kwargs['pk'])
        except self.model.DoesNotExist as e:
            print(e)

        return context

link_detail = ShortLinkDetail.as_view()


class FoolowShortRedirect(RedirectView):
    permanent = False
    query_string = True
    model = Link

    def get_redirect_url(self, *args, **kwargs):
        try:
            link = self.model.objects.get(pk=kwargs['pk'])
            link.visited += 1
            link.save()
        except:
            return render(self.request, 'shortlink/error.html', {
                'error': "Short link is incorrect"
            })

        return link.basic_link


follow_short = FoolowShortRedirect.as_view()

