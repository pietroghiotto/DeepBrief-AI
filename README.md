# 🎙️ DeepBrief AI 

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gemini 2.5 Pro](https://img.shields.io/badge/Gemini-2.5_Pro-orange.svg)
![Perplexity](https://img.shields.io/badge/Perplexity-Sonar_Pro-black.svg)
![Automation](https://img.shields.io/badge/GitHub_Actions-Automated-success.svg)

**DeepBrief AI** è un agente autonomo che ogni mattina ricerca, scrive, doppia e ti invia su Telegram un podcast di 20 minuti sulle notizie più importanti del mondo dell'Intelligenza Artificiale e della Macroeconomia.

Niente spam, niente scrolling infinito: solo un riassunto vocale pronto per il tragitto casa-lavoro.

---

## 🚀 La Pipeline

L'architettura è modulare ed è divisa in 4 agenti specializzati:

1. 🔍 **Il Ricercatore (`researcher.py`)**: Interroga l'API di **Perplexity (Sonar-Pro)** per estrarre le 10 notizie più rilevanti delle ultime 24 ore, verificando le fonti e strutturando i dati in JSON.
2. ✍️ **Lo Sceneggiatore (`writer.py`)**: Sfrutta la context window di **Gemini 2.5 Pro** per generare uno script coeso di ~3000 parole usando la tecnica *Outline-to-Expansion*. Il tono è quello di un "Informed Colleague".
3. 🗣️ **Il Doppiatore (`audio_gen.py`)**: Utilizza `edge-tts` (voci neurali Microsoft) per sintetizzare l'audio in italiano con intonazioni umane e pause realistiche.
4. 📤 **Il Postino (`notifier.py`)**: Invia il file `.mp3` generato direttamente al tuo smartphone tramite un **Bot Telegram**.

Tutto questo viene orchestrato da `main.py` ed eseguito automaticamente ogni mattina alle 08:00 tramite **GitHub Actions**.
