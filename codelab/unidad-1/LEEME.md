# Código del codelab, Unidad 1

Cada bloque de código del codelab, en el orden en que aparece, con la sangría exacta. El código del taller lo escribe tu agente con el pedido de cada paso del codelab: estos **fragmentos** son la referencia para revisar su diff (el cuerpo de una función, un método), no para pegarlos. No son archivos completos del proyecto, salvo que el paso diga lo contrario. Los `comandos.sh` se corren línea por línea en la terminal, en la raíz de tu repositorio.

| Paso | Archivo | Dónde va |
| :--- | :--- | :--- |
| 1. Entorno con uv | `paso-01-entorno-con-uv/01-comandos.sh` | terminal, en la raíz de tu repositorio |
| 1. Entorno con uv | `paso-01-entorno-con-uv/02-comandos.sh` | terminal, en la raíz de tu repositorio |
| 2. Contratos y dinero | `paso-02-contratos-y-dinero/01-schemas.py` | `app/schemas.py` |
| 2. Contratos y dinero | `paso-02-contratos-y-dinero/02-schemas.py` | `app/schemas.py` (sigue en el mismo archivo) |
| 3. Reparto al centavo | `paso-03-reparto-al-centavo/01-money.py` | `app/money.py` |
| 3. Reparto al centavo | `paso-03-reparto-al-centavo/02-comandos.sh` | terminal, en la raíz de tu repositorio |
| 4. add_expense y reglas | `paso-04-add-expense-y-reglas/01-store.py` | `app/store.py` |
| 4. add_expense y reglas | `paso-04-add-expense-y-reglas/02-store.py` | `app/store.py` |
| 4. add_expense y reglas | `paso-04-add-expense-y-reglas/03-comandos.sh` | terminal, en la raíz de tu repositorio |
| 5. Liquidación greedy | `paso-05-liquidacion-greedy/01-store.py` | `app/store.py` |
| 5. Liquidación greedy | `paso-05-liquidacion-greedy/02-comandos.sh` | terminal, en la raíz de tu repositorio |
| 6. Consola y calidad | `paso-06-consola-y-calidad/01-comandos.sh` | terminal, en la raíz de tu repositorio |
| 7. Reto y qué debe cumplir | `paso-07-reto-y-que-debe-cumplir/01-comandos.sh` | terminal, en la raíz de tu repositorio |

# Escríbelo tú

En este paso del codelab la pieza clave la escribes a mano, sin agente, antes de comparar con la referencia.

## Paso 5. Liquidación greedy

**Escríbelo tú: los dos punteros.**

**Pedido.** Esta pieza va a mano, sin agente. En `calculate_settlements`, escribe el `while` que recorre `debtors` y `creditors`, ya ordenados con `_rank`, y llena `transfers`. Los saldos netos y las listas ordenadas puedes escribirlos tú o pedírselos al agente con el pedido de este paso. Si el agente reescribe tu bucle, compara su versión con la tuya.

**Pista.** Usa dos índices: `i` para deudores y `j` para acreedores. En cada vuelta el pago es `min(deuda, crédito)`. Réstalo a los dos y avanza el índice de quien quedó en 0; en la misma vuelta pueden avanzar los dos. El bucle termina cuando se acaba cualquiera de las dos listas.

**Verifica.** Corre `uv run pytest tests/test_workshop.py -k settlements -v`. Los cinco tests de liquidación deben pasar, entre ellos `test_settlements_greedy_pays_largest_debt_first`, que revisa el orden de las transferencias. Si alguno falla, lee qué esperaba el test y compara tu bucle con la referencia de este paso.
