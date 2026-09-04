import json
from app.database.session import SessionLocal, engine, Base
from app.models.models import ProjectTemplate, User, GitHubAccount

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Demo User
        existing_user = db.query(User).filter(User.username == "demo_developer").first()
        if not existing_user:
            user = User(
                username="demo_developer",
                email="developer@devtimeline.io",
                github_user_id="dev_12345",
                avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            github_acc = GitHubAccount(
                user_id=user.id,
                github_user_id="dev_12345",
                username="demo_developer"
            )
            db.add(github_acc)
            db.commit()
            print("[OK] Default User & GitHub Account seeded successfully.")

        # 2. Seed Built-In Templates
        templates_data = [
            # Beginner
            {
                "name": "Personal Developer Portfolio",
                "slug": "personal-portfolio",
                "description": "High-performance developer portfolio showcasing projects, experience timeline, responsive design, interactive micro-animations, and contact form.",
                "difficulty": "BEGINNER",
                "category": "Frontend",
                "tech_stack": "Next.js, TypeScript, Tailwind CSS, Framer Motion",
                "estimated_days": 14,
                "repository_template": "devtimeline-templates/portfolio",
                "features": json.dumps(["Hero Section", "Projects Showcase", "Interactive Resume", "Dark/Light Theme", "Contact API"])
            },
            {
                "name": "Modern Todo & Productivity Suite",
                "slug": "todo-app",
                "description": "Comprehensive task management application featuring drag-and-drop kanban boards, priority tagging, analytics dashboard, and local storage sync.",
                "difficulty": "BEGINNER",
                "category": "Fullstack",
                "tech_stack": "React, TypeScript, Zustand, Tailwind CSS",
                "estimated_days": 14,
                "repository_template": "devtimeline-templates/todo-app",
                "features": json.dumps(["Kanban Board", "Priority Matrix", "Time Tracking", "Export Data"])
            },

            # Intermediate
            {
                "name": "E-Commerce Commerce Platform",
                "slug": "ecommerce-platform",
                "description": "Full-stack digital storefront with product catalog search, inventory management, shopping cart, Stripe payment gateway, and admin dashboard.",
                "difficulty": "INTERMEDIATE",
                "category": "Fullstack",
                "tech_stack": "Next.js, FastAPI, PostgreSQL, Tailwind CSS, Stripe",
                "estimated_days": 30,
                "repository_template": "devtimeline-templates/ecommerce",
                "features": json.dumps(["Product Catalog", "Cart & Checkout", "Order Tracking", "Admin Panel", "JWT Auth"])
            },
            {
                "name": "Real-Time Chat & Collaboration App",
                "slug": "chat-application",
                "description": "Real-time communication app supporting channels, direct messaging, WebSocket connections, file attachments, and online presence indicators.",
                "difficulty": "INTERMEDIATE",
                "category": "Fullstack",
                "tech_stack": "React, FastAPI, WebSockets, Redis, Tailwind CSS",
                "estimated_days": 30,
                "repository_template": "devtimeline-templates/chat-app",
                "features": json.dumps(["WebSockets Messaging", "Channel Rooms", "File Sharing", "User Status"])
            },

            # Advanced
            {
                "name": "Network Intrusion Detection System (IDS)",
                "slug": "intrusion-detection-system",
                "description": "Machine-learning driven network packet analyzer detecting suspicious traffic, malicious anomalies, signatures, and real-time alert visualization.",
                "difficulty": "ADVANCED",
                "category": "Security / AI",
                "tech_stack": "Python, Scapy, PyTorch, FastAPI, React, Chart.js",
                "estimated_days": 60,
                "repository_template": "devtimeline-templates/ids",
                "features": json.dumps(["Packet Sniffing Engine", "ML Anomaly Classifier", "Real-Time Threat Dashboard", "Alert Rules Engine"])
            },
            {
                "name": "AI Assistant Chatbot Platform",
                "slug": "ai-chatbot-platform",
                "description": "Enterprise-grade RAG AI chatbot platform with document vector search, prompt history, multi-persona engine, and customizable LLM pipelines.",
                "difficulty": "ADVANCED",
                "category": "AI / ML",
                "tech_stack": "Next.js, Python, FastAPI, LangChain, FAISS, OpenAI/Gemini",
                "estimated_days": 45,
                "repository_template": "devtimeline-templates/ai-chatbot",
                "features": json.dumps(["RAG Vector Search", "Multi-Persona Engine", "Document Upload Parsing", "API Rate Limiting"])
            }
        ]

        for t_data in templates_data:
            existing_template = db.query(ProjectTemplate).filter(ProjectTemplate.slug == t_data["slug"]).first()
            if not existing_template:
                template = ProjectTemplate(**t_data)
                db.add(template)
                print(f"[OK] Seeded template: {t_data['name']}")
        
        db.commit()
        print("[OK] All project templates seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
