import google.generativeai as genai
import os
genai.configure(api_key='exampleapikey')



def create_file(file_name: str):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write("Yeni dosya oluşturuldu.\n")  # Başlangıç içeriği
        return f"{file_name} dosyası başarıyla oluşturuldu."
    return f"{file_name} dosyası zaten mevcut."

def read_file(file_name: str) -> str:
    """Reads the content of a file and returns it."""
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            content = file.read()
        return content
    return f"{file_name} dosyası bulunamadı."

def write_to_file(file_name: str, content: str) -> str:
    """Writes the given content to a file, appending it if necessary."""
    with open(file_name, 'a', newline='\n') as file:  # Explicitly set newline handling
        file.write(content + "\n")  # Adding a newline after each write
    return f"{file_name} dosyasına içerik eklendi."



def multiply(a: float, b: float):
    """Multiplies two numbers and returns the result."""
    return {"result": a * b}

def add(a: float, b: float):
    """Adds two numbers and returns the result."""
    return {"result": a + b}

def subtract(a: float, b: float):
    """Subtracts the second number from the first and returns the result."""
    return {"result": a - b}

def divide(a: float, b: float):
    """Divides the first number by the second and returns the result."""
    if b == 0:
        return {"error": "Division by zero is not allowed."}
    return {"result": a / b}



model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp", tools=[multiply, add, subtract, divide,create_file,read_file,write_to_file],
    system_instruction=(
        "You are a helpful assistant. "
        "sen bugunun tarihini biliyorsun"
        "When the user provides numbers or math-related questions, "
        "call the appropriate function to perform calculations. "
        "If the user requests to create a file, read a file, or write to a file, "
        "use the appropriate functions to handle file operations. "
        "Do not explain intermediate steps unless asked. "
        "Provide answers in a short and clear format."
        "If the user says 'exit' or 'ai exit',. say exit end the conversation if response text longer than 'exit word' do not make an exit"
        "if ı sade write a example  fable any file you should write the fable to the file sentence by sentence."
    )
)
chat = model.start_chat(enable_automatic_function_calling=True)

# Kullanıcıdan sürekli mesaj al
print("Gemini Asistanına Hoş Geldiniz! Çıkmak için 'exit' yazın. Geçmişi görmek için 'history' yazın.\n")

while True:
    # Kullanıcıdan mesaj al
    user_input = input("Kullanıcı: ")


    # Sohbet geçmişini gösterme kontrolü
    if user_input.lower() == "history":
        print("\nSohbet Geçmişi:")
        for content in chat.history:
            for part in content.parts:
                # Her bir part nesnesinin türünü yazdırıyoruz
                print(f"Part türü: {type(part)}")

                # Eğer bir metin varsa, text'i yazdırıyoruz
                if hasattr(part, 'text'):
                    print(f"Metin: {part.text}")

                # Eğer bir fonksiyon çağrısı varsa, fonksiyon adını ve argümanlarını yazdırıyoruz
                if hasattr(part, 'function_call'):
                    print(f"Fonksiyon çağrısı: {part.function_call.name}, Argümanlar: {part.function_call.args}")

                # Eğer bir fonksiyon yanıtı varsa, sonucu doğru şekilde yazdırıyoruz
                if hasattr(part, 'function_response'):
                    # FunctionResponse içeriğine doğrudan erişiyoruz
                    if hasattr(part.function_response, 'result'):
                        print(f"Fonksiyon yanıtı: {part.function_response.result}")
                    else:
                        print("Fonksiyon yanıtı: Sonuç yok")

                print("-" * 80)
        continue

    # Mesajı modele gönder
    response = chat.send_message(user_input)

    # Model yanıtını ekrana yazdır
    print("Asistan:", response.text)
    # Eğer AI 'exit' ya da 'ai exit' dediyse, görüşmeyi sonlandır
    if "exit" in response.text.lower() or "ai exit" in response.text.lower():
        print("AI tarafından görüşme sonlandırıldı. Görüşmek üzere!")
        break
