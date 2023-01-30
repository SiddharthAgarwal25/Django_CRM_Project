from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent
from django.core.mail import send_mail
from .forms import LeadForm, LeadForms, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
# Create your views here.
def LeadLists(request):
    # return HttpResponse("Hello.")
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request, "leads/lead_list.html", context)

def LeadDetail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print("Lead = ", lead)
    context = {
        "lead" : lead
    }
    return render(request, "leads/detail.html", context)

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


def LeadCreate(request):
    form = LeadForms()
    if request.method == 'POST':
        print("Recieving Form data.")
        form = LeadForms(request.POST)
        if form.is_valid():
            # the following code can be replaced by "forms.save()" it does the same job because we have 
            # specified that in our model form.
            print("Here is the data = ",form.cleaned_data)
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']
            lead = Lead.objects.create(
                first_name=fname,
                last_name=lname,
                age=age,
                agent=agent
            )
            return redirect('/leads')
    context =  {
        "form" : form
    }

    return render(request, "leads/lead_create.html", context)


def Update_lead(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm()
    if request.method == 'POST':
        print("Recieving Form data.")
        form = LeadForm(request.POST)
        if form.is_valid():
            # the following code can be replaced by "forms.save()" it does the same job because we have 
            # specified that in our model form.
            print("Here is the data = ",form.cleaned_data)
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = fname
            lead.last_name = lname
            lead.age = age
            lead.save()
            return redirect('/leads')
    context = {
        "lead" : lead,
        "form" : form   
    }
    return render(request, 'leads/lead_update.html', context)

# Update function but less code with the help of django model forms functionality.
def Update_lead_model(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForms(instance=lead)
    if request.method == 'POST':
        form = LeadForms(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "lead" : lead,
        "form" : form   
    }
    return render(request, 'leads/lead_update.html', context)

def delete_lead(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


def landing_page(request):
    return render(request, template_name="landing.html")

# Class Based Views.
class LandingClassPage(TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin ,ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = "leads"

class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = 'leads/detail.html'
    queryset = Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(LoginRequiredMixin,CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadForms
    
    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        # Send email.
        send_mail(subject='A Lead has been created', message="Go on the site to see the new lead",
         from_email = "test@test.com", recipient_list =['test2@test.com'])
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadForms

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()
    def get_success_url(self):
        return reverse('leads:lead-list')

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse('login')