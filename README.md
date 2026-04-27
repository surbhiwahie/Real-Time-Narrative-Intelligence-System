# Real-Time Narrative Intelligence System

A real-time data intelligence pipeline that ingests YouTube video metadata (titles and topic-level content), classifies content into narrative themes, tracks temporal shifts in discourse, and generates AI-powered insights through a live dashboard.

 **Live Demo:**  
https://realtimeelectionvotingcapstoneproject-c3jnxdumrjkwtwqiscdip9.streamlit.app/

---

# Project Overview

Modern media ecosystems are driven by rapidly shifting narratives — politics, AI, geopolitics, technology, and crime dominate attention in fluctuating patterns.

This system builds an **end-to-end narrative intelligence pipeline** that:

- Collects real-time YouTube video metadata
- Extracts narrative signals using keyword-based classification
- Tracks how narratives evolve over time
- Computes trend dynamics (rise, fall, stability)
- Generates AI-based analytical summaries
- Visualizes everything in a live Streamlit dashboard

---

# Problem Definition

We aim to answer:

> “What topics are dominating attention right now, and how are they changing over time?”

This is not a static classification problem — it is a **temporal narrative tracking system**.

---

# System Architecture

<img width="1536" height="1024" alt="Architechture diagram - Real-Time Narrative" src="https://github.com/user-attachments/assets/84a9131b-45e6-468f-be13-907cd49507e9" />


The system is composed of 5 major layers:

## 1. Data Ingestion Layer
- File: `youtube_producer.py`
- Fetches video titles from YouTube Data API
- Supports caching and fallback mechanisms

### Output:
Raw video titles

---

## 2. Processing Layer (Narrative Engine)
- File: `processor.py`
- Performs keyword-based classification across categories:

### Narrative Categories:
- Politics
- Crime
- Science
- Tech
- AI Narrative
- Geopolitics

Each title is scanned and mapped to one or more categories.

---

## 3. Intelligence Layer (Trend Analysis)
- Compares current signal counts with historical data stored in SQLite
- Computes:
  - Current count
  - Previous average
  - Absolute change
  - Trend strength (%)

This enables detection of:
- Rising narratives
- Falling narratives
- Stable narratives

---

## 4. Storage Layer
- File: `storage.py`
- SQLite database (`narrative.db`)

Stores:
- timestamp
- topic
- count

Purpose:
- Enables historical comparison
- Builds temporal memory of narrative shifts

---

## 5. Presentation Layer
- File: `app.py` (Streamlit)

Provides:
- Real-time bar charts of narrative distribution
- Trend comparison vs historical averages
- Top narratives ranking
- AI-generated narrative summary
- Auto-refreshing live dashboard

---

# User Interface (Streamlit Dashboard)

When running the system, users see:

###  Narrative Distribution
- Bar chart of topic frequencies

###  Trend Analysis
- Comparison of current vs historical averages

###  Top Narratives
- Ranked list of dominant topics

###  AI Insights
- Natural language interpretation of trends
- Summary of rising/falling narratives

---

# Installation & Setup

## 1. Clone repository
```bash
git clone https://github.com/surbhiwahie/Real-Time-Narrative-Intelligence-System.git
cd Real-Time-Narrative-Intelligence-System
```
2. Install dependencies
```
pip install -r requirements.txt
```

3. Add environment variables

Create a .env file:
```
YOUTUBE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key
```

4. Run Streamlit app
```
streamlit run app.py
```
[Narrative Intelligence-new.pdf](https://github.com/user-attachments/files/27107475/Narrative.Intelligence-new.pdf)

<img width="1457" height="822" alt="image" src="https://github.com/user-attachments/assets/39bd84b5-873f-4b20-9bbd-61f20aa1a844" />

<img width="1462" height="828" alt="image" src="https://github.com/user-attachments/assets/4aa004dd-8163-4d62-a380-1351da1d7650" />

<img width="1447" height="820" alt="image" src="https://github.com/user-attachments/assets/a48e1ae6-bd6b-4ff0-aef7-088ecc1c3ff8" />









