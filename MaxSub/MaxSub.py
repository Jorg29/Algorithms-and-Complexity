import random as r
import timeit
import matplotlib.pyplot as plt

def prefix(a_list): # λίστα των προθεματικών αθροισμάτων
    prefix_sums = list()
    for i in range(0, len(a_list)):
        if i == 0:
            prefix_sums.append(a_list[i]) # προσθέτουμε το στοιχείο που βρίσκεται σε αυτή την θέση στον πίνακα
        else:
            prefix_sums.append(a_list[i] + prefix_sums[i - 1]) # προσθέτουμε το προηγούμενο στοιχείο της λίστας των prefix με το στοιχείο που βρίσκεται στην θέση i του αρχικού πίνακα
    return prefix_sums  


def SimpleAlgorithm(a_list):
    largest_sum = a_list[0] # αρχικοποίηση της μεταβλητής που θα αποθηκέυει το μεγαλύτερο άθροισμα
    start = 0 # αποθηκεύει την θέση που ξεκινάει το μέγιστο άθροισμα
    end = 0 # αποθηκεύει την θέση που τελειώνει το μέγιστο άθροισμα
    for i in range(0, len(a_list)): # προσθέτουμε το προηγούμενο στοιχείο της λίστας των prefix με το στοιχείο που βρίσκεται στην θέση i του αρχικού μας πίνακα
        for j in range(i, len(a_list)):
            sum = 0
            for x in range(i, j + 1):
                sum += a_list[x]
            if largest_sum < sum:
                largest_sum = sum
                start = i # Η θέση που ξεκινάει το μέγιστο άθροισμα
                end = j # Η θέση που τελειώνει το μέγιστο άθροισμα
    return largest_sum, start, end  # επιστρέφει λίστα με το μέγιστο άθροισμα κ την θέση που ξεκινάει κ την θέση που τελειώνει

def AdvanceAlgorithm(a_list):
    largest_sum = a_list[0] # αρχικοποίηση της μεταβλητής κ θα αποθηκέυει το μεγαλύτερο άθροισμα
    sum = 0 # αποθηκέυει το εκάστοτε άθροισμα
    start = 0 # αποθηκεύει την θέση που ξεκινάει το μέγιστο άθροισμα
    end = 0 # αποθηκεύει την θέση που τελειώνει το μέγιστο άθροισμα
    for i in range(0, len(a_list)):
        for j in range(i, len(a_list)):
            if i == 0:
                sum = a_list[j]
            else:
                sum = a_list[j] - a_list[i - 1]
            if largest_sum < sum:
                largest_sum = sum
                start = i # η θέση που ξεκινάει το μέγιστο άθροισμα
                end = j # η θέση που τελειώνει το μέγιστο άθροισμα
    return largest_sum, start, end

# Αλγόριθμος του Kadane
def Kadane(a_list):
    largest_sum = a_list[0]
    sum = 0
    start = 0
    end = 0
    pointer = 0
    for i in range(0, len(a_list)):
        sum += a_list[i]
        if largest_sum < sum:
            largest_sum = sum
            start = pointer
            end = i
        if sum < 0:
            sum = 0
            pointer = i + 1
    return largest_sum, start, end


# τυχαίος πίνακα
def ArrayGen(num, valuesum):
    return [r.randint(-valuesum, valuesum) for x in range(num)]


if __name__ == "__main__":
    functions = [SimpleAlgorithm, AdvanceAlgorithm, Kadane] # αρχικοποίηση του πίνακα των συναρτήσεων
    num = [10, 100, 1000]  # αρχικοποίηση του πίνακα των τιμών που καθορίζουν το μέγεθος του τυχαίου πίνακα
    valuesum = 100 # εύρος τιμών
    timed = dict()
    for f in functions:
        print(f"\n{f.__name__}\n")
        for n in num:
            sequence = ArrayGen(n, valuesum) # τυχαίος πίνακα
            prefix_sums = prefix(sequence)
            start_time = timeit.default_timer() # καταγραφή της ώρας
            if f.__name__ == "AdvanceAlgorithm":
                results = f(prefix_sums)
                duration = timeit.default_timer() - start_time
            else:
                results = f(sequence)
                duration = timeit.default_timer() - start_time
            print(f"\nThe  results is for number {n} in the range -{valuesum}, {valuesum}: {duration} seconds\n")
            print(f"Maximum sum Subarray is: {results[0]}")
            print(f"\nStart position: {results[1]}")
            print(f"\nEnd position: {results[2]}")
            timed[(f.__name__, n)] = duration
    # σχεδιάργαμμα       
    SimpleAlgorithm = list()
    AdvanceAlgorithm = list()
    Kadane = list()
    for function_name, n_size in timed:
        if function_name == "SimpleAlgorithm":
            SimpleAlgorithm.append(timed[function_name, n_size])
        elif function_name == "AdvanceAlgorithm":
            AdvanceAlgorithm.append(timed[function_name, n_size])
        elif function_name == "Kadane":
            Kadane.append(timed[function_name, n_size])
    plt.plot(num, SimpleAlgorithm, label="SimpleAlgorithm")
    plt.plot(num, AdvanceAlgorithm, label="AdvanceAlgorithm")
    plt.plot(num, Kadane, label="Kadane")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()

