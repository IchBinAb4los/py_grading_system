import tkinter.ttk
import numpy
import threading
import time
from tkinter import *
from functools import partial

small = ("Helvetica", "8")

questions = numpy.array([[["[1] ¿Pregunta 1? ¿Pregunta 1? ¿Pregunta 1?"], ["A"]],
            [["[2] ¿Pregunta 2? ¿Pregunta 2? ¿Pregunta 2?"], ["B"]],
            [["[3] ¿Pregunta 3? ¿Pregunta 3? ¿Pregunta 3?"], ["C"]],
            [["[4] ¿Pregunta 4? ¿Pregunta 4? ¿Pregunta 4?"], ["D"]],
            [["[5] ¿Pregunta 5? ¿Pregunta 5? ¿Pregunta 5?"], ["E"]]])

class App():
    def __init__(self):
        self.entries = []
        self.buttons = []
        self.alumntexts = []
        self.root = Tk()
        self.root.title("Sistema de alumnos")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.mainFrame = self.createMainFrame()
        self.c = self.createCanvas()
        self.draw()
        self.ay = 70
        self.totalalumns = 0
        self.notas = []
        self.alumnans = {}
        self.anscount = {0:0, 1:0, 2:0, 3:0, 4:0}
        self.ruts = {}

    def checkAnswers(self, ins, name, surname, rut):
        right = 0
        ans = []
        for i in questions:
            ans.append(i[1])

        for i in range(len(ans)):
            if ans[i] == ins[i]:
                right +=1
                self.anscount[i] += 1

        self.ruts[f"{name} {surname}"] = rut
        _right12 = right*12
        _right12 /= 10
        _right12 += 1
        _right12 = float(_right12)
        status = "DESAPROBADO"
        if _right12 >= 4.0:
            status = "APROBADO"

        self.alumnans[f"{name} {surname}"] = _right12
        self.notas.append(_right12)
        self.c.create_text(310, self.ay, text=f"[{right}/5] {name} {surname}: puntaje {_right12} |{status}|", anchor=W)
        self.c.itemconfig(self.waittext, text="")
        self.ay += 40
        self.totalalumns += 1
        if self.totalalumns == 6:
            self.getData()

    def getData(self):
        self.prom = round(numpy.mean(self.notas), 2)
        self.c.itemconfig(self.promtext, text=f"Promedio: {self.prom}")

        encima, debajo = [], []
        for k,v in self.alumnans.items():
            if v >= self.prom:
                encima.append(k)
            else:
                debajo.append(k)

        encima_text = ", ".join(encima)
        self.c.itemconfig(self.encimatext, text=f"({len(encima)}) Por encima: {encima_text}", anchor=W)

        debajo_text = ", ".join(debajo)
        self.c.itemconfig(self.debajotext, text=f"({len(debajo)}) Por debajo: {debajo_text}", anchor=W)

        aprobados = 0

        for i in self.notas:
            if i >= 4:
                aprobados += 1

        porc_aprob = aprobados/6*100
        porc_desaprob = 100-porc_aprob
        self.c.itemconfig(self.porcaprobtext, text=f"Porcentaje de aprobados: {round(porc_aprob, 2)}%")
        self.c.itemconfig(self.porcdesaprobtext, text=f"Porcentaje de desaprobados: {round(porc_desaprob, 2)}%")

        self.anscountcopy = self.anscount.copy()
        correct = [i for i in self.anscount.values()]
        _max1 = max(correct)
        correct.remove(_max1)
        _max2 = max(correct)
        most = []
        x = 0

        for k,v in self.anscount.items():
            if v == _max1 or v == _max2:
                most.append(str(k+1))
                x += v

        text = ", ".join(most)
        self.c.itemconfig(self.masacertadastext, text=f"Preguntas más acertadas: {text} ({x} respuestas correctas en total)")

        wrong = [i for i in self.anscountcopy.values()]
        _min1 = min(wrong)
        wrong.remove(_min1)
        _min2 = min(wrong)
        most = []
        for k,v in self.anscount.items():
            if v == _min1 or v == _min2:
                most.append(str(k+1))

        text = ", ".join(most)
        self.c.itemconfig(self.maserradastext, text=f"Preguntas más erradas: {text} ({30-x} respuestas incorrectas en total)")

        self.c.itemconfig(self.mejoresnotas, text="Mejores notas: ")
        notas = [i for i in self.alumnans.values()]
        _max1 = max(notas)
        notas.remove(_max1)
        try:
            _max2 = max(notas)
        except ValueError:
            pass

        best = {}

        for k,v in self.alumnans.items():
            if v == _max1 or v == _max2:
                best[k] = v

        y = 550
        for k,v in best.items():
            self.c.create_text(310, y, text=f"({v}) {k}: {self.ruts[k]}", anchor=W)
            y += 20

    def reloadWarning(self):
        try:
            time.sleep(1.4)
            self.c.itemconfig(self.warningText, text="")
        except RuntimeError:
            pass

    def _append(self):
        if not self.totalalumns == 6:
            gotten = []
            for i in self.entries:
                text = i.get()
                gotten.append(text)
            if "" in gotten:
                gotten = []
                self.c.itemconfig(self.warningText, fill="red", text="Error: debe ingresar todos los datos")
                threading.Thread(target=self.reloadWarning).start()
            else:
                self.checkAnswers(gotten[3:8], gotten[0], gotten[1], gotten[2])
                self.c.itemconfig(self.warningText, fill="green", text="Alumno agregado correctamente")
                threading.Thread(target=self.reloadWarning).start()

        else:
            self.c.itemconfig(self.warningText, fill="red", text="Error: ya has ingresado 6 alumnos")
            threading.Thread(target=self.reloadWarning).start()

    def draw(self):
        self.c.create_line(300, 0, 300, 600)
        self.c.create_line(300, 300, 700, 300)
        self.c.create_rectangle(10, 10, 290, 40)
        self.c.create_text(150, 25, text="Ingresar datos de alumno")
        self.c.create_rectangle(310, 10, 690, 40)
        self.c.create_text(500, 25, text="Alumnos registrados")
        self.c.create_rectangle(310, 310, 690, 340)
        self.c.create_text(500, 325, text="Estadisticas")
        self.waittext = self.c.create_text(310, 60, text="...", anchor=W)
        self.promtext = self.c.create_text(310, 360, text="...", anchor=W)
        self.encimatext = self.c.create_text(310, 380, text="", anchor=W, font=small)
        self.debajotext = self.c.create_text(310, 400, text="", anchor=W, font=small)
        self.porcaprobtext = self.c.create_text(310, 430, text="", anchor=W)
        self.porcdesaprobtext = self.c.create_text(310, 450, text="", anchor=W)
        self.masacertadastext = self.c.create_text(310, 480, text="", anchor=W)
        self.maserradastext = self.c.create_text(310, 500, text="", anchor=W)
        self.mejoresnotas = self.c.create_text(310, 530, text="", anchor=W)
        self.warningText = self.c.create_text(150, 580, text="", justify=CENTER, fill="red")

        self.c.create_text(55, 70, text="Nombre")
        name = Entry(self.root, width=15, bd=2)
        name.place(x=10, y=80)
        self.entries.append(name)

        self.c.create_text(245, 70, text="Apellido")
        surname = Entry(self.root, width=15, bd=2)
        surname.place(x=200, y=80)
        self.entries.append(surname)

        self.c.create_text(150, 110, text="RUT")
        rut = Entry(self.root, width=15, bd=2)
        rut.place(x=105, y=120)
        self.entries.append(rut)

        y1 = 200
        for i in questions:
            self.c.create_text(150, y1, text=i[0][0])
            _entry = tkinter.ttk.Combobox(self.root, state="readonly")
            _entry["values"] = ("A", "B", "C", "D", "E")
            _entry.place(x=80, y=y1+10)
            self.entries.append(_entry)
            y1 += 70

        append = Button(self.mainFrame, command=partial(self._append), text="Agregar", font=("Helvetica", "10", "bold"), borderwidth=4)
        append.place(x=115, y=530)

        exit = Button(self.mainFrame, command=partial(self.exit), text="Salir", font=("Helvetica", "10", "bold"), borderwidth=4)
        exit.place(x=650, y=562)

    def createCanvas(self):
        c = Canvas(self.mainFrame, width=600, height=600, bg="#e4deff")
        c.pack(fill="both", expand="True")
        return c

    def createMainFrame(self):
        frame = Frame(self.root, bg="#ffffff")
        frame.pack(fill="both", expand="True")
        return frame

    def exit(self):
        self.root.destroy()

    def loop(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = App()
    app.loop()