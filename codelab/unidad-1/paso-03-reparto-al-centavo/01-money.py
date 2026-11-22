def split_evenly(amount: Decimal, names: list[str]) -> Shares:
    """Reparte amount entre names sin perder centavos.

    Los centavos sobrantes van, de uno en uno, a los primeros
    nombres en orden alfabético (sin distinguir acentos).
    """
    cents = int(to_money(amount) / CENT)
    base, extra = divmod(cents, len(names))
    ordered = sorted(names, key=alphabetical_key)
    shares: Shares = {}
    for position, person in enumerate(ordered):
        own = base + 1 if position < extra else base
        shares[person] = own * CENT
    return shares
