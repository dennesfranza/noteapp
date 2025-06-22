from fastapi import FastAPI
from . import models, database
from .routes import notes, tags

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
