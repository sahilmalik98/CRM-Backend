from rest_framework.pagination import PageNumberPagination

class LeadPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to override the page size
    max_page_size = 100  # Limit maximum page size
