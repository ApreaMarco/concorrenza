from convertitore import *
from time import time


def main():
    input("Premi un tasto qualsialsi")
    t0 = time()
    tipoProduttore = [produttore1, produttore2, produttore3, produttore4,
                      produttore5, produttore6]  # Produttori disponibili
    produttoreTest = tipoProduttore[0]  # Produttore scelto per il test
    tipoMyPrint = [1, 2, 3]  # Stampe disponibili
    myPrintTest = tipoMyPrint[0]  # Tipo di stampa scelto per il test
    lst = []  # Lista dei thread in join

    for i in range(1, 11):
        # QUI IL CODICE SPECIFICO PER L’IMPLEMENTAZIONE SCELTA
        myPrint("main: prima della creazione del thread", myPrintTest)
        t = Thread(target=produttoreTest, args=(i, myPrintTest,), daemon=True)
        lst.append(t)
        myPrint("main: prima dell'esecuzione del thread", myPrintTest)
        t.start()

    myPrint("main: attesa fine esecuzione del thread", myPrintTest)

    for th in lst:  # Attendo la fine di tutti i thread contenuti nella lista
        th.join()

    tn = time()
    myPrint("main: fine del main", myPrintTest)
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
