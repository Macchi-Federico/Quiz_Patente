import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import os
import json
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Patente B")
        self.master.geometry("800x650")
        self.master.configure(bg="#f0f0f0")
        
        # Dati del quiz
        self.load_questions()
        self.score = 0
        self.question_index = 0
        self.answers = [None] * len(self.questions)  # Per memorizzare le risposte dell'utente
        self.start_time = 1800  # 30 minuti
        self.time_left = self.start_time
        self.quiz_active = True
        
        # Impostazione dell'interfaccia
        self.create_widgets()
        self.update_question()
        self.update_timer()
    
    def load_questions(self):
        # In un'applicazione reale, potresti caricare da un file JSON
        self.questions = [
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
        # Optional: Randomize questions
        random.shuffle(self.questions)
    
    def create_widgets(self):
        # Frame principale
        main_frame = tk.Frame(self.master, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame superiore per info
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.pack(fill=tk.X)
        
        # Timer e counter delle domande con stile migliorato
        self.timer_frame = tk.Frame(top_frame, bg="#e1e1e1", bd=1, relief=tk.RAISED)
        self.timer_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.timer_label = tk.Label(
            self.timer_frame, 
            text="30:00", 
            font=("Arial", 16, "bold"),
            bg="#e1e1e1",
            fg="#333333",
            padx=15,
            pady=10
        )
        self.timer_label.pack()
        
        self.question_counter = tk.Label(
            top_frame,
            text=f"Domanda 1 di {len(self.questions)}",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.question_counter.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Progressbar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            main_frame, 
            orient="horizontal", 
            length=760, 
            mode="determinate",
            variable=self.progress_var
        )
        self.progress.pack(fill=tk.X, pady=10)
        
        # Frame per la domanda e l'immagine
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Domanda
        self.question_label = tk.Label(
            content_frame,
            text="",
            wraplength=700,
            justify=tk.LEFT,
            font=("Arial", 14),
            bg="#f0f0f0",
            anchor="w"
        )
        self.question_label.pack(pady=20, fill=tk.X)
        
        # Frame per l'immagine
        self.image_frame = tk.Frame(content_frame, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        self.image_frame.pack(pady=20)
        
        self.image_label = tk.Label(self.image_frame, bg="#ffffff")
        self.image_label.pack(padx=5, pady=5)
        
        # Frame per i bottoni delle risposte
        response_frame = tk.Frame(main_frame, bg="#f0f0f0")
        response_frame.pack(fill=tk.X, pady=20)
        
        # Bottoni delle risposte
        self.true_button = tk.Button(
            response_frame,
            text="VERO",
            command=self.check_true,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.true_button.pack(side=tk.LEFT, padx=50)
        
        self.false_button = tk.Button(
            response_frame,
            text="FALSO",
            command=self.check_false,
            width=20,
            height=2,
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.false_button.pack(side=tk.RIGHT, padx=50)
        
        # Frame per la navigazione
        nav_frame = tk.Frame(main_frame, bg="#f0f0f0")
        nav_frame.pack(fill=tk.X, pady=10)
        
        self.prev_button = tk.Button(
            nav_frame,
            text="← Precedente",
            command=self.prev_question,
            width=15,
            bg="#e0e0e0",
            font=("Arial", 10)
        )
        self.prev_button.pack(side=tk.LEFT, padx=10)
        
        self.next_button = tk.Button(
            nav_frame,
            text="Successiva →",
            command=self.next_question,
            width=15,
            bg="#e0e0e0",
            font=("Arial", 10)
        )
        self.next_button.pack(side=tk.RIGHT, padx=10)
        
        # Bottone per terminare il quiz
        self.finish_button = tk.Button(
            main_frame,
            text="Termina Quiz",
            command=self.end_quiz,
            width=20,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold")
        )
        self.finish_button.pack(pady=10)
    
    def update_question(self):
        if 0 <= self.question_index < len(self.questions):
            question_text, correct_answer, image_path = self.questions[self.question_index]
            self.question_label.config(text=question_text)
            self.question_counter.config(text=f"Domanda {self.question_index + 1} di {len(self.questions)}")
            self.load_image(image_path)
            self.correct_answer = correct_answer
            
            # Aggiorna la progressbar
            self.progress_var.set(100 * (self.question_index + 1) / len(self.questions))
            
            # Evidenzia il bottone se la domanda è già stata risposta
            self.update_button_states()
    
    def load_image(self, image_path):
        try:
            # Controllo se l'immagine esiste
            if os.path.exists(image_path):
                img = Image.open(image_path)
                # Mantenere proporzioni ma con dimensione massima
                img.thumbnail((300, 300))
                self.img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.img_tk)
                self.image_label.image = self.img_tk
            else:
                # Immagine segnaposto se non esiste
                self.image_label.config(image='', text="Immagine non disponibile")
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine: {e}")
            self.image_label.config(image='', text="Errore immagine")
    
    def update_button_states(self):
        # Reset lo stato dei bottoni
        self.true_button.config(bg="#4CAF50")
        self.false_button.config(bg="#F44336")
        
        # Se la domanda è già stata risposta, evidenzia la risposta data
        if self.answers[self.question_index] is not None:
            if self.answers[self.question_index]:
                self.true_button.config(bg="#81C784")  # Verde più chiaro
            else:
                self.false_button.config(bg="#E57373")  # Rosso più chiaro
    
    def check_true(self):
        if not self.quiz_active:
            return
        
        self.answers[self.question_index] = True
        if self.correct_answer == True:
            self.score += 1
        self.update_button_states()
        self.master.after(500, self.next_question)  # Passa alla prossima domanda dopo mezzo secondo
    
    def check_false(self):
        if not self.quiz_active:
            return
        
        self.answers[self.question_index] = False
        if self.correct_answer == False:
            self.score += 1
        self.update_button_states()
        self.master.after(500, self.next_question)
    
    def next_question(self):
        if self.question_index < len(self.questions) - 1:
            self.question_index += 1
            self.update_question()
    
    def prev_question(self):
        if self.question_index > 0:
            self.question_index -= 1
            self.update_question()
    
    def update_timer(self):
        if not self.quiz_active:
            return
            
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            # Cambia colore quando rimane poco tempo
            if self.time_left < 300:  # Meno di 5 minuti
                self.timer_label.config(fg="#F44336")  # Rosso
                if self.time_left % 2 == 0 and self.time_left < 60:  # Lampeggia negli ultimi 60 secondi
                    self.timer_frame.config(bg="#FFCDD2")
                else:
                    self.timer_frame.config(bg="#e1e1e1")
            
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="00:00", fg="#F44336")
            self.end_quiz()
    
    def show_results(self):
        # Crea una nuova finestra per i risultati
        results_window = tk.Toplevel(self.master)
        results_window.title("Risultati Quiz")
        results_window.geometry("600x500")
        results_window.configure(bg="#f0f0f0")
        
        # Calcola esito
        passed = self.score >= (len(self.questions) - 4)  # Criterio di superamento (esempio)
        
        # Frame principale
        main_frame = tk.Frame(results_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titolo
        result_title = tk.Label(
            main_frame,
            text="RISULTATI QUIZ PATENTE B",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        result_title.pack(pady=10)
        
        # Frame per il punteggio
        score_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.RAISED)
        score_frame.pack(fill=tk.X, pady=20, padx=50)
        
        # Punteggio
        result_text = f"Hai risposto correttamente a {self.score} domande su {len(self.questions)}"
        result_label = tk.Label(
            score_frame,
            text=result_text,
            font=("Arial", 14),
            bg="#ffffff",
            pady=15
        )
        result_label.pack()
        
        # Valutazione
        if passed:
            outcome_text = "ESAME SUPERATO!"
            color = "#4CAF50"
        else:
            outcome_text = "ESAME NON SUPERATO"
            color = "#F44336"
            
        outcome_label = tk.Label(
            score_frame,
            text=outcome_text,
            font=("Arial", 16, "bold"),
            fg=color,
            bg="#ffffff",
            pady=10
        )
        outcome_label.pack()
        
        # Mostra dettagli delle risposte
        details_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(details_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrollable content
        canvas = tk.Canvas(details_frame, bg="#ffffff", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Frame inside canvas for details
        details_content = tk.Frame(canvas, bg="#ffffff")
        canvas.create_window((0, 0), window=details_content, anchor=tk.NW)
        
        # Popola con dettagli delle risposte
        for i, (question, correct_answer, _) in enumerate(self.questions):
            user_answer = self.answers[i]
            
            question_frame = tk.Frame(details_content, bg="#ffffff", bd=1, relief=tk.GROOVE)
            question_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Testo domanda
            q_label = tk.Label(
                question_frame,
                text=f"D{i+1}: {question}",
                wraplength=450,
                justify=tk.LEFT,
                anchor="w",
                bg="#ffffff",
                font=("Arial", 10)
            )
            q_label.pack(fill=tk.X, padx=5, pady=5)
            
            # Risposta dell'utente e correttezza
            is_correct = user_answer == correct_answer
            result_color = "#4CAF50" if is_correct else "#F44336"
            
            answer_text = "La tua risposta: "
            if user_answer is None:
                answer_text += "Non risposta"
            elif user_answer:
                answer_text += "VERO"
            else:
                answer_text += "FALSO"
                
            answer_text += f" (Risposta corretta: {'VERO' if correct_answer else 'FALSO'})"
            
            a_label = tk.Label(
                question_frame,
                text=answer_text,
                fg=result_color,
                bg="#ffffff",
                anchor="w",
                font=("Arial", 9, "bold" if is_correct else "normal")
            )
            a_label.pack(fill=tk.X, padx=5, pady=3)
        
        # Update scrollregion after all items are added
        details_content.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Bottom buttons
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=10)
        
        retry_btn = tk.Button(
            btn_frame,
            text="Riprova Quiz",
            command=lambda: [results_window.destroy(), self.restart_quiz()],
            bg="#2196F3",
            fg="white",
            font=("Arial", 11),
            padx=10
        )
        retry_btn.pack(side=tk.LEFT, padx=20)
        
        close_btn = tk.Button(
            btn_frame,
            text="Chiudi",
            command=results_window.destroy,
            bg="#e0e0e0",
            font=("Arial", 11),
            padx=10
        )
        close_btn.pack(side=tk.RIGHT, padx=20)
    
    def end_quiz(self):
        if not self.quiz_active:
            return
            
        # Chiedi conferma solo se non sono state risposte tutte le domande
        unanswered = self.answers.count(None)
        if unanswered > 0:
            confirm = messagebox.askyesno(
                "Termina Quiz",
                f"Ci sono ancora {unanswered} domande senza risposta.\nSei sicuro di voler terminare il quiz?"
            )
            if not confirm:
                return
        
        self.quiz_active = False
        self.show_results()
    
    def restart_quiz(self):
        # Resetta il quiz
        self.score = 0
        self.question_index = 0
        self.answers = [None] * len(self.questions)
        self.time_left = self.start_time
        self.quiz_active = True
        
        # Mescola le domande
        random.shuffle(self.questions)
        
        # Aggiorna l'interfaccia
        self.update_question()
        self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
