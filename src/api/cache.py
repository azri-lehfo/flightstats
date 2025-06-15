import importlib

from django.conf import settings
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.urls import resolve
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class CacheModelViewSetMixin:
    """The mixin adds caching capabilities to a view set and overrides
    a few basic methods.
    """

    timeout = settings.DEFAULT_CACHE_TIMEOUT

    def __init__(self, *args, **kwargs) -> None:
        self.cache = None

        if settings.ENABLE_REDIS_CACHE:
            self.cache = caches['redis']

        super().__init__(*args, **kwargs)

    def _get_cache_key(self, instance_pk: str, key_prefix: str = None) -> str:
        if key_prefix is None:
            key_prefix = self.cache_key_prefix

        return f"{key_prefix}_{instance_pk}"

    def perform_create(self, serializer: Serializer) -> None:
        instance = serializer.save()

        # Add the new instance to cache
        if self.cache is not None:
            self.cache.set(self._get_cache_key(instance.pk), instance, timeout=self.timeout)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance_obj = kwargs.get('instance', None)
        # Retrieve the instance from cache, or if not found, cache it
        if self.cache is not None:
            instance = self.cache.get_or_set(self._get_cache_key(kwargs['pk']), instance_obj or self.get_object(), timeout=self.timeout)
        else:
            instance = instance_obj or self.get_object()

        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs) -> Response:
        response = super().update(request, *args, **kwargs)

        # Update cache with the updated instance
        if self.cache is not None and self._get_cache_key(kwargs['pk']) in self.cache:
            instance = self.cache.get(self._get_cache_key(kwargs['pk']))
            instance.refresh_from_db()
            self.cache.set(self._get_cache_key(kwargs['pk']), instance, timeout=self.timeout)

        return response

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        response = super().destroy(request, *args, **kwargs)

        # Remove the instance from cache
        if self.cache is not None:
            self.cache.delete(self._get_cache_key(kwargs['pk']))

        return response
