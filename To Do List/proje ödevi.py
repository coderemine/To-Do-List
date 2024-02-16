from tkinter import *
import tkinter as tk
from tkinter import messagebox
import json

class Uygulama:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("To-Do List App")
        self.pencere.config(bg="purple")
        self.yapilacaklar = []
        self.tamamlananlar = []
        self.dosya_ara()

        self.basliklar_cerceve = tk.Frame(self.pencere)
        self.basliklar_cerceve.pack(pady=12)

        self.listeler_cerceve = tk.Frame(self.pencere)
        self.listeler_cerceve.pack(pady=12)

        self.gorev_yazi = tk.Label(self.basliklar_cerceve, text="Görev Listesi", font=("Times", 14))
        self.gorev_yazi.pack(side=tk.LEFT, padx=110, pady=5)

        self.tamamlanmis_yazi = tk.Label(self.basliklar_cerceve, text="Tamamlanmış Görevler Listesi", font=("Times", 14))
        self.tamamlanmis_yazi.pack(side=tk.LEFT, padx=50, pady=5)

        self.gorev_listbox = tk.Listbox(self.listeler_cerceve, selectmode=tk.SINGLE, width=50)
        self.gorev_listbox.pack(side=tk.LEFT, pady=10)

        self.tamamlanmis_listbox = tk.Listbox(self.listeler_cerceve, selectmode=tk.SINGLE, width=50)
        self.tamamlanmis_listbox.pack(side=tk.RIGHT, pady=10)

        self.gorev_scrollbar = tk.Scrollbar(self.listeler_cerceve, orient=tk.VERTICAL)
        self.gorev_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.gorev_listbox.config(yscrollcommand=self.gorev_scrollbar.set)
        self.gorev_scrollbar.config(command=self.gorev_listbox.yview)

        self.tamamlanmis_scrollbar = tk.Scrollbar(self.listeler_cerceve, orient=tk.VERTICAL)
        self.tamamlanmis_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tamamlanmis_listbox.config(yscrollcommand=self.tamamlanmis_scrollbar.set)
        self.tamamlanmis_scrollbar.config(command=self.tamamlanmis_listbox.yview)

        self.sil_buton = tk.Button(self.pencere, text="Sil", cursor="hand2", activebackground="Red", command=self.gorev_sil, bg="yellow")
        self.sil_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        self.tamamla_buton = tk.Button(self.pencere, text="Tamamla", cursor="hand2", activebackground="Green", command=self.gorev_tamamla, bg="green")
        self.tamamla_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        self.ekle_buton = tk.Button(self.pencere, text="Ekle", cursor="hand2", command=self.gorev_ekle_ekrani, bg="red")
        self.ekle_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        self.ekrana_yaz()

    def gorev_ekle_ekrani(self):
        ekle_pencere = tk.Toplevel(self.pencere)
        ekle_pencere.title("Görev Ekle")

        yazi1 = tk.Label(ekle_pencere, text="Görevinizi giriniz")
        yazi1.pack()

        girdi1 = tk.Entry(ekle_pencere)
        girdi1.pack()

        yazi2 = tk.Label(ekle_pencere, text="Görevin önem sırasını giriniz")
        yazi2.pack()

        girdi2 = tk.Entry(ekle_pencere)
        girdi2.pack()

        ekle_buton = tk.Button(ekle_pencere, text="Ekle", cursor="hand2", command=lambda: self.gorev_ekle(ekle_pencere, girdi1.get(), girdi2.get()))
        ekle_buton.pack()

    def gorev_ekle(self, pencere, girdi1, girdi2):
        if girdi1 == "":
            messagebox.showerror("Dikkat", "Boş görev girişi olamaz!")
            pencere.destroy()
        elif not girdi2.isdigit():
            messagebox.showerror("Dikkat", "Önem sırasına sayı girilmelidir!")
            pencere.destroy()
        elif girdi2 == "":
            messagebox.showerror("Dikkat", "Boş önem sırası olamaz!")
            pencere.destroy()
        else:
            messagebox.showinfo("Tebrikler", "Görev başarıyla eklendi:)")
            pencere.destroy()
            ana = {"Görev": girdi1, "Önem Sırası": int(girdi2)}
            self.yapilacaklar.append(ana)
            self.sirala()
            self.ekrana_yaz()
            self.dosyaya_kaydet()

    def sirala(self):
        for i in range(len(self.yapilacaklar)):
            for j in range(0, len(self.yapilacaklar) - i - 1):
                if self.yapilacaklar[j]["Önem Sırası"] > self.yapilacaklar[j + 1]["Önem Sırası"]:
                    temp = self.yapilacaklar[j]
                    self.yapilacaklar[j] = self.yapilacaklar[j + 1]
                    self.yapilacaklar[j + 1] = temp

    def gorev_sil(self):
        index = self.gorev_listbox.curselection()
        index2 = self.tamamlanmis_listbox.curselection()
        if index:
            del self.yapilacaklar[index[0]]
            messagebox.showinfo("!", "Görev Silindi.")
            self.dosyaya_kaydet()
            self.ekrana_yaz()
        elif index2:
            del self.tamamlananlar[index2[0]]
            messagebox.showinfo("Tebrikler", "Tamamlanmış görev silindi.")
            self.dosyaya_kaydet()
            self.ekrana_yaz()

    def gorev_tamamla(self):
        index = self.gorev_listbox.curselection()
        if index:
            tamamlanan = self.yapilacaklar[index[0]]
            self.tamamlananlar.append(tamamlanan)
            del self.yapilacaklar[index[0]]
            messagebox.showinfo("Tebrikler", "Görev tamamlandı.")
            self.ekrana_yaz()
            self.dosyaya_kaydet()

    def ekrana_yaz(self):
        self.gorev_listbox.delete(0, tk.END)
        self.tamamlanmis_listbox.delete(0, tk.END)

        for gorev in self.yapilacaklar:
            if 'Görev' in gorev and 'Önem Sırası' in gorev:
                self.gorev_listbox.insert(tk.END, f"Görev: {gorev['Görev']}, Önem Sırası: {gorev['Önem Sırası']}")

        for tgorev in self.tamamlananlar:
            if 'Görev' in tgorev and 'Önem Sırası' in tgorev:
                self.tamamlanmis_listbox.insert(tk.END, f"Görev: {tgorev['Görev']}, Önem Sırası: {tgorev['Önem Sırası']}")

    def dosyaya_kaydet(self):
        dosya = open("gorevler.json", "w")
        dosya2 = open("tgorevler.json", "w")
        json.dump(self.yapilacaklar, dosya)
        json.dump(self.tamamlananlar, dosya2)

    def dosya_ara(self):
        try:
            dosya = open("gorevler.json", "r")
            self.yapilacaklar = json.load(dosya)
        except FileNotFoundError:
            messagebox.showwarning("Dikkat", "Görev bulunamadı. Yeni dosya oluşturuldu.")
            self.yapilacaklar = []

        try:
            dosya2 = open("tgorevler.json", "r")
            self.tamamlananlar= json.load(dosya2)
        except FileNotFoundError:
            messagebox.showwarning("Dikkat", "Tamamlanmış görev bulunamadı. Yeni dosya oluşturuldu.")
            self.tamamlananlar = []

uygulama = Uygulama()
uygulama.pencere.mainloop()