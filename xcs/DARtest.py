import logging
import xcs

from xcs.bitstrings import BitCondition, BitString
from xcs.scenarios import PreClassifiedData, UnclassifiedData

# Setup logging so we can see the test run as it progresses.
logging.root.setLevel(logging.INFO)

# Create the scenario instance

situations = [BitCondition('1000####################'),
              BitCondition('0100####################'),
              BitCondition('0010####################'),
              BitCondition('0001####################'),
              BitCondition('100010##################')]

classifications = [BitString('100001011010101010001010'),
          BitString('010001011010101010001010'),
          BitString('001010011010101010001010'),
          BitString('000101011010101010001010'),
          BitString('100001011010101010001010')]

assert len(situations) == len(classifications)
problem  = PreClassifiedData(situations, classifications)

algorithm = xcs.XCSAlgorithm()

# Default parameter settings in test()
algorithm.exploration_probability = .1

# Modified parameter settings
algorithm.ga_threshold = 1
algorithm.crossover_probability = .5
algorithm.do_action_set_subsumption = True
algorithm.do_ga_subsumption = False
algorithm.wildcard_probability = .998
algorithm.deletion_threshold = 1
algorithm.mutation_probability = .002

model = algorithm.new_model(problem)

model.run(problem, learn=True)

print(model)

print(len(model))

for rule in model:
    if rule.fitness > .5 and rule.experience >= 10:
        print(rule.condition, '=>', rule.action, ' [%.5f]' % rule.fitness)

X = [BitCondition('100010##################')]
scenario = UnclassifiedData(X)
model.run(scenario, learn=False)
y = scenario.get_classifications()
print('when designer enters SPEC as IBM-32bit', X)
print('then LR recommends', y)

X = [BitCondition('010001##################')]
scenario = UnclassifiedData(X)
model.run(scenario, learn=False)
y = scenario.get_classifications()
print('When designer enters SPEC as HP-64bit', X)
print('then LR recommends', y)

X = [BitCondition('001001##################')]
scenario = UnclassifiedData(X)
model.run(scenario, learn=False)
y = scenario.get_classifications()
print('When designer enters SPEC as PowerPC64bit', X)
print('then LR recommends', y)