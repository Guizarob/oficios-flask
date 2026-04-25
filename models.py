from sqlalchemy.orm import Mapped, mapped_column
from databases import db
from sqlalchemy import Boolean, Text, Date
from datetime import date

#Modelo de datos 

class Oficios(db.Model):
    __tablename__ = "oficios"

    #id = db.Column(db.Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key = True)

    numero_oficio: Mapped[str] = mapped_column(nullable= False) #mapped_column(unique=True)

    asunto: Mapped[str]  = mapped_column(nullable = False)

    remitente: Mapped[str] = mapped_column(nullable = False)

    destinatario:  Mapped[str] = mapped_column(nullable = False)

    acusado: Mapped[bool] = mapped_column(Boolean, nullable=False, default= False )

    hipervinculo: Mapped[str] = mapped_column(Text, nullable = False)

    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    antecedentes: Mapped[str | None] = mapped_column(nullable=True)

    fecha: Mapped[date | None] = mapped_column(Date, default=date.today, nullable=True)

    def __str__(self):
        
        return(
            f'Id:{self.id},'
            f'Numero de Oficio:{self.numero_oficio},'
            f'Asunto:{self.asunto},'
            f'Fecha: {self.fecha},'
            f'Remitente: {self.remitente},'
            f'Destinatario: {self.destinatario},'
            f'Acusado: {self.acusado},'
            f'Hipervinculo: {self.hipervinculo},'
            f'Observaciones: {self.observaciones},'
            f'Antecedentes: {self.antecedentes}'

        )