from django.db import models
from django.utils import timezone

# App Imports


class TimeStampModel(models.Model):
    """TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    created_on = models.DateTimeField(
        auto_now=True,
        db_column="created_on",
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        db_column="updated_on",
    )

    class Meta:
        get_latest_by = "updated_on"
        ordering = (
            "-updated_on",
            "-created_on",
        )
        abstract = True


class SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self, *args, **kwargs):
        return super(SoftDeleteQuerySet, self).update(deleted_on=timezone.now())

    def hard_delete(self, *args, **kwargs):
        return super(SoftDeleteQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_on=None)

    def dead(self):
        return self.exclude(deleted_on=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted_on=None)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        self.get_queryset().hard_delete()


class DeleteModel(models.Model):
    """DeleteModel
    An abstract base class model that provides self-managed "deleted_on" fields.
    """

    deleted_on = models.DateTimeField(db_column="deleted_on", null=True, blank=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_on = timezone.now()
        self.save()

    def hard_delete(self):
        super(DeleteModel, self).delete()
