import logging, traceback, sys, os, inspect
sys.path.insert(0, '../')
from planet_wars import issue_order
from random import choice


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def colonize_five_neutral_planets(state):
    # (1) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (2) Find five random neutral planets.
    wishlist = []
    for i in range(5):
        random_planet = choice(state.neutral_planets())
        wishlist.append(random_planet)
        #logging.info(wishlist)
        #logging.info(" ")

    # (3) Send 5 equally-sized detachments from 3/4 of my strongest planet's garrison on a colonization mission.
    fleet_size = 3 * (strongest_planet.num_ships / 4)
    detachment = fleet_size / 5
    for target in wishlist:
        issue_order(state, strongest_planet.ID, target.ID, detachment)
    return True
    
def colonize_closest_planets(state):
    # sorted by number of ships
    shipyards = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        shipyard = next(shipyards)
        target = next(target)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return