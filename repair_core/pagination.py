from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Custom definition of PageNumberPagination class.
    It comes with the page_size attribute defined by default.
    """
    page_size = 10
