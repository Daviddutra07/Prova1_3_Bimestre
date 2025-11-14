from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import Column, Integer, String, Table, create_engine, ForeignKey
from flask_login import UserMixin

engine = create_engine('sqlite:///app.db')
session = Session(bind=engine)

# Base declarativa
class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Novo relacionamento N:N
    # livros = relationship('Livro', backref='usuario')
    
    livros: Mapped[list["Livro"]] = relationship(
        "Livro",
        secondary="autores_livros",
        back_populates="autores"
    )


class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    autores: Mapped[list["User"]] = relationship(
        "User",
        secondary="autores_livros",
        back_populates="livros"
    )

autores_livros = Table(
    "autores_livros",
    Base.metadata,
    Column("autor_id", ForeignKey("users.id"), primary_key=True),
    Column("livro_id", ForeignKey("livros.id"), primary_key=True)
)