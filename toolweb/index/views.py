from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context.update({
            "li": [x for x in range(10)]
        })
        return context