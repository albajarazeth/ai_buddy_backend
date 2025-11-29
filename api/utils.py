from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .models import Message


def generate_ai_response(session):

    llm = ChatOpenAI(model="gpt-4o-mini")

    system_message = SystemMessage(
        content=(
    "You are a warm, empathetic, and encouraging AI buddy dedicated to helping people feel cared "
    "for and offering general guidance on mental well-being and coping strategies. While you are "
    "here to listen and support, remember that you are **not a licensed professional**."
    "Always be on the lookout for signs of **immediate crisis or urgent safety concerns**. "
    "If a user expresses distress suggesting harm to themselves or others, or is in an emergency, "
    "you **must** immediately and clearly advise them to contact professional emergency services "
    "(like 911 or their local equivalent), a crisis hotline, or a trusted mental health professional."
)
    )

    messages = [system_message]

    history = Message.objects.filter(session=session).order_by("created_at")

    for msg in history:
            if msg.sender == 'USER':
                messages.append(HumanMessage(content=msg.text))
            elif msg.sender == 'AI':
                messages.append(AIMessage(content=msg.text))

    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        print(f"LLM API Error: {e}")
        return "I'm sorry, I'm having trouble connecting to my systems right now."
    
