
# Índice

- [Guia para teste rápido](#guia-para-teste-rápido)
- [Requisitos mínimos](#requisitos-mínimos)
  - [Requisitos mínimos para CPU](#requisitos-mínimos-para-cpu)
  - [Requisitos mínimos para GPU](#requisitos-mínimos-para-gpu)
- [Comandos para uso e teste do projeto](#comandos-para-uso-e-teste-do-projeto)
  - [Escolha do modelo LLM](#escolha-do-modelo-llm)
  - [Deploy dos containers e testes utilizando Makefile](#deploy-dos-containers-e-testes-utilizando-makefile)
    - [Deploy com GPU](#deploy-com-gpu)
    - [Deploy com CPU](#deploy-com-cpu)
  - [Comandos para criação de embeddings e indexação](#comandos-para-criação-de-embeddings-e-indexação)
  - [Teste com perguntas pré definidas](#teste-com-perguntas-pré-definidas)
  - [Comandos para teste de extração de url](#comandos-para-teste-de-extração-de-url)
- [Outras formas de teste](#outras-formas-de-teste)
  - [Teste com Postman Collection](#teste-com-postman-collection)
  - [Teste utilizando Swagger UI](#teste-utilizando-swagger-ui)
- [Informações do Projeto](#informações-do-projeto)
  - [Stack e Tecnologias](#stack-e-tecnologias)
    - [Vector Database](#vector-database)
    - [Backend para as APIs](#backend-para-as-apis)
    - [Ollama](#ollama)
    - [Modelo de indexação](#modelo-de-indexação)
- [Pipeline RAG](#pipeline-rag)
  - [Configurações para criação dos embedding](#configurações-para-criação-dos-embedding)
    - [Divisão do texto em chunck](#divisão-do-texto-em-chunck)
    - [Criação da collection no vector database](#criação-da-collection-no-vector-database)
    - [Criação dos pontos (embeddings) no vector database](#criação-dos-pontos-embeddings-no-vector-database)
  - [Configurações para recuperação de informação](#configurações-para-recuperação-de-informação)
- [Benchmarks](#benchmarks)
  - [llama3.2:3b](#llama32:3b)
  - [llama3.2:1b](#llama32:1b)
  - [moondream](#moondream)
  - [mistral](#mistral)
- [Próximos passos](#próximos-passos)

# Guia para teste rápido:

Garantir que o docker e o make estão instalados.

``` make -v && echo -e "\n" && docker -v ```

## Requisitos mínimos:

Para o modelo default `llama3.2:3b` e para embeddings `all-MiniLM-L6-v2`:
![alt text](docs/assets/image.png)

## Requisitos mínimos para execução em CPU:

- 6GB RAM
- 6 cores
- Linux Ubuntu
- x86_64 (não foi testado em ARM)

Instancia de CPU (EC2) foi escolhida uma instancia melhor que o minimo, pois a inferencia em CPU é mais lenta e alguns cores a mais podem ajudar:
![alt text](docs/assets/image-2.png)

CPU:
``` make up-n-wait-cpu && make create-vector && make ask-script ```

## Requisitos mínimos para execução em GPU:

- 6GB VRAM (Nvidia)
- 4GB RAM
- 6 cores
- Linux Ubuntu
- x86_64 (não foi testado em ARM)

Instancia de GPU (Sagemaker):
![alt text](docs/assets/image-1.png)

GPU:
``` make up-n-wait && make create-vector && make ask-script ```




# Comandos para uso e teste do projeto


## Escolha do modelo LLM

O modelo pode ser escolhido trocando a variável `MODEL` no arquivo `docker-compose.yml` ou  `docker-compose.cpu.yml`, essa variavel esta localizada no serviço `llm_api_service` 

Model default: `llama3.2:3b`

Lista de modelos disponíveis no ollama:

| Model              | Parameters | Size  | MODEL_NAME            |
| ------------------ | ---------- | ----- | --------------------- |
| Llama 3.2          | 3B         | 2.0GB | `llama3.2:3b`         |
| Llama 3.2          | 1B         | 1.3GB | `llama3.2:1b`         |
| Llama 3.2 Vision   | 11B        | 7.9GB | `llama3.2-vision`     |
| Llama 3.2 Vision   | 90B        | 55GB  | `llama3.2-vision:90b` |
| Llama 3.1          | 8B         | 4.7GB | `llama3.1`            |
| Llama 3.1          | 70B        | 40GB  | `llama3.1:70b`        |
| Llama 3.1          | 405B       | 231GB | `llama3.1:405b`       |
| Phi 3 Mini         | 3.8B       | 2.3GB | `phi3`                |
| Phi 3 Medium       | 14B        | 7.9GB | `phi3:medium`         |
| Gemma 2            | 2B         | 1.6GB | `gemma2:2b`           |
| Gemma 2            | 9B         | 5.5GB | `gemma2`              |
| Gemma 2            | 27B        | 16GB  | `gemma2:27b`          |
| Mistral            | 7B         | 4.1GB | `mistral`             |
| Moondream 2        | 1.4B       | 829MB | `moondream`           |
| Neural Chat        | 7B         | 4.1GB | `neural-chat`         |
| Starling           | 7B         | 4.1GB | `starling-lm`         |
| Code Llama         | 7B         | 3.8GB | `codellama`           |
| Llama 2 Uncensored | 7B         | 3.8GB | `llama2-uncensored`   |
| LLaVA              | 7B         | 4.5GB | `llava`               |
| Solar              | 10.7B      | 6.1GB | `solar`               |
[Fonte](https://raw.githubusercontent.com/ollama/ollama/refs/heads/main/README.md)

## Deploy dos containers e testes utilizando Makefile

Os comandos utilizam script shell e somente funcionam para ambiente Linux.

Pelo terminal, navegue até a pasta deste projeto.

### Deploy com GPU

Caso tenha GPU e todos os drivers nvidia para uso de GPU pelo docker, execute o seguinte comando make para rodar os containers

``` make up-n-wait ```

### Deploy com CPU

Caso contrario iremos rodar em CPU os modelos para isso devemos

``` make up-n-wait-cpu ```

Esses processos podem demorar um pouco para rodar, pois os modelos de LLM são grandes e precisam ser baixados e indexados.

### Comandos para criação de embeddings e indexação

Para criar os embeddings e indexa-los no vector database, execute o comando make:

``` make create-index ```


### Teste com perguntas pré definidas

Temos uma série de perguntas pré definidas para teste das APIs no arquivo `avaliacao/perguntas.txt`

Para testar as APIs com essas perguntas, execute o comando make:

``` make ask-script ```

### Comandos para teste de extração de url

Para testar a extração de url, execute o comando make:

``` make extract-url ```

## Outras formas de teste

Os principais endpoints das APIs são:

### Vector Service (localhost:5002)

`/extract/extract-url` para extrair o conteúdo de uma url. Payload type application/json:
| Campo       | Tipo   | Descrição                                                                 |
|-------------|--------|---------------------------------------------------------------------------|
| `url`       | string | A url que será extraida.                                                  |


`/vector/text-to-vector` para criar o embedding de um texto. Payload type multipart/form-data:
| Campo       | Tipo   | Descrição                                                                 |
|-------------|--------|---------------------------------------------------------------------------|
| `title`     | text   | O título do texto que será processado.                                    |
| `description` | text | Uma breve descrição ou contexto do texto.                                 |
| `user_id`   | text   | Identificador do usuário, usado para fins de teste.                       |
| `url`       | text   | URL do texto ou recurso associado.                                        |
| `file`      | file   | Caminho para o arquivo que contém o texto a ser processado.               |

### LLM Service (localhost:5003)

 `/llm/ask` para fazer uma pergunta ao LLM com recuperação de informação do vector database. Payload type application/json
 
 OBS: Para que a resposta seja assertiva, é necessário que o campo `title_rag` seja igual ao `title` do texto indexado no vector database. 

| Campo       | Tipo   | Descrição                                                                 |
|-------------|--------|---------------------------------------------------------------------------|
| `question`  | string | A pergunta que será feita ao modelo LLM.                                  |
| `title_rag` | string | O título do texto indexado no vector database, deve corresponder ao título original. |


Obs: O campo `title_rag` deve ser igual ao `title` do texto indexado no vector database. Pois essa é a forma como recuperamos o texto relevante para a resposta.

### Teste com Postman Collection

Para testar as APIs com o Postman, basta importar a collection `postman/Mle_Hotmart_API.postman_collection.json`

1. Utilize a request `save text vec db` para indexar o texto no vector database, não esqueça de carregar o arquivo `utils/out/output.txt`

2. Utilize a request `ask llm` para testar suas próprias perguntas

3. Utilize a request `extract url` para extrair o conteúdo de uma url e indexar no vector database


### Teste utilizando Swagger UI

A FastAPI possui uma interface swagger para teste das APIs, para acessar é necessário rodar o projeto e acessar a url:

Para extrair o conteúdo de uma url, acesse a url:

``` http://localhost:5002/docs#/default/extract_url_extract_extract_url_post ```

Para criar o embedding de um texto, acesse a url:

``` http://localhost:5002/docs#/default/text_to_vector_vector_text_to_vector_post ```

Utilize o método POST `/vector/text-to-vector` para criar o embedding


Para responder uma pergunta, acesse a url:

``` http://localhost:5003/docs#/default/generate_response_route_llm_generate_response_post ```

Utilize o método POST `/llm/ask` para responder a pergunta


# Informações do Projeto

## Stack e Tecnologias

### Vector Database

Foi escolhida Qdrant por ser escrita em Rust, assim é um banco de dados bastante performático, seguro contra erros e leve. Integração via `qdrant-client` para Python.


### Backend para as APIs

FastAPI foi escolhido por ser um dos melhores frameworks para backend em Python, com suporte para operações assíncronas, o que é fundamental para lidar com múltiplas requisições de forma eficiente.


### Ollama

Ollama facilita o deploy de modelos LLM e por isso foi adicionado a esse projeto.


### Modelo de indexação 

Modelo escolhido: `all-MiniLM-L6-v2`. Vantagens: Leve, rápido, ideal para gerar embeddings de texto com boa qualidade para recuperação semântica e Q&A. Compatível com hardware (RTX 3060 12GB).


## Pipeline RAG

### Configurações para criação dos embedding

#### Divisão do texto em chunck

Primeiramente o texto é dividido em chunks de 300 caracteres com 50 caracteres de overlap. O divisor de chunks é o ponto (.)
Após isso, os chunks são verificados para que nao tenha chunks maiores que 300 caracteres. Caso tenha, o chunk é dividido em outros mais pequenos.
Por fim, os chunks são limpos e normalizados para evitar espaços desnecessários.

#### Criação da collection no vector database

A collection é criada no vector database com o nome do valor do título do texto após a normalização, que é feita para evitar caracteres especiais e espaços desnecessários passando por uma função de hash. Caso a collection já exista, o sistema irá retornar um erro. A dimensão do vector na database é 384.

#### Criação dos pontos (embeddings) no vector database

Os chunks criados anteriormente são utilizados para criar os pontos (embeddings) no vector database. Cada ponto é composto por um id, um embedding e o payload que é composto pelo chunk de texto. 
O embedding é criado pelo modelo `all-MiniLM-L6-v2` e a dimensão do embedding é 384, compativel com a collection criada.

### Configurações para recuperação de informação

A recuperação da informação é feita criando um vetor query com o texto da pergunta e comparando com os vetores de cada ponto da collection utilizando a métrica cosine similarity. Para coletar o texto relevante para a resposta, é feita uma busca por todos os pontos que possuem uma similaridade maior que 0.5 e o limite de resultados é 5. Esse valor é enviado como contexto para o modelo LLM.

# Benchmarks

## llama3.2:3b

Modelo-embedding: all-MiniLM-L6-v2<br>
Modelo-LLM: llama3.2:3b (2.0GB)

P: Qual é a taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil? <br>
R: A taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil é de 9,9% do valor do produto.



P: Em que ano a Hotmart foi fundada e quem são seus fundadores?<br>
R: A Hotmart foi fundada em 2011.



P: Quais são os três principais papéis envolvidos no processo de venda online da Hotmart?<br>
R: Não tenho informações suficientes para responder.



P: Quantos países a Hotmart possui escritórios atualmente?<br>
R: Não tenho informações suficientes para responder. O contexto fornecido não menciona o número de escritórios da Hotmart em diferentes países.



P: O que é o Hotmart Club e quais são suas principais características?<br>
R: O Hotmart Club é uma área de membros da plataforma Hotmart, oferecendo vantagens como:

- Proteção total dos dados de compra com segurança
- Possibilidade de aumentar as conversões com as ferramentas de vendas e conteúdo personalizadas
- Área de membros gratuita, ilimitada e automática para entregar conteúdos de forma mais eficiente



P: Quais são as formas de pagamento aceitas pela Hotmart?<br>
R: Não tenho informações suficientes para responder.



P: Como funciona o sistema de comissões para Afiliados na plataforma?<br>
R: Não tenho informações suficientes para responder à pergunta sobre como funciona o sistema de comissões para Afiliados na plataforma.



P: O que é o HotLeads e para que serve?<br>
R: O HotLeads é uma ferramenta que permite rastrear leads e vincular-os a Afiliados de forma segura, garantindo que eles recebam suas comissões corretamente.



P: 9. Quantos produtos cadastrados e usuários a Hotmart possui?<br>
R: Não tenho informações suficientes para responder à sua pergunta. O contexto fornece informações sobre como vender com a Hotmart, suas ferramentas e soluções, mas não fornece dados específicos sobre o número de produtos cadastrados e usuários da plataforma.



P: Como funciona a emissão de notas fiscais na plataforma?<br>
R: A emissão de notas fiscais na plataforma funciona da seguinte maneira:

*   O produtor garante a emissão de notas fiscais para cada venda feita, mesmo quando feita por um afiliado.
*   No caso de afiliados, o produtor emite a nota fiscal ao comprador e o afiliado ao produtor, como fornecedor.
*   A plataforma oferece uma integração com as notas fiscais, permitindo que os produtos físicos sejam emitidos automaticamente.
*   A emissão de notas fiscais pode ser feita de maneira automática, graças à integração com a plataforma.



P: O que é o Club Sales e qual sua principal função?<br>
R: O Club Sales é uma ferramenta do Hotmart Club que ajuda a aumentar as conversões em vendas, permitindo que os clientes comprem com apenas 1 clique.



P: Quais são os tipos de produtos que podem ser comercializados na Hotmart?<br>
R: Os produtos digitais e físicos podem ser comercializados na Hotmart. Além disso, a plataforma também oferece ferramentas para criar comunidades e hospedar produtos, além de serviços como divulgação e venda de produtos digitais.



P: Qual é a sede global da Hotmart?<br>
R: Não tenho informações suficientes para responder.



P: Como funciona o recurso de Compra com 1 Clique?<br>
R: O recurso de Compra com 1 Clique permite que seus clientes façam a compra de um produto ou serviço com apenas 1 clique, facilitando o processo de pagamento e aumentando as chances de chegar ao final da compra. Isso ocorre porque os dados do cliente são armazenados no aplicativo do comprador, permitindo uma transação rápida e segura.



P: Qual é a política de cobrança da Hotmart para uso da plataforma?<br>
R: A política de cobrança da Hotmart é que os usuários pagam apenas 9,9% do valor por cada venda realizada. Não há custos adicionais para o uso da plataforma, somente após a realização de uma venda.





## llama3.2:1b

Modelo-embedding: all-MiniLM-L6-v2<br>
Modelo-LLM: llama3.2:1b (1.3GB)


P: Qual é a taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil?<br>
R: A Hotmart cobre uma taxa adicional de 9,9% do valor total da venda realizada, mais um valor fixo de R$1 por venda.



P: Em que ano a Hotmart foi fundada e quem são seus fundadores?<br>
R: A Hotmart foi fundada em 2004. Seus fundadores não foram mencionados no contexto.



P: Quais são os três principais papéis envolvidos no processo de venda online da Hotmart?<br>
R: As três principais papéis envolvidos na venda online da Hotmart são:

1.  **Vendedor**: É o profissional responsável por criar e vender conteúdo para os clientes através do site e plataformas de comunicação.
2.  **Contador/Contabilista**: É a pessoa que analisa todas as finanças do negócio, processa as contas das empresas, processa o pagamento dos pagamentos online em um só lugar e otimiza o tempo do vendedor para focar no crescimento do negócio.
3.  **Promotor/Promotora**: É a pessoa responsável por promover o negócio através da Hotmart, ofertando soluções de escala que ajudam a crescer a empresa online e melhorar as finanças.



P: Quantos países a Hotmart possui escritórios atualmente?<br>
R: Não tenho informações suficientes para responder.



P: O que é o Hotmart Club e quais são suas principais características?<br>
R: O Hotmart Club é um serviço que oferece a possibilidade de criar um player próprio para evitar replicação do conteúdo não autorizado, graças à segurança dos dados de compra. Além disso, o club tem recursos como uma área de membros ilimitada e um sistema automático para impulsionar as conversões (One-Click Buy) com o One-Click Buy, facilitando a venda de produtos ou conteúdo no Hotmart.



P: Quais são as formas de pagamento aceitas pela Hotmart?<br>
R: As formas de pagamento aceitas pela Hotmart incluem cartões de crédito, PayPal e outras opções de pagamento online. Além disso, a plataforma também permite que os afiliados ofereçam seu próprio pagamento gateway para suas vendas.



P: Como funciona o sistema de comissões para Afiliados na plataforma?<br>
R: O sistema de comissões para afiliados na Hotmart é uma forma de recompensar os produtores e afiliados por ajudá-los a vender conteúdos digitais. As comissões são calculadas como um valor percentual do preço de venda do conteúdo vendido, por exemplo.

Por exemplo:

* Se o preço de venda do conteúdo é R$ 10,00 e a comissão é 20%, então o produtores receberá R$ 2,00 em comissão por cada venda.
* Se o preço de venda do conteúdo é R$ 50,00 e a comissão é 30%, então o afiliado receberá R$ 15,00 em comissão por cada venda.



P: O que é o HotLeads e para que serve?<br>
R: Não tenho informações suficientes para responder.



P: 9. Quantos produtos cadastrados e usuários a Hotmart possui?<br>
R: A Hotmart possui uma grande variedade de serviços em torno de um serviço ou de um público inicial, com mais de 50 milhões de livros, apostilas, canecas, tapetes de exercícios e outros produtos digitais disponíveis para venda. Além disso, também hospeda e divulga produtos físicos, como garrafinhas, conjunto de materiais, etc., através da plataforma.



P: Como funciona a emissão de notas fiscais na plataforma?<br>
R: A emissão de notas fiscais na plataforma automática envolve o processo de certificação da venda realizada pelo empreendedor ( Produtor) para produtos ou serviços, garantindo que a transação seja válida e legal. Para Afiliados, oProdutor emite a nota financeira (NF) ao comprador, enquanto o Afiliado recebe a notifica do produtor sobre a emissão da nota fiscal.



P: O que é o Club Sales e qual sua principal função?<br>
R: Não tenho informações suficientes para responder.



P: Quais são os tipos de produtos que podem ser comercializados na Hotmart?<br>
R: Os produtos mais comuns comercializados na plataforma Hotmart incluem serviços digitais (como cursos, conteúdo educativo) e produtos físicos como livros, jogos, acessórios, etc.



P: Qual é a sede global da Hotmart?<br>
R: A sede global da Hotmart está localizada em São Paulo.



P: Como funciona o recurso de Compra com 1 Clique?<br>
R: O recurso "Compra com 1 Clique" (ou também conhecido como "One-Click Buy") no Hotmart é uma ferramenta que facilita o pagamento dos clientes, reduzindo o tempo de cadastro de dados e aumentando as chances de chegar ao final da compra.



P: Qual é a política de cobrança da Hotmart para uso da plataforma?<br>
R: Sim, a resposta é:
A Hotmart cobra 9,9% do valor da venda realizada como única opção de cobrança, desde que o usuário não faça uma venda.


## moondream

Modelo-embedding: all-MiniLM-L6-v2<br>
Modelo-LLM: moondream (829MB)

P: Qual é a taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil?<br>
R: 
 9.9%



P: Em que ano a Hotmart foi fundada e quem são seus fundadores?<br>
R: 
 2014



P: Quais são os três principais papéis envolvidos no processo de venda online da Hotmart?<br>
R: 
 1. E o melhor:tudo isso em um só lugar e com total integração com a Hotmart!  Quais são as formas de pagamento e como funciona o sistema de comissões na Hotmart? Como você pôde ver até aqui, a Hotmart é diferente, pois oferece tudo para que a venda seja feita



P: Quantos países a Hotmart possui escritórios atualmente?<br>
R: 



P: O que é o Hotmart Club e quais são suas principais características?<br>
R: 
The Hotmart Club is a club that sells products to its members. It has been described as a "hotmart" with many features, including the ability to buy one-click and to buy from multiple vendors at once. The club also offers a variety of products for sale, which can be purchased by its members through the club's sales channels. Additionally, it provides services such as customer support and product recommendations based on the preferences of its members.



P: Quais são as formas de pagamento aceitas pela Hotmart?<br>
R: 
 1. E o melhor:tudo isso em um só lugar e com total integração com a Hotmart!  Quais são as formas de pagamento e como funciona o sistema de comissões na Hotmart? Como vê pode ser encontrada no contexto, diga 
Não tenho informações suficientes para responder.



P: Como funciona o sistema de comissões para Afiliados na plataforma?<br>
R: 

Nossos Produtores e Afiliados, entregando funcionalidades e conteúdos que os ajudem a realizar vendas e ter uma renda fazendo algo que eles realmente gostem.



P: O que é o HotLeads e para que serve?<br>
R: 
HotLeadsOHotLeads



P: 9. Quantos produtos cadastrados e usuários a Hotmart possui?<br>
R: 
 9



P: Como funciona a emissão de notas fiscais na plataforma?<br>
R: 

Não tenho informações suficientes para responder.



P: O que é o Club Sales e qual sua principal função?<br>
R: 
The primary function of the Club Sales is to sell products directly to customers. It allows customers to browse and purchase items from a variety of vendors, including Hotmart Club. The club sales model provides an opportunity for customers to shop online or in-store without having to navigate through multiple pages on a website. This can be particularly beneficial for busy shoppers who want to save time by purchasing products directly from the source. Additionally, the club sales model allows businesses to reach a wider audience and increase their customer base, as it enables them to sell their products through various channels such as online platforms or physical stores.



P: Quais são os tipos de produtos que podem ser comercializados na Hotmart?<br>
R: 
There are several types of products that can be considered as commercialized at a market, such as food items and household goods. In the context of this question, it is not clear whether the product being sold is food or household goods. However, given the presence of the word "hotmart" in the question, it is likely that the product being sold could be either food or household goods.



P: Qual é a sede global da Hotmart?<br>
R: 




P: Como funciona o recurso de Compra com 1 Clique?<br>
R: 
Compra com 1 clique.



P: Qual é a política de cobrança da Hotmart para uso da plataforma?<br>
R: 
Não! A hotmart é uma plataforma gratuita, e nossa cobra por venda seu precisa preciar um sistema complexo para comunicar sua botânica.



## mistral

Modelo-embedding: all-MiniLM-L6-v2<br>
Modelo-LLM: mistral (4.1GB)

P: Qual é a taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil?<br>
R: 9% do valor do produto.



P: Em que ano a Hotmart foi fundada e quem são seus fundadores?<br>
R:  A Hotmart foi fundada em 2011. Seus fundadores são João Pedro Resende e outros associados.



P: Quais são os três principais papéis envolvidos no processo de venda online da Hotmart?<br>
R: 1. O criador de conteúdo, que cria e oferece o produto digital (cursos online, por exemplo) na plataforma Hotmart.
2. Os clientes, que acompanham o funil de vendas e decidem fazer compras dos produtos oferecidos pela Hotmart.
3. A Hotmart, que hospeda os cursos online e processa todos os pagamentos online, fornece as soluções necessárias para ajudar a escalar o negócio digital e emite as notas fiscais corretamente.



P: Quantos países a Hotmart possui escritórios atualmente?<br>
R:  Não tenho informações suficientes para responder. A descrição do contexto não fornece detalhes sobre quantos países a Hotmart possui escritórios.



P: O que é o Hotmart Club e quais são suas principais características?<br>
R:  O Hotmart Club é uma área de membros gratuita e ilimitada, desenvolvida pela plataforma de vendas Hotmart. Suas principais características incluem oferecer segurança para os dados de compra, aumentar as vendas automaticamente e facilitar a entrega de conteúdo com o recurso One-Click Buy. Ele foi desenvolvido especificamente para evitar que o conteúdo seja replicado para pessoas que não adquiriram o curso.



P: Quais são as formas de pagamento aceitas pela Hotmart?<br>
R:  A Hotmart aceita diversos métodos de pagamentos, tais como cartão de crédito, cartão de débito, boleto bancário, transferência bancária, Pix e outros meios de pagamento digital.



P: Como funciona o sistema de comissões para Afiliados na plataforma?<br>
R:  Na plataforma Hotmart, os Afiliados recebem uma comissão por cada venda realizada a partir de seus links. O percentual da comissão é definido pela empresa e pode variar de acordo com o tipo de produto ou outras condições específicas. Os Afiliados podem visualizar suas vendas, estatísticas e recebimentos em uma área exclusiva do sistema, onde também é possível gerenciar as suas promoções e links de afiliação.



P: O que é o HotLeads e para que serve?<br>
R:  O HotLeads é uma ferramenta que permite vincular leads aos afiliados de forma segura, garantindo que eles recebam suas comissões corretamente. Funciona em conjunto com a plataforma Hotmart e oferece soluções para rastrear e gerenciar esses leads.



P: 9. Quantos produtos cadastrados e usuários a Hotmart possui?<br>
R:  Não tenho informações suficientes para responder. A quantidade de produtos cadastrados e usuários na Hotmart não é fornecida no contexto fornecido.



P: Como funciona a emissão de notas fiscais na plataforma?<br>
R:  A emissão de notas fiscais na plataforma é automática. Uma empresa dentro da Hotmart Company, chamada eNotas, realiza esse serviço de integração. Quando uma venda digital ocorre, a eNotas automaticamente emite as notas fiscais tanto para o comprador quanto para o produtor (ou afiliado), funcionando como um fornecedor.



P: O que é o Club Sales e qual sua principal função?<br>
R:  O Club Sales é uma ferramenta no Hotmart Club. Sua principal função é impulsionar as conversões (vendas) aumentando a facilidade de compra dos clientes, muitos dos quais conhecem como One-Click Buy.



P: Quais são os tipos de produtos que podem ser comercializados na Hotmart?<br>
R:  Na Hotmart, é possível comercializar produtos digitais e físicos.



P: Qual é a sede global da Hotmart?<br>
R:  Não tenho informações suficientes para responder. A localização da sede global de Hotmart não foi mencionada no contexto fornecido.



P: Como funciona o recurso de Compra com 1 Clique?<br>
R:  O recurso "Compra com 1 clique" (ou "One-Click Buy") facilita o pagamento dos clientes, reduzindo o tempo e dificuldades no cadastro de informações pessoais. Quando um usuário clica em uma opção de compra, os detalhes de pagamento armazenados anteriormente serão automaticamente preenchidos, permitindo que a transação seja concluída com apenas um único clique. Se o limite do cartão for insuficiente para realizar a compra, existem recuperadores de venda que podem ajudar transformando a compra em uma recurrente.



P: Qual é a política de cobrança da Hotmart para uso da plataforma?<br>
R:  A Hotmart não exige nenhuma cobrança para o uso da plataforma gratuito. A única cobrança feita é uma comissão de 9,9% por cada venda realizada.


# Proximos passos

-   [ ] Adicionar mais perguntas pré definidas para avaliação
-   [ ] Adicionar mais modelos de LLM
-   [ ] Adicionar mais modelos de embeddings
-   [ ] Testar a performance em GPU
-   [ ] Testar a parametrização da busca por similaridade
-   [ ] Testar a parametrização do Text Splitter ao gerar os embeddings
-   [ ] Testar a possibilidade de gerar mais texto para indexação (Augmentation Techniques)
-   [ ] Melhorar a interface de teste das APIs
