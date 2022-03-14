"""
Fila Main va fi responsabila pentru input-ul user-ului si pentru afisarea pozitiei curente de joc.
"""

from multiprocessing import Process, Queue

import contextlib
import sys

with contextlib.redirect_stdout(None):
    import pygame as p

import Engine
import MoveFinder

p.display.set_caption("Sah")
ico_joc = p.image.load("imagini_piese/np.png")
p.display.set_icon(ico_joc)

Dimensiune = 8
Latime_Tabla = Inaltime_Tabla = 512
Marime_Patrat = Inaltime_Tabla // Dimensiune

Latime_Mutari = 256
Inaltime_Mutari = Inaltime_Tabla

Max_FPS = 15

Imagini = {}

'''
 Initializarea imaginilor intr-un dictionar
 Salvam imaginile cu piesele pe rand, in dictionarul "Piese"
 p.image.load incarca o imagine, iar p.transform.scale scaleaza imaginea la rezolutia unui patrat de pe tabla noastra
'''


def loadImagini():
    Piese = ["ap", "aR", "aN", "aB", "aQ", "aK", "np", "nR", "nN", "nB", "nQ", "nK", "bulina"]
    for piesa in Piese:
        Imagini[piesa] = p.transform.scale(p.image.load("imagini_piese/" + piesa + ".png"), (Marime_Patrat,
                                                                                             Marime_Patrat))


'''

'''


def main():
    p.init()  # initializare pygame
    Ecran = p.display.set_mode((Latime_Tabla + Latime_Mutari, Inaltime_Tabla))
    Clock = p.time.Clock()
    Ecran.fill(p.Color("white"))
    loadImagini()  # incarcam imaginile o singura data, inaintea buclei cu jocul

    PozitieCurenta = Engine.StareJoc()
    MutariValide = PozitieCurenta.MutariValide()
    MutareFacuta = False
    Animatie = False
    PatratSelectat = ()  # nici o piesa este selectata initial, tine minte ultimul click al utilizatorului
    ClickuriJucator = []  # tine minte click-urile utilizatorului
    gameOver = False
    FontMutari = p.font.SysFont("Helvitca", 24, False, False)

    AILoading = False
    ProcesMoveFinder = None
    MutareInapoi = False
    QueueMutariAI = Queue()

    running = True
    JucatorPieseAlbe = True  # True => Alb = uman. False => Alb = AI
    JucatorPieseNegre = False  # True => Negru = uman. False => Negru = AI

    '''
    Bucla in care ruleaza jocul
    '''

    while running:
        TuraOm = (PozitieCurenta.MutareAlb and JucatorPieseAlbe) or (not PozitieCurenta.MutareAlb and JucatorPieseNegre)
        for e in p.event.get():  # event handler
            if e.type == p.QUIT:  # daca tipul de eveniment este QUIT, jocul se opreste
                running = False
            #
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    LocatieMouse = p.mouse.get_pos()
                    col = LocatieMouse[0] // Marime_Patrat
                    rand = LocatieMouse[1] // Marime_Patrat
                    if PatratSelectat == (rand, col) or col > 7:  # in caz ca utilizatorul a dat click de doua ori pe
                        # acelasi patrat sau a dat click pe istoric

                        PatratSelectat = ()
                        ClickuriJucator = []
                    else:
                        PatratSelectat = (rand, col)
                        ClickuriJucator.append(PatratSelectat)  # adaugam patratul pe care s-a dat click in lista

                    if len(ClickuriJucator) == 2 and TuraOm:  # daca sunt doua patrate in lista, atunci utilizatorul a
                        # dat o data click pe piesa pe care vrea sa o mute, iar apoi a selectat patratul
                        # unde vrea sa o mute, deci verificam mutarea si o facem, daca este cazul

                        mutare = Engine.Mutare(ClickuriJucator[0], ClickuriJucator[1], PozitieCurenta.Pozitie)

                        for i in range(len(MutariValide)):
                            if mutare == MutariValide[i]:
                                PozitieCurenta.MutarePiesa(MutariValide[i])
                                MutareFacuta = True
                                Animatie = True
                                PatratSelectat = ()  #
                                ClickuriJucator = []
                                break

                        if not MutareFacuta:
                            ClickuriJucator = [PatratSelectat]

            #
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # mergem o mutare inapoi cand 'z' este apasat
                    PozitieCurenta.undoMutare()
                    MutareFacuta = True
                    Animatie = False
                    gameOver = False
                    if AILoading:  # daca AI-ul calcula urmatoarea mutare in timp ce 'z' este apasat,
                        # oprim procesul fiindca nu mai este nevoie
                        ProcesMoveFinder.terminate()
                        AILoading = False
                    MutareInapoi = True

                if e.key == p.K_r:  # resetam jocul la pozitia initiala
                    PozitieCurenta = Engine.StareJoc()
                    MutariValide = PozitieCurenta.MutariValide()
                    PatratSelectat = ()
                    ClickuriJucator = []
                    MutareFacuta = False
                    Animatie = False
                    gameOver = False
                    if AILoading:
                        ProcesMoveFinder.terminate()
                        AILoading = False
                    MutareInapoi = True

        # move finder
        if not gameOver and not TuraOm and not MutareInapoi:
            # Daca este tura Algormitmului, calculam o mutare
            if not AILoading:
                AILoading = True
                QueueMutariAI = Queue()  # In acest queue punem mutarile gasite de MoveFinder
                # Este necesar pentru threading
                ProcesMoveFinder = Process(target=MoveFinder.MutareAlgoritm,
                                           args=(PozitieCurenta, MutariValide, QueueMutariAI))
                                 # = MutareAlgoritm(PozitieCurenta, MutariValide, QueueMutariAI)
                ProcesMoveFinder.start()

            if not ProcesMoveFinder.is_alive():  # Daca a fost gasita o mutare
                mutareAlgoritm = QueueMutariAI.get()
                if mutareAlgoritm is None:
                    mutareAlgoritm = MoveFinder.MutareRandom(MutariValide)
                    print("Mutare Random")
                PozitieCurenta.MutarePiesa(mutareAlgoritm)
                MutareFacuta = True
                Animatie = True
                AILoading = False

        if MutareFacuta:
            if Animatie:
                animatiePiese(PozitieCurenta.LogMutari[-1], Ecran, PozitieCurenta.Pozitie, Clock)
            MutariValide = PozitieCurenta.MutariValide()
            MutareFacuta = False
            Animatie = False
            MutareInapoi = False

        afisarePozitie(Ecran, PozitieCurenta, MutariValide, PatratSelectat, FontMutari)

        if PozitieCurenta.sahmat or PozitieCurenta.pat:
            gameOver = True
            if PozitieCurenta.pat:
                text = "Pat"
            else:
                text = "Sah Mat"
            afisareText(Ecran, text)

        Clock.tick(Max_FPS)
        p.display.flip()


'''
 Functie responsabila pentru afisarea tuturor elementelor din pozitia curenta
'''


def afisarePozitie(ecran, pozitie, mutariValide, patratSelectat, font):
    afisareTabla(ecran)
    highlightMutari(ecran, pozitie, mutariValide, patratSelectat)
    highlightUltimaMutare(ecran, pozitie)
    afisarePiese(ecran, pozitie.Pozitie)
    afisareMutari(ecran, pozitie, font)


'''
 Afisarea patratelor de pe tabla, patratul din stanga sus este intotdeauna alb
'''


def afisareTabla(ecran):
    global culori
    culori = [p.Color(236, 211, 185), p.Color(161, 111, 90)]
    for r in range(Dimensiune):
        for c in range(Dimensiune):
            culoare = culori[((r + c) % 2)]
            p.draw.rect(ecran, culoare, p.Rect(c * Marime_Patrat, r * Marime_Patrat, Marime_Patrat, Marime_Patrat))


'''
Afisarea pieselor 
'''


def afisarePiese(ecran, pozitie):
    for r in range(Dimensiune):
        for c in range(Dimensiune):
            piesa = pozitie[r][c]
            if piesa != "--":
                ecran.blit(Imagini[piesa], p.Rect(c * Marime_Patrat, r * Marime_Patrat, Marime_Patrat, Marime_Patrat))


'''
Afisarea istoricului de mutari pe dreapta
'''


def afisareMutari(ecran, pozitie, font):
    IstoricDreptunghi = p.Rect(Latime_Tabla, 0, Latime_Mutari, Inaltime_Mutari)
    p.draw.rect(ecran, p.Color("black"), IstoricDreptunghi)
    logMutari = pozitie.LogMutari
    textMutare = []
    for i in range(0, len(logMutari), 2):
        stringMutare = str(i // 2 + 1) + ". " + str(logMutari[i]) + " "
        if i + 1 < len(logMutari):
            stringMutare += str(logMutari[i + 1]) + "   "
        textMutare.append(stringMutare)

    mutariPeRand = 2
    padding = 7
    paddingSus = padding
    for i in range(0, len(textMutare), mutariPeRand):
        text = ""
        for j in range(mutariPeRand):
            if i + j < len(textMutare):
                text += textMutare[i + j]
        textObject = font.render(text, True, p.Color("white"))
        textLocation = IstoricDreptunghi.move(padding, paddingSus)
        ecran.blit(textObject, textLocation)
        paddingSus += 1.5 * textObject.get_height()


'''
Afisarea mutarilor valide pentru piesele apasate
'''


def highlightMutari(ecran, pozitie, mutariValide, patratSelectat):
    if patratSelectat:
        r, c = patratSelectat
        if pozitie.Pozitie[r][c][0] == ('a' if pozitie.MutareAlb else 'n'):  #

            s = p.Surface((Marime_Patrat, Marime_Patrat))  # highlight patratul apasat
            s.set_alpha(100)
            s.fill(p.Color(30, 144, 255))
            ecran.blit(s, (c * Marime_Patrat, r * Marime_Patrat))

            s = Imagini["bulina"]  # highlight patrate valide
            s.set_alpha(150)
            for mutare in mutariValide:
                if mutare.startRand == r and mutare.startCol == c:
                    ecran.blit(s, (mutare.finalCol * Marime_Patrat, mutare.finalRand * Marime_Patrat))


'''
 Highlight ultima mutare. De unde a pornit piesa si unde a ajuns
'''


def highlightUltimaMutare(ecran, pozitie):
    if pozitie.LogMutari:
        mutare = pozitie.LogMutari[-1]
        r1 = mutare.startRand
        c1 = mutare.startCol
        r2 = mutare.finalRand
        c2 = mutare.finalCol
        Suprafata = p.Surface((Marime_Patrat, Marime_Patrat))
        Suprafata.set_alpha(100)  # transparency 0 - 255
        Suprafata.fill(p.Color(30, 144, 255))

        ecran.blit(Suprafata, (c1 * Marime_Patrat, r1 * Marime_Patrat))
        ecran.blit(Suprafata, (c2 * Marime_Patrat, r2 * Marime_Patrat))


'''
 Animatie mutari
'''


def animatiePiese(mutare, ecran, pozitie, clock):
    global culori
    DiferentaRand = mutare.finalRand - mutare.startRand
    DiferentaColoana = mutare.finalCol - mutare.startCol
    FramePerPatrat = 6
    FrameuriAnimatie = (abs(DiferentaRand) + abs(DiferentaColoana)) * FramePerPatrat
    for frame in range(FrameuriAnimatie + 1):
        # frame/frameCount = progresul animatiei
        r, c = (mutare.startRand + DiferentaRand * frame / FrameuriAnimatie,
                mutare.startCol + DiferentaColoana * frame / FrameuriAnimatie)
        afisareTabla(ecran)
        afisarePiese(ecran, pozitie)
        # stergem piesa de pe patratul destinatie
        culoare = culori[(mutare.finalRand + mutare.finalCol) % 2]
        PatratFinal = p.Rect(mutare.finalCol * Marime_Patrat, mutare.finalRand * Marime_Patrat, Marime_Patrat,
                             Marime_Patrat)
        p.draw.rect(ecran, culoare, PatratFinal)
        #
        if mutare.PiesaCapturata != "--":
            if mutare.MutareEnPassant:
                RandEnpassant = mutare.finalRand + 1 if mutare.PiesaCapturata[0] == 'n' else mutare.finalRand - 1
                PatratFinal = p.Rect(mutare.finalCol * Marime_Patrat, RandEnpassant * Marime_Patrat, Marime_Patrat,
                                     Marime_Patrat)
            ecran.blit(Imagini[mutare.PiesaCapturata], PatratFinal)
        #
        ecran.blit(Imagini[mutare.PiesaMutata],
                   p.Rect(c * Marime_Patrat, r * Marime_Patrat, Marime_Patrat, Marime_Patrat))
        p.display.flip()
        clock.tick(60)


'''
 Afisare text pe ecran, folosit la finalul jocului pentru sah mat sau pat
'''


def afisareText(ecran, text):
    font = p.font.SysFont("freesansbold.ttf", 64, True, False)
    ObiectText = font.render(text, False, p.Color("gray"))
    LocatieText = p.Rect(0, 0, Latime_Tabla, Inaltime_Tabla).move(Latime_Tabla / 2 - ObiectText.get_width() / 2,
                                                                  Inaltime_Tabla / 2 - ObiectText.get_height() / 2)
    ecran.blit(ObiectText, LocatieText)
    ObiectText = font.render(text, False, p.Color("black"))
    ecran.blit(ObiectText, LocatieText.move(2, 2))


if __name__ == "__main__":
    main()
