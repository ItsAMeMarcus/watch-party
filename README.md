# 🍿 Sessão Pipoca - Watch Party App

🌍 **Live Demo:** [Clique aqui para acessar a aplicação rodando](https://watch-party-ochre.vercel.app)


Uma aplicação Fullstack em tempo real que permite aos usuários assistirem a vídeos do YouTube sincronizados, com suporte a chat ao vivo e arquitetura orientada a eventos.

Este projeto foi desenvolvido como um desafio técnico, focado em alta performance, comunicação bidirecional via WebSockets e conteinerização.

## 🚀 Funcionalidades

* **Sincronização Perfeita:** Qualquer ação de *Play*, *Pause* ou *Seek* no vídeo é refletida instantaneamente para todos os usuários da sala.
* **Resolução do "Late Joiner":** Se um usuário entrar na sala enquanto o vídeo já estiver rolando, o backend calcula o tempo transcorrido e sincroniza o novato magicamente.
* **Bate-Papo ao Vivo:** Chat integrado em tempo real sem a necessidade de recarregar a página ou fazer requisições HTTP (tudo flui pelo WebSocket).
* **Salas Dinâmicas e Compartilháveis:** Geração de links únicos de convite para facilitar o acesso.
* **Sem Login Friccional:** Entrada imediata baseada apenas em um *username* de sessão.
* **Contador de Espectadores:** Acompanhamento em tempo real de quantas pessoas estão ativas na sala.

## 🛠️ Tecnologias Utilizadas

**Frontend:**
* Vue.js 3 (Composition API)
* Vite (Build tool configurado para produção)
* Tailwind CSS (Estilização responsiva e moderna)
* YouTube IFrame Player API

**Backend:**
* Python 3.11
* FastAPI (Alta performance para APIs assíncronas)
* Uvicorn (Servidor ASGI)
* WebSockets (Túnel bidirecional de comunicação)

**Infraestrutura:**
* Docker & Docker Compose (Isolamento total de ambiente)

## 🐳 Como rodar o projeto localmente

O projeto está 100% dockerizado. Você não precisa ter Python ou Node.js instalados na sua máquina, apenas o **Docker** e o **Docker Compose**.

1. Clone o repositório:
```bash
git clone https://github.com/ItsAMeMarcus/watch-party.git

cd watch-party
```

2. Suba a infraestrutura completa (Frontend e Backend) com um único comando:

```bash

docker-compose up --build

```

3. Acesse a aplicação:

* **Frontend:** Abra http://localhost:5173 no seu navegador.

* **Backend:** Acesse http://localhost:8000/ no seu testador de API

  Nota de arquitetura: O container do frontend já está configurado para servir o build de produção (dist) utilizando um servidor estático super leve, garantindo zero vazamento de memória e alta performance.

## 🏗️ Arquitetura do WebSocket

O coração da aplicação é o ConnectionManager no backend, responsável por:

1. Armazenar o estado global de cada sala (Tempo atual + Status).

2. Fazer o broadcasting de mensagens de controle de mídia e texto.

3. Gerenciar o ciclo de vida da conexão, lidando graciosamente com quedas de usuários e atualizando a interface gráfica.
