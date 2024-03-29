# Django
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.loader import get_template

# Third Party
from vanilla import CreateView, DetailView, GenericModelView, ListView

# First Party
from gardens.models import Garden

# Locals
from .models import HomePageHeader, HomePagePod, ModuleList, Page

#
# def error404(request):
#    response = render_to_response('pages/404.html', {},
#                                  context_instance=RequestContext(request))
#


class DetailFormView(GenericModelView):
    success_url = None
    template_name_suffix = "_form"
    base_message = "Thank you for your submission"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = None
        success_message = None

        if "success" in self.kwargs:
            success_message = self.object.success_message or self.base_message
        else:
            form = self.get_form()

        context = self.get_context_data(form=form, success_message=success_message)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()

        template = get_template("pages/email-submission.html")
        context = {
            "name": self.object.name,
            "email": self.object.email,
            "phone": self.object.phone,
            "enquiry": self.object.enquiry,
        }
        content = template.render(context)

        email = EmailMessage(
            "New contact form submission",
            content,
            "contact@rhgdesign.co.uk",
            ["rhgd@outlook.com"],
            headers={"Reply-To": self.object.email},
        )
        email.send()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_form_class(self):
        object = self.get_object()
        if object.form:
            self.form_class = object.getFormClass()

        return self.form_class

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        try:
            return cls(data=data, files=files, **kwargs)
        except BaseException:
            return None

    def get_success_url(self):
        object = self.get_object()

        return object.success_url


class PageView(DetailFormView):
    model = Page
    template_name = "pages/index.html"
    lookup_field = "slug"
    form_class = None


class HomePage(ListView):
    model = Page
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context["page"] = Page.objects.get(is_home_page=True)
        context["header_image"] = HomePageHeader.getCurrentImage()
        context["pods"] = HomePagePod.objects.all()
        context["garden_list"] = Garden.objects.order_by("position")[:4]

        return context


class ContactView(CreateView):
    model = Page
    template_name = "pages/contact.html"


class ModuleListView(DetailView):
    model = ModuleList
    base_model = ModuleList
    lookup_field = "slug"
    template_name = "pages/modulelist.html"

    def get_context_data(self, **kwargs):
        view_string = self.object.module.split(".")

        view_class = __import__(view_string[0])
        for part in view_string[1:]:
            view_class = getattr(view_class, part)

        context = super(self.__class__, self).get_context_data(**self.kwargs)
        context["list_html"] = view_class.as_view()(self.request, **context).rendered_content

        return context
