    def list_properties(
        self,
        city: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        min_bedrooms: int | None = None,
        status: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> PaginatedPropertiesResponse:
        filters = []
        if city is not None and city.strip():
            filters.append(col(Property.city_key) == make_city_key(city))
        if min_price is not None:
            filters.append(col(Property.price) >= min_price)
        if max_price is not None:
            filters.append(col(Property.price) <= max_price)
        if min_bedrooms is not None:
            filters.append(col(Property.bedrooms) >= min_bedrooms)
        if status is not None:
            filters.append(col(Property.status) == status)

        count_stmt = select(func.count()).select_from(Property).where(*filters)
        total = int(self.session.exec(count_stmt).one())

        offset = (page - 1) * size
        query_stmt = (
            select(Property, Agency.name)
            .join(Agency, col(Property.agency_id) == col(Agency.id))
            .where(*filters)
            .order_by(col(Property.id).asc())
            .offset(offset)
            .limit(size)
        )
        rows = self.session.exec(query_stmt).all()
        items = [to_property_response(prop, agency_name) for prop, agency_name in rows]
        pages = math.ceil(total / size) if total > 0 else 0
        return PaginatedPropertiesResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
        )
