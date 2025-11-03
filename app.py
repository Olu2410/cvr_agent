from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
from data import GUIDES

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "inec-cvr-chatbot-secret-key-2024")

# Services that require revalidation first
SERVICES_REQUIRING_REVALIDATION = ['transfer', 'update', 'lost-pvc']

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

def send_step(process, step_index):
    """Send a specific step to the user"""
    steps = GUIDES[process]['steps']
    
    if step_index < len(steps):
        step = steps[step_index]
        response = f"**Step {step['number']}:** {step['instruction']}"
        
        if 'question' in step:
            response += f"\n\n{step['question']}"
        
        # Add navigation hints
        nav_hints = []
        if step_index > 0:
            nav_hints.append("'back' for previous step")
        if process != 'universal-signup':
            nav_hints.append("'restart' for different service")
        
        if nav_hints:
            response += f"\n\n💡 *You can type {', '.join(nav_hints)}*"
            
        return jsonify({"reply": response})
    else:
        return jsonify({"reply": "You've completed all steps! 🎉"})

def handle_universal_signup(user_message, state):
    """Handle the universal sign-up process that everyone must complete"""
    process = 'universal-signup'
    current_step = state['current_step']
    steps = GUIDES[process]['steps']
    
    # Handle user responses during sign-up
    if any(word in user_message for word in ['back', 'previous']):
        if current_step > 0:
            state['current_step'] = current_step - 1
        return send_step(process, state['current_step'])
    
    if any(word in user_message for word in ['restart', 'start over']):
        state['current_step'] = 0
        return send_step(process, 0)
    
    # Check for completion confirmation
    if any(word in user_message for word in ['yes', 'ready', 'done', 'ok', 'continue', 'completed']):
        if current_step + 1 < len(steps):
            state['current_step'] = current_step + 1
            return send_step(process, current_step + 1)
        else:
            # Universal sign-up completed - move to service selection
            state['current_process'] = 'service-selection'
            state['current_step'] = 0
            state['completed_processes'].append('universal-signup')
            
            service_menu = """
🎉 **Great! You're now signed into the INEC CVR portal.**

**Which service would you like to proceed with?**

• **New Registration** - For first-time voters
• **Transfer** - If you've moved to a new location  
• **Update** - To correct your information
• **Lost PVC** - To replace a missing/damaged card
• **Revalidation** - To review your existing details

Just tell me which service you need help with!"""
            
            return jsonify({"reply": service_menu})
    
    # If user needs help or says no, repeat current step
    elif any(word in user_message for word in ['no', 'help', 'not sure', "can't", 'problem']):
        current_step_data = steps[current_step]
        clarification = f"No problem! Let me help you with this step:\n\n**Step {current_step_data['number']}:** {current_step_data['instruction']}"
        if 'question' in current_step_data:
            clarification += f"\n\n{current_step_data['question']}"
        return jsonify({"reply": clarification})
    
    # Default: continue with current step
    return send_step(process, current_step)

def handle_service_selection(user_message, state):
    """Handle service selection after universal sign-up"""
    service_keywords = {
        'new-registration': ['new', 'register', 'first time', 'never registered'],
        'transfer': ['transfer', 'move', 'relocate', 'new address'],
        'update': ['update', 'correct', 'change', 'wrong information'],
        'lost-pvc': ['lost', 'missing', 'damaged', 'replace pvc'],
        'revalidation': ['review', 'revalidate', 'check my details']
    }
    
    # Identify selected service
    selected_service = None
    for service, keywords in service_keywords.items():
        if any(keyword in user_message for keyword in keywords):
            selected_service = service
            break
    
    if selected_service:
        # Check if this service requires revalidation first
        if (selected_service in SERVICES_REQUIRING_REVALIDATION and 
            'revalidation' not in state.get('completed_processes', [])):
            
            state['pending_service'] = selected_service  # Store the intended service
            state['current_process'] = 'revalidation'
            state['current_step'] = 0
            
            revalidation_message = f"""
🔍 **Important Notice**

Before proceeding with **{GUIDES[selected_service]['title']}**, INEC requires you to first complete the **Voter Revalidation** process before making any changes.

Let's start with revalidation first:"""
            
            return jsonify({"reply": revalidation_message})
        else:
            # No revalidation needed or already completed
            state['current_process'] = selected_service
            state['current_step'] = 0
            return send_step(selected_service, 0)
    else:
        # Show service menu again
        return jsonify({"reply": """I'm not sure which service you need. Please choose one:

• **New Registration** - For first-time voters
• **Transfer** - If you've moved to a new location  
• **Update** - To correct your information
• **Lost PVC** - To replace a missing/damaged card
• **Revalidation** - To review your existing details

Which one would you like assistance with?"""})

def handle_specific_service(user_message, state):
    """Handle steps for specific services"""
    process = state['current_process']
    current_step = state['current_step']
    steps = GUIDES[process]['steps']
    
    # Handle navigation
    if any(word in user_message for word in ['back', 'previous']):
        if current_step > 0:
            state['current_step'] = current_step - 1
        return send_step(process, state['current_step'])
    
    if any(word in user_message for word in ['restart', 'start over', 'different service']):
        state['current_process'] = 'service-selection'
        state['current_step'] = 0
        if 'pending_service' in state:
            del state['pending_service']
        return jsonify({"reply": "Okay, let's choose a different service. What would you like help with?"})
    
    # Check for completion confirmation
    if any(word in user_message for word in ['yes', 'ready', 'done', 'ok', 'continue', 'completed']):
        if current_step + 1 < len(steps):
            state['current_step'] = current_step + 1
            return send_step(process, current_step + 1)
        else:
            # Service completed
            completion_text = f"""🎉 **Excellent! You've completed all steps for {GUIDES[process]['title']}**

**Required Documents:**
{chr(10).join(['• ' + doc for doc in GUIDES[process]['required_documents']])}

**Important Note:**
{GUIDES[process].get('completion_note', 'Your request has been submitted and will be processed by INEC.')}"""

            # Check if there's a pending service after revalidation
            if process == 'revalidation' and 'pending_service' in state:
                pending_service = state['pending_service']
                del state['pending_service']
                state['completed_processes'].append('revalidation')
                
                # Automatically proceed to the pending service
                state['current_process'] = pending_service
                state['current_step'] = 0
                
                continuation_text = f"""

🔄 **Now proceeding with your original request: {GUIDES[pending_service]['title']}**

{completion_text}

Let's continue with your {GUIDES[pending_service]['title'].lower()}:"""
                return send_step(pending_service, 0)
            else:
                # Regular completion
                completion_text += """

Would you like to:
• **Start over** with a new service
• Get help with something **else**
• **End** this conversation"""
                
                state['current_process'] = 'service-selection'
                state['current_step'] = 0
                state['completed_processes'].append(process)
                return jsonify({"reply": completion_text})
    
    # If user needs help, repeat current step
    elif any(word in user_message for word in ['no', 'help', 'not sure', "can't"]):
        current_step_data = steps[current_step]
        clarification = f"Let me help with this step:\n\n**Step {current_step_data['number']}:** {current_step_data['instruction']}"
        if 'question' in current_step_data:
            clarification += f"\n\n{current_step_data['question']}"
        return jsonify({"reply": clarification})
    
    # Default: continue with current step
    return send_step(process, current_step)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip().lower()
        
        if not user_message:
            return jsonify({"reply": "Please type a message so I can help you with INEC CVR services."})
        
        # Initialize session if not exists
        if 'conversation_state' not in session:
            session['conversation_state'] = {
                'current_process': 'universal-signup',
                'current_step': 0,
                'completed_processes': [],
                'pending_service': None
            }
        
        conversation_state = session['conversation_state']
        
        # Handle the conversation based on current state
        if conversation_state['current_process'] == 'universal-signup':
            response = handle_universal_signup(user_message, conversation_state)
        elif conversation_state['current_process'] == 'service-selection':
            response = handle_service_selection(user_message, conversation_state)
        else:
            response = handle_specific_service(user_message, conversation_state)
        
        session['conversation_state'] = conversation_state
        return response
        
    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"reply": "I apologize for the technical issue. Please refresh the page and try again."})

@app.route("/reset", methods=["POST"])
def reset_conversation():
    """Reset the conversation"""
    session.clear()
    return jsonify({"status": "success", "reply": "Conversation reset. How can I help you with INEC CVR services today?"})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)



@app.route("/telex/a2a", methods=["POST"])
def telex_a2a():
    """A2A endpoint for Telex.im integration"""
    try:
        data = request.json
        print("Telex A2A request received:", data)
        
        # Extract message from Telex
        message_text = data.get('message', {}).get('text', '').strip()
        session_id = data.get('sessionId', 'default-session')
        
        # Initialize session for Telex users
        if 'telex_sessions' not in session:
            session['telex_sessions'] = {}
        
        if session_id not in session['telex_sessions']:
            session['telex_sessions'][session_id] = {
                'current_process': 'universal-signup',
                'current_step': 0,
                'completed_processes': [],
                'awaiting_phone': False
            }
        
        # Get session state for this Telex user
        conversation_state = session['telex_sessions'][session_id]
        
        # Process the message using your existing logic
        if conversation_state['current_process'] == 'universal-signup':
            response = handle_universal_signup(message_text, conversation_state)
        elif conversation_state['current_process'] == 'service-selection':
            response = handle_service_selection(message_text, conversation_state)
        else:
            response = handle_specific_service(message_text, conversation_state)
        
        # Update session
        session['telex_sessions'][session_id] = conversation_state
        
        # Extract the reply text from the response
        if hasattr(response, 'json'):
            reply_data = response.json
            reply_text = reply_data.get('reply', 'Sorry, I encountered an error.')
        else:
            reply_text = response.get('reply', 'Sorry, I encountered an error.')
        
        # Format response for Telex A2A
        telex_response = {
            "reply": {
                "text": reply_text
            },
            "sessionId": session_id
        }
        
        return jsonify(telex_response)
        
    except Exception as e:
        print(f"Telex A2A error: {e}")
        error_response = {
            "reply": {
                "text": "I apologize, I'm having trouble processing your request. Please try again in a moment."
            },
            "sessionId": data.get('sessionId', 'default-session') if 'data' in locals() else 'error-session'
        }
        return jsonify(error_response)

@app.route("/telex/webhook", methods=["POST"])
def telex_webhook():
    """Webhook for receiving Telex events (delivery status, etc.)"""
    try:
        data = request.json
        print("Telex webhook event:", data)
        
        # Handle different webhook events
        event_type = data.get('type')
        
        if event_type == 'message_delivered':
            print("Message delivered successfully")
        elif event_type == 'message_read':
            print("Message was read by user")
        elif event_type == 'message_failed':
            print("Message failed to deliver")
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Telex webhook error: {e}")
        return jsonify({"status": "error"}), 500
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))