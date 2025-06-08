import pandas as pd
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import Sentimento


csv_path = "database/database_sentimentos.csv"

df = pd.read_csv(csv_path)


df = df.rename(columns={
    "sentimento do cliente": "sentimento_do_cliente"
})

db: Session = SessionLocal()
for _, row in df.iterrows():
    sentimento = Sentimento(
        id=row["id"],
        atendente=row["atendente"],
        sentimento_do_cliente=row["sentimento_do_cliente"],
        grupo_sentimento=row["grupo_sentimento"],
        score=row["score"],
        mes=row["mes"],
        nome_cliente=row["nome_cliente"],
        sentimento_atendente=row["sentimento_atendente"],
        score_cliente=row["score_cliente"]
    )
    db.merge(sentimento)  
db.commit()
db.close()

print("Importação concluída!")