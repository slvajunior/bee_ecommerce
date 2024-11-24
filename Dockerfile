# Use uma imagem base do Python
FROM python:3.10-slim

# Instale as dependências do sistema para o mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*


# Copiar o script wait-for-it.sh para o contêiner
COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de dependências para o contêiner
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Defina a variável de ambiente para evitar que o Django faça migrações automaticamente no início
ENV PYTHONUNBUFFERED 1

# Exponha a porta em que o Django será executado
EXPOSE 8000

# Comando para rodar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
