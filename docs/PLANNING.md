# avaliaca_mle_hotmart
Repositorio para desenvolvimento case mle hotmart

# Contexto

Na Hotmart, a principal capacidade que buscamos no prossional do futuro é a de **resolver desafios com protótipos que podem crescer e virar produtos incríveis.**

Seu desafioo será mostrar suas habilidades em aplicar tecnologias já existentes em uma tarefa que envolve **a criação de um protótipo de LLM com base em conhecimento.**

# Dois microsserviços:

1. O primeiro será responsável por **receber** um documento de texto extraído dessa página aqui, fazer seu processamento e o armazenar em um Vector Database;

2. O segundo será uma API que, **dado um texto de entrada no formato de pergunta**, busca nesse knowledge base qual(is) trecho(s) corresponde(m) a esse contexto, e usa isso como entrada para uma LLM gerar uma resposta.


# duvidas iniciais

## Extração de texto de uma pagina WEB

* Preciso me preocupar com o código que irá extrair o texto da pagina mencionada?

## Primeiro microsserviço

* Temos duas possibilidades para o primeiro microserviço, ele pode:
    * ser uma API que recebe um documento
    * ficar listening em uma pasta e processar qlqr documento que caia nessa pasta

R: Esperamos que as **duas APIs** e o VectorDB funcionem localmente via Docker compose;

# Escolha de tecnologias e frameworks

Entendendo a escolhas para esse projeto

## Backend API Framework

[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

FastAPI: fastAPI tem se mostrado como um dos melhores frameworks para backend python

Rapidez: compara-se com apis escritas em node e go

Suporte para operações assincronas: Modelos LLM, principalmente quando executados localmente, podem ter requisições demoradas e o suporte async é fundamental para nao haver bloqueio no servidor. Permitindo assim lidar com muitiplas requisições recorrentes de forma eficiente

Baseada em starlette e pydantic: altamente performatica para ASGI (Asynchronous Server Gateway Interface) e o Pydantic permite validação e parsing rapido de dados util ao lidar com dados estruturados.

## Vector DB

Dados são representados como vetores em um espaço dimensional.

Esses dados estão relacionados entre si. Embbedings de texto e imagem.

Estou bastante inclinado a escolher a lib em Rust, pois estou aprendendo aos poucos Rust. Então colocar essa DB na stack ira me incentivar ainda mais o uso e aprendizado em Rust.

Também estou praticando um pouco de Go, porém acho que Rust tem um diferencial em performance maior e tenho escutado um pessoal falar mal de GraphQL

Opções:

![alt text](image.png)


