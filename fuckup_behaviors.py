# *** Attack neutral planets. ***
def take_defenseless_territory(state):
    # (1) Sort our planets from weakest to strongest.
    fortresses = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    # (2) Identify all untouched neutral planets.
    wishlist = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())] 

    # (3) Calculate average strength among all neutral planets.
    def strength(fortress):
        return fortress.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == fortress.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == fortress.ID)

    # -- determine which neutral planets are weaker or stronger than the average
    avg_power = sum(strength(planet) for planet in wishlist) / len(wishlist)
    weakpoints = [planet for planet in wishlist if strength(planet) < avg_power]
    strongpoints = [planet for planet in wishlist if strength(planet) > avg_power]

    # (3) Given enough ships for a target, send an invasion force to capture it.
    try:
        our_fortress = next(fortresses)
        while(True):
            # -- creates sorted list of distances from one allied planet to all weak neutral planets --
            dist = []
            for planet in wishlist:
                if planet is in weakpoints:
                    dist.append(state.distance(our_fortress, planet), planet)
            dist.sort()
            dist = iter(dist)

            # -- find weak planets shorter than the average distance of all neutral planets --
            avg_dist = (max(dist) - min(dist)) / 2

            for target_dist, target_planet in dist:
                # -- send in required ships to neutral planets that are both weak and close --
                legion_size = target_planet.num_ships + 1
                if neutral_dist < avg_dist and our_fortress.num_ships > legion_size:
                    issue_order(state, our_fortress.ID, target_planet.ID, legion_size)

                    # -- stop checking as soon as current allied planet finds a viable target --
                    our_fortress = next(fortresses)
                    break   

    except StopIteration:
        return