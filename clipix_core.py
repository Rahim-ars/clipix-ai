# clipix_core.py - SECURE VERSION
import json
import os
import re
import time
from collections import defaultdict
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv  # ADD THIS

# Load environment variables from .env file
load_dotenv()

class ClipixAI:
    def __init__(self):
        print("🧠 CLIPIX AI - Secure Version...")
        
        # File paths
        self.knowledge_file = "ai_knowledge.json"
        self.documents_folder = "documents"
        
        # Knowledge storage
        self.knowledge_base = defaultdict(list)
        self.fact_timestamps = {}
        self.memory_cache = {}
        
        # APIs - FROM ENVIRONMENT VARIABLES (SECURE)
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = os.getenv('SEARCH_ENGINE_ID')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        self.google_enabled = bool(self.google_api_key and self.search_engine_id)
        self.deepseek_enabled = bool(self.deepseek_api_key)
        
        # Create folders
        self._setup_folders()
        self.load_knowledge()
        
        print(f"✅ Clipix AI Ready! {len(self.knowledge_base)} topics")
        if self.google_enabled:
            print("🔍 Google Search: Enabled (Secure)")
        else:
            print("⚠️ Google Search: Not configured - add to .env file")
        if self.deepseek_enabled:
            print("🧠 DeepSeek: Enabled (Secure)")
    
    def _setup_folders(self):
        folders = [
            self.documents_folder,
            os.path.join(self.documents_folder, "technology"),
            os.path.join(self.documents_folder, "science"), 
            os.path.join(self.documents_folder, "history"),
            os.path.join(self.documents_folder, "mathematics"),
            os.path.join(self.documents_folder, "literature"),
            os.path.join(self.documents_folder, "general"),
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def load_knowledge(self):
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.knowledge_base = defaultdict(list, data.get('knowledge_base', {}))
                self.fact_timestamps = data.get('fact_timestamps', {})
                self._clean_old_knowledge()
                self._build_memory_cache()
                print(f"📚 Loaded knowledge: {len(self.knowledge_base)} topics")
        except Exception as e:
            print(f"❌ Knowledge load error: {e}")
            self.knowledge_base = defaultdict(list)
            self.fact_timestamps = {}
    
    def _clean_old_knowledge(self):
        current_time = datetime.now()
        expiration_days = 30
        topics_to_clean = ['sports', 'news', 'current', 'technology', 'politics']
        for category in topics_to_clean:
            if category in self.knowledge_base:
                updated_facts = []
                for fact in self.knowledge_base[category]:
                    fact_key = f"{category}_{fact[:50]}"
                    if fact_key in self.fact_timestamps:
                        fact_time = datetime.fromisoformat(self.fact_timestamps[fact_key])
                        if (current_time - fact_time).days < expiration_days:
                            updated_facts.append(fact)
                        else:
                            print(f"🗑️ Removed outdated fact: {fact[:50]}...")
                    else:
                        updated_facts.append(fact)
                        self.fact_timestamps[fact_key] = datetime.now().isoformat()
                self.knowledge_base[category] = updated_facts
    
    def _build_memory_cache(self):
        self.memory_cache = {}
        for category, facts in self.knowledge_base.items():
            for fact in facts:
                words = fact.lower().split()
                for word in words:
                    if len(word) > 3:
                        if word not in self.memory_cache:
                            self.memory_cache[word] = []
                        self.memory_cache[word].append(fact)
    
    def _is_time_sensitive_question(self, question):
        question_lower = question.lower()
        time_sensitive_keywords = [
            'current', 'now', 'today', 'recent', 'latest', 'new', 'nowadays',
            'who is', 'what is happening', 'breaking', 'news', 'update',
            'coach', 'manager', 'president', 'prime minister', 'ceo',
            'score', 'result', 'winner', 'election', 'appointed'
        ]
        sports_teams = [
            'tottenham', 'spurs', 'arsenal', 'chelsea', 'manchester', 'liverpool',
            'real madrid', 'barcelona', 'bayern', 'psg'
        ]
        return (any(keyword in question_lower for keyword in time_sensitive_keywords) or
                any(team in question_lower for team in sports_teams))
    
    def chat(self, question):
        start_time = time.time()
        
        if not self._is_time_sensitive_question(question):
            memory_result = self._instant_memory_search(question)
            if memory_result:
                memory_time = time.time() - start_time
                return f"🤖 {memory_result} ⚡({memory_time:.3f}s)"
        
        if self.google_enabled:
            google_start = time.time()
            if self._is_time_sensitive_question(question):
                search_query = self._get_aggressive_current_query(question)
                result = self._fast_google_search(search_query, "recent_aggressive")
            else:
                result = self._fast_google_search(question, "standard")
            
            if result and "error" not in result.lower():
                if not self._is_time_sensitive_question(question):
                    self._learn_from_response(question, result)
                total_time = time.time() - start_time
                return f"🔍 {result} ⚡({total_time:.2f}s)"
        
        if self.deepseek_enabled:
            deepseek_start = time.time()
            deepseek_result = self._ask_deepseek(question)
            deepseek_time = time.time() - deepseek_start
            
            if deepseek_result and "error" not in deepseek_result.lower():
                if not self._is_time_sensitive_question(question):
                    self._learn_from_response(question, deepseek_result)
                total_time = time.time() - start_time
                return f"🧠 {deepseek_result} ⚡({total_time:.2f}s)"
        
        total_time = time.time() - start_time
        return f"🤖 I don't know about that yet. Try teaching me! ⚡({total_time:.2f}s)"
    
    def _get_aggressive_current_query(self, question):
        current_year = datetime.now().year
        return f"{question} {current_year} latest news update today"
    
    def _instant_memory_search(self, question):
        if self._is_time_sensitive_question(question):
            return None
        question_lower = question.lower()
        question_words = set(question_lower.split())
        best_match = None
        best_score = 0
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'tell', 'me', 'about'}
        meaningful_words = [word for word in question_words if word not in stop_words and len(word) > 3]
        for word in meaningful_words:
            if word in self.memory_cache:
                for fact in self.memory_cache[word]:
                    if not self._is_fact_time_sensitive(fact):
                        score = self._calculate_relevance(question_lower, fact.lower())
                        if score > best_score:
                            best_score = score
                            best_match = fact
        return best_match if best_score > 3 else None
    
    def _is_fact_time_sensitive(self, fact):
        fact_lower = fact.lower()
        time_sensitive_indicators = [
            '2021', '2022', '2023', '2024', 'coach', 'manager', 'appointed',
            'tottenham', 'conte', 'kane', 'contract'
        ]
        return any(indicator in fact_lower for indicator in time_sensitive_indicators)
    
    def _calculate_relevance(self, question, fact):
        score = 0
        q_words = set(question.split())
        f_words = set(fact.split())
        common_words = q_words.intersection(f_words)
        score += len(common_words) * 2
        return score
    
    def save_knowledge(self):
        try:
            data = {
                'knowledge_base': dict(self.knowledge_base),
                'fact_timestamps': self.fact_timestamps,
                'metadata': {
                    'total_facts': sum(len(facts) for facts in self.knowledge_base.values()),
                    'total_topics': len(self.knowledge_base),
                    'last_updated': datetime.now().isoformat()
                }
            }
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._build_memory_cache()
        except Exception as e:
            print(f"❌ Knowledge save error: {e}")
    
    def _fast_google_search(self, query, search_type="standard"):
        if not self.google_enabled:
            return "Google Search not configured"
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,  # FROM ENV VARIABLE
                'cx': self.search_engine_id, # FROM ENV VARIABLE
                'q': query,
                'num': 5
            }
            response = requests.get(url, params=params, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    best_result = self._find_most_recent_result(data['items'], query)
                    if best_result:
                        return f"{best_result['title']}: {best_result['snippet']}"
                    else:
                        first_item = data['items'][0]
                        return f"{first_item['title']}: {first_item['snippet']}"
                else:
                    return "No results found"
            else:
                return f"Google Error: {response.status_code}"
        except Exception as e:
            return f"Google unavailable: {str(e)}"
    
    def _find_most_recent_result(self, items, query):
        current_year = datetime.now().year
        scored_results = []
        for item in items:
            score = 0
            title = item.get('title', '').lower()
            snippet = item.get('snippet', '').lower()
            if str(current_year) in title or str(current_year) in snippet:
                score += 20
            if any(term in title or term in snippet for term in ['2024', '2025', 'latest', 'current']):
                score += 10
            scored_results.append((score, item))
        if scored_results:
            scored_results.sort(key=lambda x: x[0], reverse=True)
            return scored_results[0][1]
        return None
    
    def _ask_deepseek(self, question):
        if not self.deepseek_enabled:
            return "DeepSeek not configured"
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",  # FROM ENV
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": question}],
                "max_tokens": 500,
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"DeepSeek Error: {response.status_code}"
        except Exception as e:
            return f"DeepSeek unavailable: {str(e)}"
    
    def _learn_from_response(self, question, response):
        category = self._categorize_question(question)
        if len(response) > 30 and len(response) < 500:
            self.knowledge_base[category].append(response)
            fact_key = f"{category}_{response[:50]}"
            self.fact_timestamps[fact_key] = datetime.now().isoformat()
            words = response.lower().split()
            for word in words:
                if len(word) > 3:
                    if word not in self.memory_cache:
                        self.memory_cache[word] = []
                    self.memory_cache[word].append(response)
            self.save_knowledge()
    
    def _categorize_question(self, question):
        question_lower = question.lower()
        categories = {
            'technology': ['computer', 'programming', 'software', 'hardware', 'code', 'ai', 'tech'],
            'science': ['physics', 'chemistry', 'biology', 'scientific', 'research', 'space'],
            'history': ['history', 'historical', 'war', 'ancient', 'century', 'battle'],
            'mathematics': ['math', 'calculus', 'algebra', 'equation', 'geometry', 'calculate'],
        }
        for category, keywords in categories.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        return 'general'
    
    def train_from_documents(self):
        print("📚 Training from organized documents...")
        all_documents = []
        for root, dirs, files in os.walk(self.documents_folder):
            for file in files:
                if file.endswith(('.txt', '.md')):
                    full_path = os.path.join(root, file)
                    all_documents.append((full_path, os.path.basename(root)))
        if not all_documents:
            print("❌ No documents found. Add files to documents/ folder")
            return 0
        total_facts = 0
        for doc_path, folder_name in all_documents:
            facts = self._process_document(doc_path, folder_name)
            total_facts += len(facts)
            print(f"   ✅ {os.path.basename(doc_path)}: {len(facts)} facts")
        self.save_knowledge()
        print(f"🎯 Training complete! Added {total_facts} facts")
        return total_facts
    
    def _process_document(self, file_path, category):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            facts = self._extract_facts(content, category)
            for fact in facts:
                self.knowledge_base[category].append(fact)
            return facts
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return []
    
    def _extract_facts(self, content, category):
        facts = []
        paragraphs = re.split(r'\n\s*\n', content)
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) < 50:
                continue
            if len(paragraph) > 200:
                sentences = re.split(r'[.!?]+', paragraph)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if self._is_meaningful(sentence):
                        facts.append(sentence)
            else:
                if self._is_meaningful(paragraph):
                    facts.append(paragraph)
        return facts
    
    def _is_meaningful(self, text):
        return len(text) >= 20 and len(text) <= 500 and len(text.split()) >= 5
    
    def get_stats(self):
        total_facts = sum(len(facts) for facts in self.knowledge_base.values())
        return {
            'total_facts': total_facts,
            'topics': {topic: len(facts) for topic, facts in self.knowledge_base.items()},
            'deepseek_enabled': self.deepseek_enabled,
            'google_enabled': self.google_enabled
        }