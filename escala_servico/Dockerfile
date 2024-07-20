# Use uma imagem base oficial do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo do diretório atual para o diretório de trabalho no container
COPY . .

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
