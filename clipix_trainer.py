# clipix_trainer.py - FIXED MAIN CALL
import os
import time
from clipix_core import ClipixAI


class ClipixTrainer:
    def __init__(self):
        print("⚡ CLIPIX TRAINER - Loading...")
        self.ai = ClipixAI()
        print("✅ Trainer Ready!")
    
    def show_menu(self):
        """Show main menu options"""
        print("\n" + "="*50)
        print("🤖 CLIPIX AI TRAINING MENU")
        print("="*50)
        print("1. 📚 Train from Documents")
        print("2. 💡 Teach Manually") 
        print("3. 🧪 Test AI")
        print("4. 📊 Show Statistics")
        print("5. 💬 Chat with AI")
        print("6. ⚙️  Configure APIs")
        print("7. 🚪 Exit")
        print("="*50)
    
    def train_from_documents(self):
        """Option 1: Train from documents"""
        print("\n📚 TRAINING FROM DOCUMENTS")
        print("This will process all files in the 'documents' folder")
        
        confirm = input("Continue? (y/n): ").lower()
        if confirm == 'y':
            self.ai.train_from_documents()
        else:
            print("Training cancelled.")
    
    def teach_manually(self):
        """Option 2: Manual teaching"""
        print("\n💡 MANUAL TEACHING")
        
        print("\nAvailable categories:")
        categories = ['programming', 'science', 'technology', 'mathematics', 'history', 'geography', 'literature', 'general']
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        try:
            cat_choice = int(input("\nChoose category (1-8): ")) - 1
            if 0 <= cat_choice < len(categories):
                category = categories[cat_choice]
            else:
                category = "general"
                print("Invalid choice, using 'general'")
        except:
            category = "general"
            print("Invalid input, using 'general'")
        
        fact = input("Enter fact to teach: ").strip()
        if fact:
            self.ai.add_knowledge(category, fact)
            self.ai.save_knowledge()
            print(f"✅ Added to '{category}': {fact}")
        else:
            print("❌ No fact entered.")
    
    def test_ai(self):
        """Option 3: Test the AI"""
        print("\n🧪 TESTING AI")
        print("Type 'back' to return to menu")
        
        while True:
            question = input("\n❓ Question: ").strip()
            if question.lower() == 'back':
                break
            if question:
                response = self.ai.chat(question)
                print(f"🤖 {response}")
    
    def show_statistics(self):
        """Option 4: Show statistics"""
        stats = self.ai.get_stats()
        
        print("\n📊 AI KNOWLEDGE STATISTICS")
        print("="*30)
        print(f"Total Facts: {stats['total_facts']}")
        print(f"Google Search: {'✅ Enabled' if stats['google_enabled'] else '❌ Disabled'}")
        print(f"DeepSeek: {'✅ Enabled' if stats['deepseek_enabled'] else '❌ Disabled'}")
        
        if stats['topics']:
            print("\n📁 Topics:")
            for topic, count in stats['topics'].items():
                print(f"  {topic}: {count} facts")
    
    def chat_with_ai(self):
        """Option 5: Interactive chat"""
        print("\n💬 CHAT WITH AI")
        print("Type 'quit' to end chat")
        print("Speed: Memory → Google → DeepSeek")
        
        while True:
            message = input("\n👤 You: ").strip()
            if message.lower() == 'quit':
                break
            if message:
                response = self.ai.chat(message)
                print(f"🤖 {response}")
    
    def configure_apis(self):
        """Option 6: Configure APIs"""
        print("\n⚙️ API CONFIGURATION")
        print("1. Configure Google Search")
        print("2. Configure DeepSeek")
        print("3. Back to menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            self.configure_google()
        elif choice == '2':
            self.configure_deepseek()
    
    def configure_google(self):
        """Configure Google Search"""
        print("\n🔍 GOOGLE SEARCH SETUP")
        print("Free: 100 searches/day")
        print("Get API Key from: https://console.cloud.google.com/")
        print("Get Search Engine ID from: https://cse.google.com/cse/")
        
        api_key = input("\nGoogle API Key: ").strip()
        search_id = input("Search Engine ID: ").strip()
        
        if api_key and search_id:
            self.ai.google_api_key = api_key
            self.ai.search_engine_id = search_id
            self.ai.google_enabled = True
            self.ai.save_config()
            print("✅ Google Search configured! (100 free searches/day)")
        else:
            print("❌ Both API Key and Search Engine ID are required.")
    
    def configure_deepseek(self):
        """Configure DeepSeek"""
        print("\n🧠 DEEPSEEK API SETUP")
        print("Get API Key from: https://platform.deepseek.com/")
        
        api_key = input("DeepSeek API Key: ").strip()
        if api_key:
            self.ai.deepseek_api_key = api_key
            self.ai.deepseek_enabled = True
            self.ai.save_config()
            print("✅ DeepSeek API configured!")
    
    def run(self):
        """Main training loop"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\n🎯 Select option (1-7): ").strip()
                
                if choice == '1':
                    self.train_from_documents()
                elif choice == '2':
                    self.teach_manually()
                elif choice == '3':
                    self.test_ai()
                elif choice == '4':
                    self.show_statistics()
                elif choice == '5':
                    self.chat_with_ai()
                elif choice == '6':
                    self.configure_apis()
                elif choice == '7':
                    print("👋 Thank you for using Clipix AI!")
                    break
                else:
                    print("❌ Invalid option. Please choose 1-7.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Session interrupted.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


# FIXED: Make sure main() is called properly
if __name__ == "__main__":
    print("🚀 Starting Clipix AI Trainer...")
    trainer = ClipixTrainer()
    trainer.run()