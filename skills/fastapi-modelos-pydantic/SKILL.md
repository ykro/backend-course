---
name: fastapi-modelos-pydantic
description: Usar cuando hay que diseñar o corregir modelos Pydantic de un API FastAPI - cuerpos de entrada, respuestas, actualizaciones parciales (PATCH), dinero, fechas, validaciones cruzadas, campos que no deben exponerse, o errores 500 por datos inesperados.
---

# Modelos Pydantic para un API

Cada recurso tiene al menos tres modelos (crear, actualizar y salida) y ninguno es la tabla de la base de datos. La entrada rechaza lo que no conoce y pone límites; la salida decide qué se expone. El tipo del dinero se mantiene de punta a punta, también en la columna.

1. Separa los modelos. `TaskCreate` (campos obligatorios), `TaskUpdate` (todos opcionales, para PATCH) y `TaskOut` (lo que ve el cliente). Nunca devuelvas el objeto del ORM ni `__dict__`; declara `response_model=TaskOut` y usa `model_config = ConfigDict(from_attributes=True)` en la salida.
2. En la entrada usa `model_config = ConfigDict(extra="forbid")` para que un campo de más (`owner_id`, `is_admin`) sea 422 y no una escalada de privilegios.
3. Pon límites con `Annotated` y `Field`. Textos con `min_length` y `max_length` (y `str_strip_whitespace=True`), números con `gt`, `le`, listas con `max_length`. Una entrada extrema da 422, nunca 500.
4. Dinero en `Decimal` con `max_digits` y `decimal_places`, y columna `Numeric(12, 2)`. Convertir a `float` al guardar anula todo; si la columna es `Float`, la migración es parte del cambio.
5. Para PATCH distingue ausente de `null`. `payload.model_dump(exclude_unset=True)` trae solo lo enviado; un campo enviado con `null` donde el contrato no lo permite se rechaza con un validador. Qué hacer con un PATCH vacío (`{}`) es una decisión de contrato; propón 422 con un `model_validator` que exige al menos un campo y pregúntala.
6. Validaciones que cruzan campos van en `@model_validator(mode="after")`; las de un campo, en `@field_validator`.
7. Aplica el PATCH en el servicio, validando todo antes de mutar el objeto.
8. Prueba al menos el caso feliz, un campo extra, un límite exacto, `null` y el PATCH parcial que no toca los demás campos. Corre los tests y revisa `/docs` para confirmar que el esquema publicado es el que esperas.

```python
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator

Title = Annotated[str, Field(min_length=1, max_length=120)]
Money = Annotated[Decimal, Field(gt=0, le=Decimal("1000000"), max_digits=12, decimal_places=2)]

class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: Title | None = None
    amount: Money | None = None
    done: bool | None = None

    @field_validator("title", "amount", "done", mode="before")
    @classmethod
    def no_null(cls, v: object) -> object:
        if v is None:
            raise ValueError("no puede ser null; omite el campo")
        return v

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    amount: Decimal
    done: bool
```

Con `mode="before"` el validador solo corre para campos enviados, así que omitir el campo sigue siendo válido.

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.
