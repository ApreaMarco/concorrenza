from convertitore import *
from time import time


def main():
    input("Premi un tasto qualsialsi")
    t0 = time()
    tipoProduttore = [produttore1, produttore2, produttore3, produttore4,
                      produttore5, produttore6]  # Produttori disponibili
    produttoreTest = tipoProduttore[4]  # Produttore scelto per il test
    tipoMyPrint = [1, 2, 3]  # Stampe disponibili
    myPrintTest = tipoMyPrint[2]  # Tipo di stampa scelto per il test

    for i in range(1, 11):
        # QUI IL CODICE SPECIFICO PER L’IMPLEMENTAZIONE SCELTA
        produttoreTest(i, myPrintTest)

    tn = time()
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
