from threading import *
from random import *
from time import sleep


class Semaforo:
    lck = RLock()  # Variabile statica di tipo reentrant Lock


class SemaforoDati:
    lckDati = RLock()  # Variabile statica di tipo reentrant Lock


class Dati:
    listaDati = []


def selettoreProduttore(tipoProduttore, numeroLancio, tipoMyPrint):
    if tipoProduttore == "produttore1":
        produttore1(numeroLancio, tipoMyPrint)
    elif tipoProduttore == "produttore2":
        produttore2(numeroLancio, tipoMyPrint)
    elif tipoProduttore == "produttore3":
        produttore3(numeroLancio, tipoMyPrint)
    elif tipoProduttore == "produttore4":
        produttore4(numeroLancio, tipoMyPrint)


def produttore1(numeroLancio, tipoMyPrint):
    myPrint(f"Inizio Thread corrente: {current_thread().name}", tipoMyPrint)
    numero = randint(1, 1000)
    myPrint(f"--- {numeroLancio}° Numero generato: {numero} ---", tipoMyPrint)
    conversioneBinaria = binario(numero, tipoMyPrint)
    conversioneOttale = ottale(numero, tipoMyPrint)
    conversioneEsadecimale = esadecimale(numero, tipoMyPrint)
    sleep(randint(1, 4))
    myPrint(f"--- {numeroLancio}° Numero convertito ---", tipoMyPrint)
    myPrint(f"Fine Thread corrente: {current_thread().name}", tipoMyPrint)
    return numero, conversioneBinaria, conversioneOttale, conversioneEsadecimale


def produttore2(numeroLancio, tipoMyPrint):
    dato = produttore1(numeroLancio, -1)
    status = updateDati(numeroLancio, dato)
    myPrint(f"Lancio {numeroLancio}: Storicizzati {status[0]}; {status[1]} -> {Dati.listaDati}", tipoMyPrint)


def produttore3(numeroLancio, tipoMyPrint):
    SemaforoDati.lckDati.acquire()
    try:
        dato = produttore1(numeroLancio, -1)
        status = updateDati(numeroLancio, dato)
    finally:
        SemaforoDati.lckDati.release()

    sleep(0.01)  # Forza lo scambio di contesto fra i due semafori, che non sono vincolati
    myPrint(f"Lancio {numeroLancio}: Storicizzati {status[0]}; {status[1]} -> {Dati.listaDati}", tipoMyPrint)


def produttore4(numeroLancio, tipoMyPrint):
    SemaforoDati.lckDati.acquire()
    try:
        dato = produttore1(numeroLancio, -1)
        status = updateDati(numeroLancio, dato)
    finally:
        myPrint(f"Lancio {numeroLancio}: Storicizzati {status[0]}; {status[1]} -> {Dati.listaDati}", tipoMyPrint)
        SemaforoDati.lckDati.release()


def binario(numero, tipoMyPrint):
    sistema = "Binario"
    convertito = bin(numero)
    convertitoSistema = int(convertito, 2)
    logConversione(sistema, numero, convertito, convertitoSistema, tipoMyPrint)
    return convertito, convertitoSistema


def ottale(numero, tipoMyPrint):
    sistema = "Ottale"
    convertito = oct(numero)
    convertitoSistema = int(convertito, 8)
    logConversione(sistema, numero, convertito, convertitoSistema, tipoMyPrint)
    return convertito, convertitoSistema


def esadecimale(numero, tipoMyPrint):
    sistema = "Esadecimale"
    convertito = hex(numero)
    convertitoSistema = int(convertito, 16)
    logConversione(sistema, numero, convertito, convertitoSistema, tipoMyPrint)
    return convertito, convertitoSistema


def logConversione(sistema, numero, convertito, convertitoSistema, tipoMyPrint):
    myPrint(f"--- {sistema} ---", tipoMyPrint)
    myPrint(f"Numero: {numero} -> {sistema}: {convertito}", tipoMyPrint)
    myPrint(f"--- Verifica {sistema} ---", tipoMyPrint)
    myPrint(f"{sistema}: {convertito} -> Decimale: {convertitoSistema}", tipoMyPrint)


def updateDati(numeroLancio, numero):
    Dati.listaDati.append(numero)
    sleep(randint(0, 1) / 2)
    storicizzati = len(Dati.listaDati)
    messaggio = "Dato non pronto"

    if storicizzati >= numeroLancio:
        messaggio = Dati.listaDati[numeroLancio - 1]

    return storicizzati, messaggio


def myPrint(stringa, tipoMyPrint):
    if tipoMyPrint == "sistema":  # Stampa di sistema
        print(stringa)
    elif tipoMyPrint == "carattere":  # Stampa carattere per carattere
        myPrint2(stringa)
    elif tipoMyPrint == "messaggio":  # Stampa carattere per carattere, uso del semaforo
        myPrint3(stringa)
    else:
        pass


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
