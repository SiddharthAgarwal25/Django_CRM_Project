from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent, Category
from django.core.mail import send_mail
from .forms import LeadForm, CustomUserCreationForm, AssignAgentForm, LeadModelForm, LeadCategoryUpdateForm
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from agents.mixins import OraganiserAndLoginRequiredMixin
from datetime import datetime
# Create your views here.
# def LeadLists(request):
#     # return HttpResponse("Hello.")
#     leads = Lead.objects.all()
#     context = {
#         "leads" : leads
#     }
#     return render(request, "leads/lead_list.html", context)

# def LeadDetail(request, pk):
#     print(pk)
#     lead = Lead.objects.get(id=pk)
#     print("Lead = ", lead)
#     context = {
#         "lead" : lead
#     }
#     return render(request, "leads/detail.html", context)

# def LeadCreate(request):
#     form = LeadForm()
#     if request.method == 'POST':
#         print("Recieving Form data.")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("Here is the data = ",form.cleaned_data)
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead = Lead.objects.create(
#                 first_name=fname,
#                 last_name=lname,
#                 age=age,
#                 agent=agent
#             )
#             return redirect('/leads')
#     context =  {
#         "form" : form
#     }

#     return render(request, "leads/lead_create.html", context)


# def LeadCreate(request):
#     form = LeadForms()
#     if request.method == 'POST':
#         print("Recieving Form data.")
#         form = LeadForms(request.POST)
#         if form.is_valid():
#             # the following code can be replaced by "forms.save()" it does the same job because we have 
#             # specified that in our model form.
#             print("Here is the data = ",form.cleaned_data)
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']
#             lead = Lead.objects.create(
#                 first_name=fname,
#                 last_name=lname,
#                 age=age,
#                 agent=agent
#             )
#             return redirect('/leads')
#     context =  {
#         "form" : form
#     }

#     return render(request, "leads/lead_create.html", context)


# def Update_lead(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == 'POST':
#         print("Recieving Form data.")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             # the following code can be replaced by "forms.save()" it does the same job because we have 
#             # specified that in our model form.
#             print("Here is the data = ",form.cleaned_data)
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = fname
#             lead.last_name = lname
#             lead.age = age
#             lead.save()
#             return redirect('/leads')
#     context = {
#         "lead" : lead,
#         "form" : form   
#     }
#     return render(request, 'leads/lead_update.html', context)

# Update function but less code with the help of django model forms functionality.
# def Update_lead_model(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForms(instance=lead)
#     if request.method == 'POST':
#         form = LeadForms(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
#     context = {
#         "lead" : lead,
#         "form" : form   
#     }
#     return render(request, 'leads/lead_update.html', context)

# def delete_lead(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect('/leads')


def landing_page(request):
    return render(request, template_name="landing.html")

# Class Based Views.
class LandingClassPage(TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin ,ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = "leads"
    def get_queryset(self):
        user = self.request.user
    # the following code means that the agents of a particular organisation can only see the leads of that organisation. 
    # if a user is an agent then the following code will show the leads of that particular organisation.
        if user.is_organiser:
            # We are able to access their userprofile because we know they are an organiser.
            # All leads of a particular organisation.
            queryset = Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)
        else:
            # All leads assigned to a particular agent of that organisation.
            queryset = Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False )
            # Filter for the agent currently logged in.
            queryset = queryset.filter(agent__user=self.request.user) 

        return queryset
    
    def get_context_data(self, **kwargs):
        # calling predefined data and adding custom data.
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads" : queryset
            })    
        return context
class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = 'leads/detail.html'
    context_object_name = "lead"
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=self.request.user) 

        return queryset

class LeadCreateView(OraganiserAndLoginRequiredMixin,CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # Send email.
        send_mail(subject='A Lead has been created', message="Go on the site to see the new lead",
         from_email = "test@test.com", recipient_list =['test2@test.com'])
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OraganiserAndLoginRequiredMixin,UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadDeleteView(OraganiserAndLoginRequiredMixin,DeleteView):
    template_name = 'leads/lead_delete.html'
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset
    def get_success_url(self):
        return reverse('leads:lead-list')

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse('login')

class AssignAgentView(OraganiserAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        print(f"1st kwargs {kwargs}")
        kwargs.update({
            "request" : self.request
        })
        print(f"second kwarg - {kwargs} and request - {kwargs['request']}")
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(ragent__user=user)
        context.update({
            "unassigned_lead_count": Lead.objects.filter(category__isnull=True).count()
        })
        return context
        
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryDetailView(LoginRequiredMixin,DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryCreateView(CreateView):
    pass

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})
    



class CategoryDeleteView(DeleteView):
    pass
