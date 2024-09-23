import os
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

device = "cuda"  # the device to load the model onto

# Now you do not need to add "trust_remote_code=True"
tokenizer = AutoTokenizer.from_pretrained('/home/yinrigao/models/qwen25_coder_7b')
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=1024)
# MODEL = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Coder-7B", device_map="auto").eval()
MODEL = LLM(model="/home/yinrigao/models/qwen25_coder_7b")

# tokenize the input into tokens
input_text = """<|repo_name|>library-system
<|file_sep|>library.py
class Book:
    def __init__(self, title, author, isbn, copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Copies: {self.copies}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn, copies):
        book = Book(title, author, isbn, copies)
        self.books.append(book)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def list_books(self):
        return self.books

<|file_sep|>student.py
class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.borrowed_books = []

    def borrow_book(self, book, library):
        if book and book.copies > 0:
            self.borrowed_books.append(book)
            book.copies -= 1
            return True
        return False

    def return_book(self, book, library):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.copies += 1
            return True
        return False

<|file_sep|>main.py
from library import Library
from student import Student

def main():
    # Set up the library with some books
    library = Library()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890", 3)
    library.add_book("To Kill a Mockingbird", "Harper Lee", "1234567891", 2)

    # Set up a student
    student = Student("Alice", "S1")

    # Student borrows a book
"""
# model_inputs = TOKENIZER([input_text], return_tensors="pt").to(device)
message = [
    {"role": "system", "content": "你是一个python专家，请根据已有的代码情况，补全已经写好注释但还没完成的代码。"},
    {"role": "user", "content": input_text}
]
text = tokenizer.apply_chat_template(
    message,
    tokenize=False,
    add_generation_prompt=True
)
# Use `max_new_tokens` to control the maximum output length.
# generated_ids = MODEL.generate(model_inputs.input_ids)[0]
outputs = MODEL.generate([text], sampling_params)
# The generated_ids include prompt_ids, so we only need to decode the tokens after prompt_ids.
# output_text = TOKENIZER.decode(generated_ids[len(model_inputs.input_ids[0]):], skip_special_tokens=True)
# output_text = TOKENIZER.decode(generated_ids[len(model_inputs.input_ids[0]):], skip_special_tokens=True)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: \n{input_text}\n\nGenerated text: \n{generated_text}")
    print(f"Prompt: \n{prompt}")
# print(f"Prompt: \n{input_text}\n\nGenerated text: \n{res}")
