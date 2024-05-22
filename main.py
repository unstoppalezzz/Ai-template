import pyttsx3
import speech_recognition as sr
from datetime import datetime
from llama_cpp import Llama
import logging
import time

# Setup logging
logging.basicConfig(filename='ai_log.txt', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize Llama model
LLM = Llama(model_path=r"Put Your path to the ai here")

# Initialize the Recognizer
UserVoiceRecognizer = sr.Recognizer()

def get_time():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M')}"

def get_date():
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}"

def use_Ai(prompt):
    # Ensure the prompt is properly formatted
    prompt = prompt.strip()
    output = LLM(prompt)
    generated_text = output["choices"][0]["text"].strip()
    print(generated_text)
    logging.info(f"Generated: {generated_text}")
    engine.say(generated_text)
    engine.runAndWait()

def check_confirmation(prompt, question):
    # Ensure the prompt is properly formatted
    prompt = prompt.strip()
    response = LLM("Is asking '{prompt}' equivalent to asking '{question}'? Answer with yes or no.")
    return "yes" in response["choices"][0]["text"].lower()

class ConversationContext:
    def __init__(self):
        self.context = ""

    def update_context(self, new_input):
        self.context += f" {new_input}"

    def get_context(self):
        return self.context.strip()

    def reset_context(self):
        self.context = ""

context_manager = ConversationContext()

def main():
    conversation_started = False
    while True:
        try:
            with sr.Microphone() as source:
                UserVoiceRecognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = UserVoiceRecognizer.listen(source)
                text = UserVoiceRecognizer.recognize_google(audio).lower()
                print(f"Recognized: {text}")
                logging.info(f"Recognized: {text}")

            if "ai" in text:
                prompt = text.replace("ai", "").strip()
                conversation_started = True
                context_manager.update_context(prompt)
        #Commands for the Ai
                if "time" in prompt:
                    if check_confirmation(prompt, "What is the time?"):
                        response = get_time()
                        print(response)
                        logging.info(f"Response: {response}")
                        engine.say(response)
                        engine.runAndWait()
                        conversation_started = False
                        context_manager.reset_context()
                elif "date" in prompt:
                    if check_confirmation(prompt, "What is today's date?"):
                        response = get_date()
                        print(response)
                        logging.info(f"Response: {response}")
                        engine.say(response)
                        engine.runAndWait()
                        conversation_started = False
                        context_manager.reset_context()
                else:
                    use_Ai(context_manager.get_context() + " " + prompt)

                # Adding a short delay between repeated requests
                time.sleep(1)

        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
        except sr.RequestError as e:
            logging.error(f"Could not request results; {e}")
        except KeyboardInterrupt:
            logging.info("Exiting program.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
