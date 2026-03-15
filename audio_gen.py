import os
import yaml
import asyncio
import edge_tts
import shutil
from pydub import AudioSegment

AudioSegment.converter = shutil.which("ffmpeg")
class DeepBriefAudio:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.voice = self.config['podcast']['voice']
        self.output_dir = "segments"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def generate_segment(self, text, index):
        """Genera un singolo file MP3 per un paragrafo."""
        output_path = f"{self.output_dir}/seg_{index:03d}.mp3"
        communicate = edge_tts.Communicate(text, self.voice, rate="+5%") # più alto se vuoi più ritmo
        await communicate.save(output_path)
        return output_path

    def split_script(self, script):
        """Divide lo script in paragrafi basandosi sui doppi a capo."""
        paragraphs = [p.strip() for p in script.split("\n\n") if p.strip()]
        return paragraphs

    async def process_script(self, script_path="podcast_script.txt", output_name="deepbrief_final.mp3"):
        """Legge lo script, genera i segmenti e li unisce."""
        if not os.path.exists(script_path):
            print(f"❌ Errore: File {script_path} non trovato.")
            return

        with open(script_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        paragraphs = self.split_script(full_text)
        print(f"🎙️ Inizio generazione audio per {len(paragraphs)} paragrafi...")

        audio_files = []
        for i, p in enumerate(paragraphs):
            print(f"🔊 Generazione segmento {i+1}/{len(paragraphs)}...")
            path = await self.generate_segment(p, i)
            audio_files.append(path)

        self.merge_audio(audio_files, output_name=output_name)

    def merge_audio(self, files, output_name="deepbrief_final.mp3"):
        """Unisce tutti i segmenti MP3 in un unico file con silenzi naturali."""
        print("🏗️ Unione segmenti in corso...")
        combined = AudioSegment.empty()
        
        # Mezzo secondo di silenzio tra i paragrafi per naturalezza
        silence = AudioSegment.silent(duration=500) 

        for file in files:
            segment = AudioSegment.from_mp3(file)
            combined += segment + silence
            # Rimuoviamo il file temporaneo dopo averlo aggiunto
            os.remove(file)

        combined.export(output_name, format="mp3", bitrate="192k")
        print(f"✅ Podcast finale pronto: {output_name}")
        
        # Pulizia cartella temporanea
        os.rmdir(self.output_dir)

if __name__ == "__main__":
    generator = DeepBriefAudio()
    # Utilizziamo asyncio per eseguire la generazione asincrona di edge-tts
    asyncio.run(generator.process_script())