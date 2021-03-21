from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'applications/top_page.html'