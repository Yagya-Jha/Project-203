import socket
import threading
import random

questions=[]
answers=[]

def get_random_question_answer(client_socket):
    questions = [
        "What is the capital of France?\n(a) Paris\n(b) Rome\n(c) Madrid\n(d) London\n",
        "What is the currency of Japan?\n(a) Yen\n(b) Yuan\n(c) Dollar\n(d) Euro\n",
        "What is the highest mountain in the world?\n(a) Mount Everest\n(b) Mount Kilimanjaro\n(c) Mount Fuji\n(d) Mount Rushmore\n",
        "Who is the founder of Microsoft?\n(a) Steve Jobs\n(b) Jeff Bezos\n(c) Bill Gates\n(d) Mark Zuckerberg\n",
        "What is the largest country in the world?\n(a) Russia\n(b) Canada\n(c) China\n(d) USA\n"
    ]
    answers = ["a", "a", "a", "c", "a"]

    random_index = random.randint(0, len(questions)-1)
    question = questions[random_index]
    answer = answers[random_index]

    client_socket.send(question.encode('utf-8'))
    return random_index, question, answer

def clientthread(conn, addr):
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(1024).decode('utf-8')
    print(nickname, "has joined the game.")
    
    score = 0
    conn.send("Welcome to the quiz game! Here are the instructions:\n\n\
        1. You will receive multiple choice questions.\n\
        2. Send your answer by entering the corresponding letter.\n\
        3. There will be 5 questions in total.\n\
        4. Good luck!\n\n".encode('utf-8'))

    for i in range(5):
        question_index, question, answer = get_random_question_answer(conn)
        while True:
            client_response = conn.recv(1024).decode('utf-8').lower()
            print(client_response)

            if client_response == answer:
                score += 1
                conn.send("Correct! Your score is now {}.\n".format(score).encode('utf-8'))
                break
            elif client_response == "":
                continue
            else:
                conn.send("Incorrect. The correct answer was {}\n".format(answer).encode('utf-8'))
                break
        if len(questions)>0 and len(answers)>0:
            questions.pop(question_index)
            answers.pop(question_index)

    conn.send("Game over! Your final score is {}.\n".format(score).encode('utf-8'))
    conn.close()

host = '127.0.0.1'
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print("Server started...(at", host, ":", port,")")

clients = []
while True:
    try:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(target=clientthread, args=(conn, addr)).start()
    except:
        print("\n")