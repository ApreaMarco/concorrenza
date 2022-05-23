from threading import *
from random import *
from time import sleep


class Semaforo:
    lck = RLock()  # Variabile statica di tipo reentrant Lock


class SemaforoDati:
    lckDati = RLock()  # Variabile statica di tipo reentrant Lock


class Dati:
    listaDati = [-1] * 10


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
