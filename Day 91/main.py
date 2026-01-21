import time

import PyPDF2
from deepgram import DeepgramClient
import os
from dotenv import load_dotenv

def extract_text_from_pdf(file: str) -> [str]:
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        text = []

        for page in reader.pages:
            extracted = page.extract_text()
            text.append(extracted)

        return text

def split_text_by_sentences(text, max_len=2000):
    if len(text) <= max_len:
        return [text]

    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_len:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def text_to_mp3(text, base_filename="output"):

    load_dotenv()
    client = DeepgramClient(api_key=os.getenv("API_KEY_SPEECH"))

    text_chunks = split_text_by_sentences(text, max_len=1000)

    for i, chunk in enumerate(text_chunks):
        print(f"Converting part {i + 1}/{len(text_chunks)} ({len(chunk)} symbols)...")

        response = client.speak.v1.audio.generate(
            text=chunk,
            encoding="mp3",
            model="aura-2-andromeda-en"
        )
        filename = f"{base_filename}_part_{i + 1}.mp3"

        with open(filename, "wb") as audio_file:
            for data_chunk in response:
                audio_file.write(data_chunk)
        print(f"Saving: {filename}")

        time.sleep(1)

if __name__ == '__main__':

    extracted_text = "".join(extract_text_from_pdf("sample.pdf")) #also there is "example.pdf" in project folder

    if extracted_text:
        text_to_mp3(extracted_text)