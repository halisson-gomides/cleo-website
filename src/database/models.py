from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List

table_registry = registry()


# Define a tabela de clientes
@table_registry.mapped_as_dataclass
class Cliente():
    __tablename__ = 'tab_clients'
    
    id: Mapped[int]               = mapped_column(init=False, autoincrement=True, primary_key=True)
    name: Mapped[str]             = mapped_column(nullable=False)
    email: Mapped[str]            = mapped_column(nullable=True, unique=True)
    document: Mapped[str]         = mapped_column(nullable=False, unique=True)
    gender_id:  Mapped[int]       = mapped_column(ForeignKey('tab_genders.id'), nullable=False)
    birthdate: Mapped[datetime]   = mapped_column(nullable=True)
    phone: Mapped[str]            = mapped_column(nullable=True)
    instagram: Mapped[str]        = mapped_column(nullable=True)    
    created_at: Mapped[datetime]  = mapped_column(init=False, server_default=func.now())
    
    gender: Mapped["PessoaGenero"] = relationship(back_populates='clients', init=False)

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name})"
    

# Definição da tabela Genero
@table_registry.mapped_as_dataclass
class PessoaGenero():
    __tablename__ = 'tab_genders'

    id:         Mapped[int]     = mapped_column(init=False, primary_key=True, autoincrement=True) 
    description:Mapped[str]     = mapped_column(nullable=False, unique=True)
    flag_active:Mapped[int]     = mapped_column(init=False, default=1)
    created_at: Mapped[datetime]= mapped_column(init=False, server_default=func.now())
    
    clients:      Mapped[List["Cliente"]]= relationship(back_populates='gender', default_factory=list, init=False)
    
    def __repr__(self):
        return f"PessoaGenero(id={self.id}, nome={self.description})"