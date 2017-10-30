def expand_with_strength(state):
    # (1) Sort our planets from strongest to weakest.
    fortresses = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    # (2) Identify planets we are not currently attacking.
    wishlist = [planet for planet in state.not_my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    # (3) Sort new targets from strongest to weakest.                 
    wishlist = iter(sorted(wishlist, key=lambda p: p.num_ships, reverse=True))

    # (4) Given enough ships for a target, send an invasion force to capture it.
    try:
        our_fortress = next(fortresses)
        our_target = next(wishlist)
        while True:
            #-- if neutral, send more than enough for a sustainable colony --
            if our_target.owner == 0:    
                legion_size = our_target.num_ships + int(our_target.num_ships/10) + 1

            #-- if hostile, send just enough, considering distance to target and its production rate --
            else:   
                legion_size = our_target.num_ships + \
                                 state.distance(our_fortress.ID, our_target.ID) * our_target.growth_rate + 1

            #-- if enough available ships, deploy legion into hyperspace --
            if our_fortress.num_ships > legion_size:
                issue_order(state, our_fortress.ID, our_target.ID, legion_size)
                our_fortress = next(fortresses)
                our_target = next(wishlist)
            #-- otherwise, leave alone until we have built enough strength --
            else:
                our_target = next(wishlist)

    except StopIteration:
        return


def reinforce_with_vengeance(state):
    # (1) Identify territory under our control.
    fortresses = [planet for planet in state.my_planets()]
    if not fortresses:
        return

    # (2) Determine strength of a given allied planet, considering friendlies and hostiles en route.
    def strength(fortress):
        return fortress.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == fortress.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == fortress.ID)

    # (3) Calculate average strength among all planets, and determine the least-defended from the well-defended.
    avg = sum(strength(planet) for planet in fortresses) / len(fortresses)
    weakpoints = [planet for planet in fortresses if strength(planet) < avg]
    strongpoints = [planet for planet in fortresses if strength(planet) > avg]

    if (not weakpoints) or (not strongpoints):
        return

    # (4) Prioritize checking weakest planets, and see which other planet can provide reinforcements.
    weakpoints = iter(sorted(weakpoints, key=strength))
    strongpoints = iter(sorted(strongpoints, key=strength, reverse=True))

    try:
        weak_base = next(weakpoints)
        strong_base = next(strongpoints)
        while True:
            # -- determine amount of ships a base needs, and how much another base can provide --
            reinforcements = int(avg - strength(weak_base))
            spare_forces = int(strength(strong_base) - avg)

            # -- if enough ships available, deploy to weaker base
            if spare_forces >= reinforcements > 0:
                issue_order(state, strong_base.ID, weak_base.ID, reinforcements)
                weak_base = next(weakpoints)

            # -- if not enough available, go all-in, THIS IS AN EMERGENCY
            elif spare_forces > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, spare_forces)
                strong_planet = next(strong_planets)
        
            else:
                strong_planet = next(strong_planets)

    except StopIteration:
        return