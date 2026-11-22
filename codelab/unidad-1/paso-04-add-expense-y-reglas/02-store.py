    def add_expense(
        self,
        trip_id: str,
        payload: ExpenseCreate,
    ) -> ExpenseResponse:
        record = self._get_trip_or_raise(trip_id)
        self._check_expense_rules(record, payload)
        expense = ExpenseResponse(
            id=f"exp-{uuid4().hex[:8]}",
            trip_id=record.id,
            created_at=datetime.now(UTC),
            **payload.model_dump(),
        )
        record.expenses.append(expense)
        return expense
