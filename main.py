# main.py
import asyncio
import requests
from researcher import DeepBriefResearcher
from writer import DeepBriefWriter
from audio_gen import DeepBriefAudio
from notifier import TelegramNotifier

async def run_deepbrief_pipeline():
    print("--- 🚀 AVVIO DEEPBRIEF AI ---")
    
    # 1. Ricerca
    researcher = DeepBriefResearcher()
    news_data = researcher.fetch_latest_news()
    if not news_data:
        print("Errore nella ricerca. Esco.")
        return

    # 2. Scrittura Script
    writer = DeepBriefWriter()
    script = writer.write_full_podcast(news_data) # <--- Deve essere questo nome
    writer.save_script(script)

    # 3. Generazione Audio
    audio_gen = DeepBriefAudio()
    await audio_gen.process_script()

    # 4. Notifica Telegram
    notifier = TelegramNotifier(config)
    notifier.send_audio(audio_file)

    print("--- ✨ PODCAST GENERATO CON SUCCESSO ---")

if __name__ == "__main__":
    asyncio.run(run_deepbrief_pipeline())