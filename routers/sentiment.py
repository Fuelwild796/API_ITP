from fastapi import APIRouter, Request, Depends, HTTPException, Query
from utils import predict_sentiment, labels
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import Acao, Sentimento, User, Event
from datetime import datetime
from sqlalchemy import func
from datetime import datetime

router = APIRouter()

class BatchRequest(BaseModel):
    textos: List[str]

class BatchResult(BaseModel):
    texto: str
    sentimento: str
    grupo: str

class SentimentoResponse(BaseModel):
    id: int
    atendente: str
    sentimento_do_cliente: str
    grupo_sentimento: str
    score: int
    mes: str
    nome_cliente: str
    sentimento_atendente: str
    score_cliente: int

class AcaoCreate(BaseModel):
    descricao: str = Field(..., min_length=1)
    event_id: int
    user_id: Optional[int] = None
    agent_id: Optional[int] = None

class AcaoResposta(BaseModel):
    acao_id: int
    descricao: str
    sentimento: str
    event_id: int
    user_id: Optional[int]
    agent_id: Optional[int]
    data_acao: datetime

    class Config:
        orm_mode = True


class AnaliseTextoRequest(BaseModel):
    texto_cliente: str
    texto_atendente: str
    atendente: str
    nome_cliente: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

POSITIVOS = ["Satisfação"]
NEGATIVOS = ["Raiva/Irritação", "Frustração"]
NEUTROS = ["Neutro","Urgência/Pressão","Confusão"]

def classificar_grupo(sentimento: str) -> str:
    if sentimento in POSITIVOS:
        return "Positivo"
    elif sentimento in NEGATIVOS:
        return "Negativo"
    elif sentimento in NEUTROS:
        return "Neutro"
    return "Outro"

def get_next_id(db, model):
    max_id = db.query(func.max(model.id)).scalar()
    return (max_id or 0) + 1

@router.get("/atendentes")
def listar_atendentes(
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retorna atendentes com score total, paginado.
    """
    offset = (page - 1) * limit
    total = db.query(Sentimento.atendente).distinct().count()
    atendentes = (
        db.query(
            Sentimento.atendente,
            func.sum(Sentimento.score).label("score")
        )
        .group_by(Sentimento.atendente)
        .order_by(func.sum(Sentimento.score).desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    items = [{"nome": a[0], "score": a[1]} for a in atendentes]
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/clientes")
def listar_clientes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retorna clientes com score total, paginado.
    """
    offset = (page - 1) * limit
    total = db.query(Sentimento.nome_cliente).distinct().count()
    clientes = (
        db.query(
            Sentimento.nome_cliente,
            func.sum(Sentimento.score_cliente).label("score")
        )
        .group_by(Sentimento.nome_cliente)
        .order_by(func.sum(Sentimento.score_cliente).desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    items = [{"nome": c[0], "score": c[1]} for c in clientes]
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/performance-geral")
def performance_geral(db: Session = Depends(get_db)):
    """
    Retorna a distribuição percentual dos sentimentos para gráfico de pizza.
    """
    total = db.query(Sentimento).count()
    label_list = [
        'Satisfação',
        'Frustração',
        'Confusão',
        'Urgência/Pressão',
        'Raiva/Irritação',
        'Neutro'
    ]
    valores = []
    for label in label_list:
        count = db.query(Sentimento).filter(Sentimento.sentimento_do_cliente == label).count()
        percent = (count / total * 100) if total else 0
        valores.append(round(percent, 1))
    return {"labels": label_list, "valores": valores}

@router.get("/evolucao-mensal")
def evolucao_mensal(db: Session = Depends(get_db)):
    """
    Retorna a evolução mensal dos sentimentos para gráfico de barras.
    """
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    negativo = []
    positivo = []
    neutro = []
    for mes in meses:
        total_neg = db.query(Sentimento).filter(Sentimento.mes == mes, Sentimento.grupo_sentimento == "Negativo").count()
        total_pos = db.query(Sentimento).filter(Sentimento.mes == mes, Sentimento.grupo_sentimento == "Positivo").count()
        total_neu = db.query(Sentimento).filter(Sentimento.mes == mes, Sentimento.grupo_sentimento == "Neutro").count()
        negativo.append(total_neg)
        positivo.append(total_pos)
        neutro.append(total_neu)
    return {
        "meses": meses,
        "negativo": negativo,
        "positivo": positivo,
        "neutro": neutro
    }


@router.post("/acoes/", response_model=AcaoResposta, summary="Cria uma nova ação")
def criar_acao(
    acao: AcaoCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova ação. Se user_id ou event_id não existirem, são criados automaticamente.
    """
    if not acao.descricao or not acao.event_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Descrição e event_id são obrigatórios."
        )

    if acao.user_id:
        user = db.query(User).filter(User.id == acao.user_id).first()
        if not user:
            user = User(id=acao.user_id, nome="Usuário Padrão")
            db.add(user)
            db.commit()
            db.refresh(user)

    if acao.event_id:
        event = db.query(Event).filter(Event.id == acao.event_id).first()
        if not event:
            event = Event(id=acao.event_id, nome="Evento Padrão")
            db.add(event)
            db.commit()
            db.refresh(event)
    if acao.agent_id:
        agent = db.query(User).filter(User.id == acao.agent_id).first()
        if not agent:
            agent = User(id=acao.agent_id, nome="Agente Padrão")
            db.add(agent)
            db.commit()
            db.refresh(agent)

    infer = request.app.state.infer
    tokenizer = request.app.state.tokenizer
    sentimento = predict_sentiment(acao.descricao, infer, tokenizer)

    nova_acao = Acao(
        descricao=acao.descricao,
        sentimento=sentimento,
        event_id=acao.event_id,
        user_id=acao.user_id,
        agent_id=acao.agent_id,
    )
    db.add(nova_acao)
    db.commit()
    db.refresh(nova_acao)
    return nova_acao


@router.post("/analisar_texto/", summary="Analisa o sentimento de um texto")
def analisar_texto(
    req: AnaliseTextoRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Recebe frases do cliente e do atendente, retorna sentimentos, grupos e scores.
    """
    campos_faltando = []
    if not req.texto_cliente:
        campos_faltando.append("texto_cliente")
    if not req.texto_atendente:
        campos_faltando.append("texto_atendente")
    if not req.atendente:
        campos_faltando.append("atendente")
    if not req.nome_cliente:
        campos_faltando.append("nome_cliente")
    if campos_faltando:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Campos obrigatórios faltando: {', '.join(campos_faltando)}"
        )

    infer = request.app.state.infer
    tokenizer = request.app.state.tokenizer


    sentimento_cliente = predict_sentiment(req.texto_cliente, infer, tokenizer)
    grupo_cliente = classificar_grupo(sentimento_cliente)
    if grupo_cliente == "Positivo":
        score_cliente = 1
    elif grupo_cliente == "Negativo":
        score_cliente = -1
    else:
        score_cliente = 0


    sentimento_atendente = predict_sentiment(req.texto_atendente, infer, tokenizer)
    grupo_atendente = classificar_grupo(sentimento_atendente)
    if grupo_atendente == "Positivo":
        score_atendente = 1
    elif grupo_atendente == "Negativo":
        score_atendente = -1
    else:
        score_atendente = 0

    meses_pt = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes_atual = meses_pt[datetime.now().month - 1]

    novo = Sentimento(
        atendente=req.atendente,
        sentimento_do_cliente=sentimento_cliente,
        grupo_sentimento=grupo_cliente,
        score=score_cliente,
        mes=mes_atual,
        nome_cliente=req.nome_cliente,
        sentimento_atendente=sentimento_atendente,
        score_cliente=score_cliente
    )
    novo.id = get_next_id(db, Sentimento)
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "sentimento_cliente": sentimento_cliente,
        "grupo_cliente": grupo_cliente,
        "score_cliente": score_cliente,
        "sentimento_atendente": sentimento_atendente,
        "grupo_atendente": grupo_atendente,
        "score_atendente": score_atendente
    }

@router.post("/batch_analyze/", response_model=List[BatchResult], summary="Analisa uma lista de textos")
def batch_analyze(req: BatchRequest, request: Request):
    """
    Recebe uma lista de textos e retorna sentimento e grupo para cada um.
    """
    if not req.textos or not isinstance(req.textos, list) or len(req.textos) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A lista de textos não pode estar vazia."
        )
    infer = request.app.state.infer
    tokenizer = request.app.state.tokenizer
    resultados = []
    for t in req.textos:
        if not t or not isinstance(t, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todos os textos devem ser strings não vazias."
            )
        sentimento = predict_sentiment(t, infer, tokenizer)
        grupo = classificar_grupo(sentimento)
        resultados.append(BatchResult(texto=t, sentimento=sentimento, grupo=grupo))
    return resultados

@router.get("/sentimentos/", response_model=List[SentimentoResponse], summary="Lista sentimentos com filtros e paginação")
def listar_sentimentos(
    atendente: Optional[str] = Query(None),
    grupo_sentimento: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista sentimentos, com filtros opcionais e paginação.
    """
    query = db.query(Sentimento)
    if atendente:
        query = query.filter(Sentimento.atendente == atendente)
    if grupo_sentimento:
        query = query.filter(Sentimento.grupo_sentimento == grupo_sentimento)
    resultados = query.offset(offset).limit(limit).all()
    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum sentimento encontrado com os filtros fornecidos."
        )
    return resultados

@router.get("/sentimentos/{sentimento_id}", response_model=SentimentoResponse, summary="Busca sentimento por ID")
def buscar_sentimento(sentimento_id: int, db: Session = Depends(get_db)):
    sentimento = db.query(Sentimento).filter(Sentimento.id == sentimento_id).first()
    if not sentimento:
        raise HTTPException(status_code=404, detail="Sentimento não encontrado")
    return sentimento

@router.delete("/sentimentos/{sentimento_id}", summary="Deleta sentimento por ID")
def deletar_sentimento(sentimento_id: int, db: Session = Depends(get_db)):
    sentimento = db.query(Sentimento).filter(Sentimento.id == sentimento_id).first()
    if not sentimento:
        raise HTTPException(status_code=404, detail="Sentimento não encontrado")
    db.delete(sentimento)
    db.commit()
    return {"msg": "Sentimento deletado com sucesso"}

@router.get("/sentimentos/estatisticas/", summary="Estatísticas de sentimentos")
def estatisticas(db: Session = Depends(get_db)):
    total = db.query(Sentimento).count()
    positivos = db.query(Sentimento).filter(Sentimento.grupo_sentimento == "Positivo").count()
    negativos = db.query(Sentimento).filter(Sentimento.grupo_sentimento == "Negativo").count()
    neutros = db.query(Sentimento).filter(Sentimento.grupo_sentimento == "Neutro").count()
    if total == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum dado de sentimento encontrado para estatísticas."
        )
    return {"total": total, "positivos": positivos, "negativos": negativos, "neutros": neutros}