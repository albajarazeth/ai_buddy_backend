# AI Buddy - Supportive Chat Companion Application

A Django REST API application that provides an AI-powered supportive chat buddy designed to offer guidance, encouragement, and helpful conversation. The application uses JWT authentication for secure user sessions and integrates with OpenAI’s GPT-4o-mini model through LangChain to deliver intelligent, friendly, and empathetic responses.

## Libraries Used

### Core Framework
- **Django 5.0.0** - High-level Python web framework for rapid development
- **Django REST Framework 3.15.0** - Powerful toolkit for building Web APIs

### Authentication & Security
- **djangorestframework-simplejwt 5.3.1** - JWT authentication for Django REST Framework
  - Provides secure token-based authentication
  - Handles access and refresh token generation and validation
  - Enables stateless authentication for API endpoints

### AI & Language Processing
- **langchain** - Framework for developing applications powered by language models
- **langchain-openai** - OpenAI integration for LangChain
  - Enables seamless integration with OpenAI's GPT models
  - Provides structured message handling for conversation context

### Additional Dependencies
- **django-cors-headers** - Handles Cross-Origin Resource Sharing (CORS) for frontend integration
- **PyJWT** - JSON Web Token implementation (used by simplejwt)

## JWT Authentication Implementation

### How JWT is Used

The application implements JWT (JSON Web Tokens) for secure, stateless authentication:

1. **Token Generation on Registration/Login**
   - When a user registers or logs in, the system generates a pair of tokens:
     - **Access Token**: Short-lived token (30 minutes) for API requests
     - **Refresh Token**: Long-lived token (7 days) for obtaining new access tokens

2. **Token Configuration** (`backend/settings.py`)
   ```python
   SIMPLE_JWT = {
       "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
       "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
   }
   ```

3. **Authentication Middleware**
   - All protected endpoints require JWT authentication
   - The `JWTAuthentication` class is set as the default authentication method in REST Framework settings
   - Tokens are validated on each request to protected endpoints

4. **Token Usage Flow**
   - User registers/logs in → Receives access and refresh tokens
   - Client includes access token in `Authorization: Bearer <token>` header for protected endpoints
   - When access token expires, client uses refresh token to obtain a new access token
   - Protected endpoints automatically extract user information from the JWT token

## API Endpoints & Features

### 1. User Registration
**Endpoint:** `POST /api/register/`

**Description:** Creates a new user account and immediately returns JWT tokens for authentication.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "example_user"
  },
  "token": "access_token_string",
  "refresh": "refresh_token_string"
}
```

**Features:**
- Validates username and password are provided
- Checks for duplicate usernames
- Hashes password securely using Django's password hashing
- Automatically generates and returns JWT tokens upon successful registration
- Returns appropriate error messages for validation failures

---

### 2. User Login
**Endpoint:** `POST /api/login/`

**Description:** Authenticates existing users and returns JWT tokens.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access": "access_token_string",
  "refresh": "refresh_token_string"
}
```

**Features:**
- Validates user credentials against database
- Returns JWT access and refresh tokens upon successful authentication
- Uses Django REST Framework SimpleJWT's built-in `TokenObtainPairView`

---

### 3. Token Refresh
**Endpoint:** `POST /api/refresh/`

**Description:** Generates a new access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "refresh_token_string"
}
```

**Response (200 OK):**
```json
{
  "access": "new_access_token_string"
}
```

**Features:**
- Allows clients to obtain new access tokens without re-authenticating
- Validates refresh token before issuing new access token
- Extends user session without requiring login credentials
- Uses Django REST Framework SimpleJWT's built-in `TokenRefreshView`

---

### 4. Send Message to AI
**Endpoint:** `POST /api/send-message/`

**Description:** Sends a message to the AI buddy and receives an empathetic, supportive response. Requires JWT authentication.

**Authentication:** Required (JWT Bearer Token)

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "text": "I'm feeling anxious about my upcoming exam",
  "session_id": 1  // Optional: if not provided, uses most recent session or creates new one
}
```

**Response (201 Created):**
```json
{
  "message": "Message successfully processed.",
  "session_id": 1,
  "ai_response": "I understand that exams can be really stressful..."
}
```

**Features:**
- **JWT Authentication Required**: Validates user identity from JWT token
- **Session Management**: 
  - Automatically uses the most recent chat session if `session_id` is not provided
  - Creates a new session if no previous sessions exist
  - Allows explicit session selection via `session_id`
- **Message Storage**: Saves both user and AI messages to the database
- **AI Response Generation**: 
  - Uses OpenAI's GPT-4o-mini model through LangChain
  - Maintains conversation context by including full message history
  - Configured as an empathetic, supportive AI buddy
  - Includes safety protocols for crisis situations
- **Error Handling**: Returns appropriate errors for unauthenticated users, missing text, or invalid sessions

**AI Buddy Characteristics:**
- Warm, empathetic, and encouraging
- Provides general guidance on mental well-being
- Offers coping strategies
- Includes crisis detection and emergency service recommendations
- Clearly states it is not a licensed professional

---

### 5. Get All Messages
**Endpoint:** `GET /api/get-messages/`

**Description:** Retrieves all messages from a specific chat session.

**Query Parameters:**
- `session_id` (required): The ID of the chat session

**Response (200 OK):**
```json
{
  "messages": [
    {
      "id": 1,
      "user": 1,
      "session": 1,
      "sender": "USER",
      "text": "Hello",
      "created_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": 2,
      "user": 1,
      "session": 1,
      "sender": "AI",
      "text": "Hello! How can I help you today?",
      "created_at": "2024-01-01T12:00:05Z"
    }
  ]
}
```

**Features:**
- Retrieves all messages for a given session
- Messages are ordered chronologically by creation time
- Returns both user and AI messages
- Includes metadata (sender, timestamp, session ID)


## Data Models

### ChatSession
- **user**: Foreign key to Django User model
- **created_at**: Timestamp of session creation
- Represents a conversation session between a user and the AI

### Message
- **user**: Foreign key to Django User model
- **session**: Foreign key to ChatSession (with related_name "messages")
- **sender**: Choice field ('USER' or 'AI')
- **text**: The message content
- **created_at**: Timestamp of message creation

## 🔧 Setup & Installation

### Prerequisites
- Python 3.12+
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   cd ai_buddy
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Set your OpenAI API key as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Usage Examples

### Complete Authentication Flow

1. **Register a new user:**
   ```bash
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

2. **Login (alternative to registration):**
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

3. **Send a message (using access token from step 1 or 2):**
   ```bash
   curl -X POST http://localhost:8000/api/send-message/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{"text": "I need someone to talk to"}'
   ```

4. **Refresh access token:**
   ```bash
   curl -X POST http://localhost:8000/api/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
   ```

5. **Get messages from a session:**
   ```bash
   curl -X GET "http://localhost:8000/api/get-messages/?session_id=1"
   ```

## Security Features

- **JWT-based Authentication**: Secure, stateless authentication
- **Password Hashing**: Passwords are hashed using Django's secure password hashing
- **CORS Configuration**: Configured for cross-origin requests (adjust for production)
- **Token Expiration**: Access tokens expire after 30 minutes for security
- **User Isolation**: Users can only access their own chat sessions and messages

## Key Features Summary

1. **Secure User Authentication** - JWT-based registration and login system
2. **Session Management** - Automatic and manual chat session handling
3. **AI-Powered Conversations** - Empathetic AI responses using GPT-4o-mini
4. **Conversation History** - Full message history maintained per session
5. **Context-Aware AI** - AI maintains conversation context across messages
6. **Crisis Detection** - AI includes safety protocols for emergency situations
7. **RESTful API Design** - Clean, standard REST endpoints
8. **Database Persistence** - All messages and sessions stored in SQLite database

## Technology Stack Summary

- **Backend Framework**: Django 5.0
- **API Framework**: Django REST Framework 3.15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **AI Integration**: LangChain + OpenAI GPT-4o-mini
- **Database**: SQLite (development)
- **CORS Handling**: django-cors-headers

