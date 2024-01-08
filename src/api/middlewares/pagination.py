from rest_framework import pagination, serializers


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000
    min_limit = 1
    min_offset = 0
    max_offset = 1000

    def paginate_queryset(self, queryset, request, view=None):
        limit = request.query_params.get("limit")
        offset = request.query_params.get("offset")

        if limit:
            limit = int(limit)
            if limit > self.max_limit:
                raise serializers.ValidationError(
                    {
                        "limit": [
                            "Limit should be less than or equal to {}".format(
                                self.max_limit
                            )
                        ]
                    }
                )
            elif limit < self.min_limit:
                raise serializers.ValidationError(
                    {
                        "limit": [
                            "Limit should be greater than or equal to {}".format(
                                self.min_limit
                            )
                        ]
                    }
                )
        if offset:
            offset = int(offset)
            if offset > self.max_offset:
                raise serializers.ValidationError(
                    {
                        "offset": [
                            "Offset should be less than or equal to {}".format(
                                self.max_offset
                            )
                        ]
                    }
                )
            elif offset < self.min_offset:
                raise serializers.ValidationError(
                    {
                        "offset": [
                            "Offset should be greater than or equal to {}".format(
                                self.min_offset
                            )
                        ]
                    }
                )

        return super(self.__class__, self).paginate_queryset(queryset, request, view)