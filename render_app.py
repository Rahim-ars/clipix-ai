# render_app.py - FIXED VERSION
from flask import Flask, request, jsonify
from flask_cors import CORS
from clipix_core import ClipixAI  # CHANGED FROM SmartClipixAI to ClipixAI
import os
import time

app = Flask(__name__)
CORS(app)

# Initialize AI
print("🚀 Initializing Clipix AI for Mobile App...")
start_time = time.time()
ai = ClipixAI()  # CHANGED FROM SmartClipixAI() to ClipixAI()
load_time = time.time() - start_time

# Get stats - UPDATED METHOD
stats = ai.get_stats()
print(f"✅ AI Ready in {load_time:.2f}s with {stats['total_facts']} facts")

@app.route('/')
def home():
    stats = ai.get_stats()
    return jsonify({
        "message": "Clipix AI Mobile API", 
        "status": "running",
        "facts": stats['total_facts'],
        "load_time": f"{load_time:.2f}s"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_id = data.get('userId', 'default')
        user_message = data.get('message', '')
        conversation_history = data.get('conversationHistory', [])
        
        print(f"📨 {user_id}: {user_message}")
        print(f"📝 History: {conversation_history[-2:] if conversation_history else 'None'}")
        
        # Get AI response - UPDATED METHOD
        response = ai.chat(user_message)  # CHANGED FROM quick_chat_with_memory to chat
        
        print(f"🤖 AI: {response}")
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'response': '🤖 Sorry, I encountered an error'})

@app.route('/api/teach', methods=['POST'])
def teach():
    try:
        data = request.get_json()
        topic = data.get('topic', 'general').strip()
        fact = data.get('fact', '').strip()
        
        if not fact:
            return jsonify({'success': False, 'error': 'No fact provided'})
        
        ai.add_knowledge(topic, fact)
        
        # Get updated stats
        stats = ai.get_stats()
        
        return jsonify({
            'success': True,
            'message': f'✅ Learned: {fact[:50]}...',
            'topic': topic,
            'total_facts': stats['total_facts']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats', methods=['GET'])
def stats():
    stats = ai.get_stats()
    return jsonify({
        'total_facts': stats['total_facts'],
        'total_topics': len(stats['topics']),
        'topics': stats['topics'],
        'google_enabled': stats['google_enabled'],
        'deepseek_enabled': stats['deepseek_enabled']
    })

@app.route('/health', methods=['GET'])
def health():
    stats = ai.get_stats()
    return jsonify({
        'status': 'healthy',
        'service': 'Clipix AI Mobile API',
        'facts': stats['total_facts'],
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
