 

# 🎯 TalentMapper AI
### Autonomous business intelligence and talent signal detection

TalentMapper AI is a job discovery tool built for blue-collar and local service workers — a demographic underserved by platforms like LinkedIn and Indeed. Instead of relying on job postings, it autonomously finds businesses in any area, detects hiring signals from their websites, classifies HR contacts using a hybrid BERT + GraphRAG pipeline, and calculates a skill match percentage for each business. The result: direct access to HR emails and career pages for businesses that are actively hiring — no job board required.

Check out the project live at https://talentmapper-7jnxsrgvtf5hydg8dgz7e9.streamlit.app

---

## 🏗️ Pipeline Architecture

![TalentMapper Pipeline](https://github.com/user-attachments/assets/0a9c202d-42b4-42bf-b175-b081ed52ecd7)

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Language | Python 3.11 |
| AI / LLM | GPT-4o, Gemini 2.5 Pro, MiniLM-L6-v2, BERT |
| Classification | 78-pattern email scorer + 52-pattern URL classifier |
| Knowledge Graph | NetworkX + Neo4j + Supabase pgvector |
| NLP | spaCy NER, LangChain, LoRA/PEFT fine-tuning |
| Web Crawling | Playwright, Selenium, Crawl4AI, BeautifulSoup |
| Frontend | Streamlit — search, results, analytics dashboard |
| Deployment | Streamlit Cloud, GitHub Actions |

---

## ✨ Features

- **Natural language search** — type "cafe jobs in Chicago" or "pet groomer in Austin"
- **Radius filtering** — search within 1, 5, 10, or 25 miles
- **Skill matching** — select your skills, get a match % for every business
- **HR signal detection** — classifies emails as HR, Sales, or Ambiguous with confidence scores
- **Career page detection** — identifies hiring pages and external ATS systems
- **GraphRAG knowledge graph** — connects businesses, skills, emails, and hiring signals
- **Analytics dashboard** — aggregate metrics, charts, and signal distribution across all searches

---

## 🚀 Run Locally

```bash
git clone https://github.com/Kaanishkaa/talentmapper.git
cd talentmapper
pip install -r requirements.txt
streamlit run app.py
```

App runs in demo mode by default — all APIs mocked with realistic data. To use live APIs, copy `.env.example` to `.env` and add your keys.

---



---

*Built by [Kanishka Ghodke](https://linkedin.com/in/kanishka-ghodke)*
