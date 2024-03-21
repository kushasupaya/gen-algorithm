import random

import csv

# Initialize an empty dictionary
solution_dict = {}

# Path to your CSV file
csv_file_path = 'your_file.csv'

# Open the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Assuming 'solution' is the column name for keys
        # and 'value' is the column name for values
        solution = row['solution']
        value = row['value']
        
        # Add the key-value pair to the dictionary
        solution_dict[solution] = value

# Print the dictionary
print(solution_dict)

population=[]
popsize = 20 #define size to which population is always trimmed
generations = 10
trials = 10
k = 3 #define tournament size
pm = 0.4 #probability of mutation

#material handeling cost from ex1 is distance

distance = [[0,1,2,3,3,4,2,6,7],
            [1,0,12,4,7,5,8,6,5],
            [2,12,0,5,9,1,1,1,1],
            [3,4,5,0,1,1,1,4,6],
            [3,7,9,1,0,1,1,1,1],
            [4,5,1,1,1,0,1,4,6],
            [2,8,1,1,1,1,0,7,1],
            [6,6,1,4,1,4,7,0,1],
            [7,5,1,6,1,6,1,1,0]]

flow = [[0,100,3,0,6,35,190,14,12],
        [3,6,0,0,0,17,100,1,31],
        [0,8,0,0,100,1,247,178,1],
        [6,109,0,100,0,1,10,1,79],
        [35,78,17,1,1,0,0,1,0],
        [190,1,100,247,10,0,0,0,0],
        [14,1,1,178,1,1,0,0,12],
        [12,104,31,1,79,0,0,12,0]]


# NOTE: See (C:\Users\SIS Lab Admin\Desktop\Fall 2019\Legacy Files\Spring 2017\ISE 592) for working 3x3 examply

#--------------------------------------------------------------------------------------

# NOTE: replace with random permutations with appropriapte number of "1" and "0" values
        # initial size of population will be a lot larger  then trimmed down to length of "popsize" with the most fit solutions

# generate combinations
def initialize():
#Creates the initial population, a list of lists containing numbers 1-6 in random order
    for j in range (popsize):
        #changed range from 1,7,6 to 1,10,9
        population.append(random.sample(range(1,10),9))
    print("pop:",population)

#--------------------------------------------------------------------------------------

# NOTE: This will come from the csv file containing all possible solutions
# population variable will be dictionary  containing key, value pairs instead of just a list of solutions (keys)

def fitness(solution):
#Computes and returns fitness of input individual
    sorteddistance = [[],[],[],[],[],[],[],[],[]]

#Sort the distance matrix based on the order of solution
    #changed range from 6 to 9
    for i in range(9):
        row = solution[i]-1
        for j in range(9):
            col = solution[j]-1
            sorteddistance[i].append(distance[row][col])

#Compute sumproduct of sorted distance matrix and flow matrix
    products = []
    #changed range from 6 to 9
    for i in range(9):
        for j in range(9):
            products.append(sorteddistance[i][j]*flow[i][j])
    sump = sum(products)
    return(sump)

#--------------------------------------------------------------------------------------

# NOTE: can be replace with call to dictionary for population dict that contains key, value pairs
        # child solutions will be appended to the population dict using the csv containing all solutions

def fit_eval(array):
#Evaluates the fitness of every member of a population and stores it in a dictionary called fit_dict
    fit_dict = {}
    for n in range(len(array)):
        key_name = str(array[n])
        fit_dict[key_name]=fitness(array[n])
    return fit_dict

#--------------------------------------------------------------------------------------

def tournament(k):
#Pairs couples for crossover based on most fit member in random samples
#k being the size of the sample - typically 3, can be changed for more/less diversity

    crossovercouple = []

    for j in range(2):
#Takes a sample of k competitors and creates a dictionary of competitors and their corresponding fitnesses
        competitors = random.sample(population,k)
        fitnesses = fit_eval(competitors)
#Sorts the dictionary based on fitness values
        sortedfitnesses = sorted(fitnesses.values())
#Stores the most fit competitor as a string called "best"
        best =(list(fitnesses.keys())[list(fitnesses.values()).index(sortedfitnesses[0])])
#Converts the string "best" into a list called "bestlist"
        bestlist=[]
        for i in range(1,len(best),3):
            bestlist.append(int(best[i]))

#Adds the two tournament winners into list called "crossovercouple"
        crossovercouple.append(bestlist)
    return crossovercouple

#--------------------------------------------------------------------------------------

# NOTE: this should be almost directly usable if the numbers in the "random.ranint" function are replaced with (1 minus len) of the solution string
        # I also had one or two other mutation function ideas in mind that should be relatively sime to

def mutate(individual):
#Executes a mutation on the input individual
#Identifies a section of the individual to remain the same,
#scrambles everything before and after that section.
#Mutated individual is stored in a new list called result

    before=[]
    after=[]
    result=[]

#Choose location points to define unchanged section
    #change from (1,5) to (1,8)
    L1 = random.randint(1,8);
    L2 = random.randint(1,8);
#Ensure the locations are different
#change from (1,5) to (1,8)
    while ( L1 == L2 ):
        L1 = random.randint(1,8);
        L2 = random.randint(1,8);
#Ensure the locations are ascending
    if (L1 > L2):
        tmp = L2
        L2 = L1
        L1 = tmp;
#Shuffle the material before and after the unchanged section
    before = individual[0:L1]
    after = individual[L2:]
    random.shuffle(before)
    random.shuffle(after)

#Populate the result list with shuffled material, unchanged section, shuffled material
    for i in range(len(before)):
        result.append(before[i])
    for i in range(L1, L2):
        result.append(individual[i])
    for i in range(len(after)):
        result.append(after[i])

    return result

#--------------------------------------------------------------------------------------

# NOTE: This can be directly replaced with the cell-based mutation function that has already been written
        # only change would that is needed would be to compute the fitness value for the children solutions
        # before they are appended to the dictionary.

def crossover():
#Executes a two-point crossover from two parents who are winners of tournament
#Creates two new "children" lists, offs1 and offs2, and adds them to the population whole

#ID parents: winners of tournament
    couple = tournament(3)
    ind1 = couple[0]
    ind2 = couple[1]

#Randomly determine two points for crossover
    size = min(len(ind1), len(ind2))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
#Ensure crossover points are in ascending order
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

#Populate each offspring with section from parents between the two crossover points
    offs2=ind1[cxpoint1:cxpoint2]
    offs1=ind2[cxpoint1:cxpoint2]
#Copy parental material before crossover section to children in order, skipping duplicates
    for i in range(cxpoint1):
        if not ind1[i] in offs1:
            offs1.insert(i, ind1[i])
        else:
            dupe1 = i
        if not ind2[i] in offs2:
            offs2.insert(i, ind2[i])
        else:
            dupe2 = i
#Copy parental material after crossover section to children in order, skipping duplicates
    for i in range(cxpoint2,size):
        if not ind1[i] in offs1:
            offs1.insert(i, ind1[i])
        else: dupe1 = i
        if not ind2[i] in offs2:
            offs2.insert(i, ind2[i])
        else: dupe2 = i

#Ensure each child contains every number from 1-6, add missing number(s) in location of skipped duplicates
    #changed from 6 to 9. and range(1,7) to (1,10)
    if len(offs1) < 9:
        for j in range (1,10):
            if not j in offs1:
                offs1.insert(dupe1, j)
    if len(offs2) < 9:
        for j in range (1,10):
            if not j in offs2:
                offs2.insert(dupe2, j)

#Determine whether the offspring will be mutated by comparing random numbers to mutation probability
    mutation1 = random.random()
    mutation2 = random.random()
#Offspring are mutated in place if random number >= mutation probability
    if mutation1 >= pm:
        offs1 = mutate(offs1)
    if mutation2 >= pm:
        offs2 = mutate(offs2)

#Add the two offspring to the population whole
    population.append(offs1)
    population.append(offs2)

#--------------------------------------------------------------------------------------

# NOTE: not exactly sure why all of this is necesary
    # I think we should be able to replace replace this with something that sorts the values (fitness scores) of "population" dict
    # and simply trims it down based on the "popsize" value

def trimpop():
#Removes least fit members of population to keep population size constant

    mostfit = []
    popfitness = fit_eval(population)
    sortedpopfitness = sorted(popfitness.values())
    for i in range(popsize):
        best =(list(popfitness.keys())[list(popfitness.values()).index(sortedpopfitness[i])]) #returns a string corresponding to the competitor with best fitness
        bestlist=[]
        for i in range(1,len(best),3):
            bestlist.append(int(best[i]))#converts the string "best" into a list
        mostfit.append(bestlist)
    del population[:]
    for i in range(len(mostfit)):
        population.append(mostfit[i])
    #print("trimmed pop is: ", population)

#--------------------------------------------------------------------------------------

# NOTE:  I think we should be able to replace replace this with something that sorts the values (fitness scores) of "population"
    # and returns the first/best value

def absolutebest(pop):
#Returns individual with best fitness from input population
    fitnesses = fit_eval(pop)
    sortedfitnesses = sorted(fitnesses.values()) #sorts the dictionary based on fitness values
    best =(list(fitnesses.keys())[list(fitnesses.values()).index(sortedfitnesses[0])]) #returns a string corresponding to the competitor with best fitness
    return [best, sortedfitnesses[0]]

#--------------------------------------------------------------------------------------

# NOTE: Will need to implement something that tracks the "absolutebest" value for each iteration
        # we will want to track the this value using a sliding window over multiple iterations
        # to establish a stopping condidtion for terminating the algorithm where the "rate of improvement"
        # is not longer suffienct to justify searching the solution space any further.
        #
        # this information will be plotted over time in the results section.

#--------------------------------------------------------------------------------------

def GA():

    initialize()
    for j in range(generations):
        for i in range(popsize):
            crossover()
        trimpop()
        genfitness = fit_eval(population)
        #print("generation ", j+1, "fitnesses:")
        #print("Individual\t\tFitness")
        #for k in genfitness:
        #    print("{}\t{}".format(k,genfitness[k]))
        #print("--------------------------")

    result = absolutebest(population)
    most_fit = (result[0],result[1])

    #print("MOST FIT INDIVIDUAL: ", result[0],result[1])

    print( most_fit)


GA()
