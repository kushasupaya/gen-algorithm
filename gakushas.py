import random
import csv
import json
from itertools import combinations
import pandas as pd


population ={}
popsize = 15 #define size to which population is always trimmed
generations = 12
trials = 10
k = 3 #define tournament size
pm = 0.4 #probability of mutation
#material handeling cost from ex1 is distance


# Initialize an empty dictionary
solution_dict = {}
length_of_input_array = 27
num_ones =6
# Path to your CSV file
csv_file_path = 'LB_RAAM_outputs.csv'
df = pd.read_csv('LB_RAAM_outputs.csv')

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


def initialize():
    keys = random.sample(list(solution_dict), popsize)
    values = [solution_dict[k] for k in keys]
    population.update(dict(zip(keys, values)))
    # print(list(solution_dict.items())[:2])

def select_samples(size):
    # Selecting 3 random samples
    samples = list(population.keys())
    selected_samples_matchup = [];
    # print("pop",population)
    for _ in range(2):

        random_samples = random.sample(samples, size)
    
    # Sorting the samples based on their values
        sorted_samples = sorted(random_samples, key=lambda x: float(population[x]))
    
    # Selecting the sample with the lowest values
        selected_samples = sorted_samples[0]
        selected_samples_matchup.append(selected_samples)
    # returning the best sample out of two
    return [(sample, population[sample]) for sample in selected_samples_matchup]



def get_fitness(child):
    corresponding_value = df[df['solutions'] == str(child)]['value'].values
    return corresponding_value[0]


def crossover_new():
    # print("init:",population)
    data = select_samples(3)
    parents = [eval(t[0]) for t in data]
    p1 = parents[0]
    p2 = parents[1]
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



    fitval_c1=get_fitness(child = c1)
    fitval_c2=get_fitness(child = c2)
    population[str(c1)] = str(fitval_c1)
    population[str(c2)] = str(fitval_c2)


def trim_pop2():
    global population;
    sample_new = list(population.keys())
    
    # Sorting the samples based on their values
    sorted_samples_update = sorted(sample_new, key=lambda x: float(population[x]))
    
    # Selecting the 2 samples with the lowest values
    selected_samples_update = sorted_samples_update[:popsize]
    population = {sample: population[sample] for sample in selected_samples_update}

def GA():
    initialize()
    for j in range(generations):
        for i in range(popsize):
            crossover_new()
        trim_pop2()

    # print("sorted",population,"sorted done");
    res_key = list(population.keys())[0]
    res_value = list(population.values())[0]
    print('iteration:', j,"best", next(iter(population.values())))

    print("test",res_key, res_value)
GA();
