    @staticmethod
    def _check_expense_rules(
        record: _TripRecord,
        expense: ExpenseLike,
    ) -> None:
        expected = record.default_currency
        if expense.currency != expected:
            msg = f"La moneda {expense.currency} no es la del viaje ({expected})"
            raise CurrencyMismatchError(msg)
        allowed = set(record.participants)
        names = [expense.paid_by, *expense.split_among]
        outsiders = sorted({n for n in names if n not in allowed})
        if outsiders:
            msg = f"No pertenecen al viaje: {', '.join(outsiders)}"
            raise InvalidParticipantError(msg)
