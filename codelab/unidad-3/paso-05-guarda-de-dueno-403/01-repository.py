def _get_owned_property_or_raise(self, property_id: int, current_agent: Agent) -> Property:
    """Guard anti-IDOR (BOLA): 404 si no existe, 403 si no es dueño ni admin."""
    prop = self.session.get(Property, property_id)
    if prop is None:
        raise PropertyNotFoundError(property_id)
    if prop.owner_agent_id != current_agent.id and current_agent.role != "admin":
        raise ForbiddenOwnerError(property_id)
    return prop
