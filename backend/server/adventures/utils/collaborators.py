from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def get_collaborator_user_ids(user):
    """Return user IDs that share at least one Collection with ``user``.

    A "collaborator" is any user on the other side of a
    ``Collection.shared_with`` relationship in either direction:

      * users who appear in ``shared_with`` on collections ``user`` owns, and
      * owners of collections that have ``user`` in their ``shared_with`` set.

    Excludes ``user`` themselves. Returns a QuerySet of user IDs.
    """
    if not user or not user.is_authenticated:
        return User.objects.none().values_list('id', flat=True)

    return (
        User.objects
        .filter(Q(shared_with__user=user) | Q(collection__shared_with=user))
        .exclude(id=user.id)
        .distinct()
        .values_list('id', flat=True)
    )


def get_visible_user_ids(user):
    """User IDs whose user-scoped data should be visible to ``user``.

    That's the user themselves plus every collaborator.
    """
    return [user.id, *get_collaborator_user_ids(user)]
