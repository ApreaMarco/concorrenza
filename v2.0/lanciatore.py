from libConvertitore import *
from time import time


def selettoreImplementazione(tipoImplementazione, tipoProduttore, numeroLanci, tipoMyPrint):
    myPrint(f"p1: {tipoImplementazione}, p2: {tipoProduttore}, p3: {numeroLanci}, p4: {tipoMyPrint}", tipoMyPrint)

    if tipoImplementazione == "sequenziale":
        implementazione1(tipoProduttore, numeroLanci, tipoMyPrint)
    elif tipoImplementazione == "thread":
        implementazione2(tipoProduttore, numeroLanci, tipoMyPrint)
    elif tipoImplementazione == "deamon":
        implementazione3(tipoProduttore, numeroLanci, tipoMyPrint)
    elif tipoImplementazione == "threadJoin":
        implementazione4(tipoProduttore, numeroLanci, tipoMyPrint)
    elif tipoImplementazione == "deamonJoin":
        implementazione5(tipoProduttore, numeroLanci, tipoMyPrint)


def implementazione1(tipoProduttore, numeroLanci, tipoMyPrint):
    for numeroLancio in range(1, numeroLanci + 1):
        selettoreProduttore(tipoProduttore, numeroLancio, tipoMyPrint)


def implementazione2(tipoProduttore, numeroLanci, tipoMyPrint):
    for numeroLancio in range(1, numeroLanci + 1):
        myPrint("main: prima della creazione del thread", tipoMyPrint)
        t = Thread(target=selettoreProduttore, args=(tipoProduttore, numeroLancio, tipoMyPrint,))
        myPrint("main: prima dell'esecuzione del thread", tipoMyPrint)
        t.start()


def implementazione3(tipoProduttore, numeroLanci, tipoMyPrint):
    for numeroLancio in range(1, numeroLanci + 1):
        myPrint("main: prima della creazione del thread", tipoMyPrint)
        t = Thread(target=selettoreProduttore, args=(tipoProduttore, numeroLancio, tipoMyPrint,), daemon=True)
        myPrint("main: prima dell'esecuzione del thread", tipoMyPrint)
        t.start()


def implementazione4(tipoProduttore, numeroLanci, tipoMyPrint):
    lst = []  # Lista dei thread in join

    for numeroLancio in range(1, numeroLanci + 1):
        myPrint("main: prima della creazione del thread", tipoMyPrint)
        t = Thread(target=selettoreProduttore, args=(tipoProduttore, numeroLancio, tipoMyPrint,))
        myPrint("main: prima dell'esecuzione del thread", tipoMyPrint)
        t.start()
        lst.append(t)

    myPrint("main: attesa fine esecuzione dei thread", tipoMyPrint)

    for th in lst:  # Attendo la fine di tutti i thread contenuti nella lista
        th.join()


def implementazione5(tipoProduttore, numeroLanci, tipoMyPrint):
    lst = []  # Lista dei thread in join

    for numeroLancio in range(1, numeroLanci + 1):
        myPrint("main: prima della creazione del thread", tipoMyPrint)
        t = Thread(target=selettoreProduttore, args=(tipoProduttore, numeroLancio, tipoMyPrint,), daemon=True)
        myPrint("main: prima dell'esecuzione del thread", tipoMyPrint)
        t.start()
        lst.append(t)

    myPrint("main: attesa fine esecuzione dei thread", tipoMyPrint)

    for th in lst:  # Attendo la fine di tutti i thread contenuti nella lista
        th.join()


def main():
    t0 = time()
    tipoImplementazione = ["sequenziale", "thread", "deamon", "threadJoin", "deamonJoin"]  # Implementazioni disponibili
    tipoProduttore = ["produttore1", "produttore2", "produttore3", "produttore4"]  # Produttori disponibili
    tipoMyPrint = ["sistema", "carattere", "messaggio"]  # Stampe disponibili

    tipoImplementazioneTest = tipoImplementazione[3]  # Tipo di implementazione scelta per il test
    produttoreTest = tipoProduttore[2]  # Produttore scelto per il test
    numeroLanci = 10
    myPrintTest = tipoMyPrint[0]  # Tipo di stampa scelto per il test

    # QUI IL CODICE SPECIFICO PER L’IMPLEMENTAZIONE SCELTA
    selettoreImplementazione(tipoImplementazioneTest, produttoreTest, numeroLanci, myPrintTest)

    tn = time()
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
