# Klasyczny algorytm ewolucyjny

Klasyczny algorytm ewolucyjny operuje na liczbach rzeczywistych. Na początku
populacja jest inicjalizowana oraz oceniana. Następnie dokonywana jest selekcja
osobników do reprodukcji. Na wybranej populacji dokonywane są, z odpowiednimi prawdopodobieństwami, operatory krzyżowania i mutacji. Tak powstały
zbiór jest oceniany i następuje sukcesja, czyli wybór, jakie osobniki przechodzą
do następnej generacji. Kolejne generacje powtarzają te same kroki zaczynając
od selekcji, aż nie zostanie spełniony warunek stopu, którym jest najczęściej
liczba wywołań funkcji oceny.</br>

Rodzaje zaimplementowanej selekcji:</br>
* Ruletkowa
* Progowa
* Turniejowa