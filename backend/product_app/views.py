from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q # For complex queries
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id' # Specifies that the URL will use 'id' to look up a product

class ProductSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"error": "Please provide a search query."}, status=400)

        # Search by product name or description (case-insensitive)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct() # Use .distinct() to avoid duplicate results if a product matches both name and description

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)