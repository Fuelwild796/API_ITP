from database.database import Base, engine
import database.models  
# Crie as tabelas
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")