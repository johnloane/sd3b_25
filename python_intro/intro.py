import pyttsx3
import speech_recognition
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
import qrcode
import os
from google import genai
from dotenv import load_dotenv, find_dotenv


def main():
    talk_to_gemini()  


def say_hello():
    engine = pyttsx3.init()
    name = input("What is your name? ")
    engine.say(f"Hello, {name}")
    engine.runAndWait()
    
    
def my_speech_recognition():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Say something: ")
        audio = recognizer.listen(source)
        print("You said: ")
        print(recognizer.recognize_google(audio))


def find_faces():
    image = face_recognition.load_image_file("sd3b_25.jpg")
    face_locations = face_recognition.face_locations(image)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        

def find_dylan():
    known_image = face_recognition.load_image_file("dylan_linkedin.jpg")
    encoding = face_recognition.face_encodings(known_image)[0]
    unknown_image = face_recognition.load_image_file("sd3b_25.jpg")
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    for(top, right, bottom, left), face_encodings in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([encoding], face_encodings)
        face_distances = face_recognition.face_distance([encoding], face_encodings)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            draw.rectangle(((left-20, top - 20), (right+20, bottom+20)), outline=(0, 255, 0), width=20)
    del draw 
    pil_image.show()
    
    
def find_individual_face_in_group(individual_face_image, group_image):
    known_face = face_recognition.load_image_file(individual_face_image)
    known_face_encoding = face_recognition.face_encodings(known_face)[0]
    image_to_search = face_recognition.load_image_file(group_image)
    face_locations = face_recognition.face_locations(image_to_search)
    face_encodings = face_recognition.face_encodings(image_to_search, face_locations)
    pil_image = Image.open(group_image)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), face_encodings in zip(
        face_locations, face_encodings
    ):
        matches = face_recognition.compare_faces([known_face_encoding], face_encodings)
        face_distances = face_recognition.face_distance(
            [known_face_encoding], face_encodings
        )
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=5)
    del draw
    pil_image.show()
    
    
def test_qrcode():
    img = qrcode.make("https://github.com/johnloane/sd3b_25")
    img.save("qr.png", "PNG")

   
def talk_to_gemini():
    _ = load_dotenv(find_dotenv())
    gemini_api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=gemini_api_key)
    llm_model = "gemini-2.5-flash"
    system_prompt = "You are a logical and supportive lecturer at DkIT who likes to be succinct. If you don't know the answer, please just say you don't know. Please only deal with questions about college and DkIT"
    question = input("What would you like to know: ")
    llm_content = system_prompt + question
    
    response = client.models.generate_content(model=llm_model, contents=llm_content)
    print(response.text)
    
    
        

if __name__ == "__main__":
    main()
