from django.shortcuts import render
from django.views.generic import TemplateView


class MeView(TemplateView):
    template_name = "me.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
