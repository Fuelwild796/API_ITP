# API_RESIDENCIA

API de análise de sentimentos utilizando BERTimbau, FastAPI e PostgreSQL.

## Funcionalidades

- Análise de sentimentos de textos em português
- Classificação em grupos: Positivo, Negativo, Neutro
- Registro dos resultados em banco de dados PostgreSQL
- Endpoints REST para CRUD de sentimentos
- Deploy fácil com Docker e Docker Compose
- Segurança de endpoints com API Key via header

## Estrutura do Projeto

```
API_RESIDENCIA/
├── database/                # Modelos e scripts do banco
├── routers/                 # Rotas da API
├── bertimbau_sentiment_model.keras/   # Modelo TensorFlow salvo
├── bertimbau_tokenizer/                # Tokenizer BERTimbau
├── main.py                  # Ponto de entrada da API
├── utils.py                 # Funções utilitárias
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente
├── Dockerfile               # Build da imagem da API
├── docker-compose.yml       # Orquestração dos containers
└── README.md                # Este arquivo
```

## Como rodar localmente

1. **Clone o repositório e entre na pasta**
    ```sh
    git clone <url-do-repo>
    cd API_RESIDENCIA
    ```

2. **Configure o arquivo `.env`**
    ```
    MODEL_URL="https://drive.google.com/uc?id=1d-O5uQfuEdS33fxevD3j7it7Xl2a2Gdj"
    DATABASE_URL=postgresql://postgres:postgres@db:5432/sentimentos
    API_KEY=sua_chave_aqui
    ```

3. **Instale as dependências**
    ```sh
    pip install -r requirements.txt
    ```

4. **Suba a API e o banco com Docker Compose**
    ```sh
    docker-compose up --build
    ```

5. **Acesse a documentação**
    - [http://localhost:8000/docs](http://localhost:8000/docs)

## Segurança com API_KEY

- Algumas rotas exigem autenticação via API Key.
- Envie o header `X-API-Key` com o valor definido em seu `.env`:
    ```
    X-API-Key: sua_chave_aqui
    ```

## Principais Endpoints

- `POST /analisar_texto/` — Analisa o sentimento de um texto
- `GET /sentimentos/` — Lista todos os sentimentos registrados
- `GET /sentimentos/{id}` — Busca sentimento por ID
- `DELETE /sentimentos/{id}` — Remove sentimento por ID
- `GET /sentimentos/grupo/{grupo}` — Filtra sentimentos por grupo
- `GET /health/` — Verifica se a API está online

## Observações

- O modelo e o tokenizer são baixados automaticamente na primeira execução.
- Certifique-se de que as pastas `bertimbau_sentiment_model.keras` e `bertimbau_tokenizer` estejam corretamente extraídas na raiz do projeto.
- Para rodar sem Docker, instale as dependências com `pip install -r requirements.txt` e execute `uvicorn main:app --reload`.
