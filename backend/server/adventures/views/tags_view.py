from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from adventures.models import Location

class ActivityTypesView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def types(self, request):
        """
        Retrieve a list of distinct activity types for locations the current
        user owns or can see via a shared collection.
        """
        user = request.user
        locations = Location.objects.filter(
            Q(user=user)
            | Q(collections__user=user)
            | Q(collections__shared_with=user)
        ).distinct()
        types = locations.values_list('tags', flat=True)

        allTypes = []

        for i in types:
            if not i:
                continue
            for x in i:
                if x and x not in allTypes:
                    allTypes.append(x)

        return Response(allTypes)