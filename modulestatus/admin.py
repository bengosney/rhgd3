class statusAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status"] + list(self.list_display)
        self.list_filter = ["status"] + list(self.list_filter)

    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        if ordering := self.ordering or ():
            qs = qs.order_by(*ordering)

        return qs


class statusDateAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published"] + list(self.list_display)
        self.list_filter = ["status", "published"] + list(self.list_filter)

    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        if ordering := self.ordering or ():
            qs = qs.order_by(*ordering)

        return qs


class statusDateRangeAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published_from", "published_to"] + list(self.list_display)
        self.list_filter = ["status", "published_from", "published_to"] + list(self.list_filter)

    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        if ordering := self.ordering or ():
            qs = qs.order_by(*ordering)

        return qs
