from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from crm.models import Company, CompanyAttachment, Contact, Opportunity, Task
from django.contrib.auth.models import User

from decimal import Decimal, InvalidOperation
from datetime import datetime, date, timedelta
import datetime as dt_module
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
import logging
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# ------------------------------
# CRM HOME
# ------------------------------
@login_required
def crm_home(request):
    if request.method == 'POST':
        escolha = request.POST.get('escolha')
        caminhos = {
            'contas': 'escolha:contas',
            'contatos': 'escolha:contatos',
            'oportunidades': 'escolha:oportunidades',
            'tarefas': 'escolha:tarefas',
        }
        return redirect(caminhos.get(escolha, 'escolha:contas'))
    return render(request, 'crm/crm.html')


# ------------------------------
# PÁGINAS GERAIS
# ------------------------------
@login_required
def vendas_home(request):
    return render(request, 'crm/vendas.html')

@login_required
def servicos_home(request):
    return render(request, 'crm/servicos.html')

@login_required
def compras_home(request):
    return render(request, 'crm/compras.html')

@login_required
def financas_home(request):
    return render(request, 'crm/financas.html')

@login_required
def contador_home(request):
    return render(request, 'crm/contador.html')


# ------------------------------
# LISTAGENS / OPÇÕES DO CRM
# ------------------------------
@login_required
def contas(request):
    user_account = request.user.perfil.account
    query = request.GET.get('q', '')
    # Filtra por account
    if query:
        empresas = Company.objects.filter(account=user_account, name__icontains=query).order_by('name')
    else:
        empresas = Company.objects.filter(account=user_account).order_by('name')
        
    paginator = Paginator(empresas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'crm/crm_opcoes/contas.html', {'contas': page_obj, 'query': query})

@login_required
def contatos(request):
    user_account = request.user.perfil.account
    query = request.GET.get('q', '')
    
    # Filtra por account
    contatos_qs = Contact.objects.filter(account=user_account)
    if query:
        contatos_qs = contatos_qs.filter(name__icontains=query).order_by('name')
    else:
        contatos_qs = contatos_qs.order_by('name')
        
    empresas = Company.objects.filter(account=user_account).order_by('name')
    paginator = Paginator(contatos_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    erro = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        sobrenome = request.POST.get('sobrenome', '').strip()
        email = request.POST.get('email', '').strip()
        cargo = request.POST.get('cargo', '').strip()
        empresa_nome = request.POST.get('empresa', '').strip()

        if nome and empresa_nome:
            try:
                # Garante que só busca empresa da própria conta
                empresa = Company.objects.get(account=user_account, name=empresa_nome)
            except Company.DoesNotExist:
                erro = f"A empresa '{empresa_nome}' não existe. Cadastre-a em Contas primeiro."
            else:
                nome_completo = f"{nome} {sobrenome}".strip()
                if Contact.objects.filter(account=user_account, name__iexact=nome_completo, company=empresa).exists():
                    erro = "Esse contato já existe nessa empresa!"
                else:
                    Contact.objects.create(
                        account=user_account, 
                        company=empresa, 
                        name=nome_completo, 
                        email=email or None, 
                        role=cargo or None
                    )
                    return redirect('escolha:contatos')
        else:
            erro = "Preencha os campos obrigatórios."

    return render(request, 'crm/crm_opcoes/contatos.html', {
        'contatos': page_obj,
        'query': query,
        'erro': erro,
        'empresas': empresas,
    })


@login_required
def oportunidades(request):
    return redirect('escolha:oportunidades_kanban')


@login_required
def tarefas(request):
    user_account = request.user.perfil.account
    tarefas = Task.objects.filter(account=user_account).order_by('-due_date')
    paginator = Paginator(tarefas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'crm/crm_opcoes/tarefas.html', {'tarefas': page_obj})


# ------------------------------
# DETALHES / CADASTRO DE EMPRESA
# ------------------------------
@login_required
def detalhes_empresa(request, empresa_id):
    user_account = request.user.perfil.account
    erro = None
    
    if empresa_id == 0:
        if request.method == 'POST':
            nome = request.POST.get('nome', '').strip()
            cnpj = request.POST.get('cnpj', '').strip()
            oportunidades_txt = request.POST.get('oportunidades', '').strip()
            endereco = request.POST.get('endereco', '').strip()
            telefones = request.POST.get('telefones', '').strip()
            mapa = request.POST.get('mapa', '').strip()
            info = request.POST.get('info', '').strip()
            caracteristicas = request.POST.get('caracteristicas', '').strip()
            vendedor = request.POST.get('vendedor', '').strip() # <--- Pegando o vendedor do POST

            if not nome:
                erro = "O nome da empresa é obrigatório."
            elif Company.objects.filter(account=user_account, name__iexact=nome).exists():
                erro = "Essa empresa já existe!"
            else:
                # Criando a empresa com TODOS os campos
                empresa = Company.objects.create(
                    account=user_account,
                    name=nome,
                    cnpj=cnpj,
                    oportunidades=oportunidades_txt,
                    endereco=endereco,
                    telefones=telefones,
                    mapa=mapa,
                    info=info,
                    caracteristicas=caracteristicas,
                    vendedor=vendedor,      # <--- Salvando o vendedor
                    criado_por=request.user # <--- Salvando quem criou (Rogério)
                )

                arquivos = request.FILES.getlist('anexo')
                for arquivo in arquivos:
                    CompanyAttachment.objects.create(account=user_account, company=empresa, arquivo=arquivo)

                return redirect('escolha:detalhes_empresa', empresa_id=empresa.id)

        return render(request, 'crm/crm_opcoes/detalhes_empresa.html', {'nova_empresa': True, 'erro': erro, 'anexos': []})

    else:
        # Modo Edição
        empresa = get_object_or_404(Company, id=empresa_id, account=user_account)
        contatos = empresa.contacts.all()
        anexos = empresa.anexos.all()

        if request.method == 'POST':
            empresa.name = request.POST.get('nome', empresa.name)
            empresa.cnpj = request.POST.get('cnpj', empresa.cnpj)
            empresa.oportunidades = request.POST.get('oportunidades', empresa.oportunidades)
            empresa.endereco = request.POST.get('endereco', empresa.endereco)
            empresa.telefones = request.POST.get('telefones', empresa.telefones)
            empresa.mapa = request.POST.get('mapa', empresa.mapa)
            empresa.info = request.POST.get('info', empresa.info)
            empresa.caracteristicas = request.POST.get('caracteristicas', empresa.caracteristicas)
            empresa.vendedor = request.POST.get('vendedor', empresa.vendedor) # <--- Atualizando o vendedor
            empresa.save()

            arquivos = request.FILES.getlist('anexo')
            for arquivo in arquivos:
                CompanyAttachment.objects.create(account=user_account, company=empresa, arquivo=arquivo)

            return redirect('escolha:detalhes_empresa', empresa_id=empresa.id)

        return render(request, 'crm/crm_opcoes/detalhes_empresa.html', {
            'empresa': empresa,
            'contatos': contatos,
            'anexos': anexos,
            'nova_empresa': False
        })

@login_required
def lista_contatos(request):
    user_account = request.user.perfil.account
    query = request.GET.get('q', '')

    contatos_list = Contact.objects.filter(account=user_account).select_related('company').order_by('name')

    if query:
        contatos_list = contatos_list.filter(name__icontains=query)

    paginator = Paginator(contatos_list, 50)
    page = request.GET.get('page')
    contatos_obj = paginator.get_page(page)

    return render(request, 'contatos.html', {
        'contatos': contatos_obj,
        'query': query,
    })

# ------------------------------
# DETALHES / CADASTRO DE CONTATO
# ------------------------------
@login_required
def detalhes_contato(request, contato_id=None):
    user_account = request.user.perfil.account
    empresas = Company.objects.filter(account=user_account).order_by('name')
    erro = None
    contato = None
    novo_contato = False

    if contato_id and contato_id != 0:
        contato = get_object_or_404(Contact, id=contato_id, account=user_account)
    else:
        novo_contato = True
        contato = Contact(id=0, name='', email='', role='', company=None)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        sobrenome = request.POST.get('sobrenome', '').strip()
        email = request.POST.get('email', '').strip()
        cargo = request.POST.get('cargo', '').strip()
        empresa_nome = request.POST.get('empresa', '').strip()

        if nome and empresa_nome:
            try:
                empresa = Company.objects.get(account=user_account, name=empresa_nome)
            except Company.DoesNotExist:
                erro = f"A empresa '{empresa_nome}' não existe. Cadastre-a em Contas primeiro."
            else:
                nome_completo = f"{nome} {sobrenome}".strip()
                if contato_id and contato_id != 0:
                    contato.name = nome_completo
                    contato.email = email or None
                    contato.role = cargo or None
                    contato.company = empresa
                    contato.save()
                    return redirect('escolha:detalhes_contato', contato_id=contato.id)
                else:
                    if Contact.objects.filter(account=user_account, name__iexact=nome_completo, company=empresa).exists():
                        erro = "Esse contato já existe nessa empresa!"
                    else:
                        contato = Contact.objects.create(
                            account=user_account,
                            name=nome_completo,
                            email=email or None,
                            role=cargo or None,
                            company=empresa
                        )
                        return redirect('escolha:detalhes_contato', contato_id=contato.id)
        else:
            erro = "Preencha os campos obrigatórios."

    return render(request, 'crm/crm_opcoes/detalhes_contato.html', {
        'contato': contato,
        'empresas': empresas,
        'erro': erro,
        'novo_contato': novo_contato,
        'contato_id': contato.id if contato and contato.id != 0 else None,
    })


# ------------------------------
# DETALHES / CADASTRO DE OPORTUNIDADE
# ------------------------------
@login_required
def detalhes_oportunidade(request, contato_id=None, oportunidade_id=None):
    user_account = request.user.perfil.account
    contato = None
    if contato_id:
        contato = get_object_or_404(Contact, id=contato_id, account=user_account)

    empresas = Company.objects.filter(account=user_account).order_by('name')
    erro = None
    oportunidade = None
    novo = False

    if oportunidade_id:
        oportunidade = get_object_or_404(Opportunity, id=oportunidade_id, account=user_account)
    elif contato:
        oportunidade = Opportunity.objects.filter(account=user_account, contato=contato).last()
        if not oportunidade:
            oportunidade = Opportunity.objects.create(
                account=user_account,
                contato=contato,
                company=contato.company,
                vendedor=request.user,
                title="Nova Oportunidade",
                stage='prospect'
            )
            novo = True

    if request.method == 'POST' and oportunidade:
        nome = request.POST.get('nome', '').strip()
        stage = request.POST.get('stage', 'prospect')
        status = request.POST.get('status', 'Ativo')
        motivo_conclusao = request.POST.get('motivo_conclusao', '')
        ticket_numero = request.POST.get('ticket_numero', '')
        value_raw = request.POST.get('value', '').strip()
        data_previsao_raw = request.POST.get('data_previsao', '').strip()
        solucao = request.POST.get('solucao', '').strip()
        origem = request.POST.get('origem', '').strip()
        temperatura = request.POST.get('temperatura', '').strip()
        email_enviado = request.POST.get('email_enviado', '').strip()
        observacoes = request.POST.get('observacoes', '').strip()
        outras_info = request.POST.get('outras_info', '').strip()
        envolvidos = request.POST.get('envolvidos', '').strip()
        caracteristica = request.POST.get('caracteristica', '').strip()

        value = None
        if value_raw:
            try:
                value = Decimal(value_raw.replace(',', '.'))
            except InvalidOperation:
                erro = "Valor inválido."

        data_previsao = None
        if data_previsao_raw:
            try:
                data_previsao = datetime.strptime(data_previsao_raw, '%Y-%m-%d').date()
            except ValueError:
                erro = "Data inválida."

        if not erro:
            oportunidade.title = nome
            oportunidade.stage = stage
            oportunidade.status = status
            oportunidade.motivo_conclusao = motivo_conclusao
            oportunidade.ticket_numero = ticket_numero
            oportunidade.value = value
            oportunidade.data_previsao = data_previsao
            oportunidade.solucao = solucao
            oportunidade.origem = origem
            oportunidade.temperatura = temperatura
            oportunidade.email_enviado = email_enviado
            oportunidade.observacoes = observacoes
            oportunidade.outras_info = outras_info
            oportunidade.envolvidos = envolvidos
            oportunidade.caracteristica = caracteristica
            oportunidade.vendedor = request.user
            if contato:
                oportunidade.contato = contato
                oportunidade.company = contato.company
            oportunidade.save()

            return redirect('escolha:detalhes_oportunidade', contato_id=contato.id if contato else 0, oportunidade_id=oportunidade.id)

    return render(request, 'crm/crm_opcoes/detalhes_oportunidade.html', {
        'oportunidade': oportunidade,
        'erro': erro,
        'empresas': empresas,
    })


# -----------------------------
# Kanban Oportunidades
# -----------------------------
@login_required
def oportunidades_view(request):
    user_account = request.user.perfil.account
    stages = ['prospect', 'qualificacao', 'apresentacao', 'proposta', 'negociacao', 'conclusao']
    oportunidades_por_stage = {}
    for stage in stages:
        oportunidades_por_stage[stage] = Opportunity.objects.filter(account=user_account, stage__iexact=stage).order_by('-id')
    return render(request, 'crm/crm_opcoes/oportunidades.html', {
        'oportunidades': oportunidades_por_stage,
        'stages': stages,
    })


@csrf_exempt
@login_required
def update_oportunidade_stage(request):
    user_account = request.user.perfil.account
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            opp_id = data.get("id")
            new_stage = data.get("stage")

            # Filtra por ID e Account para segurança
            oportunidade = Opportunity.objects.get(id=opp_id, account=user_account)
            oportunidade.stage = new_stage
            oportunidade.save()

            return JsonResponse({"status": "ok", "id": opp_id, "stage": new_stage})
        except Opportunity.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Oportunidade não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Método inválido"}, status=400)


# ------------------------------
# TAREFAS AJAX
# ------------------------------
@login_required
def create_task(request):
    user_account = request.user.perfil.account
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            desc = data.get('description')
            due_date = data.get('due_date')
            opportunity_id = data.get('opportunity_id')

            opportunity = Opportunity.objects.get(id=opportunity_id, account=user_account)

            task = Task.objects.create(
                account=user_account,
                description=desc,
                due_date=due_date,
                opportunity=opportunity
            )

            return JsonResponse({'message': 'Tarefa criada com sucesso!', 'task_id': task.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required
def list_tasks_by_opportunity(request):
    user_account = request.user.perfil.account
    try:
        opportunity_id = request.GET.get('opportunity_id')
        tasks = Task.objects.filter(
            account=user_account,
            opportunity_id=opportunity_id
        ).values('id', 'description', 'due_date', 'done')

        return JsonResponse({'tasks': list(tasks)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def mark_task_done(request):
    user_account = request.user.perfil.account
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id, account=user_account)
            task.done = True
            task.save()
            return JsonResponse({'message': 'Tarefa concluída!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required
def popup_tarefas(request, pk):
    user_account = request.user.perfil.account
    oportunidade = get_object_or_404(Opportunity, id=pk, account=user_account)
    hoje = timezone.now().date()

    tarefas_qs = Task.objects.filter(account=user_account, opportunity=oportunidade)
    tarefas_concluidas = tarefas_qs.filter(done=True)
    tarefas_atrasadas = tarefas_qs.filter(done=False, due_date__lt=hoje)
    tarefas_execucao = tarefas_qs.filter(done=False, due_date__gte=hoje)

    return render(request, "crm/crm_opcoes/tarefas_popup.html", {
        "tarefas_concluidas": tarefas_concluidas,
        "tarefas_atrasadas": tarefas_atrasadas,
        "tarefas_execucao": tarefas_execucao,
        "oportunidade": oportunidade,
    })


@login_required
def update_task(request):
    user_account = request.user.perfil.account
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        description = data.get('description', '').strip()
        due_date_raw = data.get('due_date', '').strip()

        task = Task.objects.get(id=task_id, account=user_account)

        if description:
            task.description = description
        if due_date_raw:
            try:
                dd = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
                task.due_date = dd
            except Exception:
                return JsonResponse({'error': 'Formato de data inválido'}, status=400)

        task.save()
        return JsonResponse({
            'status': 'ok',
            'task': {'id': task.id, 'description': task.description, 'due_date': task.due_date.isoformat(), 'done': task.done}
        })
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def delete_task(request):
    user_account = request.user.perfil.account
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        task = Task.objects.get(id=task_id, account=user_account)
        task.delete()
        return JsonResponse({'status': 'ok', 'message': 'Tarefa removida'})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def move_task(request):
    user_account = request.user.perfil.account
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
        column = data.get('column')
        task = Task.objects.get(id=task_id, account=user_account)

        hoje = timezone.localdate()

        if column == 'concluidas':
            task.done = True
        elif column == 'execucao':
            task.done = False
            if task.due_date < hoje:
                task.due_date = hoje
        elif column == 'atrasadas':
            task.done = False
            if task.due_date >= hoje:
                task.due_date = hoje - timedelta(days=1)
        else:
            return JsonResponse({'error': 'Coluna inválida'}, status=400)

        task.save()
        return JsonResponse({'status': 'ok', 'task': {'id': task.id, 'done': task.done, 'due_date': task.due_date.isoformat()}})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def lista_tarefas(request):
    user_account = request.user.perfil.account
    hoje = timezone.now().date()
    tarefas_qs = Task.objects.filter(account=user_account).select_related('opportunity').order_by('due_date')

    tarefas_concluidas = [t for t in tarefas_qs if t.done]
    tarefas_execucao = [t for t in tarefas_qs if not t.done and t.due_date >= hoje]
    tarefas_atrasadas = [t for t in tarefas_qs if not t.done and t.due_date < hoje]

    return render(request, "crm/crm_opcoes/tarefas.html", {
        "tarefas_concluidas": tarefas_concluidas,
        "tarefas_execucao": tarefas_execucao,
        "tarefas_atrasadas": tarefas_atrasadas,
    })


@login_required
def tarefas_view(request):
    user_account = request.user.perfil.account
    hoje = timezone.now().date()
    tarefas_qs = Task.objects.filter(account=user_account)

    tarefas_execucao = tarefas_qs.filter(done=False, due_date__gte=hoje)
    tarefas_atrasadas = tarefas_qs.filter(done=False, due_date__lt=hoje)
    tarefas_concluidas = tarefas_qs.filter(done=True)

    return render(request, "crm/crm_opcoes/tarefas.html", {
        "tarefas_execucao": tarefas_execucao,
        "tarefas_atrasadas": tarefas_atrasadas,
        "tarefas_concluidas": tarefas_concluidas,
    })


# ------------------------------
# EXCLUSÕES
# ------------------------------
@login_required
def excluir_empresa(request, empresa_id):
    user_account = request.user.perfil.account
    empresa = get_object_or_404(Company, id=empresa_id, account=user_account)
    empresa.delete()
    return redirect('escolha:contas')

@login_required
def excluir_contato(request, contato_id):
    user_account = request.user.perfil.account
    contato = get_object_or_404(Contact, id=contato_id, account=user_account)
    contato.delete()
    return redirect('escolha:contatos')

@login_required
def excluir_oportunidade(request, oportunidade_id):
    user_account = request.user.perfil.account
    oportunidade = get_object_or_404(Opportunity, id=oportunidade_id, account=user_account)
    oportunidade.delete()
    return redirect('escolha:oportunidades')