    def schedule_visit(self, property_id: int, payload: VisitCreate) -> VisitResponse:
        begin_write(self.session)  # verificar y luego insertar: candado de escritura primero
        prop = self.session.get(Property, property_id)
        if prop is None:
            raise PropertyNotFoundError(property_id)
        if prop.status == "sold":
            raise PropertyUnavailableError(property_id, prop.status)

        # [start_A, end_A) y [start_B, end_B) se traslapan si start_A < end_B y end_A > start_B
        overlap_stmt = select(Visit.id).where(
            col(Visit.property_id) == property_id,
            col(Visit.scheduled_start) < payload.scheduled_end,
            col(Visit.scheduled_end) > payload.scheduled_start,
        )
        if self.session.exec(overlap_stmt).first() is not None:
            raise VisitSlotConflictError(property_id)

        visit = Visit(
            property_id=property_id,
            visitor_name=payload.visitor_name,
            visitor_email=payload.visitor_email,
            scheduled_start=payload.scheduled_start,
            scheduled_end=payload.scheduled_end,
            notes=payload.notes,
        )
        self.session.add(visit)
        self.session.commit()
        self.session.refresh(visit)
        return to_visit_response(visit)
