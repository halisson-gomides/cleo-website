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
    address_code:       Mapped[str]         = mapped_column(nullable=True) # CEP
    address_street:     Mapped[str]         = mapped_column(nullable=True)
    address_number:     Mapped[str]         = mapped_column(nullable=True)
    address_complement: Mapped[str]         = mapped_column(nullable=True)
    address_district:   Mapped[str]         = mapped_column(nullable=True) # Bairro
    city_id:            Mapped[int]         = mapped_column(ForeignKey('tab_cities.id'), nullable=True)
    state_id:           Mapped[int]         = mapped_column(ForeignKey('tab_states.id'), nullable=True) 
    created_at: Mapped[datetime]  = mapped_column(init=False, server_default=func.datetime(func.now(), 'localtime'))
    
    gender: Mapped["PessoaGenero"] = relationship(back_populates='clients', init=False)
    city:  Mapped["EnderecoMuni"]   = relationship(back_populates='clients', init=False)


    def __repr__(self):
        return f"Client(id={self.id}, name={self.name})"
    

# Definição da tabela Genero
@table_registry.mapped_as_dataclass
class PessoaGenero():
    __tablename__ = 'tab_genders'

    id:         Mapped[int]     = mapped_column(init=False, primary_key=True, autoincrement=True) 
    description:Mapped[str]     = mapped_column(nullable=False, unique=True)
    flag_active:Mapped[int]     = mapped_column(init=False, default=1)
    created_at: Mapped[datetime]= mapped_column(init=False, server_default=func.datetime(func.now(), 'localtime'))
    
    clients:      Mapped[List["Cliente"]]= relationship(back_populates='gender', default_factory=list, init=False)
    
    def __repr__(self):
        return f"PessoaGenero(id={self.id}, nome={self.description})"
    

# Definição da tabela de Estados - UF
@table_registry.mapped_as_dataclass
class EnderecoUF():
    __tablename__ = 'tab_states'

    id:         Mapped[int]       = mapped_column(init=True, primary_key=True) 
    description:Mapped[str]       = mapped_column(nullable=False, unique=True)
    code:       Mapped[str]       = mapped_column(nullable=False, unique=True)
    region:     Mapped[str]       = mapped_column(nullable=False)
    flag_active:Mapped[int]       = mapped_column(init=False, default=1)
    created_at: Mapped[datetime]  = mapped_column(init=False, server_default=func.datetime(func.now(), 'localtime'))   

    cities:     Mapped[List["EnderecoMuni"]] = relationship(back_populates="state", init=False) 
    
    def __repr__(self):
        return f"EnderecoUF(id={self.id}, nome={self.description})"
    

# Definição da tabela de Municipios
@table_registry.mapped_as_dataclass
class EnderecoMuni():
    __tablename__ = 'tab_cities'

    id:         Mapped[int]       = mapped_column(init=True, primary_key=True) 
    description:Mapped[str]       = mapped_column(nullable=False)
    state_id:   Mapped[int]       = mapped_column(ForeignKey('tab_states.id'), nullable=False)    
    flag_active:Mapped[int]       = mapped_column(init=False, default=1)
    created_at: Mapped[datetime]  = mapped_column(init=False, server_default=func.datetime(func.now(), 'localtime'))    

    state:        Mapped["EnderecoUF"]        = relationship(back_populates='cities', init=False)
    clients:      Mapped[List["Cliente"]]= relationship(back_populates='city', default_factory=list, init=False)
    
    def __repr__(self):
        return f"EnderecoMuni(id={self.id}, nome={self.description})"