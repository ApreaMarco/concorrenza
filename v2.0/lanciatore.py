from libConvertitore import *
from time import time
from sys import argv


def validaArgs(args, tipoImplementazione, tipoProduttore, tipoMyPrint):
    if len(args) != 4:
        exit(0)

    lstArgs = []
    for arg in args:
        try:
            lstArgs.append(int(arg))
        except:
            exit(1)

    if lstArgs[0] >= len(tipoImplementazione):
        exit(2)

    if lstArgs[1] >= len(tipoProduttore):
        exit(3)

    if lstArgs[2] >= len(tipoMyPrint):
        exit(4)

    if lstArgs[3] < 1:
        exit(5)
    return lstArgs


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
    args = argv[1:]  # lista di parametri d'ingresso
    tipoImplementazione = ["sequenziale", "thread", "deamon", "threadJoin", "deamonJoin"]  # Implementazioni disponibili
    tipoProduttore = ["produttore1", "produttore2", "produttore3", "produttore4"]  # Produttori disponibili
    tipoMyPrint = ["sistema", "carattere", "messaggio"]  # Stampe disponibili

    lstArgs = validaArgs(args, tipoImplementazione, tipoProduttore, tipoMyPrint)

    input("Premi un tasto")
    tipoImplementazioneTest = tipoImplementazione[lstArgs[0]]  # Tipo di implementazione scelta per il test
    produttoreTest = tipoProduttore[lstArgs[1]]  # Produttore scelto per il test
    myPrintTest = tipoMyPrint[lstArgs[2]]  # Tipo di stampa scelto per il test
    numeroLanci = lstArgs[3]

    # QUI IL CODICE SPECIFICO PER L’IMPLEMENTAZIONE SCELTA
    selettoreImplementazione(tipoImplementazioneTest, produttoreTest, numeroLanci, myPrintTest)

    tn = time()
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
