import requests
import os
import yaml

class TelegramNotifier:
    def __init__(self, config_path="config.yaml"):
        config_data = {'api_keys': {}} 
        
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
                
        self.token = os.getenv('TELEGRAM_BOT_TOKEN') or config_data['api_keys'].get('telegram_bot_token')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID') or config_data['api_keys'].get('telegram_chat_id')

    def send_audio(self, file_path, caption="🎙️ Nuovo episodio di DeepBrief AI pronto!"):
        if not self.token or not self.chat_id:
            print("⚠️ Telegram non configurato. Salto l'invio.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': self.chat_id, 'caption': caption}
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
            print("✅ Podcast inviato con successo a Telegram!")
        except Exception as e:
            print(f"❌ Errore nell'invio a Telegram: {e}")

            # ... (il resto del tuo codice TelegramNotifier) ...

if __name__ == "__main__":
    import yaml
    
    # 1. Carica le tue credenziali dal config
    print("⚙️ Caricamento config per il test...")
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    # 2. Crea il file di test (se non hai già un .mp3 pronto)
    test_filename = "deepbrief_final.mp3"
    
    # Se hai già un file mp3 vero generato prima, commenta le 4 righe sopra 
    # e cambia la variabile qui sotto con il nome del tuo file:
    # test_filename = "il_tuo_vero_audio.mp3"

    # 3. Testa l'invio
    print("🚀 Inizializzazione TelegramNotifier...")
    notifier = TelegramNotifier(config)
    notifier.send_audio(test_filename, caption="🧪 Test di isolamento: Invio da DeepBrief AI funzionante!")
    
    print("✅ Test concluso.")