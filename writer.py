import os
import yaml
import json
import time
import google.generativeai as genai
from google.api_core import exceptions

class DeepBriefWriter:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        genai.configure(api_key=self.config['api_keys']['gemini'])
        
        self.system_instruction = (
            "Sei Marco, l'host di 'DeepBrief AI'. Il tuo stile è 'Informed Colleague'. "
            "Analogie brillanti, niente liste puntate, paragrafi narrativi fluidi. Parla in italiano."
        )

        # Utilizziamo gemini-1.5-flash che solitamente ha quote free più generose del 2.0
        self.model_name = 'gemini-2.5-flash'
        print(f"🎯 Utilizzo modello: {self.model_name}")
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )

    def safe_generate(self, prompt, retries=3, delay=35):
        """Genera contenuti gestendo l'errore di Quota (429)."""
        for i in range(retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except exceptions.ResourceExhausted:
                print(f"⏳ Quota raggiunta. Attendo {delay} secondi prima di riprovare (Tentativo {i+1}/{retries})...")
                time.sleep(delay)
            except Exception as e:
                print(f"❌ Errore imprevisto: {e}")
                time.sleep(5)
        return "Errore: impossibile generare il contenuto dopo diversi tentativi."

    def generate_refined_outline(self, news_data):
        print("📝 Generazione arco narrativo...")
        prompt = f"Analizza queste news: {json.dumps(news_data)}\nCrea un indice di 5 sezioni numerate per il podcast. Solo i titoli."
        raw_text = self.safe_generate(prompt)
        
        lines = [line.strip() for line in raw_text.split('\n') if len(line.strip()) > 5]
        outline = [line.lstrip('0123456789.-*# ') for line in lines][:6]
        
        if not outline:
            return ["Intro", "AI News", "Econ News", "Analisi", "Outro"]
        return outline

    def expand_section_verbose(self, section_title, news_context, section_index, total_sections, previous_text=""):
        prompt = f"""
        SEZIONE: {section_title} ({section_index + 1}/{total_sections})
        NOTIZIE: {json.dumps(news_context)}
        PRECEDENTE: {previous_text[-600:]}
        SCRIVI IL COPIONE: Almeno 600 parole in stile parlato. Niente markdown.
        """
        return self.safe_generate(prompt)

    def write_full_podcast(self, news_data):
        outline = self.generate_refined_outline(news_data)
        full_script = []
        cumulative_text = ""

        print(f"🎙️ Inizio scrittura script ({len(outline)} sezioni)...")

        for i, section in enumerate(outline):
            print(f"✍️ Scrittura capitolo {i+1}: {section}...")
            section_content = self.expand_section_verbose(section, news_data, i, len(outline), cumulative_text)
            full_script.append(section_content)
            cumulative_text += section_content + "\n\n"
            
            words = len(cumulative_text.split())
            print(f"📊 Word count attuale: {words} parole")
            
            # Pausa precauzionale tra le sezioni per non saturare la quota
            if i < len(outline) - 1:
                print("☕ Breve pausa per rispettare i limiti API...")
                time.sleep(20) 

        return cumulative_text

    def save_script(self, script, filename="podcast_script.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"✅ Script salvato in {filename}")