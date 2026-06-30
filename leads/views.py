from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse

from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.core.mail import send_mail
from .models import Category, Lead, Agent
from .forms import AssignAgentForm, CategoryModelForm, LeadCategoryUpdateForm, LeadForm, LeadModelForm, CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin # mixins has to come first so they get executed first
from agents.mixins import OrganizerAndLoginRequiredMixin
# Create your views here.
# all of these are function based views
# class based views would remove many repitions (all after function based views)
'''
all class based views can come from django.views.generic
all CRUD+L actions have class based views
'''

def landing_page(request):
    return render(request, "landing.html")

def lead_list(request):
    # return HttpResponse("Hello world")
    # return render(request, "leads/home_page.html") # in case we create a template folder inside our app
    # return render(request, "home_page.html") # in case we create a template folder in the base directory

    leads = Lead.objects.all()

    context  = {
        "leads": leads
    }

    return render(request, "leads/leads_list.html", context)

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, 'leads/lead_detail.html', context)

'''
def lead_create(request): # Form
    
    form = LeadForm() # instantiate it

    if request.method == "POST":
        form = LeadForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            
            agent = Agent.objects.first()

            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent
            )

            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)
'''

def lead_create(request): # ModelForm
    
    form = LeadModelForm() # instantiate it

    if request.method == "POST":
        # form = LeadForm()
        form = LeadModelForm(request.POST)

        if form.is_valid():
            form.save() # works only if we are working with forms.ModelForm
            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)

'''
def lead_update(request, pk): # Form
    lead = Lead.objects.get(id=pk)

    form = LeadForm() # instantiate it
    if request.method == "POST":
        form = LeadForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            
            lead.save()

            return redirect("/leads")

    context = {
        "lead": lead,
        "form": form
    }

    return render(request, "leads/lead_update.html", context)
'''

def lead_update(request, pk): # ModelForm
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)

    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect("/leads")

    context = {
        "lead": lead,
        "form": form
    }

    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

# class based views
class LandingPageView(TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/leads_list.html"
    # queryset = Lead.objects.all() # context now has object_list key
    context_object_name = "leads" # this updates context key 

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
                
            context.update({
                "unassigned_leads": queryset
            })
        return context
        

class LeadDetailView(OrganizerAndLoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    # queryset = Lead.objects.all() # context now has object_list key
    context_object_name = "lead" # this updates context key 


    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return resolve_url("leads:lead-list")
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

    
class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return resolve_url("leads:lead-list")


    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return resolve_url("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return resolve_url("login")

class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return resolve_url("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super().form_valid(form)


class CategoryCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm
    
    def get_success_url(self):
        return resolve_url("leads:category-list")


    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm
    
    def get_success_url(self):
        return resolve_url("leads:category-detail", pk=self.object.pk)

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset


class CategoryDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = "leads/category_delete.html"
    
    def get_success_url(self):
        return resolve_url("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)


        return queryset
    


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = 'category'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        leads = self.get_object().leads.all() # self.get_object().lead_set.all() # queryset = Lead.objects.filter(self.get_object())
        
        context.update({
            "leads": leads
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)


        return queryset
    
class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return resolve_url("leads:lead-detail", pk=self.object.pk)