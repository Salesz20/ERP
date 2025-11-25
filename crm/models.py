from django.db import models
from django.contrib.auth.models import User



# ------------------------------
# EMPRESA
# ------------------------------
class Company(models.Model):
    name = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    oportunidades = models.TextField(blank=True, null=True)      # Aba Oportunidades
    endereco = models.TextField(blank=True, null=True)           # Aba Endereço
    telefones = models.TextField(blank=True, null=True)          # Aba Telefones e E-mail
    mapa = models.TextField(blank=True, null=True)               # Aba Mapa
    info = models.TextField(blank=True, null=True)               # Aba Informações Adicionais
    caracteristicas = models.TextField(blank=True, null=True)    # Aba Características
    vendedor = models.CharField(max_length=200, blank=True, null=True)  # Vendedor responsável
    data_registro = models.DateField(auto_now_add=True)          # Data de registro
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ------------------------------
# ANEXOS DE EMPRESA
# ------------------------------
class CompanyAttachment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.arquivo.name} - {self.company.name}"

# ------------------------------
# CONTATOS
# ------------------------------
class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, blank=True, null=True)    # Sobrenome
    role = models.CharField(max_length=200, blank=True, null=True)       # Cargo
    email = models.EmailField(blank=True, null=True)                     # E-mail opcional
    phone = models.CharField(max_length=20, blank=True, null=True)       # Telefone opcional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        full_name = f"{self.name} {self.surname}" if self.surname else self.name
        return f"{full_name} - {self.company.name}"

# ------------------------------
# OPORTUNIDADES
# ------------------------------
class Opportunity(models.Model):

    # RELACIONAMENTOS
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="opportunities")
    contato = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="opportunities_by_contact", null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # CAMPOS PRINCIPAIS
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


    # DADOS DE TOPO
    solucao = models.CharField(max_length=50, null=True, blank=True)
    origem = models.CharField(max_length=50, null=True, blank=True)

    # DADOS DE FASES/STATUS/PREVISÃO
    status = models.CharField(max_length=50, null=True, blank=True)
    motivo_conclusao = models.CharField(max_length=50, null=True, blank=True)
    ticket_numero = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.CharField(max_length=20, null=True, blank=True)
    email_enviado = models.CharField(max_length=10, null=True, blank=True)
    data_previsao = models.DateField(null=True, blank=True)

    # CAMPOS DE TEXTO LONGO
    observacoes = models.TextField(null=True, blank=True)
    outras_info = models.TextField(null=True, blank=True)
    envolvidos = models.TextField(null=True, blank=True)
    caracteristica = models.TextField(null=True, blank=True)

    # DATAS DE CONTROLE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

# ------------------------------
# TAREFAS
# ------------------------------
class Task(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=255)
    due_date = models.DateField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.description

# ------------------------------
# DOCUMENTOS GENERICOS
# ------------------------------
class Documento(models.Model):
    nome = models.CharField(max_length=200)
    anexo = models.FileField(upload_to='uploads/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
