from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "cs_user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(70), unique=True)
    username = Column(String(255))

class Agent(Base):
    __tablename__ = "cs_agents"
    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150))
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)

class Event(Base):
    __tablename__ = "cs_events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False)
    data_abertura = Column(DateTime, nullable=False, default=datetime.utcnow)
    data_baixa = Column(DateTime)
    status_id = Column(Integer, nullable=False)

class Acao(Base):
    __tablename__ = "cs_acoes"
    acao_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("cs_events.event_id"), nullable=False)
    descricao = Column(Text, nullable=False)
    agent_id = Column(Integer, ForeignKey("cs_agents.agent_id"))
    user_id = Column(Integer, ForeignKey("cs_user.user_id"))
    data_acao = Column(DateTime, default=datetime.utcnow)
    sentimento = Column(String(50))  # campo extra para o sentimento

    # Relacionamentos (opcional)
    event = relationship("Event")
    agent = relationship("Agent")
    user = relationship("User")

class Sentimento(Base):
    __tablename__ = "sentimentos"
    id = Column(Integer, primary_key=True, index=True)
    atendente = Column(String)
    sentimento_do_cliente = Column(String)
    grupo_sentimento = Column(String)
    score = Column(Integer)
    mes = Column(String)
    nome_cliente = Column(String)
    sentimento_atendente = Column(String)
    score_cliente = Column(Integer)