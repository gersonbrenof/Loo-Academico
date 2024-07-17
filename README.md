# Projeto Django com Django Rest Framework

Este projeto é uma aplicação Django que utiliza Django Rest Framework para construir APIs.

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
# No Windows
python -m venv venv
venv\Scripts\activate

# No MacOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
