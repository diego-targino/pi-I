# API - Projeto Backend

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-REST-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## Sobre o Projeto

API backend desenvolvida com **Django + Django REST Framework**, seguindo uma arquitetura organizada em camadas:

* Controllers (Views)
* Services (Regras de negócio)
* Repositories (Acesso a dados)
* Core (Infraestrutura compartilhada + IA)

---

## Estrutura do Projeto

```
API/
│
├── config/                # Configurações principais do Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                  # Código compartilhado
│   ├── ai/                # Integração com IA
│   └── database/
│       └── base_repository.py  # repository genérico com funções basicas
│
├── users/                 # Módulo de usuários
│   ├── models.py          # Classes que representam tabelas no banco de dados
│   ├── repositories.py    # classe de repository
│   ├── services.py        # classe com a lógica dos endpoints
│   ├── serializers.py     # configura mapeamento, validações entre outros
│   ├── views.py           # 'controllers' definem os endpoints
│   ├── urls.py
│   └── migrations/
├── .env                   # Variáveis de ambiente (ignorado)
├── .env.example           # Exemplo de configuração
├── manage.py
├── requirements.txt
└── README.md
```

---

## Arquitetura

```
Request → View → Service → Repository → Database
                        ↓
                      Core (IA / Utils)
```

---

## Configuração do Ambiente

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente

**Windows:**

```bash
venv\Scripts\activate
```

---

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DB_NAME=pi-I
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_PORT=5432
DB_SSL=require
```

---

## Configuração do Banco (Django)

No `config/settings.py`:

```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'sslmode': config('DB_SSL', default='require'),
        }
    }
}
```

---

## Banco de Dados

### Aplicar migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Criar Superusuário

```bash
python manage.py createsuperuser
```

Acessar:

```
http://127.0.0.1:8000/admin/
```

---

## Executar o Projeto

```bash
python manage.py runserver
```

API disponível em:

```
http://127.0.0.1:8000/
```

---

## Endpoints

| Método | Rota                 | Descrição         |
| ------ | -------------------- | ----------------- |
| GET    | `/api/users/`        | Listar usuários   |
| POST   | `/api/users/`        | Criar usuário     |

---

## Boas Práticas

* ❌ Nunca subir `.env`
* ✅ Usar `.env.example`
* ✅ Rodar `migrate` após alterar models
* ❌ Não colocar lógica na View
* ✅ Services controlam regras
* ✅ Repositories acessam dados

---

## Observações

* Django já gerencia conexão com banco automaticamente
* O `core` centraliza reutilização (IA, base repository)
* Cada módulo é independente

---

## Dependências principais

```txt
Django
djangorestframework
psycopg2-binary
python-decouple
```
