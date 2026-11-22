Money = Annotated[
    Decimal,
    Field(gt=0, le=MAX_MONEY, max_digits=8, decimal_places=2),
    AfterValidator(to_money),
]
MoneyText = Annotated[
    Decimal,
    PlainSerializer(_money_text, return_type=str),
]
