from threading import *
from random import *
from time import sleep


class Semaforo:
    lck = RLock()  # Variabile statica di tipo reentrant Lock


class SemaforoDati:
    lckDati = RLock()  # Variabile statica di tipo reentrant Lock


class Dati:
    listaDati = [-1] * 10


class DatiSync:
    lckDati = RLock()  # Variabile statica di tipo reentrant Lock
    listaDati = [-1] * 10

    @staticmethod
    def write(listaEsterna):
        DatiSync.lckDati.acquire()

        # DatiSync.listaDati = listaEsterna
        """
        Errore: DatiSync.listaDati diventa alias di listaEsterna,
        poichè viene copiato solo l'indirizzo e non il contenuto (mutabile)
        Soluzione: Bisogna quindi copiare elemento per elemento
        """
        for pos in range(len(listaEsterna)):
            DatiSync.listaDati[pos] = listaEsterna[pos]
            sleep(randint(0, 1) / 2)

        DatiSync.lckDati.release()

    @staticmethod
    def read():
        DatiSync.lckDati.acquire()
        # nuova variabile su cui verrà copiato il contenuto listaDati, da ritornare all'esterno
        listaCopia = [-1] * 10

        for pos in range(len(DatiSync.listaDati)):
            listaCopia[pos] = DatiSync.listaDati[pos]
            sleep(randint(0, 1) / 2)

        DatiSync.lckDati.release()

        return listaCopia


class DatiCoop:
    lckDati = RLock()  # Variabile statica di tipo reentrant Lock
    varCondPieno = Condition(lckDati)
    varCondVuoto = Condition(lckDati)
    pieno = False  # Stato di partenza non si può leggere
    vuoto = True  # Stato di partenza si può scrivere
    listaDati = [-1] * 10

    @staticmethod
    def write(listaEsterna):
        DatiCoop.lckDati.acquire()

        # DatiSync.listaDati = listaEsterna
        """
        Errore: DatiSync.listaDati diventa alias di listaEsterna,
        poichè viene copiato solo l'indirizzo e non il contenuto (mutabile)
        Soluzione: Bisogna quindi copiare elemento per elemento
        """
        while DatiCoop.pieno:
            DatiCoop.varCondPieno.wait()

        # Quando sono qui significa che la mia attesa è finita
        # pieno vale false: posso scrivere
        for pos in range(len(listaEsterna)):
            DatiCoop.listaDati[pos] = listaEsterna[pos]
            sleep(randint(0, 1) / 2)

        DatiCoop.pieno = True
        DatiCoop.vuoto = False

        DatiCoop.varCondVuoto.notify()
        DatiCoop.lckDati.release()

    @staticmethod
    def read():
        DatiCoop.lckDati.acquire()
        # nuova variabile su cui verrà copiato il contenuto listaDati, da ritornare all'esterno
        listaCopia = [-1] * 10

        while DatiCoop.vuoto:
            DatiCoop.varCondVuoto.wait()

        # Quando sono qui significa che la mia attesa è finita
        # vuoto vale false: posso leggere
        for pos in range(len(DatiCoop.listaDati)):
            listaCopia[pos] = DatiCoop.listaDati[pos]
            # imposto a -1 la lista statica in modo da renderla logicamente vuota
            DatiCoop.listaDati[pos] = -1
            sleep(randint(0, 1) / 2)

        DatiCoop.pieno = False
        DatiCoop.vuoto = True

        DatiCoop.varCondPieno.notify()
        DatiCoop.lckDati.release()

        return listaCopia


def produttore1(numeroLancio, tipoMyPrint):
    myPrint(f"Inizio Thread corrente: {current_thread().name}", tipoMyPrint)
    numero = randint(1, 1000)
    myPrint(f"--- {numeroLancio}° Numero generato: {numero} ---", tipoMyPrint)
    binario(numero, tipoMyPrint)
    ottale(numero, tipoMyPrint)
    esadecimale(numero, tipoMyPrint)
    sleep(randint(1, 4))
    myPrint(f"--- {numeroLancio}° Numero convertito ---", tipoMyPrint)
    myPrint(f"Fine Thread corrente: {current_thread().name}", tipoMyPrint)


def produttore2(numeroLancio, tipoMyPrint):
    updateDati(numeroLancio)
    myPrint(f"{Dati.listaDati}", tipoMyPrint)


def produttore3(numeroLancio, tipoMyPrint):
    SemaforoDati.lckDati.acquire()
    try:
        updateDati(numeroLancio)
    finally:
        SemaforoDati.lckDati.release()

    sleep(0.01)  # Forza lo scambio di contesto fra i due semafori, che non sono vincolati
    myPrint(f"{Dati.listaDati}", tipoMyPrint)


def produttore4(numeroLancio, tipoMyPrint):
    SemaforoDati.lckDati.acquire()
    try:
        updateDati(numeroLancio)
    finally:
        myPrint(f"{Dati.listaDati}", tipoMyPrint)
        SemaforoDati.lckDati.release()


def produttore5(numeroLancio, tipoMyPrint):
    listaEsterna = [numeroLancio] * 10
    try:
        DatiSync.write(listaEsterna)
    finally:
        myPrint(f"Write{numeroLancio}: {DatiSync.listaDati}", tipoMyPrint)


def produttore6(numeroLancio, tipoMyPrint):
    try:
        produttore5(numeroLancio, -1)
    finally:
        listaEsterna = DatiSync.read()
        myPrint(f"Read{numeroLancio}: {listaEsterna}", tipoMyPrint)


def produttore(numeroLancio, tipoMyPrint):
    listaEsterna = [numeroLancio] * 10
    DatiCoop.write(listaEsterna)
    myPrint(f"Write Produttore {numeroLancio}: {listaEsterna}", tipoMyPrint)


def consumatore(numeroLancio, tipoMyPrint):
    listaEsterna = DatiCoop.read()
    myPrint(f"Read Consumatore {numeroLancio}: {listaEsterna}", tipoMyPrint)


def binario(numero, tipoMyPrint):
    dec2bin = bin(numero)
    bin2dec = int(dec2bin, 2)
    myPrint(f"--- Binario ---", tipoMyPrint)
    myPrint(f"Numero: {numero} -> Ottale: {dec2bin}", tipoMyPrint)
    myPrint(f"--- Verifica Ottale ---", tipoMyPrint)
    myPrint(f"Ottale: {dec2bin} -> Decimale: {bin2dec}", tipoMyPrint)


def ottale(numero, tipoMyPrint):
    dec2oct = oct(numero)
    oct2dec = int(dec2oct, 8)
    myPrint(f"--- Ottale ---", tipoMyPrint)
    myPrint(f"Numero: {numero} -> Ottale: {dec2oct}", tipoMyPrint)
    myPrint(f"--- Verifica Ottale ---", tipoMyPrint)
    myPrint(f"Ottale: {dec2oct} -> Decimale: {oct2dec}", tipoMyPrint)


def esadecimale(numero, tipoMyPrint):
    dec2hex = hex(numero)
    hex2dec = int(dec2hex, 16)
    myPrint(f"--- Esadecimale ---", tipoMyPrint)
    myPrint(f"Numero: {numero} -> Esadecimale: {dec2hex}", tipoMyPrint)
    myPrint(f"--- Verifica Esadecimale ---", tipoMyPrint)
    myPrint(f"Esadecimale: {dec2hex} -> Decimale: {hex2dec}", tipoMyPrint)


def updateDati(numeroLancio):
    for i in range(len(Dati.listaDati)):
        Dati.listaDati[i] = numeroLancio
        sleep(randint(0, 1) / 2)


def myPrint(stringa, tipoMyPrint):
    if tipoMyPrint == 1:  # Stampa di sistema
        print(stringa)
    elif tipoMyPrint == 2:  # Stampa carattere per carattere
        myPrint2(stringa)
    elif tipoMyPrint == 3:  # Stampa carattere per carattere, uso del semaforo
        myPrint3(stringa)


def myPrint2(stringa):
    for s in stringa:
        print(s, end="")

    print('\n', end="")


def myPrint3(stringa):
    Semaforo.lck.acquire()
    try:
        myPrint2(stringa)
    finally:
        Semaforo.lck.release()
