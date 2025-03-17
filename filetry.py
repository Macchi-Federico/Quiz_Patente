import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image

# Lista di domande e risposte (domanda, risposta corretta, immagine)
domande = [
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
    ("È obbligatorio avere un estintore a bordo di un veicolo?", True, 'img/estintore.png'),
    ("Il segnale di precedenza è un triangolo con il vertice rivolto verso il basso?", True, 'img/Dare_precedenza.png'),
    ("È possibile utilizzare il cellulare mentre si guida se si utilizza un auricolare?", False, 'img/cellulare.png'),
    ("Il conducente deve rispettare il semaforo anche se non ci sono veicoli in circolazione?", True, 'img/semaforo.png'),
    ("Il limite di velocità per i neopatentati è di 100 km/h in autostrada?", False, 'img/neopatentati.png'),
    ("Un veicolo deve sempre dare la precedenza ai pedoni sulle strisce?", True, 'img/pedoni.png'),
    ("È consentito sorpassare a destra in autostrada?", False, 'img/sorpasso_destra.png'),
    ("Il segnale di stop deve essere rispettato anche se non ci sono veicoli in arrivo?", True, 'img/stop.png'),
    ("La distanza di sicurezza deve essere mantenuta sempre, indipendentemente dalla velocità?", True, 'img/distanza_sicurezza.png'),
    ("È vietato circolare in contromano su strade a senso unico?", True, 'img/contromano.png'),
    ("Un veicolo commerciale può superare il limite di peso se viaggia su strade extraurbane?", False, 'img/veicolo_commerciale.png'),
    ("È possibile parcheggiare in seconda fila se non ci sono posti disponibili?", False, 'img/parcheggio.png'),
    ("Il segnale di divieto di sosta è valido in tutti i giorni e a tutte le ore?", False, 'img/divieto_sosta.png'),
    ("Un motociclista deve sempre indossare il casco, anche se è in sosta?", True, 'img/casco.png'),
    ("È consentito viaggiare a velocità superiore al limite se si sta superando un altro veicolo?", False, 'img/superare.png'),
    ("È obbligatorio utilizzare il seggiolino per bambini anche se il bambino ha più di 12 anni e supera i 150 cm di altezza?", False, 'img/seggiolino.png'),
]

class AppQuiz:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Patente B")
        
        self.punteggio = 0
        self.indice_domanda = 0
        self.tempo_iniziale = 1800  # tempo in secondi
        self.tempo_rimanente = self.tempo_iniziale
        
        # Frame principale
        frame_principale = tk.Frame(self.master, bg="#f0f0f0")
        frame_principale.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame superiore per info
        frame_superiore = tk.Frame(frame_principale, bg="#f0f0f0")
        frame_superiore.pack(fill=tk.X)
        
        # Timer e counter delle domande con stile migliorato
        self.frame_timer = tk.Frame(frame_superiore, bg="#e1e1e1", bd=1, relief=tk.RAISED)
        self.frame_timer.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.etichetta_timer = tk.Label(
            self.frame_timer, 
            text="30:00", 
            font=("Arial", 16, "bold"),
            bg="#e1e1e1",
            fg="#333333",
            padx=15,
            pady=10
        )
        self.etichetta_timer.pack()
        
        self.etichetta_counter_domande = tk.Label(
            frame_superiore,
            text=f"Domanda 1 di {len(domande)}",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.etichetta_counter_domande.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Creazione dello stile per la barra di avanzamento
        self.style = ttk.Style()
        self.style.theme_use('default')  # Usa il tema predefinito
        self.style.configure("TProgressbar",
                             troughcolor="#e0e0e0",  # Colore dello sfondo della barra
                             background="#4CAF50")  # Colore della barra per il punteggio
        
        self.style.configure("TProgressbarTempo",
                             troughcolor="#e0e0e0",  # Colore dello sfondo della barra
                             background="#2196F3")  # Colore della barra per il tempo
        
        # Progressbar per il punteggio
        self.var_progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            frame_principale, 
            orient="horizontal", 
            length=760, 
            mode="determinate",
            variable=self.var_progress,
            style="TProgressbar",
        )
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Progressbar per il tempo
        self.var_progress_tempo = tk.DoubleVar()
        self.progress_bar_tempo = ttk.Progressbar(
            frame_principale, 
            orient="horizontal", 
            length=760, 
            mode="determinate",
            variable=self.var_progress_tempo,
            style="TProgressbarTempo",
        )
        self.progress_bar_tempo.pack(fill=tk.X, pady=10)

        # Frame per la domanda e l'immagine
        frame_contenuto = tk.Frame(frame_principale, bg="#f0f0f0")
        frame_contenuto.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Domanda
        self.etichetta_domanda = tk.Label(
            frame_contenuto,
            text="",
            wraplength=700,
            justify=tk.CENTER,
            font=("Arial", 14),
            bg="#f0f0f0",
            anchor="center"
        )
        self.etichetta_domanda.pack(pady=20, fill=tk.X)
        
        # Frame per l'immagine
        self.frame_immagine = tk.Frame(frame_contenuto, bg="#ffffff", bd=1, relief=tk.SUNKEN)
        self.frame_immagine.pack(pady=20)
        
        self.etichetta_immagine = tk.Label(self.frame_immagine, bg="#ffffff")
        self.etichetta_immagine.pack(padx=5, pady=5)
        
        # Frame per i bottoni delle risposte
        frame_risposte = tk.Frame(frame_principale, bg="#f0f0f0")
        frame_risposte.pack(fill=tk.X, pady=20)
        
        # Bottoni delle risposte
        self.bottone_vero = tk.Button(
            frame_risposte,
            text="VERO",
            command=self.controlla_vero,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.bottone_vero.pack(side=tk.LEFT, padx=50)
        
        self.bottone_falso = tk.Button(
            frame_risposte,
            text="FALSO",
            command=self.controlla_falso,
            width=20,
            height=2,
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.bottone_falso.pack(side=tk.RIGHT, padx=50)
        
        # Frame per la navigazione
        frame_navigazione = tk.Frame(frame_principale, bg="#f0f0f0")
        frame_navigazione.pack(fill=tk.X, pady=10)
        
        self.bottone_precedente = tk.Button(
            frame_navigazione,
            text="← Precedente",
            command=self.domanda_precedente,
            width=15,
            bg="#e0e0e0",
            font=("Arial", 10)
        )
        self.bottone_precedente.pack(side=tk.LEFT, padx=10)
        
        self.bottone_successiva = tk.Button(
            frame_navigazione,
            text="Successiva →",
            command=self.domanda_successiva,
            width=15,
            bg="#e0e0e0",
            font=("Arial", 10)
        )
        self.bottone_successiva.pack(side=tk.RIGHT, padx=10)
        
        # Bottone per terminare il quiz
        self.bottone_termina = tk.Button(
            frame_principale,
            text="Termina Quiz",
            command=self.termina_quiz,
            width=20,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold")
        )
        self.bottone_termina.pack(pady=10)

        self.aggiorna_domanda()
        self.aggiorna_timer()

    def aggiorna_domanda(self):
        if self.indice_domanda < len(domande):
            testo_domanda, risposta_corretta, percorso_immagine = domande[self.indice_domanda]
            self.etichetta_domanda.config(text=testo_domanda)
            self.carica_immagine(percorso_immagine)
            self.risposta_corretta = risposta_corretta  # Salva la risposta corretta per il controllo
            self.etichetta_counter_domande.config(text=f"Domanda {self.indice_domanda + 1} di {len(domande)}")
            self.var_progress.set((self.indice_domanda + 1) / len(domande) * 100)  # Aggiorna la progress bar
            
        else:
            self.termina_quiz()

    def carica_immagine(self, percorso_immagine):
        if percorso_immagine:
            try:
                img = Image.open(percorso_immagine)
                img = img.resize((200, 200))  # Cambia la dimensione come necessario
                self.img_tk = ImageTk.PhotoImage(img)
                self.etichetta_immagine.config(image=self.img_tk)
                self.etichetta_immagine.image = self.img_tk  # Mantieni un riferimento all'immagine
            except Exception as e:
                print(f"Errore nel caricamento dell'immagine: {e}")
                self.etichetta_immagine.config(image='')  # Nascondi l'immagine se c'è un errore
        else:
            self.etichetta_immagine.config(image='')  # Nascondi l'immagine se non c'è

    def controlla_vero(self):
        if self.risposta_corretta == True:
            self.punteggio += 1
        self.domanda_successiva()

    def controlla_falso(self):
        if self.risposta_corretta == False:
            self.punteggio += 1
        self.domanda_successiva()

    def domanda_successiva(self):
        self.indice_domanda += 1
        self.aggiorna_domanda()
        
    def domanda_precedente(self):
        if self.indice_domanda > 0:  # Controllo per non scendere sotto zero
            self.indice_domanda -= 1
            self.aggiorna_domanda()

    def aggiorna_timer(self):
        if self.tempo_rimanente > 0:
            minuti = self.tempo_rimanente // 60
            secondi = self.tempo_rimanente % 60
            self.etichetta_timer.config(text=f"{minuti:02d}:{secondi:02d}")
            self.tempo_rimanente -= 1  # Decrementa il tempo rimanente
            
            # Aggiorna la progress bar del tempo
            self.var_progress_tempo.set((self.tempo_iniziale - self.tempo_rimanente) / self.tempo_iniziale * 100)
            
            self.master.after(1000, self.aggiorna_timer)
        else:
            self.termina_quiz()

    def termina_quiz(self):
        if self.punteggio >= 27:
            messagebox.showinfo("Quiz Terminato", f"Hai totalizzato {self.punteggio} punti su {len(domande)}. Sei PASSATOO!")
        else:
            messagebox.showinfo("Quiz Terminato", f"Hai totalizzato {self.punteggio} punti su {len(domande)}. Puoi fare meglio la prossima volta!")
            
        self.bottone_vero.config(state=tk.DISABLED)
        self.bottone_falso.config(state=tk.DISABLED)
        self.bottone_successiva.config(state=tk.DISABLED)
        self.bottone_precedente.config(state=tk.DISABLED)
        self.bottone_termina.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app_quiz = AppQuiz(root)
    root.mainloop()
