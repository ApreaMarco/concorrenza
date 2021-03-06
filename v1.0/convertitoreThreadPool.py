import concurrent.futures
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

    myPrint("main: prima della creazione del thread", myPrintTest)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        myPrint("main: prima dell'esecuzione del thread", myPrintTest)
        executor.map(produttoreTest, range(1, 11), [myPrintTest] * 10)

    tn = time()
    myPrint("main: fine del main", myPrintTest)
    myPrint(f"Tempo di esecuzione: {tn - t0}", myPrintTest)


if __name__ == "__main__":
    main()
