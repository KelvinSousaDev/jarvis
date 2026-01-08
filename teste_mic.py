import speech_recognition as sr

print("🎤 Rastreando dispositivos de áudio...")
mics = sr.Microphone.list_microphone_names()

for i, nome in enumerate(mics):
    print(f"[{i}] - {nome}")

print("\n🦇 Procure o número do seu Headset/Microfone na lista acima.")