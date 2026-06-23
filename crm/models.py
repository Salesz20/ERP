from django.db import models
from django.contrib.auth.models import User

# ==============================================================
# MULTI-EMPRESA (TENANT)
# ==============================================================

class ERPAccount(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome da Empresa Cliente")
    cnpj = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)

    modulo_crm_ativo = models.BooleanField(default=True)
    modulo_servicos_ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE, related_name='usuarios')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.account.name}"


# ==============================================================
# CRM
# ==============================================================

class Company(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    oportunidades = models.TextField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    telefones = models.TextField(blank=True, null=True)
    mapa = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    caracteristicas = models.TextField(blank=True, null=True)
    vendedor = models.CharField(max_length=200, blank=True, null=True)
    
    # MUDE O RELATED_NAME PARA 'crm_empresas_criadas' para não dar conflito
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="crm_empresas_criadas" 
    )

    data_registro = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CompanyAttachment(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.arquivo.name} - {self.company.name}"


class Contact(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        full_name = f"{self.name} {self.surname}" if self.surname else self.name
        return f"{full_name} - {self.company.name}"


class Opportunity(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="opportunities")
    contato = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="opportunities_by_contact", null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stage = models.CharField(
        max_length=50,
        choices=[
            ("prospect", "Prospect"),
            ("qualificacao", "Qualificação"),
            ("apresentacao", "Apresentação"),
            ("proposta", "Proposta"),
            ("negociacao", "Negociação"),
            ("conclusao", "Conclusão"),
        ],
        default="prospect"
    )
    solucao = models.CharField(max_length=50, null=True, blank=True)
    origem = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    motivo_conclusao = models.CharField(max_length=50, null=True, blank=True)
    ticket_numero = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.CharField(max_length=20, null=True, blank=True)
    email_enviado = models.CharField(max_length=10, null=True, blank=True)
    data_previsao = models.DateField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    outras_info = models.TextField(null=True, blank=True)
    envolvidos = models.TextField(null=True, blank=True)
    caracteristica = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"


class Task(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=255)
    due_date = models.DateField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Documento(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    anexo = models.FileField(upload_to='uploads/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# ==============================================================
# SERVIÇOS
# ==============================================================

class Cliente(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class OportunidadeServico(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cliente} - {self.servico}"


class ServicoRecorrente(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    dia_da_semana = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.cliente} - {self.dia_da_semana}"


class ServicoEmpresa(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=255)
    cnpj_cpf = models.CharField(max_length=20, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    ddd = models.CharField(max_length=5, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    nome_contato = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    consulta_credito = models.TextField(blank=True, null=True)
    telefones_email = models.TextField(blank=True, null=True)
    dados_bancarios = models.TextField(blank=True, null=True)
    inscricoes_cnae = models.TextField(blank=True, null=True)
    integracao = models.TextField(blank=True, null=True)
    faturamento_credito = models.TextField(blank=True, null=True)
    tags_selecionadas = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresas_criadas')
    alterado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresas_alteradas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)


class DetalhesServicos(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    descricao_resumida = models.CharField(max_length=255)
    codigo_servico = models.CharField(max_length=50, blank=True, null=True)
    tributacao = models.CharField(
        max_length=1,
        choices=[
            ("P", "Exportação de Serviços"),
            ("T", "Operação tributável / Tributado no município"),
            ("F", "Tributado fora do município"),
            ("V", "Tributado fora do município, Exigibilidade Suspensa"),
            ("N", "Tributado fora do município, Imune"),
            ("B", "Tributado fora do município, Isento"),
            ("X", "Tributado no município, Exigibilidade Suspensa"),
            ("M", "Tributado no município, Imune"),
            ("A", "Tributado no município, Isento"),
        ],
        blank=True,
        null=True
    )
    codigo_nbs = models.CharField(max_length=20, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    descricao_servico = models.TextField(blank=True, null=True)
    impostos_retencoes = models.TextField(blank=True, null=True)
    produtos_utilizados = models.TextField(blank=True, null=True)
    situacao = models.CharField(max_length=10, default="Ativo")
    criado_por = models.ForeignKey(User, related_name='servico_criado', on_delete=models.SET_NULL, null=True, blank=True)
    alterado_por = models.ForeignKey(User, related_name='servico_alterado', on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao_resumida
    
# ordem de serviços

class OrdemServico(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=255)
    funcionario = models.CharField(max_length=255)
    data_faturamento = models.DateField(null=True, blank=True)
    parcelas = models.CharField(max_length=50, blank=True)


    # Aba Produtos / Despesas / Email / Obs
    produtos = models.TextField(blank=True)
    despesas = models.TextField(blank=True)
    email = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    # Aba Informações
    categoria = models.CharField(max_length=100, blank=True)
    conta_corrente = models.CharField(max_length=100, blank=True)
    projeto = models.CharField(max_length=100, blank=True)
    origem = models.CharField(max_length=50, default="Manual")

    pedido_cliente = models.CharField(max_length=100, blank=True)
    contrato_venda = models.CharField(max_length=100, blank=True)
    contato = models.CharField(max_length=100, blank=True)
    cidade_prestacao = models.CharField(max_length=100, blank=True)

    dados_nf = models.TextField(blank=True)
    codigo_obra = models.CharField(max_length=50, blank=True)
    codigo_cei = models.CharField(max_length=50, blank=True)
    hora = models.CharField(max_length=50, blank=True)
    atividade = models.CharField(max_length=50, blank=True)

    encapsulamento = models.CharField(max_length=50, blank=True)
    data_servico = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=50, default="Aguardando faturamento")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    criado_em = models.DateTimeField(auto_now_add=True)
    numero_os = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_os:
            # Pega o maior número já existente e soma 1
            ultimo = OrdemServico.objects.aggregate(models.Max('numero_os'))['numero_os__max'] or 0
            self.numero_os = ultimo + 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"OS #{self.id} - {self.cliente}"


class OrdemServicoItem(models.Model):
    account = models.ForeignKey(ERPAccount, on_delete=models.CASCADE)
    ordem_servico = models.ForeignKey(
        OrdemServico,
        related_name="itens",
        on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=255)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.descricao
