from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from .serializer import OrderSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def checkout(request):
    """
    يتوقع JSON بالشكل:
    {
      "customer_name": "اسم",
      "customer_email": "a@b.com",
      "customer_phone": "012345",
      "customer_address": "العنوان",
      "notes": "ملاحظات اختيارية",
      "items": [
         {"product_name": "...", "product_image": "url", "price": 100.0, "quantity": 2},
         ...
      ]
    }
    """
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                order = serializer.save()
        except Exception as e:
            return Response({"detail": "خطأ في إنشاء الطلب." , "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "تم إنشاء الطلب بنجاح", "order_id": order.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
