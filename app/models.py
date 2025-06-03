from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cliente = Column(String(255), nullable=False)
    direccion_envio = Column(String(255), nullable=False)
    productos = Column(Text, nullable=False)
    estado = Column(String(255), nullable=False, default="pendiente")

    def as_dict(self):
        return {
            "id": self.id,
            "nombre_cliente": self.nombre_cliente,
            "direccion_envio": self.direccion_envio,
            "productos": self.productos,
            "estado": self.estado
        }

    def __repr__(self):
        return f"<Pedido: {self.id}, {self.nombre_cliente}>"
