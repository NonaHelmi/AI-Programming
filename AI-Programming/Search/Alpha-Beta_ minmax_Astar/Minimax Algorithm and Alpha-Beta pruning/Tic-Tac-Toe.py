# Racovita Andra-Georgiana
# Grupa 232
# X si 0

import time
import copy


def elem_identice(lista):
    """ Primeste o lista si returneaza
    -> simbolul jucatorului castigator (daca lista contine doar acel simbol repetat)
    -> sau False (daca a fost remiza sau daca nu s-a terminat jocul)
    """
    mt = set(lista)
    if len(mt) == 1:
        castigator = list(mt)[0]
        if castigator != Joc.GOL:
            return castigator
        else:
            return False
    else:
        return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_LINII = 3
    NR_COLOANE = 3
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.matr = tabla or [Joc.GOL]*(Joc.NR_COLOANE * Joc.NR_LINII)
        # self.matr = tabla or [[self.GOL for j in range(self.NR_COLOANE)]
        #                       for i in range(self.NR_LINII)]

    def final(self):
        # Folosim slice-uri pe lista de 9 elemente
        # pentru a gasi usor cele 3 linii, 3 coloane si 2 diagonale
        # si a verifica daca a castigat cineva (return simbolul castigatorului),
        # daca a fost remiza (return "remiza"),
        # sau daca nu s-a terminat jocul (return False)
        rez = (elem_identice(self.matr[0:3])
               or elem_identice(self.matr[3:6])
               or elem_identice(self.matr[6:9])
               or elem_identice(self.matr[0:9:3])
               or elem_identice(self.matr[1:9:3])
               or elem_identice(self.matr[2:9:3])
               or elem_identice(self.matr[0:9:4])
               or elem_identice(self.matr[2:8:2]))
        if(rez):
            return rez
        elif Joc.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari_joc(self, jucator):
        """
        Pentru configuratia curenta de joc "self.matr" (de tip lista, cu 9 elemente),
        trebuie sa returnati o lista "l_mutari" cu elemente de tip Joc,
        corespunzatoare tuturor configuratiilor-succesor posibile.

        "jucator" este simbolul jucatorului care face mutarea
        """
        l_mutari = []

        for i in range(self.NR_COLOANE * self.NR_LINII):
            if self.matr[i] == "#":
                mutare = copy.deepcopy(self.matr)
                mutare[i] = jucator
                l_mutari.append(Joc(mutare))

        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate
    # forma o configuratie castigatoare
    def linie_deschisa(self, lista, jucator):
        """
        # rezolvare alternativa:
        juc_opus = 'x' if jucator=='0' else '0'
        if juc_opus in lista:
                return 0
        return 1
        """

        # obtin multimea simbolurilor de pe linie
        mt = set(lista)
        # verific daca sunt maxim 2 simboluri
        if len(mt) <= 2:
            # daca multimea simbolurilor nu are alte simboluri decat pentru cel de "gol" si jucatorul curent
            if mt <= {Joc.GOL, jucator}:  # incluziune de seturi
                # inseamna ca linia este deschisa
                return 1
            else:
                return 0
        else:
            return 0

    def linii_deschise(self, jucator):
        return (self.linie_deschisa(self.matr[0:3], jucator)
                + self.linie_deschisa(self.matr[3:6], jucator)
                + self.linie_deschisa(self.matr[6:9], jucator)
                + self.linie_deschisa(self.matr[0:9:3], jucator)
                + self.linie_deschisa(self.matr[1:9:3], jucator)
                + self.linie_deschisa(self.matr[2:9:3], jucator)
                # prima diagonala
                + self.linie_deschisa(self.matr[0:9:4], jucator)
                + self.linie_deschisa(self.matr[2:8:2], jucator))  # a doua diagonala

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (99 + adancime)
        elif t_final == Joc.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.linii_deschise(Joc.JMAX) - self.linii_deschise(Joc.JMIN)

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:3]])+"\n" +
               " ".join([str(x) for x in self.matr[3:6]])+"\n" +
               " ".join([str(x) for x in self.matr[6:9]])+"\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
        self.j_curent = j_curent  # simbolul jucatorului curent

        # adancimea in arborele de stari
        #	(scade cu cate o unitate din „tata” in „fiu”)
        self.adancime = adancime

        # scorul starii (daca e finala, adica frunza a arborelui)
        # sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []  # lista va contine obiecte de tip Stare

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari_stare(self):
        l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
        juc_opus = self.jucator_opus()

        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent+")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):

    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Altfel, calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari_stare()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Conditia de retezare:
    if alpha >= beta:
        return stare  # este intr-un interval invalid, deci nu o mai procesez

    # Calculez toate mutarile posibile din starea curenta (toti „fiii”)
    stare.mutari_posibile = stare.mutari_stare()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

        # pentru fiecare „fiu” de tip MIN:
        for mutare in stare.mutari_posibile:
            # calculeaza scorul fiului curent
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (cresc) scorul si alfa
            # „tatalui” de tip MAX, folosind scorul fiului curent
            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MIN

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')  # scorul „tatalui” de tip MIN

        # pentru fiecare „fiu” de tip MAX:
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (scad) scorul si beta
            # „tatalui” de tip MIN, folosind scorul fiului curent
            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if(final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat "+final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input(
            "Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', Stare.ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    linie = int(input("linie="))
                    coloana = int(input("coloana="))

                    if (linie in range(0, 3) and coloana in range(0, 3)):
                        if stare_curenta.tabla_joc.matr[linie*3+coloana] == Joc.GOL:
                            raspuns_valid = True
                        else:
                            print("Exista deja un simbol in pozitia ceruta.")
                    else:
                        print(
                            "Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2).")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie*3+coloana] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
