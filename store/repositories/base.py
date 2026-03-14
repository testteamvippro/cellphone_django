"""
Base repository class providing common CRUD operations
"""
from typing import TypeVar, Generic, List, Optional, Dict, Any
from django.db.models import Model, QuerySet

T = TypeVar('T', bound=Model)


class BaseRepository(Generic[T]):
    """
    Generic repository class for common database operations.
    Implements the Repository Pattern for data abstraction.
    """

    def __init__(self, model_class: type[T]):
        self.model = model_class

    def get_by_id(self, obj_id: int) -> Optional[T]:
        """Get an object by its ID"""
        try:
            return self.model.objects.get(id=obj_id)
        except self.model.DoesNotExist:
            return None

    def get_all(self) -> QuerySet[T]:
        """Get all objects"""
        return self.model.objects.all()

    def filter(self, **kwargs) -> QuerySet[T]:
        """Filter objects by criteria"""
        return self.model.objects.filter(**kwargs)

    def get_single(self, **kwargs) -> Optional[T]:
        """Get a single object by criteria"""
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def create(self, **kwargs) -> T:
        """Create a new object"""
        return self.model.objects.create(**kwargs)

    def get_or_create(self, defaults: Optional[Dict[str, Any]] = None, **kwargs) -> tuple[T, bool]:
        """Get or create an object (returns tuple of object and created flag)"""
        return self.model.objects.get_or_create(defaults=defaults, **kwargs)

    def update(self, obj_id: int, **kwargs) -> Optional[T]:
        """Update an object"""
        obj = self.get_by_id(obj_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.save()
        return obj

    def delete(self, obj_id: int) -> bool:
        """Delete an object"""
        obj = self.get_by_id(obj_id)
        if obj:
            obj.delete()
            return True
        return False

    def exists(self, **kwargs) -> bool:
        """Check if object exists"""
        return self.model.objects.filter(**kwargs).exists()

    def count(self, **kwargs) -> int:
        """Count objects matching criteria"""
        return self.model.objects.filter(**kwargs).count()

    def bulk_create(self, objects: List[T]) -> List[T]:
        """Create multiple objects at once"""
        return self.model.objects.bulk_create(objects)

    def bulk_update(self, objects: List[T], fields: List[str]) -> int:
        """Update multiple objects at once"""
        return self.model.objects.bulk_update(objects, fields)
