from pydantic import BaseModel

class GrupoPoliticaPermissaoBase(BaseModel):
    grupo_politica_id: int
    permissao_id: int

class GrupoPoliticaPermissaoCreate(GrupoPoliticaPermissaoBase):
    pass

class GrupoPoliticaPermissaoOut(GrupoPoliticaPermissaoBase):
    class Config:
        orm_mode = True