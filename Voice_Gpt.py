import openai
import pyttsx3
import speech_recognition as sr
import time

# Temp: Set API Key
openai.api_key = "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"

# Init the text-to-speeach engine
engine = pyttsx3.init()


def transscribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_token=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        # Wait for the user to say "fait" (first AI TTS )
        print("Say 'Genius' to start you question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "genius":
                # Record audio
                filename = "input.wav"
                print("Say your question...")
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(
                        source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                        # Transcribe audio to text
                        text = transscribe_audio_to_text(filename)
                        if text:
                            print(f"You said: {text}")

                            # Generate response using GPT
                            response = generate_response(text)
                            print(f"GPT-3 says: {response}")

                            # Read reponse using text-to-speech
                            speak_text(response)
        except Exception as e:
            print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()
