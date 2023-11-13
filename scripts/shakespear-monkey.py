from numpy.random import choice as np_choice
from random import choices, sample, choice
from typing import List
from math import ceil


MUTATION_RATE = 0.2
CHARS = 'abcdefghijklmnopqrstuvwxyz ,?'


class Monkey:

    mutation_rate = MUTATION_RATE
    chars = CHARS

    def __init__(
            self, 
            how_many_chars: int,
        ):
        self.chars_count = how_many_chars

        self.generated_sentence = ''
        self.fitness = 0

    @property
    def sentence(self) -> str:
        return self.generated_sentence

    @sentence.setter
    def sentence(self, new_sentence: str):
        if len(new_sentence) != self.chars_count:
            raise ValueError(
                'The length of the sentence must be the same as the length of the mon' \
                'key'
            )
        self.generated_sentence = new_sentence
    
    def generate(self, parent: 'Monkey' = None) -> str:
        self.generated_sentence = ''.join(choices(self.chars, k=self.chars_count))
        return self.generated_sentence

    def fitness_function(self, objective_sentence: str) -> int:
        self.fitness = 0
        for i in range(self.chars_count):
            if self.generated_sentence[i] == objective_sentence[i]:
                self.fitness += 1
        return self.fitness

    def crossover(self, other_monkey: 'Monkey') -> 'Monkey':
        child = Monkey(self.chars_count)
        sent = ""
        for i in range(self.chars_count):
            if choice([True, False]):
                sent += self.generated_sentence[i]
            else:
                sent += other_monkey.generated_sentence[i]
        child.sentence = sent
        return child

    def mutate(self) -> None:
        if not np_choice([True, False], p=[self.mutation_rate, 1 - self.mutation_rate]):
            return
        must_choose = int(self.mutation_rate * self.chars_count)
        chosen_indexes = sample(range(self.chars_count), must_choose)
        for ind in chosen_indexes:
            self.generated_sentence = self.generated_sentence[:ind] + \
                choice(self.chars) + self.generated_sentence[ind+1:]



class Population:
    
    def __init__(
            self, 
            population_size: int, 
            objective_sentence: str,
            generations: int,
            selection_number: int
        ):
        self.population_size = population_size
        self.objective_sentence = objective_sentence
        self.generations = generations
        if selection_number < ceil(2 * population_size / 3):
            raise ValueError(
                'The selection number must be less than 2/3 of the population size'
            )
        self.selection_number = selection_number
        self.population = []

    def generate_initial_population(self) -> None:
        for i in range(self.population_size):
            monkey = Monkey(len(self.objective_sentence))
            monkey.generate()
            self.population.append(monkey)
    
    def calculate_fitness(self) -> None:
        for monkey in self.population:
            monkey.fitness_function(self.objective_sentence)

    def selection(self) -> None:
        self.population = sorted(
            self.population, 
            key=lambda x: x.fitness, reverse=True
        )[:self.selection_number]

    def generate_children(self) -> None:
        childrens = []
        for i in range(self.population_size - len(self.population)):
            parent_1, parent_2 = sample(self.population, 2)
            child = parent_1.crossover(parent_2)
            child.mutate()
            childrens.append(child)
        self.population.extend(childrens)

    def run(self) -> str:
        self.generate_initial_population()
        for i in range(self.generations):
            self.calculate_fitness()
            self.selection()
            self.generate_children()
            print(f'Generation {i+1}: {self.population[0].generated_sentence}')
            if self.population[0].generated_sentence == self.objective_sentence:
                return self.population[0].generated_sentence
    

if __name__ == '__main__':

    objective_sentence = 'to be or not to be, that is the question'
    population = Population(2000, objective_sentence, 10000, 1400)
    result = population.run()
