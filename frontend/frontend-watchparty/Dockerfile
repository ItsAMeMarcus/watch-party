# Usa a imagem oficial do Node.js
FROM node:20-alpine

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY package*.json ./
RUN npm install

# Copia o resto do projeto
COPY . .

# 1. Faz o BUILD DE PRODUÇÃO (Gera a pasta 'dist')
RUN npm run build

# 2. Instala um servidor estático super leve globalmente
RUN npm install -g serve

# Expõe a porta 5173
EXPOSE 5173

# 3. Serve a pasta compilada (sem hot reload, consumindo quase 0 RAM)
CMD ["serve", "-s", "dist", "-l", "5173"]
