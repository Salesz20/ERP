from django.contrib import admin
from .models import (
    ERPAccount, UserProfile, Company, CompanyAttachment, Contact, Opportunity, Task,
    Documento, Cliente, Servico, OportunidadeServico, ServicoRecorrente,
    ServicoEmpresa, DetalhesServicos,
    OrdemServico, OrdemServicoItem
    
)

# =====================================================
# ERPAccount + UserProfile Inline
# =====================================================
class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1  # Linhas em branco para adicionar novos usuários

@admin.register(ERPAccount)
class ERPAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'modulo_crm_ativo', 'modulo_servicos_ativo', 'active')
    list_filter = ('modulo_crm_ativo', 'modulo_servicos_ativo', 'active')
    search_fields = ('name', 'cnpj')
    inlines = [UserProfileInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'is_admin')
    list_filter = ('account',)
    search_fields = ('user__username', 'account__name')

# =====================================================
# CRM
# =====================================================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'vendedor', 'data_registro')
    search_fields = ('name', 'cnpj', 'vendedor')

@admin.register(CompanyAttachment)
class CompanyAttachmentAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'company', 'criado_em')
    search_fields = ('company__name', 'arquivo')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'role', 'email', 'phone', 'company')
    search_fields = ('name', 'surname', 'email', 'company__name')
    list_filter = ('company',)

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'contato', 'vendedor', 'stage', 'value', 'data_previsao')
    search_fields = ('title', 'company__name', 'contato__name', 'vendedor__username')
    list_filter = ('stage', 'status', 'origem', 'solucao')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'opportunity', 'due_date', 'done')
    search_fields = ('description', 'opportunity__title')
    list_filter = ('done',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)

# =====================================================
# SERVIÇOS
# =====================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf")
    search_fields = ("nome", "cpf")

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)

@admin.register(OportunidadeServico)
class OportunidadeServicoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "servico", "status")
    search_fields = ("cliente__nome", "servico__nome", "status")

@admin.register(ServicoRecorrente)
class ServicoRecorrenteAdmin(admin.ModelAdmin):
    list_display = ("cliente", "servico", "dia_da_semana")
    search_fields = ("cliente__nome", "servico__nome")

@admin.register(ServicoEmpresa)
class ServicoEmpresaAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "cnpj_cpf", "nome_fantasia", "telefone", "nome_contato")
    search_fields = ("razao_social", "cnpj_cpf", "nome_fantasia", "nome_contato")
    list_filter = ("cidade", "estado")

@admin.register(DetalhesServicos)
class DetalhesServicosAdmin(admin.ModelAdmin):
    list_display = ("descricao_resumida", "codigo_servico", "categoria", "preco_unitario", "situacao")
    search_fields = ("descricao_resumida", "codigo_servico", "categoria")
    list_filter = ("situacao", "tributacao")




class OrdemServicoItemInline(admin.TabularInline):
    model = OrdemServicoItem
    extra = 1
    fields = ('descricao', 'quantidade', 'preco_unitario', 'subtotal')

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'funcionario', 'status', 'total')
    inlines = [OrdemServicoItemInline]