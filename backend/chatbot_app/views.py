import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq
from dotenv import load_dotenv
from django.db.models import Q
from .models import ChatInteraction
from product_app.models import Product, Category
from product_app.serializers import ProductSerializer


load_dotenv()

class ChatbotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        session_id = request.data.get('session_id')

        if not user_message:
            return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not session_id:
            return Response({'error': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return Response({'error': 'Groq API key not configured on the server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        client = Groq(api_key=groq_api_key)

        # --- Search for products based on user query ---
        relevant_products_info = ""
        matching_products = Product.objects.none() # Initialize as empty queryset

        try:
            # 1. Try to find products that directly match the user's message
            initial_query = user_message.strip()
            if initial_query:
                matching_products = Product.objects.filter(
                    Q(name__icontains=initial_query) | Q(description__icontains=initial_query)
                ).distinct()

            # 2. If no direct matches or if the query is a common synonym, broaden the search
            if not matching_products.exists():
                broad_search_terms = []
                lower_user_message = user_message.lower()

                if "phone" in lower_user_message or "phones" in lower_user_message:
                    broad_search_terms.extend(["smartphone", "mobile phone", "cell phone", "handset"])
                if "laptop" in lower_user_message or "notebook" in lower_user_message:
                    broad_search_terms.append("laptop computer")
                if "headphone" in lower_user_message or "headphones" in lower_user_message:
                    broad_search_terms.append("earbuds")
                # Add more synonyms/broad terms for other categories as needed

                if broad_search_terms:
                    broad_q_objects = Q()
                    for term in broad_search_terms:
                        broad_q_objects |= Q(name__icontains=term) | Q(description__icontains=term)
                    
                    # Combine with initial query if it exists, or just use broad terms
                    if initial_query:
                         matching_products = Product.objects.filter(
                            (Q(name__icontains=initial_query) | Q(description__icontains=initial_query)) | broad_q_objects
                         ).distinct()
                    else:
                        matching_products = Product.objects.filter(broad_q_objects).distinct()
            
            # Limit to top 5 products for concise LLM context
            matching_products = matching_products[:5]

            if matching_products.exists():
                serializer = ProductSerializer(matching_products, many=True)
                products_list_for_llm = []
                for product_data in serializer.data:
                    category_name = product_data['category']['name'] if product_data.get('category') else 'N/A'
                    products_list_for_llm.append(
                        f"Product Name: {product_data['name']}, "
                        f"Category: {category_name}, "
                        f"Price: ₹{product_data['price']}, "
                        f"Stock: {product_data['stock_quantity']}, "
                        f"Description: {product_data['description'][:150]}..." 
                    )
                relevant_products_info = "\n\nAvailable Products Relevant to Query:\n" + "\n---\n".join(products_list_for_llm)
                # print(f"DEBUG: Relevant products found: {relevant_products_info}") # For debugging

        except Exception as e:
            self.stdout.write(f"Error during product search in chatbot view: {e}", self.style.ERROR)
            relevant_products_info = "\n\n(Note: Product search encountered an internal issue, respond generally.)"


        # --- System Prompt Refinement ---
        system_prompt = (
            "You are an AI sales assistant for an e-commerce store. "
            "Your goal is to help customers find products, provide details about specific products "
            "they ask about, and suggest relevant products based on their needs. "
            "You have access to product information which might be provided in the user's query context. "
            "Always be polite, helpful, and concise. "
            "If product information is provided, use it to answer the user's question directly or to make suggestions. "
            "If a user asks for product details, provide them from the given information. "
            "If a user is looking for recommendations, suggest relevant products from the provided list. "
            "Do NOT invent product details. If you cannot find a relevant product in the provided information, "
            "state that politely and suggest they try a different search term or browse general categories. "
            "Keep responses natural and conversational. Include prices and stock if available for suggested products."
        )

  
        # Embed relevant_products_info directly into the user's message for better context
        full_user_content = user_message
        if relevant_products_info:
            full_user_content = f"{user_message}\n\n[Relevant Product Context:\n{relevant_products_info}\n]"
        
        messages_for_llm = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_content}
        ]
            
        # print(f"DEBUG: Messages sent to LLM: {messages_for_llm}") # For debugging


        try:
            chat_completion = client.chat.completions.create(
                messages=messages_for_llm,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=300,
                top_p=1,
                stop=None,
                stream=False,
            )
            bot_response = chat_completion.choices[0].message.content

            # Save the interaction to the database
            ChatInteraction.objects.create(
                session_id=session_id,
                user_message=user_message,
                bot_response=bot_response
            )

            return Response({'response': bot_response}, status=status.HTTP_200_OK)

        except Exception as e:
            self.stdout.write(f"Error calling Groq API or saving interaction: {e}", self.style.ERROR)
            return Response(
                {'error': 'An error occurred while processing your request. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

