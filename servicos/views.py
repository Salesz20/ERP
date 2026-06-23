from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.db import transaction
from django.core.paginator import Paginator

from crm.models import (
    DetalhesServicos,
    ServicoEmpresa,
    OrdemServico,
    OrdemServicoItem
)

# ============================================================
# SERVIÇOS - MENU
# ============================================================

@login_required
def servicos_opcoes(request):
    return render(request, 'crm/servicos.html')


# ============================================================
# CADASTRAR / LISTAR SERVIÇOS
# ============================================================

@login_required
def cadastrar_servicos(request):
    account = request.user.perfil.account
    query = request.GET.get('q', '')

    if query:
        servicos = DetalhesServicos.objects.filter(
            account=account,
            descricao_resumida__icontains=query
        )
    else:
        servicos = DetalhesServicos.objects.filter(account=account)

    return render(request, "crm/servicos_opcoes/cadastrar_servicos.html", {
        "servicos": servicos,
        "query": query
    })


# ============================================================
# OPORTUNIDADE SERVIÇOS
# ============================================================




@login_required
def oportunidade_servicos(request):

    account = request.user.perfil.account

    ordens_qs = OrdemServico.objects.filter(
        account=account
    ).order_by("-id")

    paginator = Paginator(ordens_qs, 50)

    page_number = request.GET.get("page")

    ordens = paginator.get_page(page_number)

    return render(
        request,
        "crm/servicos_opcoes/oportunidade_servicos.html",
        {
            "ordens": ordens
        }
    )



# ============================================================
# SERVIÇOS RECORRENTES
# ============================================================

@login_required
def servicos_recorrentes(request):
    return render(request, 'crm/servicos_opcoes/servicos_recorrentes.html')


# ============================================================
# ADICIONAR ORDEM DE SERVIÇO
# ============================================================

from django.shortcuts import render, get_object_or_404, redirect
import json

@login_required
def adicionar_ordem_servico(request, os_id=None): # Adicionamos o os_id aqui
    account = request.user.perfil.account
    nome_fantasia = request.GET.get("nome_fantasia", "")
    os_criada = None

    # Tenta buscar a OS se o ID for passado (Modo Edição)
    if os_id:
        os_criada = get_object_or_404(OrdemServico, id=os_id, account=account)

    if request.method == "POST":  
        # Dicionário com os dados do formulário
        os_data = {
            "cliente": request.POST.get("in_cliente"),
            "funcionario": request.POST.get("in_funcionario"),
            "data_faturamento": request.POST.get("in_data") or None,
            "parcelas": request.POST.get("in_parcelas"),
            "produtos": request.POST.get("produtos"),
            "despesas": request.POST.get("despesas"),
            "email": request.POST.get("email"),
            "observacoes": request.POST.get("in_obs"),
            "categoria": request.POST.get("categoria"),
            "conta_corrente": request.POST.get("conta_corrente"),
            "projeto": request.POST.get("in_projeto"),
            "origem": request.POST.get("origem", "Manual"),
            "pedido_cliente": request.POST.get("in_pedido"),
            "contrato_venda": request.POST.get("contrato_venda"),
            "contato": request.POST.get("contato"),
            "cidade_prestacao": request.POST.get("cidade_prestacao"),
            "dados_nf": request.POST.get("dados_nf"),
            "codigo_obra": request.POST.get("codigo_obra"),
            "codigo_cei": request.POST.get("codigo_cei"),
            "encapsulamento": request.POST.get("encapsulamento"),
            "data_servico": request.POST.get("data_servico") or None,
            "hora": request.POST.get("hora"),
            "atividade": request.POST.get("atividade"),
        }

        if os_criada:
            # EDITAR OS EXISTENTE
            for attr, value in os_data.items():
                setattr(os_criada, attr, value)
            os_criada.save()
            # Opcional: Limpar itens antigos se for substituir por novos
            os_criada.itens.all().delete() 
        else:
            # CRIAR NOVA OS
            os_criada = OrdemServico.objects.create(account=account, **os_data)

        # Processar Itens
        itens = json.loads(request.POST.get("itens_servico", "[]"))
        total = 0
        for item in itens:
            subtotal = float(item["preco"]) * float(item["qtd"])
            total += subtotal
            OrdemServicoItem.objects.create(
                account=account,
                ordem_servico=os_criada,
                descricao=item["nome"],
                quantidade=item["qtd"],
                preco_unitario=item["preco"],
                subtotal=subtotal
            )

        os_criada.total = total
        os_criada.save()

        print("✅ OS PROCESSADA COM ID:", os_criada.id)
        
        # Redireciona para a mesma tela passando o ID (assim os dados permanecem)
        return redirect("editar_ordem_servicos", os_id=os_criada.id)

    # GET
    servicos = DetalhesServicos.objects.filter(account=account, situacao="Ativo")

# Buscamos todas as empresas para servir de Cliente e Funcionário
    lista_empresas = ServicoEmpresa.objects.filter(account=account).order_by('nome_fantasia')

    return render(request, "crm/servicos_opcoes/adicionar_os.html", {
        "servicos": servicos,
        "os": os_criada,
        "nome_fantasia": nome_fantasia,
        "clientes_lista": lista_empresas,     # Enviando para o HTML
        "funcionarios_lista": lista_empresas # Enviando para o HTML
    })


# ============================================================
# DETALHES SERVIÇOS (CRIAR / EDITAR)
# ============================================================

@login_required
def detalhes_servicos(request, servico_id=None):
    account = request.user.perfil.account

    servico = None
    if servico_id:
        servico = get_object_or_404(
            DetalhesServicos,
            id=servico_id,
            account=account
        )

    mensagem_sucesso = None

    if request.method == "POST":
        data = {
            "descricao_resumida": request.POST.get("descricao_resumida"),
            "codigo_servico": request.POST.get("codigo_servico"),
            "tributacao": request.POST.get("tributacao"),
            "codigo_nbs": request.POST.get("codigo_nbs"),
            "categoria": request.POST.get("categoria"),
            "preco_unitario": request.POST.get("preco_unitario") or None,
            "desconto": request.POST.get("desconto") or None,
            "descricao_servico": request.POST.get("descricao_servico"),
            "impostos_retencoes": request.POST.get("impostos_retencoes"),
            "produtos_utilizados": request.POST.get("produtos_utilizados"),
        }

        # EDITAR
        if servico:
            for k, v in data.items():
                setattr(servico, k, v)

            servico.alterado_por = request.user
            servico.save()
            mensagem_sucesso = "Serviço atualizado com sucesso!"

        # CRIAR
        else:
            servico = DetalhesServicos.objects.create(
                account=account,
                criado_por=request.user,
                alterado_por=request.user,
                **data
            )
            mensagem_sucesso = "Serviço criado com sucesso!"

    return render(request, "crm/servicos_opcoes/detalhes_servicos.html", {
        "servico": servico,
        "mensagem_sucesso": mensagem_sucesso
    })


# ============================================================
# DETALHES CLIENTES (CRIAR / EDITAR)
# ============================================================

@login_required
def detalhes_clientes(request, empresa_id=None):
    account = request.user.perfil.account

    empresa = None
    if empresa_id:
        empresa = get_object_or_404(
            ServicoEmpresa,
            id=empresa_id,
            account=account
            
        )

    if request.method == "POST":
        empresa_data = {

            "razao_social": request.POST.get("razao_social"),
            "cnpj_cpf": request.POST.get("cnpj_cpf"),
            "nome_fantasia": request.POST.get("nome_fantasia"),
            "ddd": request.POST.get("ddd"),
            "telefone": request.POST.get("telefone"),
            "nome_contato": request.POST.get("nome_contato"),
            "endereco": request.POST.get("endereco"),
            "cep": request.POST.get("cep"),
            "bairro": request.POST.get("bairro"),
            "cidade": request.POST.get("cidade"),
            "estado": request.POST.get("estado"),
            "pais": request.POST.get("pais"),
            "complemento": request.POST.get("complemento"),
            "consulta_credito": request.POST.get("consulta_credito"),
            "telefones_email": request.POST.get("telefones_email"),
            "dados_bancarios": request.POST.get("dados_bancarios"),
            "inscricoes_cnae": request.POST.get("inscricoes_cnae"),
            "integracao": request.POST.get("integracao"),
            "faturamento_credito": request.POST.get("faturamento_credito"),
            "tags_selecionadas": request.POST.get("tags_selecionadas"),
        }

        # EDITAR
        if empresa:
            for k, v in empresa_data.items():
                setattr(empresa, k, v)

            empresa.alterado_por = request.user
            empresa.save()

        # CRIAR
        else:
            empresa = ServicoEmpresa.objects.create(
                account=account,
                criado_por=request.user,
                alterado_por=request.user,
                **empresa_data
            )

        return redirect("escolha:clientes")

    return render(request, "crm/servicos_opcoes/detalhes_clientes.html", {
        "empresa": empresa
    })


# ============================================================
# LISTAGEM DE CLIENTES
# ============================================================

@login_required
def clientes(request):
    account = request.user.perfil.account
    query = request.GET.get('q', '')

    if query:
        clientes_list = ServicoEmpresa.objects.filter(
            account=account
        ).filter(
            Q(razao_social__icontains=query) |
            Q(nome_fantasia__icontains=query) |
            Q(cnpj_cpf__icontains=query)
        ).order_by('razao_social')
    else:
        clientes_list = ServicoEmpresa.objects.filter(
            account=account
        ).order_by('razao_social')

    return render(request, 'crm/servicos_opcoes/clientes.html', {
        'clientes': clientes_list,
        'query': query
    })

# excluir OSs
@login_required
def excluir_ordem_servico(request, os_id):

    user_account = request.user.perfil.account

    os = get_object_or_404(
        OrdemServico,
        id=os_id,
        account=user_account
    )

    os.delete()

    return redirect('oportunidade_servicos')
