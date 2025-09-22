# 📅 PlanTask AI  

**PlanTask AI** is an open-source, AI-powered daily planner designed for **students and early-career professionals**.  
It helps you manage **studies, projects, and career growth** by generating adaptive daily schedules.  

If you miss a task, PlanTask AI automatically **reschedules and reprioritizes**, so you stay on track without the overwhelm.  

---

## ✨ Features
- 📝 Add tasks with title, duration, priority, and deadline  
- ⏱ Generate a realistic daily schedule with time blocks  
- 🔄 Reschedule missed tasks to the next day  
- 🎯 Mark tasks as complete  
- 📊 (Coming soon) Daily reflections and AI-powered task breakdowns  

---

## 🛠 Tech Stack
- **Python 3.9+**  
- **JSON** for local task storage  
- (Future) OpenAI API for natural input & smart planning  
- (Future) FastAPI + React for web app  

---

## 🚀 Roadmap
- [x] CLI MVP — task input, scheduling, mark complete  
- [ ] Smart rescheduling for missed tasks  
- [ ] AI integration (natural input, task breakdowns)  
- [ ] FastAPI backend  
- [ ] Web UI (React/Streamlit)  
- [ ] Integrations (Google Calendar, Notion)  

---

## 📂 Project Structure
```bash
plantask-ai/
├── planner.py # Core CLI logic
├── tasks.json # Task storage
├── requirements.txt # Dependencies
├── .gitignore # Ignore unnecessary files
├── LICENSE # MIT license
└── README.md # Project documentation
```

## ⚡ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR-USERNAME/plantask-ai.git
cd plantask-ai
```

### 2. Create virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
### 3. Install dependencies
bash
Copy code
pip install -r requirements.txt
### 4. Run the planner
bash
python planner.py




## 🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss your idea.

## 📜 License
This project is licensed under the MIT License — free to use and modify.