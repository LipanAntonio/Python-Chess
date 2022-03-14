"""
 In fila Engine se calculeaza toate mutarile valide in pozitia curenta, de asemenea
 aici se vor stoca tuturor informatiile relevante pozitiei curente
"""

'''
 In clasa StareJoc se stocheaza pozitia curenta si se calculeaza mutarile valide
'''


class StareJoc:

    def __init__(self):

        self.Pozitie = [  # Folosim o lista de liste pentru a reprezenta pozitia jocului. (incepe cu pozitia initiala)
            ["nR", "nN", "nB", "nQ", "nK", "nB", "nN", "nR"],
            ["np", "np", "np", "np", "np", "np", "np", "np"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["ap", "ap", "ap", "ap", "ap", "ap", "ap", "ap"],
            ["aR", "aN", "aB", "aQ", "aK", "aB", "aN", "aR"]]

        self.MutareAlb = True
        self.LogMutari = []
        self.sahmat = False
        self.pat = False

        self.FunctiiMutari = {"p": self.mutariPion, "R": self.mutariTura, "N": self.mutariCal,
                              "B": self.mutariNebun, "Q": self.mutariRegina, "K": self.mutariRege}

        self.inSah = False
        self.pin = []
        self.sahuri = []

        self.LocatieRegeAlb = (7, 4)
        self.LocatieRegeNegru = (0, 4)

        self.enpassantPosibil = ()  # patratul unde o mutare en passant este valida
        self.enpassantPosibilLog = [self.enpassantPosibil]

        self.RocadePosibile = DrepturiRocada(True, True, True, True)
        self.LogRocadePosibile = [DrepturiRocada(self.RocadePosibile.aRege, self.RocadePosibile.nRege,
                                                 self.RocadePosibile.aRegina, self.RocadePosibile.nRegina)]

    '''
    Metoda pentru mutarea pieselor
    '''

    def MutarePiesa(self, mutare):
        self.Pozitie[mutare.finalRand][mutare.finalCol] = mutare.PiesaMutata
        self.Pozitie[mutare.startRand][mutare.startCol] = "--"
        self.LogMutari.append(mutare)
        self.MutareAlb = not self.MutareAlb

        # update pozitia regilor
        if mutare.PiesaMutata == "aK":
            self.LocatieRegeAlb = (mutare.finalRand, mutare.finalCol)
        elif mutare.PiesaMutata == "nK":
            self.LocatieRegeNegru = (mutare.finalRand, mutare.finalCol)

        # promotia pionilor
        if mutare.PromotiePion:
            self.Pozitie[mutare.finalRand][mutare.finalCol] = mutare.PiesaMutata[0] + 'Q'

        # en passant
        if mutare.MutareEnPassant:
            self.Pozitie[mutare.startRand][mutare.finalCol] = "--"

        # la mutari de pion de doua patrate, adaugam patratul unde se poate captura en passant
        if mutare.PiesaMutata[1] == 'p' and abs(mutare.startRand - mutare.finalRand) == 2:
            self.enpassantPosibil = ((mutare.startRand + mutare.finalRand) // 2, mutare.startCol)
        else:
            self.enpassantPosibil = ()

        # folosim un log pentru en passant pentru undo move
        self.enpassantPosibilLog.append(self.enpassantPosibil)

        # daca mutarea  este rocada, mutam tura in patratul potrivit
        if mutare.MutareRocada:
            if mutare.finalCol - mutare.startCol == 2:  # regele s-a mutat in dreapta (partea regelui)
                self.Pozitie[mutare.finalRand][mutare.finalCol - 1] = mutare.PiesaMutata[0] + 'R'
                self.Pozitie[mutare.finalRand][mutare.finalCol + 1] = "--"
            else:  # stanga
                self.Pozitie[mutare.finalRand][mutare.finalCol + 1] = mutare.PiesaMutata[0] + 'R'
                self.Pozitie[mutare.finalRand][mutare.finalCol - 2] = "--"

        # drepturi rocada
        self.LogRocadePosibile.append(DrepturiRocada(self.RocadePosibile.aRege, self.RocadePosibile.nRege,
                                                     self.RocadePosibile.aRegina, self.RocadePosibile.nRegina))
        self.updateDrepturiRocada(mutare)

    '''    
    Dam ultima mutare inapoi
    '''

    def undoMutare(self):
        if len(self.LogMutari) != 0:
            mutare = self.LogMutari.pop()
            self.Pozitie[mutare.startRand][mutare.startCol] = mutare.PiesaMutata
            self.Pozitie[mutare.finalRand][mutare.finalCol] = mutare.PiesaCapturata
            self.MutareAlb = not self.MutareAlb
            self.pat = False
            self.sahmat = False

            # dam inapoi pozitia regilor
            if mutare.PiesaMutata == "aK":
                self.LocatieRegeAlb = (mutare.startRand, mutare.startCol)
            elif mutare.PiesaMutata == "nK":
                self.LocatieRegeNegru = (mutare.startRand, mutare.startCol)

            # en passant
            if mutare.MutareEnPassant:
                self.Pozitie[mutare.finalRand][mutare.finalCol] = "--"
                self.Pozitie[mutare.startRand][mutare.finalCol] = mutare.PiesaCapturata

            self.enpassantPosibilLog.pop()
            self.enpassantPosibil = self.enpassantPosibilLog[-1]

            # rocada
            if mutare.MutareRocada:
                if mutare.finalCol - mutare.startCol == 2:  # kingside
                    self.Pozitie[mutare.finalRand][mutare.finalCol + 1] = self.Pozitie[mutare.finalRand][
                        mutare.finalCol - 1]
                    self.Pozitie[mutare.finalRand][mutare.finalCol - 1] = "--"
                else:
                    self.Pozitie[mutare.finalRand][mutare.finalCol - 2] = self.Pozitie[mutare.finalRand][
                        mutare.finalCol + 1]
                    self.Pozitie[mutare.finalRand][mutare.finalCol + 1] = "--"

            # drepturi rocada
            self.LogRocadePosibile.pop()  # scapam de castle right de la mutarea pe care o dam inapoi
            self.RocadePosibile = self.LogRocadePosibile[-1]  # le punem inapoi pe cele anterioare

    '''
    Calcularea mutarilor valide, luand in considerare sah-urile
    '''

    def MutariValide(self):
        mutari = []
        self.inSah, self.pin, self.sahuri = self.verificareSahuriPinuri()

        if self.MutareAlb:
            randRege = self.LocatieRegeAlb[0]
            colRege = self.LocatieRegeAlb[1]
        else:
            randRege = self.LocatieRegeNegru[0]
            colRege = self.LocatieRegeNegru[1]

        if self.inSah:
            if len(self.sahuri) == 1:  # daca regele este in sah o singura data
                mutari = self.MutariPosibile()
                # luam toate mutarile posibile si le taiem pe cele care ne lasa in sah
                sah = self.sahuri[0]  # sah[0], sah[1] = patratul piesei care da sah
                # sah[2], sa[3] = directia sahului
                randSah = sah[0]
                colSah = sah[1]
                piesaSah = self.Pozitie[randSah][colSah]
                PatrateValide = []

                # orice mutare care pune o piesa intre piesa care da sah si rege este valida, fiindca regele nu mai este
                # in sah
                if piesaSah[1] != 'N':
                    for i in range(1, 8):
                        patratValid = (randRege + sah[2] * i, colRege + sah[3] * i)  #
                        PatrateValide.append(patratValid)
                        if patratValid[0] == randSah and patratValid[1] == colSah:  #
                            break
                # daca piesa care da sah este un cal, singurul patrat valid inafara de mutarea regelui
                # este patratul pe care este calul (capturarea calului)
                else:
                    PatrateValide = [(randSah, colSah)]

                # daca mutarea nu ajunge pe un patrat valid (care opreste sahul), o scoatem
                for i in range(len(mutari) - 1, -1, -1):
                    if mutari[i].PiesaMutata[1] != 'K':
                        if not (mutari[i].finalRand, mutari[i].finalCol) in PatrateValide:
                            mutari.remove(mutari[i])

            # daca sunt mai multe sahuri, singura optiune este sa muti regele
            else:
                self.mutariRege(randRege, colRege, mutari)

        else:
            mutari = self.MutariPosibile()

        # daca sunt zero mutari valide si regele este in sah = sah mat, daca regele nu este in sah = pat
        if len(mutari) == 0:
            if self.inSah:
                self.sahmat = True
                return mutari

            else:
                self.pat = True
                return mutari

        '''
        if self.whiteToMove:
            print("mutari pentru alb:", len(moves))
        else:
            print("mutari pentru negru:", len(moves))
        '''
        return mutari

    '''
    Toate mutarile, fara consideratie catre sah-uri
    '''

    def MutariPosibile(self):
        mutari = []
        for r in range(len(self.Pozitie)):
            for c in range(len(self.Pozitie[r])):
                culoarePiesa = self.Pozitie[r][c][0]
                if (culoarePiesa == 'a' and self.MutareAlb) or (culoarePiesa == 'n' and not self.MutareAlb):
                    tipPiesa = self.Pozitie[r][c][1]
                    self.FunctiiMutari[tipPiesa](r, c, mutari)

        return mutari

    '''
    Mutari pioni
    '''

    def mutariPion(self, r, c, mutari):
        piesaPin = False
        directiePin = ()
        # daca piesa este in pin, are voie sa se mute doar in directia pinului
        for i in range(len(self.pin) - 1, -1, -1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piesaPin = True
                directiePin = (self.pin[i][2], self.pin[i][3])
                self.pin.remove(self.pin[i])
                break

        if self.MutareAlb:
            directiePion = -1
            randInitial = 6
            culoareOponent = 'n'
            randRege, colRege = self.LocatieRegeAlb
        else:
            directiePion = 1
            randInitial = 1
            culoareOponent = 'a'
            randRege, colRege = self.LocatieRegeNegru

        if self.Pozitie[r + directiePion][c] == "--":  # 1 square
            if not piesaPin or directiePin == (directiePion, 0):
                mutari.append(Mutare((r, c), (r + directiePion, c), self.Pozitie))
                if r == randInitial and self.Pozitie[r + 2 * directiePion][c] == "--":  # 2 squares
                    mutari.append(Mutare((r, c), (r + 2 * directiePion, c), self.Pozitie))

        if c - 1 >= 0:  # capturare in stanga
            if not piesaPin or directiePin == (directiePion, -1):
                if self.Pozitie[r + directiePion][c - 1][0] == culoareOponent:
                    mutari.append(Mutare((r, c), (r + directiePion, c - 1), self.Pozitie))

                if (r + directiePion, c - 1) == self.enpassantPosibil:  # en passant
                    # verificare in cazul ciudat in care regele este pe acelasi rand cu pionul care captureaza
                    # en passant si este si o piesa care ar ataca regele dupa en passant
                    piesaAtacatoare = piesaBlocaj = False
                    if randRege == r:
                        if colRege < c:  # regele la stanga pionului
                            rangeInterior = range(colRege + 1, c - 1)  # intre rege si pion
                            rangeExterior = range(c + 1, len(self.Pozitie))
                        else:
                            rangeInterior = range(colRege - 1, c, -1)
                            rangeExterior = range(c - 2, -1, -1)

                        for i in rangeInterior:
                            if self.Pozitie[r][i] != "--":
                                piesaBlocaj = True

                        for i in rangeExterior:
                            patrat = self.Pozitie[r][i]
                            if patrat[0] == culoareOponent and (patrat[1] == 'R' or patrat[1] == 'Q'):
                                piesaAtacatoare = True
                            elif patrat != "--":
                                piesaBlocaj = True

                    if not piesaAtacatoare or piesaBlocaj:
                        mutari.append(Mutare((r, c), (r + directiePion, c - 1), self.Pozitie, enpassant=True))

        if c + 1 <= 7:  # capturare in dreapta
            if not piesaPin or directiePin == (directiePion, 1):
                if self.Pozitie[r + directiePion][c + 1][0] == culoareOponent:
                    mutari.append(Mutare((r, c), (r + directiePion, c + 1), self.Pozitie))

                if (r + directiePion, c + 1) == self.enpassantPosibil:  # en passant
                    piesaAtacatoare = piesaBlocaj = False
                    if randRege == r:
                        if colRege < c:  # regele la stanga
                            rangeInterior = range(colRege + 1, c)  # intre rege si pion
                            rangeExterior = range(c + 2, len(self.Pozitie))
                        else:
                            rangeInterior = range(colRege - 1, c + 1, -1)
                            rangeExterior = range(c - 1, -1, -1)

                        for i in rangeInterior:
                            if self.Pozitie[r][i] != "--":
                                piesaBlocaj = True

                        for i in rangeExterior:
                            patrat = self.Pozitie[r][i]
                            if patrat[0] == culoareOponent and (patrat[1] == 'R' or patrat[1] == 'Q'):
                                piesaAtacatoare = True
                            elif patrat != "--":
                                piesaBlocaj = True

                    if not piesaAtacatoare or piesaBlocaj:
                        mutari.append(Mutare((r, c), (r + directiePion, c + 1), self.Pozitie, enpassant=True))

    '''
    Calcularea mutarilor pentru tura
    '''

    def mutariTura(self, r, c, mutari):
        piesaPin = False
        directiePin = ()
        # daca piesa este in pin, are voie sa se mute doar in directia pinului
        for i in range(len(self.pin) - 1, -1, -1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piesaPin = True
                directiePin = (self.pin[i][2], self.pin[i][3])
                if self.Pozitie[r][c][1] != 'Q':
                    self.pin.remove(self.pin[i])
                break

        directii = ((-1, 0), (0, -1), (1, 0), (0, 1))
        culoareOponent = 'n' if self.MutareAlb else 'a'

        for dr in directii:
            for i in range(1, 8):
                finalRand = r + dr[0] * i
                finalCol = c + dr[1] * i
                if 0 <= finalRand < 8 and 0 <= finalCol < 8:  #
                    if not piesaPin or directiePin == dr or directiePin == (-dr[0], -dr[1]):
                        PatratFinal = self.Pozitie[finalRand][finalCol]
                        if PatratFinal == "--":  #
                            mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))
                        elif PatratFinal[0] == culoareOponent:  #
                            mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))
                            break
                        else:  #
                            break
                else:  #
                    break

    '''
    Calcularea mutarilor pentru cal
    '''

    def mutariCal(self, r, c, mutari):
        piesaPin = False
        # daca un cal este in pin, nu are voie sa se mute orice ar fi
        for i in range(len(self.pin) - 1, -1, -1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piesaPin = True
                self.pin.remove(self.pin[i])
                break

        patrateMutari = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        culoarePiesa = 'a' if self.MutareAlb else 'n'

        for patrat in patrateMutari:
            finalRand = r + patrat[0]
            finalCol = c + patrat[1]
            if 0 <= finalRand < 8 and 0 <= finalCol < 8:
                if not piesaPin:
                    patratFinal = self.Pozitie[finalRand][finalCol]
                    if patratFinal[0] != culoarePiesa:  #
                        mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))

    '''
    Calcularea mutarilor nebunului
    '''

    def mutariNebun(self, r, c, mutari):
        piesaPin = False
        directiePin = ()
        # daca piesa este in pin, are voie sa se mute doar in directia pinului
        for i in range(len(self.pin) - 1, -1, -1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piesaPin = True
                directiePin = (self.pin[i][2], self.pin[i][3])
                self.pin.remove(self.pin[i])
                break

        directii = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        culoareOponent = 'n' if self.MutareAlb else 'a'

        for dr in directii:
            for i in range(1, 8):
                finalRand = r + dr[0] * i
                finalCol = c + dr[1] * i
                if 0 <= finalRand < 8 and 0 <= finalCol < 8:
                    if not piesaPin or directiePin == dr or directiePin == (-dr[0], -dr[1]):
                        patratFinal = self.Pozitie[finalRand][finalCol]
                        if patratFinal == "--":  #
                            mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))
                        elif patratFinal[0] == culoareOponent:  #
                            mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))
                            break
                        else:
                            break
                else:
                    break

    '''
    Mutarile reginei sunt mutarile turei + nebunului combinate
    '''

    def mutariRegina(self, r, c, mutari):
        self.mutariTura(r, c, mutari)
        self.mutariNebun(r, c, mutari)

    '''
    Calcularea mutarilor regelui, cu consideratie catre sah
    '''

    def mutariRege(self, r, c, mutari):
        mutariRand = (-1, -1, -1, 0, 0, 1, 1, 1)
        mutariCol = (-1, 0, 1, -1, 1, -1, 0, 1)
        culoareRege = 'a' if self.MutareAlb else 'n'

        for i in range(8):
            finalRand = r + mutariRand[i]
            finalCol = c + mutariCol[i]

            if 0 <= finalRand < 8 and 0 <= finalCol < 8:
                patratFinal = self.Pozitie[finalRand][finalCol]
                if patratFinal[0] != culoareRege:  #
                    # Daca punem regele pe patrat, verificam daca este in sah
                    if culoareRege == 'a':
                        self.LocatieRegeAlb = (finalRand, finalCol)
                    else:
                        self.LocatieRegeNegru = (finalRand, finalCol)

                    inSah, pin, sahuri = self.verificareSahuriPinuri()  # verificare daca regele este in sah
                    # daca nu este in sah dupa ce il mutam, adaugam mutarea
                    if not inSah:
                        mutari.append(Mutare((r, c), (finalRand, finalCol), self.Pozitie))

                    # repunem regele pe pozitia in care este acum
                    if culoareRege == 'a':
                        self.LocatieRegeAlb = (r, c)
                    else:
                        self.LocatieRegeNegru = (r, c)

                # adaugam si rocadele valabile
                self.mutariRocada(r, c, mutari, culoareRege)

    '''
    Rocadele regilor
    '''

    def mutariRocada(self, r, c, mutari, culoareRege):
        if not self.inSah:
            if (self.MutareAlb and self.RocadePosibile.aRege) or (not self.MutareAlb and self.RocadePosibile.nRege):
                self.rocadaRege(r, c, mutari, culoareRege)

            if (self.MutareAlb and self.RocadePosibile.aRegina) or (not self.MutareAlb and self.RocadePosibile.nRegina):
                self.rocadaRegina(r, c, mutari, culoareRege)

    def rocadaRege(self, r, c, mutari, culoareRege):
        if self.Pozitie[r][c + 1] == "--" and self.Pozitie[r][c + 2] == "--":
            if not self.patratAtacat(r, c + 1, culoareRege) and not self.patratAtacat(r, c + 2, culoareRege):
                mutari.append(Mutare((r, c), (r, c + 2), self.Pozitie, rocada=True))

    def rocadaRegina(self, r, c, mutari, culoareRege):
        if self.Pozitie[r][c - 1] == "--" and self.Pozitie[r][c - 2] == "--" and self.Pozitie[r][c - 3] == "--":
            if not self.patratAtacat(r, c - 1, culoareRege) and not self.patratAtacat(r, c - 2, culoareRege):
                mutari.append(Mutare((r, c), (r, c - 2), self.Pozitie, rocada=True))

    '''
     Verificare daca un patrat este atacat, folosit pentru rocada
    '''

    def patratAtacat(self, r, c, culoarePiesa):
        culoareOponent = 'a' if culoarePiesa == 'n' else 'n'
        directii = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directii)):
            dr = directii[j]

            for i in range(1, 8):
                finalRand = r + dr[0] * i
                finalCol = c + dr[1] * i

                if 0 <= finalRand < 8 and 0 <= finalCol < 8:
                    patratFinal = self.Pozitie[finalRand][finalCol]
                    if patratFinal[0] == culoarePiesa:
                        break
                    elif patratFinal[0] == culoareOponent:
                        piesa = patratFinal[1]
                        if (0 <= i <= 3 and piesa == 'R') or \
                                (4 <= j <= 7 and piesa == 'B') or \
                                (i == 1 and piesa == 'p' and (
                                        (culoareOponent == 'a' and 6 <= j <= 7) or (
                                         culoareOponent == 'n' and 4 <= j <= 5))) or \
                                (piesa == 'Q') or (i == 1 and piesa == 'K'):
                            return True
                        else:
                            break
                else:
                    break

        patrateCal = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for patrat in patrateCal:
            finalRand = r + patrat[0]
            finalCol = c + patrat[1]
            if 0 <= finalRand < 8 and 0 <= finalCol < 8:
                pozitieCal = self.Pozitie[finalRand][finalCol]
                if pozitieCal[0] == culoareOponent and pozitieCal[1] == 'N':  #
                    return True

        return False

    '''
    Updatare drepturi rocada (cand se muta o tura sau regele)
    '''

    def updateDrepturiRocada(self, mutare):
        if mutare.PiesaMutata == "aK":
            self.RocadePosibile.aRege = False
            self.RocadePosibile.aRegina = False
        elif mutare.PiesaMutata == "nK":
            self.RocadePosibile.nRege = False
            self.RocadePosibile.nRegina = False
        elif mutare.PiesaMutata == "aR":
            if mutare.finalRand == 7:
                if mutare.finalCol == 0:  # tura stanga
                    self.RocadePosibile.aRegina = False
                elif mutare.finalCol == 7:  # tura dreapta
                    self.RocadePosibile.aRege = False
        elif mutare.PiesaMutata == "nR":
            if mutare.finalRand == 0:
                if mutare.finalCol == 0:  # tura stanga
                    self.RocadePosibile.nRegina = False
                elif mutare.finalCol == 7:  # tura dreapta
                    self.RocadePosibile.nRege = False

    '''
    Verificarea de sahuri si pinuri, folosit la calcularea mutarilor valide
    '''

    def verificareSahuriPinuri(self):
        pinuri = []  #
        sahuri = []  #
        inSah = False
        if self.MutareAlb:
            culoareOponent = 'n'
            culoareRege = 'a'
            regeRand = self.LocatieRegeAlb[0]
            regeCol = self.LocatieRegeAlb[1]
        else:
            culoareOponent = 'a'
            culoareRege = 'n'
            regeRand = self.LocatieRegeNegru[0]
            regeCol = self.LocatieRegeNegru[1]

        directii = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1),
                    (1, 1))  # sus, stanga, jos, dreapta, stanga-sus, dreapta-sus, stanga-jos, dreapta-jos

        for j in range(len(directii)):
            dr = directii[j]
            pinPosibil = ()  #
            for i in range(1, 8):
                randPin = regeRand + dr[0] * i
                colPin = regeCol + dr[1] * i

                if 0 <= randPin < 8 and 0 <= colPin < 8:
                    piesa = self.Pozitie[randPin][colPin]
                    if piesa[0] == culoareRege and piesa[1] != 'K':
                        if pinPosibil == ():
                            pinPosibil = (randPin, colPin, dr[0], dr[1])
                        else:
                            break

                    elif piesa[0] == culoareOponent:
                        tipPiesa = piesa[1]
                        # Toate posibilitatile de sah, daca piesa este tura si se afla sus, stanga, jos sau dreapta,
                        # sau este nebun si se afla in diagonala regelui, sau este pion si se afla la un patrat distanta
                        # de rege in diagonala
                        if (0 <= j <= 3 and tipPiesa == 'R') or \
                                (4 <= j <= 7 and tipPiesa == 'B') or \
                                (i == 1 and tipPiesa == 'p' and (
                                        (culoareOponent == 'a' and 6 <= j <= 7) or (
                                        culoareOponent == 'n' and 4 <= j <= 5))) or \
                                (tipPiesa == 'Q') or (i == 1 and tipPiesa == 'K'):
                            if pinPosibil == ():  # daca piesa ataca regele, atunci regele este in sah, si adaugam
                                # sahul in lista
                                inSah = True
                                sahuri.append((randPin, colPin, dr[0], dr[1]))
                                break
                            else:  # daca sahul este blocat, atunci piesa care blocheaza sahul este in pin
                                pinuri.append(pinPosibil)
                                break
                        else:
                            break
                else:
                    break
        # pentru cal este diferit fiindca calul poate sari alte piese, asa ca nu poate face pin altor piese
        patrateCal = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for patrat in patrateCal:
            randCal = regeRand + patrat[0]
            colCal = regeCol + patrat[1]
            if 0 <= randCal < 8 and 0 <= colCal < 8:
                piesa = self.Pozitie[randCal][colCal]
                if piesa[0] == culoareOponent and piesa[1] == 'N':  #
                    inSah = True
                    sahuri.append((randCal, colCal, patrat[0], patrat[1]))

        return inSah, pinuri, sahuri


'''
 Clasa DrepturiRocada stocheaza drepturile pentru rocadele ambilor regi, pentru accesibilitate
'''


class DrepturiRocada:
    def __init__(self, aRege, nRege, aRegina, nRegina):  # alb in partea regelui (dreapta), negru in partea regelui...
        self.aRege = aRege
        self.nRege = nRege
        self.aRegina = aRegina
        self.nRegina = nRegina


'''
 In clasa Mutare se stocheaza toate datele legate de mutari
'''


class Mutare:

    def __init__(self, PatratStart, PatratFinal, pozitie, enpassant=False, rocada=False):
        self.startRand = PatratStart[0]
        self.startCol = PatratStart[1]
        self.finalRand = PatratFinal[0]
        self.finalCol = PatratFinal[1]
        self.PiesaMutata = pozitie[self.startRand][self.startCol]
        self.PiesaCapturata = pozitie[self.finalRand][self.finalCol]

        # promotie
        self.PromotiePion = False
        if (self.PiesaMutata == "ap" and self.finalRand == 0) or (self.PiesaMutata == "np" and self.finalRand == 7):
            self.PromotiePion = True

        # en passant
        self.MutareEnPassant = enpassant
        if self.MutareEnPassant:
            self.PiesaCapturata = "ap" if self.PiesaMutata == "np" else "np"

        # rocada
        self.MutareRocada = rocada
        self.MutareCaptura = self.PiesaCapturata != '--'

        # folosim IDmutare pentru compararea mutarilor unele cu altele
        self.IDmutare = self.startRand * 1000 + self.startCol * 100 + self.finalRand * 10 + self.finalCol

    NotatieRanduri = {0: '8',
                      1: '7',
                      2: '6',
                      3: '5',
                      4: '4',
                      5: '3',
                      6: '2',
                      7: '1'}

    NotatieColoane = {0: 'a',
                      1: 'b',
                      2: 'c',
                      3: 'd',
                      4: 'e',
                      5: 'f',
                      6: 'g',
                      7: 'h'}

    '''
    Supraincarcarea operatorului == pe care il folosim de mai multe ori
    '''

    def __eq__(self, arg):
        if isinstance(arg, Mutare):
            return self.IDmutare == arg.IDmutare
        return False

    def NotatiePatrat(self, r, c):
        return self.NotatieColoane[c] + self.NotatieRanduri[r]

    '''
    supraincarcarea functiei tostring, o facem sa returneze notatie oficiala de sah
    '''

    def __str__(self):
        if self.MutareRocada:
            return "0-0" if self.finalCol == 6 else "0-0-0"

        PatratFinal = self.NotatiePatrat(self.finalRand, self.finalCol)

        # notatia pentru pioni este diferita, nu se mai scrie numele piesei, doar patratul de unde a plecat si unde
        # a ajuns
        if self.PiesaMutata[1] == 'p':
            if (self.finalRand == 0 and self.PiesaMutata[0] == 'a') or (
                    self.finalRand == 7 and self.PiesaMutata[0] == 'n'):
                return PatratFinal + "=Q"

            if self.MutareCaptura:
                return self.NotatieColoane[self.startCol] + 'x' + PatratFinal

            else:
                return PatratFinal

        TipPiesa = self.PiesaMutata[1]
        if self.MutareCaptura:
            TipPiesa += 'x'

        return TipPiesa + PatratFinal
