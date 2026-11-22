    def calculate_settlements(self, trip_id: str) -> SettlementSummaryResponse:
        record = self._get_trip_or_raise(trip_id)
        balances = {p: ZERO for p in record.participants}
        for expense in record.expenses:
            balances[expense.paid_by] += expense.amount
            for person, share in expense.shares.items():
                balances[person] -= share

        entries = balances.items()
        debtors = [_Balance(p, -b) for p, b in entries if b < 0]
        creditors = [_Balance(p, b) for p, b in entries if b > 0]
        debtors.sort(key=_rank)
        creditors.sort(key=_rank)

        transfers: list[SettlementTransfer] = []
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, creditor = debtors[i], creditors[j]
            paid = min(debtor.amount, creditor.amount)
            transfers.append(
                SettlementTransfer(
                    from_participant=debtor.participant,
                    to_participant=creditor.participant,
                    amount=paid,
                    currency=record.default_currency,
                )
            )
            debtor.amount -= paid
            creditor.amount -= paid
            if debtor.amount == 0:
                i += 1
            if creditor.amount == 0:
                j += 1

        return SettlementSummaryResponse(
            trip_id=record.id,
            currency=record.default_currency,
            total_spent=self._total(record),
            net_balances=balances,
            transfers=transfers,
        )
