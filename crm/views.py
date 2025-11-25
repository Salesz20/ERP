from django.shortcuts import render
from .models import Company, Contact, Opportunity, Task
from django.http import HttpResponse

def dashboard(request):
    companies = Company.objects.all()
    contacts = Contact.objects.all()
    opportunities = Opportunity.objects.all()
    tasks = Task.objects.all()
    return render(request, "crm/dashboard.html", {
        "companies": companies,
        "contacts": contacts,
        "opportunities": opportunities,
        "tasks": tasks,
    })



def crm_home(request):
    return HttpResponse("<h1>CRM - Configurações iniciais</h1>")

def company_list(request):
    return HttpResponse("<h2>Lista de Empresas</h2>")

def contact_list(request):
    return HttpResponse("<h2>Lista de Contatos</h2>")

def opportunity_list(request):
    return HttpResponse("<h2>Lista de Oportunidades</h2>")

def task_list(request):
    return HttpResponse("<h2>Lista de Tarefas</h2>")
