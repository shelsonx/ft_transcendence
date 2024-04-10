from django.views.generic import TemplateView

class NotFoundView(TemplateView):
    template_name = "index.html"

    @classmethod
    def get_rendered_view(cls):
        as_view_fn = cls.as_view()

        def view_fn(request, exception):
            response = as_view_fn(request)
            # this is what was missing before
            response.render()
            return response

        return view_fn