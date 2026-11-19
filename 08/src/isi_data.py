from sqlmodel import Field, Session, SQLModel, create_engine


class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    stok: int
    harga: float
    tersedia: bool


engine = create_engine("sqlite:///inventaris.db")


def main():
    daftar_produk = [
        Produk(kode="PRD01", nama="Keyboard Mekanikal", stok=15, harga=450000.50, tersedia=True),
        Produk(kode="PRD02", nama="Mouse Wireless", stok=30, harga=175000.00, tersedia=True),
        Produk(kode="PRD03", nama="Monitor 24 Inch", stok=8, harga=1850000.75, tersedia=True),
        Produk(kode="PRD04", nama="Webcam HD", stok=0, harga=320000.00, tersedia=False),
        Produk(kode="PRD05", nama="USB Hub Type-C", stok=22, harga=125500.25, tersedia=True),
    ]

    with Session(engine) as session:
        for item in daftar_produk:
            session.add(item)
        session.commit()
        print("Berhasil memasukkan 5 data produk ke database!")


if __name__ == "__main__":
    main()
