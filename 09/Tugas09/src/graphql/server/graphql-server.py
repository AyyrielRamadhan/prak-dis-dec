import typing
import strawberry
from sqlmodel import Field, Session, SQLModel, create_engine, select

@strawberry.type
class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    stok: int
    harga: float
    tersedia: bool

engine = create_engine("sqlite:///inventaris.db")

def get_produks():
    with Session(engine) as session:
        statement = select(Produk)
        results = session.exec(statement).all()
        return results

@strawberry.type
class Query:
    produks: typing.List[Produk] = strawberry.field(resolver=get_produks)

schema = strawberry.Schema(query=Query)
