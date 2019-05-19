import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

obstacle_universe = np.arange(0, 401, 1)
wall_universe = np.arange(0, 501, 1)
speed_universe = np.arange(0, 11, 1)

shift_universe  = np.arange(0, 11, 1)


# Antecedents and Consequents
obstacle = ctrl.Antecedent(obstacle_universe, 'obstacle')
wall = ctrl.Antecedent(wall_universe, 'wall')
speed = ctrl.Antecedent(speed_universe, 'speed')

shift = ctrl.Consequent(shift_universe, 'shift')


# Membership functions
obstacle['close'] = fuzz.trimf(obstacle_universe, [0, 0, 200] )
obstacle['medium'] = fuzz.trimf(obstacle_universe, [150, 200, 250] )
obstacle['far'] = fuzz.trimf(obstacle_universe, [200, 250, 400] )

wall['close'] = fuzz.trimf(wall_universe,  [0, 0, 250])
wall['medium'] = fuzz.trimf(wall_universe,  [200, 300, 400] )
wall['far'] = fuzz.trimf(wall_universe,  [350, 500, 500] )

speed['slow'] = fuzz.trimf(speed_universe , [0, 0, 2])
speed['medium'] = fuzz.trimf(speed_universe , [1, 4, 7])
speed['fast'] = fuzz.trimf(speed_universe , [5, 8, 9])
speed['very_fast'] = fuzz.trimf(speed_universe , [ 7, 10, 10])



# Output
shift['none'] = fuzz.trimf(shift_universe, [0, 0, 3])
shift['small'] = fuzz.trimf(shift_universe, [2, 4, 6])
shift['medium'] = fuzz.trimf(shift_universe, [5, 7, 9])
shift['big'] = fuzz.trimf(shift_universe, [8, 10, 10])




rules = [


    ctrl.Rule(antecedent=
              (obstacle['far'] & wall['close'] & speed['slow']) |
              (obstacle['far'] & wall['close'] & speed['medium']) |
              (obstacle['far'] & wall['close'] & speed['fast']) |
              (obstacle['far'] & wall['close'] & speed['very_fast']) |

              (obstacle['far'] & wall['medium'] & speed['slow']) |
              (obstacle['far'] & wall['medium'] & speed['medium']) |
              (obstacle['far'] & wall['medium'] & speed['fast']) |
              (obstacle['far'] & wall['medium'] & speed['very_fast']) |

              (obstacle['far'] & wall['far'] & speed['slow']) |
              (obstacle['far'] & wall['far'] & speed['medium']) |
              (obstacle['far'] & wall['far'] & speed['fast']) |
              (obstacle['far'] & wall['far'] & speed['very_fast'])

              ,

              consequent=shift['none']
              ),


    ctrl.Rule(antecedent=
              (obstacle['medium'] & wall['medium'] & speed['slow']) |
              (obstacle['medium'] & wall['medium'] & speed['medium']) |
              (obstacle['medium'] & wall['medium'] & speed['fast']) |
              (obstacle['medium'] & wall['medium'] & speed['very_fast']) |

              (obstacle['medium'] & wall['far'] & speed['slow']) |
              (obstacle['medium'] & wall['far'] & speed['medium']) |
              (obstacle['medium'] & wall['far'] & speed['fast']) |
              (obstacle['medium'] & wall['far'] & speed['very_fast'])

            ,

            consequent=shift['small']
            ),


    ctrl.Rule(antecedent=

              (obstacle['medium'] & wall['close'] & speed['slow']) |
              (obstacle['medium'] & wall['close'] & speed['medium']) |
              (obstacle['medium'] & wall['close'] & speed['fast']) |
              (obstacle['medium'] & wall['close'] & speed['very_fast'])
              ,

              consequent=shift['medium']
              ),


    ctrl.Rule(antecedent=
             (obstacle['close'] & wall['close'] & speed['slow']) |
             (obstacle['close'] & wall['close'] & speed['medium']) |
             (obstacle['close'] & wall['close'] & speed['fast']) |
             (obstacle['close'] & wall['close'] & speed['very_fast']) |

             (obstacle['close'] & wall['medium'] & speed['slow']) |
             (obstacle['close'] & wall['medium'] & speed['medium']) |
             (obstacle['close'] & wall['medium'] & speed['fast']) |
             (obstacle['close'] & wall['medium'] & speed['very_fast']) |

             (obstacle['close'] & wall['far'] & speed['slow']) |
             (obstacle['close'] & wall['far'] & speed['medium']) |
             (obstacle['close'] & wall['far'] & speed['fast']) |
             (obstacle['close'] & wall['far'] & speed['very_fast'])
                 ,

            consequent=shift['big']
            ),

]


system = ctrl.ControlSystem(rules=rules)
simulation = ctrl.ControlSystemSimulation(system)


def compute(obstacle_param, wall_param, speed_param):
    inputs = {
        'obstacle': obstacle_param,
        'wall': wall_param,
        'speed': speed_param
    }

    simulation.inputs(inputs)
    simulation.compute()
    return simulation.output['shift']



if __name__ == '__main__':
    obstacle.view()
    wall.view()
    speed.view()
    shift.view()
    plt.show()
