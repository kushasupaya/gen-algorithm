import random
import csv
import json
from itertools import combinations

# Initialize an empty dictionary
solution_dict = {}
length_of_input_array = 27
num_ones =6
# Path to your CSV file
csv_file_path = 'LB_RAAM_outputs.csv'

# Open the CSV file
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Assuming 'solution' is the column name for keys
        # and 'value' is the column name for values
        solution = row['solutions']
        value = row['value']
        
        # Add the key-value pair to the dictionary
        solution_dict[solution] = value

# Print the dictionary
# print(solution_dict)
population=[]
popsize = 5 #define size to which population is always trimmed
generations = 4
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
        [100,0,6,8,109,78,1,1,104],
        [3,6,0,0,0,17,100,1,31],
        [0,8,0,0,100,1,247,178,1],
        [6,109,0,100,0,1,10,1,79],
        [35,78,17,1,1,0,0,1,0],
        [190,1,100,247,10,0,0,0,0],
        [14,1,1,178,1,1,0,0,12],
        [12,104,31,1,79,0,0,12,0]]
#--------------------------------------------------------------------------------------

# def generate_combinations(length, ones_count):
#     indices = [i for i in range(length)]
#     for ones_indices in combinations(indices, ones_count):
#         combination = [1 if i in ones_indices else 0 for i in range(length)]
#         population.append(combination)
    
#     print("pop:",population)

#         # yield combination


def fitness_new(solution):
    return solution_dict[str(solution)]


def initialize():
    keys = random.sample(list(solution_dict), popsize)
    values = [solution_dict[k] for k in keys]
    population.append(dict(zip(keys, values)))
#Creates the initial population, a list of lists containing numbers 1-6 in random order
    # print("pop:",population)
#--------------------------------------------------------------------------------------
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
    sample_dicts= population[0]
    for j in range (2):
        print("sample:",sample_dicts);
#Takes a sample of k competitors and creates a dictionary of competitors and their corresponding fitnesses
        competitors = random.sample(list(sample_dicts.keys()),k)
        # print("tttt:",competitors)

        fitnesses = [sample_dicts[key] for key in competitors]
        # print("value:",fitnesses)
        
        
        # fitnesses = competitors.values()
#Sorts the dictionary based on fitness values
        sortedfitnesses = sorted(fitnesses)
        # print("fot:",sortedfitnesses)
#Stores the most fit competitor as a string called "best"
        best =sortedfitnesses[0]
        #Converts the string "best" into a list called "bestlist"
        bestlist=[]
        for key, value in sample_dicts.items():
            # Check if the value matches the given value
            if value == best:
                # If found, add the corresponding key to the list
                crossovercouple.append(json.loads(key))
        
        # crossovercouple.append(bestlist)
    # print("cc:",crossovercouple);
    return crossovercouple
#--------------------------------------------------------------------------------------
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

def crossover_new():
    # print("init:",population)
    p1,p2 = tournament(3)
    # print("test",p1,p2);
    set_a = []
    set_b = []
    all_common=[]
    c1=[0]*length_of_input_array
    c2=[0]*length_of_input_array
    set_a = [i for i in range(len(p1)) if p1[i] == 1 and p2[i] == 1] # values where both parent has 1
    all_common = [i for i in range(len(p1)) if p1[i] == 1 or p2[i] == 1]
    set_b =[x for x in all_common if x not in set_a] # values where either parent has 1 minus the both case
    for i in set_a:
        c1[i]=1
        c2[i]=1
    #for child 1
    count_ones = len(set_a)
    while count_ones < num_ones:
        selected_index = random.choice(set_b)
        if c1[selected_index] == 0: #to make sure selected position is not already filled since it is random
            c1[selected_index] =1
            count_ones+=1
    #for child 2
    count_ones = len(set_a) #resetting the count
    while count_ones < num_ones:
        selected_index = random.choice(set_b)
        if c2[selected_index] == 0: #to make sure selected position is not already filled since it is random
            c2[selected_index] =1
            count_ones+=1

    fitval_c1=fitness_new(c1);
    fitval_c2=fitness_new(c2);
    population[0].update({str(c1):fitval_c1})
    population[0].update({str(c2):fitval_c2})
    print("final",population)


#Executes a two-point crossover from two parents who are winners of tournament
#Creates two new "children" lists, offs1 and offs2, and adds them to the population whole
#ID parents: winners of tournament
def trimpop():
#Removes least fit members of population to keep population size constant
    mostfit = []
    popfitness = population[0]
    sortedpopfitness = sorted(popfitness.values())
    for i in range(popsize):
        best =sortedpopfitness[0]
         #returns a string corresponding to the competitor with best fitness
        bestlist=[]
        for i in range(1,len(best),3):
            bestlist.append(int(best[i]))#converts the string "best" into a list
        mostfit.append(bestlist)
    del population[0][:]
    for i in range(len(mostfit)):
        population[0].append(mostfit[i])
    #print("trimmed pop is: ", population)
#--------------------------------------------------------------------------------------
def absolutebest(pop):
#Returns individual with best fitness from input population
    fitnesses = fit_eval(pop)
    sortedfitnesses = sorted(fitnesses.values()) #sorts the dictionary based on fitness values
    best =(list(fitnesses.keys())[list(fitnesses.values()).index(sortedfitnesses[0])]) #returns a string corresponding to the competitor with best fitness
    return [best, sortedfitnesses[0]]


def GA():
    length = 27
    ones_count = 6
    initialize()
    for j in range(generations):
        for i in range(popsize):
            crossover_new()
        trimpop()
        genfitness = fit_eval(population)
        # print("generation ", j+1, "fitnesses:")
        # print("Individual\t\tFitness")
        # for k in genfitness:
        #    print("{}\t{}".format(k,genfitness[k]))
        # print("--------------------------")
    result = absolutebest(population)
    print('iteration:', j,"best", next(iter(population.values())))
    most_fit = (result[0],result[1])
    # print("MOST FIT INDIVIDUAL: ", result[0],result[1])
    # print( most_fit)
GA()