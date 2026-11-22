    def validate_time_window(self) -> VisitCreate:
        start_utc = normalize_utc(self.scheduled_start)
        end_utc = normalize_utc(self.scheduled_end)
        problem = window_error(start_utc, end_utc)
        if problem is not None:
            raise ValueError(problem)
        self.scheduled_start = start_utc
        self.scheduled_end = end_utc
        return self
