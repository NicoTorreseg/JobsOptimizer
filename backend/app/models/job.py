from sqlalchemy import String, ForeignKey, Integer, Text, Float, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    
    name: Mapped[str] = mapped_column(String(100), index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True) # Para URLs bonitas
    domain: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    
    # Lógica de Negocio: Reputación
    reputation_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    job_offers: Mapped[list["JobOffer"]] = relationship(back_populates="company")

class JobOffer(Base):
    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Relación con FK Entera
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    
    title: Mapped[str] = mapped_column(String(200))
    normalized_title: Mapped[str] = mapped_column(String(200), index=True) # BUSQUEDAS AQUÍ
    
    description_raw: Mapped[str] = mapped_column(Text)
    seniority: Mapped[str] = mapped_column(String(50), index=True) # FILTROS AQUÍ
    tech_stack: Mapped[list[str]] = mapped_column(JSON, default=[])
    
    # Lógica Anti-Duplicados
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    
    # Metadata
    url: Mapped[str] = mapped_column(String, nullable=True) # Added URL field to store link
    location: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    company: Mapped["Company"] = relationship(back_populates="job_offers")

    @property
    def company_name(self) -> str:
        return self.company.name if self.company else "Unknown"
