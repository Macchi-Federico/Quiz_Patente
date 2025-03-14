import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

# Lista di domande e risposte (domanda, risposta corretta, immagine)

questions = [
    ("Il segnale di stop è un triangolo con il vertice rivolto verso l'alto?", False, 'img/Dare_precedenza.png'),
    ("La velocità massima in autostrada è di 130 km/h?", True, 'img/foto_130.png'),
    ("Il semaforo rosso indica di fermarsi?", True, 'img/semaforo.png'),
    ("È possibile sorpassare in curva?", False, 'img/curva.png'),
    ("Il conducente deve sempre allacciare la cintura di sicurezza?", True, 'img/cintura.png'),
    ("Il limite di velocità in città è generalmente di 50 km/h, ma può essere ridotto in zone scolastiche?", True, 'img/50km.png'),
    ("È possibile circolare con pneumatici invernali durante l'estate se si viaggia in montagna?", False, 'img/ruote.png'),
    ("Il segnale di divieto di sorpasso è valido solo in tratti di strada con doppia linea continua?", True, 'img/sorpasso.png'),
    ("Il conducente deve segnalare sempre le manovre, anche se non ci sono veicoli nelle vicinanze?", True, 'img/segnaletiche.png'),
    ("Il limite di velocità su strade extraurbane è di 90 km/h, ma può essere aumentato in caso di strade a scorrimento veloce?", True, 'img/90km.png'),
    ("È vietato trasportare passeggeri su un motociclo senza casco, anche se si viaggia a bassa velocità?", True, 'img/moto.png'),
    ("Il segnale di divieto di transito è valido solo per i veicoli a motore?", False, 'img/vuoto.png'),
    ("Il conducente deve sempre mantenere la destra, anche in caso di traffico intenso?", True, 'img/auto.png'),
    ("È possibile utilizzare i fari abbaglianti in presenza di nebbia se non ci sono altri veicoli?", False, 'img/abbaglianti.png'),
]

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Patente B")
        
        self.score = 0
        self.question_index = 0
        self.start_time = 1800  # tempo in secondi
        self.time_left = self.start_time
        
        # Creazione dei widget
        self.timer_label = tk.Label(master, text="Tempo rimasto: 1800")
        self.timer_label.pack()
        
        self.question_label = tk.Label(master, text="", wraplength=300)
        self.question_label.pack(pady=20)
        
        # Widget per l'immagine
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=20)
        
        self.true_button = tk.Button(master, text="VERO", command=self.check_true)
        self.true_button.pack(side=tk.LEFT, padx=200, pady=20)
        
        self.false_button = tk.Button(master, text="FALSO", command=self.check_false)
        self.false_button.pack(side=tk.RIGHT, padx=200, pady=20)
        
        self.next_button = tk.Button(master, text="Prossima Domanda", command=self.next_question)
        self.next_button.pack(pady=20)
        
        self.last_button = tk.Button(master, text="Domanda Precedente", command=self.last_question)
        self.last_button.pack(pady=20)
        
        self.update_question()
        self.update_timer()

    def update_question(self):
        if self.question_index < len(questions):
            question_text, correct_answer, image_path = questions[self.question_index]
            self.question_label.config(text=question_text)
            self.load_image(image_path)
            self.correct_answer = correct_answer  # Salva la risposta corretta per il controllo
        else:
            self.end_quiz()

    def load_image(self, image_path):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((200, 200))  # Cambia la dimensione come necessario
                self.img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.img_tk)
                self.image_label.image = self.img_tk  # Mantieni un riferimento all'immagine
            except Exception as e:
                print(f"Errore nel caricamento dell'immagine: {e}")
                self.image_label.config(image='')  # Nascondi l'immagine se c'è un errore
        else:
            self.image_label.config(image='')  # Nascondi l'immagine se non c'è

    def check_true(self):
        if self.correct_answer == True:
            self.score += 1
        self.next_question()

    def check_false(self):
        if self.correct_answer == False:
            self.score += 1
        self.next_question()

    def next_question(self):
        self.question_index += 1
        self.update_question()
        
    def last_question(self):
        if self.question_index > 0:  # Controllo per non scendere sotto zero
            self.question_index -= 1
            self.update_question()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Tempo rimasto: {self.time_left}")
            self.master.after(1000, self.update_timer)
        else:
            self.end_quiz()

    def end_quiz(self):
        messagebox.showinfo("Quiz Terminato", f"Hai totalizzato {self.score} punti su {len(questions)}.")
        self.true_button.config(state=tk.DISABLED)
        self.false_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.last_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = QuizApp(root)
    root.mainloop()