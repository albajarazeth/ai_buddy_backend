from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ChatSession, Message
from django.contrib.auth.hashers import make_password
from .utils import generate_ai_response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")    

    if not username or not password:
        return Response({"error": "All fields are required"}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status = 400)
    
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "user": {
            "id": user.id,
            "username": user.username,
        },
        "token": str(refresh.access_token),
        "refresh": str(refresh),
    }, status=201)

@api_view(["POST"])
def send_message_view(request):
    user = request.user

    if not user.is_authenticated:
        return Response({"error": "User must be logged in."}, status=401)

    text = request.data.get("text")
    if not text:
        return Response({"error": "Message text is required."}, status=400)

    session_id = request.data.get("session_id")

    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found or not owned by user."}, status=404)

    else:
        try:
            session = ChatSession.objects.filter(user=user).latest("created_at")
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(user=user)

    Message.objects.create(
        user=user,
        session=session,
        sender="USER",
        text=text
    )

    ai_response_text = generate_ai_response(session=session)
    
    ai_msg = Message.objects.create(
        user=user,
        session=session,
        sender = "AI",
        text = ai_response_text
    )

    return Response({
        "message": "Message successfully processed.", 
        "session_id": session.id,
        "ai_response": ai_msg.text, 
    }, status=201)


@api_view(["GET"])
def get_all_messages(session_id):

    try: 
        messages = Message.objects.filter(session_id=session_id).order_by("created_at")
        return Response({"messages": list(messages.values())}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


        

        

