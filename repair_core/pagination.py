from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Custom definition of PageNumberPagination class.
    It comes with the page_size attribute defined by default.
    """
    page_size = 10
    # https://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style
    page_size_query_param = 'page_size'
    max_page_size = 50
