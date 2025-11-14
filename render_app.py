# render_app.py - OPTIMIZED FOR MOBILE APP
from flask import Flask, request, jsonify
from flask_cors import CORS
from clipix_core import SmartClipixAI
import os
import time

app = Flask(__name__)
CORS(app)

# Initialize AI
print("🚀 Initializing Clipix AI for Mobile App...")
start_time = time.time()
ai = SmartClipixAI()
load_time = time.time() - start_time
print(f"✅ AI Ready in {load_time:.2f}s with {len(ai.all_facts)} facts")

@app.route('/')
def home():
    return jsonify({
        "message": "Clipix AI Mobile API", 
        "status": "running",
        "facts": len(ai.all_facts),
        "load_time": f"{load_time:.2f}s"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_id = data.get('userId', 'anonymous')
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'response': '🤖 Please send a message'})
        
        print(f"📱 [{user_id}]: {message}")
        
        # Get AI response
        response = ai.quick_chat(message)
        
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
        
        return jsonify({
            'success': True,
            'message': f'✅ Learned: {fact[:50]}...',
            'topic': topic,
            'total_facts': len(ai.all_facts)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        'total_facts': len(ai.all_facts),
        'total_topics': len(ai.knowledge_base),
        'topics': {topic: len(facts) for topic, facts in ai.knowledge_base.items()}
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Clipix AI Mobile API',
        'facts': len(ai.all_facts),
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)