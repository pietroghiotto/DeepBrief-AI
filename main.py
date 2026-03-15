# main.py
import asyncio
import requests
from datetime import datetime
from researcher import DeepBriefResearcher
from writer import DeepBriefWriter
from audio_gen import DeepBriefAudio
from notifier import TelegramNotifier

async def run_deepbrief_pipeline():
    print("--- 🚀 AVVIO DEEPBRIEF AI ---")
    
    date = datetime.now().strftime("%Y-%m-%d")
    nome_podcast = f"DeepBrief {date}.mp3"
    
    # 1. Ricerca
    researcher = DeepBriefResearcher()
    news_data = researcher.fetch_latest_news()
    if not news_data:
        print("Errore nella ricerca. Esco.")
        return

    # 2. Scrittura Script
    writer = DeepBriefWriter()
    script = writer.write_full_podcast(news_data)
    writer.save_script(script)

    # 3. Generazione Audio
    audio_gen = DeepBriefAudio()
    await audio_gen.process_script(output_name=nome_podcast)

    # 4. Notifica Telegram
    notifier = TelegramNotifier() 
    notifier.send_audio(nome_podcast)

    print("--- ✨ PODCAST GENERATO CON SUCCESSO ---")

if __name__ == "__main__":
    asyncio.run(run_deepbrief_pipeline())