class ExpenseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: Description
    amount: Money = Field(examples=["150.00"])
    currency: CurrencyCode = "USD"
    category: ExpenseCategory = "other"
    paid_by: PersonName
    split_among: People
