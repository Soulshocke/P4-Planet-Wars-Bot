
""" 
Name:       Zechariah Neak                        Partner:    Jesus Hernandez
Email:      zneak@ucsc.edu                        Email:      
ID:         1367249
Course:     CMPM146 Game AI
Professor:  Daniel G Shapiro

                                \\\\\\\ Program 4 ///////

Description:
    The functions below are checks and conditionals used as leaf nodes in bt_bot's
    behavior tree.
"""

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# returns true if total ships > enemy ships
def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

# returns any allied planet currently targeted by hostile barbarians
def if_under_attack(state):
    fortresses = [planet for planet in state.my_planets()
                      if any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    return any(fortresses)