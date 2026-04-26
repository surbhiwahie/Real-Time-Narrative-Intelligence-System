# Real-Time-Narrative-Intelligence-System

This project is a real-time narrative intelligence pipeline that collects YouTube data, extracts thematic signals, and analyzes shifts in global discourse. It simulates a lightweight data engineering system that detects emerging narratives across topics such as AI, politics, geopolitics, science, and crime.

The system is designed to demonstrate:

a. Data ingestion from external APIs (YouTube Data API)

b. Stream-style processing pipeline

c. Rule-based narrative classification

d. Temporal trend tracking

e. AI-assisted narrative summarization


The system follows a modular data pipeline:
YouTube API (Producer) -> Raw Video Titles -> Processor (Signal Extraction) -> Storage Layer (Stateful History) -> Trend Engine (Comparative Analysis) -> AI Insight Layer (Narrative Summary) -> Final Output Dashboard (CLI)


youtube_producer.py (data ingestion):

This module is responsible for data ingestion from the YouTube Data API. It acts as the entry point of the pipeline, fetching recent video titles based on configurable search queries. The goal of this layer is to simulate real-time external data ingestion while keeping it decoupled from downstream processing logic. By isolating API interaction in this module, the system remains flexible and extensible for adding additional data sources in the future.

processor.py (signal extraction):

The processor module transforms raw text data into structured narrative signals. It applies keyword-based classification to map video titles into predefined thematic categories such as politics, technology, science, crime, geopolitics, and AI narratives. In addition to classification, it computes signal strength and distribution, enabling the system to quantify which narratives are dominating at any given time.

storage.py (state tracking):

This module provides a lightweight persistence layer that stores historical narrative signals across runs. By maintaining state, it enables temporal comparisons and trend detection. Instead of treating each execution as independent, the system evolves into a stateful pipeline capable of identifying rising, falling, or stable narratives over time.

main.py (trend computation):

The main module orchestrates the entire pipeline by connecting all components together. It controls the execution flow from data ingestion to processing, storage, trend computation, and final output generation. This separation ensures that business logic and orchestration remain centralized, making the system easier to maintain, debug, and extend.

ai_insights.py (semantic interpretation):

This module introduces an AI layer that converts quantitative trend data into human-readable insights. Using a language model, it interprets changes in narrative signals and generates structured summaries, including trend explanations and executive-level observations. This bridges the gap between raw data and decision-making by transforming metrics into meaningful narratives.

Features:

a. Real-time YouTube data ingestion

b. Multi-topic narrative detection

c. Temporal trend analysis (current vs previous runs)

d. AI-generated narrative summaries

e. Modular pipeline design (producer → processor → storage → AI layer)


Setup Instructions: 

1. Clone repository
   
```
git clone https://github.com/your-username/real-time-narrative-intelligence-system.git

cd Real-Time-Narrative-Intelligence-System 
```

2. Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Setup environment variables: 
Create a .env file:
```
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key
```

5. Run the system
```
python3 main.py
```

Output Example:
```
TECH -> STRONG SIGNAL
AI_NARRATIVE -> EMERGING SIGNAL
POLITICS -> WEAK SIGNAL
GEOPOLITICS -> WEAK SIGNAL
```
Plus AI-generated narrative interpretation.
