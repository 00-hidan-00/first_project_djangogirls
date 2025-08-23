from django.http import HttpRequest


def get_favorite_ids(request: HttpRequest) -> list[int]:
    """Return list of favorited post IDs."""
    if request.user.is_authenticated:
        return list(request.user.favorites.values_list("id", flat=True))
    return [int(i) for i in request.session.get("post_favorites", [])]
