import os
import yaml
import json
from openai import OpenAI

class DeepBriefResearcher:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.client = OpenAI(
            api_key=self.config['api_keys']['perplexity'],
            base_url="https://api.perplexity.ai"
        )

    def fetch_latest_news(self):
        """
        Versione super-compatibile: rimosso response_format per evitare errore 400.
        """
        system_prompt = (
            "Sei un analista esperto di DeepBrief AI. "
            "Rispondi ESCLUSIVAMENTE con un oggetto JSON puro. "
            "Non includere riflessioni, non usare markdown come ```json."
        )

        user_prompt = f"""
        Trova le {self.config['researcher']['news_count_ai']} news AI e 
        le {self.config['researcher']['news_count_econ']} news Economia più importanti delle ultime 24 ore.
        
        Usa questo schema JSON:
        {{
          "ai_news": [{{ "title": "...", "summary": "...", "url": "..." }}],
          "economy_news": [{{ "title": "...", "summary": "...", "url": "..." }}]
        }}
        """

        try:
            print("🔍 Ricerca news in corso su Perplexity...")
            
            # CHIAMATA PULITA: Senza response_format
            response = self.client.chat.completions.create(
                model=self.config['researcher']['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            
            raw_content = response.choices[0].message.content
            
            # Pulizia di sicurezza se il modello aggiunge ```json o testo extra
            clean_content = raw_content.strip()
            if "```" in clean_content:
                clean_content = clean_content.split("```")[1]
                if clean_content.startswith("json"):
                    clean_content = clean_content[4:]
            
            news_data = json.loads(clean_content)
            
            print(f"✅ Ricerca completata con successo.")
            return news_data

        except Exception as e:
            print(f"❌ Errore durante la ricerca: {e}")
            if 'raw_content' in locals():
                print(f"DEBUG - Risposta grezza del server: {raw_content[:200]}...")
            return None

    def save_to_file(self, data, filename="latest_research.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"💾 Ricerca salvata in {filename}")

if __name__ == "__main__":
    researcher = DeepBriefResearcher()
    results = researcher.fetch_latest_news()
    if results:
        researcher.save_to_file(results)