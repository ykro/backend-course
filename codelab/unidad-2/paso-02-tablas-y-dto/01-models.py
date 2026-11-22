class Property(SQLModel, table=True):
    """Tabla relacional de propiedades inmobiliarias vinculadas a una agencia."""

    id: int | None = Field(default=None, primary_key=True)
    agency_id: int = Field(foreign_key="agency.id", index=True)
    title: str = Field(min_length=3, max_length=140)
    city: str = Field(min_length=2, max_length=80)
    city_key: str = Field(default="", index=True, max_length=80)
    price: int = Field(gt=0, index=True, description="Precio entero en USD, sin flotantes")
    bedrooms: int = Field(ge=1, le=20, index=True)
    status: str = Field(default="available", index=True)
    created_at: datetime = Field(default_factory=utc_now)

    agency: Agency | None = Relationship(back_populates="properties")
    visits: list["Visit"] = Relationship(back_populates="property")
