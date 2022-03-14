import random

Sahmat = 1000
Pat = 0
adancimeRecursivitate = 3

scorPiese = {"K": 0,
             "Q": 9,
             "R": 5,
             "B": 3,
             "N": 3,
             "p": 1}

calScor = [[1, 1, 1, 1, 1, 1, 1, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 1, 1, 1, 1, 1, 1, 1]]

AnebunScor = [[2, 1, 1, 1, 1, 1, 1, 2],
              [1, 3, 1, 1, 1, 1, 3, 1],
              [2, 2, 3, 2, 2, 3, 2, 2],
              [1, 4, 3, 4, 4, 3, 4, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [2, 2, 4, 3, 3, 4, 2, 2],
              [2, 4, 2, 2, 2, 2, 4, 2],
              [3, 2, 1, 1, 1, 1, 2, 3]]

NnebunScor = [[3, 2, 1, 1, 1, 1, 2, 3],
              [2, 4, 2, 2, 2, 2, 4, 2],
              [2, 2, 4, 3, 3, 4, 2, 2],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 4, 3, 4, 4, 3, 4, 1],
              [2, 2, 3, 2, 2, 3, 2, 2],
              [1, 3, 1, 1, 1, 1, 3, 1],
              [2, 1, 1, 1, 1, 1, 1, 2]]

AturaScor = [[3, 3, 3, 4, 4, 3, 3, 3],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [2, 2, 2, 4, 4, 2, 2, 2],
             [2, 2, 2, 4, 4, 2, 2, 2]]

NturaScor = [[2, 2, 2, 4, 4, 2, 2, 2],
             [2, 2, 2, 4, 4, 2, 2, 2],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [3, 3, 3, 4, 4, 3, 3, 3]]

AreginaScor = [[3, 3, 3, 3, 3, 3, 3, 3],
               [3, 3, 3, 3, 3, 3, 3, 3],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 2, 2, 2, 2, 2, 2],
               [2, 1, 2, 2, 2, 2, 3, 1],
               [1, 4, 1, 2, 2, 4, 1, 1],
               [1, 1, 3, 2, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

NreginaScor = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 1, 3, 2, 3, 1, 1, 1],
               [1, 4, 1, 2, 2, 4, 1, 1],
               [2, 1, 2, 2, 2, 2, 3, 1],
               [1, 2, 2, 2, 2, 2, 2, 2],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [3, 3, 3, 3, 3, 3, 3, 3],
               [3, 3, 3, 3, 3, 3, 3, 3]]

ApionScor = [[9, 9, 9, 9, 9, 9, 9, 9],
             [8, 8, 8, 8, 8, 8, 8, 8],
             [5, 6, 6, 7, 7, 6, 6, 5],
             [2, 3, 3, 4, 4, 3, 3, 2],
             [1, 2, 3, 3, 3, 3, 2, 1],
             [1, 1, 2, 3, 3, 1, 1, 1],
             [1, 1, 1, 0, 0, 2, 2, 2],
             [0, 0, 0, 0, 0, 0, 0, 0]]

NpionScor = [[0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 1, 1, 1],
             [1, 1, 2, 3, 3, 1, 1, 1],
             [1, 2, 3, 3, 3, 2, 2, 1],
             [2, 3, 3, 4, 4, 3, 3, 2],
             [5, 6, 6, 7, 7, 6, 6, 5],
             [8, 8, 8, 8, 8, 8, 8, 8],
             [9, 9, 9, 9, 9, 9, 9, 9]]

AregeScor = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 2, 5, 0, 0, 0, 5, 2]]

NregeScor = [[1, 2, 5, 0, 0, 0, 5, 2],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

ScorPozitional = {"aK": AregeScor,
                  "nK": NregeScor,
                  "aQ": AreginaScor,
                  "nQ": NreginaScor,
                  "aR": AturaScor,
                  "nR": NturaScor,
                  "aB": AnebunScor,
                  "nB": NnebunScor,
                  "aN": calScor,
                  "nN": calScor,
                  "ap": ApionScor,
                  "np": NpionScor}


def MutareRandom(mutariValide):
    return mutariValide[random.randint(0, len(mutariValide) - 1)]


'''
Helper method to make the first recursive call
'''


def MutareAlgoritm(stareJoc, mutariValide, queueMutari):
    global mutareaUrmatoare, contor
    mutareaUrmatoare = None
    random.shuffle(mutariValide)
    contor = 0
    # MutareMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # MutareNegaMax(stareJoc, mutariValide, adancimeRecursivitate, 1 if stareJoc.MutareAlb else -1)
    MutareNegaMaxAlphaBeta(stareJoc, mutariValide, adancimeRecursivitate, -Sahmat, Sahmat, 1 if stareJoc.MutareAlb else -1)
    #print("Pozitii evaluate cu AB pruning:", contor)
    queueMutari.put(mutareaUrmatoare)


def MinMaxNonRecursiv(stareJoc, mutariValide):
    coeficientCuloare = 1 if stareJoc.MutareAlb else -1
    scorOponentMinMax = Sahmat
    Mutare = None

    for mutareJucator in mutariValide:
        stareJoc.MutarePiesa(mutareJucator)
        mutariOponent = stareJoc.MutariValide()

        if stareJoc.pat:
            scorMaxOponent = Pat

        elif stareJoc.sahmat:
            scorMaxOponent = Sahmat * coeficientCuloare

        else:
            scorMaxOponent = Sahmat * -coeficientCuloare
            for mutareOponent in mutariOponent:
                stareJoc.MutarePiesa(mutareOponent)
                stareJoc.MutariValide()
                if stareJoc.sahmat:
                    scor = Sahmat * -coeficientCuloare
                elif stareJoc.pat:
                    scor = Pat
                else:
                    scor = ScorPozitie(stareJoc.Pozitie)
                if coeficientCuloare == 1 and scor > scorMaxOponent:
                    scorMaxOponent = scor
                elif coeficientCuloare == -1 and scor < scorMaxOponent:
                    scorMaxOponent = scor
                stareJoc.undoMutare()

        if coeficientCuloare == 1 and scorMaxOponent > scorOponentMinMax:
            scorOponentMinMax = scorMaxOponent
            Mutare = mutareJucator
        elif coeficientCuloare == -1 and scorMaxOponent < scorOponentMinMax:
            scorOponentMinMax = scorMaxOponent
            Mutare = mutareJucator
        stareJoc.undoMutare()

    return Mutare


def MutareMinMax(stareJoc, mutariValide, adancime, mutareAlb):
    global mutareaUrmatoare, contor
    contor += 1
    if adancime == 0:
        return ScorPozitie(stareJoc.Pozitie)

    if mutareAlb:
        maxScor = -Sahmat
        for move in mutariValide:
            stareJoc.MutarePiesa(move)
            mutariOponent = stareJoc.MutariValide()
            scor = MutareMinMax(stareJoc, mutariOponent, adancime - 1, False)
            if scor > maxScor:
                maxScor = scor
                if adancime == adancimeRecursivitate:
                    mutareaUrmatoare = move
            stareJoc.undoMutare()
        return maxScor

    else:
        minScore = Sahmat
        for move in mutariValide:
            stareJoc.MutarePiesa(move)
            mutariOponent = stareJoc.MutariValide()
            scor = MutareMinMax(stareJoc, mutariOponent, adancime - 1, True)
            if scor < minScore:
                minScore = scor
                if adancime == adancimeRecursivitate:
                    mutareaUrmatoare = move
            stareJoc.undoMutare()
        return minScore


def MutareNegaMax(stareJoc, mutariValide, adancime, coeficientCuloare):
    global mutareaUrmatoare, contor
    contor += 1
    if adancime == 0:
        return coeficientCuloare * ScorPozitie(stareJoc)

    maxScor = -Sahmat
    for mutare in mutariValide:
        stareJoc.MutarePiesa(mutare)
        mutariOponent = stareJoc.MutariValide()
        scor = -MutareNegaMax(stareJoc, mutariOponent, adancime - 1, -coeficientCuloare)
        if scor > maxScor:
            maxScor = scor
            if adancime == adancimeRecursivitate:
                mutareaUrmatoare = mutare

        stareJoc.undoMutare()
    return maxScor


def MutareNegaMaxAlphaBeta(stareJoc, mutariValide, adancime, alpha, beta, coeficientCuloare):
    global mutareaUrmatoare, contor
    contor += 1
    if adancime == 0:
        return coeficientCuloare * ScorPozitie(stareJoc)

    maxScor = -Sahmat
    for mutare in mutariValide:
        stareJoc.MutarePiesa(mutare)
        mutariOponent = stareJoc.MutariValide()
        scor = -MutareNegaMaxAlphaBeta(stareJoc, mutariOponent, adancime - 1, -beta, -alpha, -coeficientCuloare)
        if scor > maxScor:
            maxScor = scor
            if adancime == adancimeRecursivitate:
                mutareaUrmatoare = mutare
                # print(mutare, scor)

        stareJoc.undoMutare()
        if maxScor > alpha:
            alpha = maxScor
        if alpha >= beta:
            break

    return maxScor


def ScorPozitie(stareJoc):
    if stareJoc.sahmat:
        if stareJoc.MutareAlb:
            return -Sahmat
        else:
            return Sahmat
    elif stareJoc.pat:
        return Pat

    scor = 0
    for r in range(len(stareJoc.Pozitie)):
        for c in range(len(stareJoc.Pozitie[r])):
            patrat = stareJoc.Pozitie[r][c]
            if patrat != "--":
                scorPatrat = ScorPozitional[patrat][r][c]
                if patrat[0] == 'a':
                    scor += scorPiese[patrat[1]] + scorPatrat * 0.1
                elif patrat[0] == 'n':
                    scor -= scorPiese[patrat[1]] + scorPatrat * 0.1

    return scor
