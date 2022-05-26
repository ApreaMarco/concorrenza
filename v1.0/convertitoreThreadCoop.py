from convertitore import *
from time import time


def main():
    input("Premi un tasto qualsialsi")
    t0 = time()
    tipoMyPrint = [1, 2, 3]  # Stampe disponibili
    myPrintTest = tipoMyPrint[2]  # Tipo di stampa scelto per il test
    lst = []  # Lista dei thread in join

    for i in range(1, 11):
        myPrint("main: prima della creazione del thread produttore", myPrintTest)
        t = Thread(target=produttore, args=(i, myPrintTest,))
        myPrint("main: prima dell'esecuzione del thread produttore", myPrintTest)
        t.start()
        lst.append(t)

    for i in range(1, 11):
        myPrint("main: prima della creazione del thread consumatore", myPrintTest)
        t = Thread(target=consumatore, args=(i, myPrintTest,))
        myPrint("main: prima dell'esecuzione del thread consumatore", myPrintTest)
        t.start()
        lst.append(t)

    myPrint("main: attesa fine esecuzione dei thread", myPrintTest)

    for th in lst:  # Attendo la fine di tutti i thread contenuti nella lista
        th.join()

    tn = time()
    myPrint("main: fine del main", myPrintTest)
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
