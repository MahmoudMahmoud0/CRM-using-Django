import random

from django.shortcuts import render, resolve_url

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AgentModelForm
from leads.models import Agent
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
    
class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return resolve_url("agents:agent-list")

    def form_valid(self, form):
        # agent = form.save(commit=False)
        # agent.organization = self.request.user.userprofile
        # agent.save()

        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        
        Agent.objects.create(user=user, organization=self.request.user.userprofile)

        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please login to start working",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)
    
class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
    
class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)

    def get_success_url(self):
        return resolve_url("agents:agent-detail", pk=self.object.pk)

class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
    
    def get_success_url(self):
        return resolve_url("agents:agent-list")