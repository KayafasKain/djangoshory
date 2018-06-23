from django.shortcuts import render, redirect
from .forms import CreateLinkModelForm
from django.urls import reverse
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import FormView
from .models import Link

class MainPage(ListView):
    model = Link
    template_name = 'shortlink/index.html'
    context_object_name = 'main'
    form_class = CreateLinkModelForm

    def get_queryset(self):
        return self.model.objects.all().order_by('-visited')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

main = MainPage.as_view()

class FormHandle(FormView):
    model = Link
    context_object_name = 'link-create'
    template_name = 'shortlink/index.html'
    form_class = CreateLinkModelForm

    def get_success_url(self):
        return redirect('/short/' + str(link.pk))

    def form_valid(self, form):
        try:
            link = self.model.objects.get(basic_link=form.cleaned_data['basic_link'])
        except self.model.DoesNotExist as e:
            link = form.save()
        return redirect(reverse('link-detail', kwargs = { 'pk': str(link.pk)} ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all().order_by('-visited')[:5]
        return context

form_handle = FormHandle.as_view()

class ShortLinkDetail(DetailView):
    template_name = 'shortlink/get_short.html'
    model = Link

    #All these is already done by default, so my versino does not required
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

