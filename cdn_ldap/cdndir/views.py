# -*- coding: utf-8 -*-


from django.views.generic.base import TemplateView


class PageFotFound(TemplateView):

    template_name = "error/404.html"

    def get(self, request, *args, **kwargs):
        return super(PageFotFound, self).get(**kwargs)


class PageError(TemplateView):
    template_name = "error/500.html"

    def get(self, request, *args, **kwargs):
        return super(PageError, self).get(**kwargs)


class PermissionDenied(TemplateView):
    template_name = "error/403.html"

    def get(self, request, *args, **kwargs):
        return super(PermissionDenied, self).get(**kwargs)