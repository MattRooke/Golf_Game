import random

# par and hole distance can be easily edited to change the game parameters.
PAR = 5
HOLE_DISTANCE = 230

# percent and hit power constants are used by both calculate_swing and calculate_putt functions.
PERCENT = 100
HIT_POWER_MIN = 80
HIT_POWER_MAX = 120


# main function:
# loops the game until the user quits.
# inputs; players name, game scores, player pars, number of swings and play again.
def main():
    game_scores = []
    player_pars = []
    number_of_swings = 0
    play_again = "y"
    player_name = input("What is your name?\n>")
    print("Welcome to the golf course", player_name + ".\n")
    while play_again != "n":
        play_again = game_menu("Main Menu:", "| Golf!              |\n"
                                             "|  Instructions  (I) |\n"
                                             "|  Play a Hole   (P) |\n"
                                             "|  Quit Game     (Q) |")

        if play_again != "n":
            number_of_swings = club_selection_menu("Welcome to the tee off, this hole is 230m par 5. "
                                                   "Please select your club:",
                                                   "| Swing!             |\n"
                                                   "|  Driver ~ 100m (D) |\n"
                                                   "|  Iron   ~ 30m  (I) |\n"
                                                   "|  Putter ~ 10m  (P) |")

        if number_of_swings > 0 and play_again != "n":
            calculate_score(player_pars, game_scores, number_of_swings)
            play_again = input("Play again? (y/n)").lower()

    # Prints the list of past scores with par results when the player quits:
    if number_of_swings > 0:
        print("\nYour score for...")
        for index, round_score in enumerate(game_scores):
            print("Round", str(index + 1) + ":", round_score, "shots.", player_pars[index])

    print("\nFarewell and thanks for playing " + player_name + "!")


# Main menu:
# returns the players choice to continue.
# inputs; player menu selection.
def game_menu(prompt, ui):
    user_input = ""
    while user_input != "q":
        print(prompt)
        print(ui)
        user_input = input(">").lower()
        if user_input == "i":
            print("This is a simple golf game in which each hole is 230m game away with par 5.\n"
                  "You are able to choose from 3 clubs, the Driver, Iron or Putter.\n"
                  "The Driver will hit around 100m, the Iron around 30m and the Putter around 10m.\n"
                  "The putter is best used very close to the hole.\n")
        elif user_input == "p":
            play_again = "y"
            return play_again
        elif user_input != "q":
            print("Invalid menu choice entered...")
    play_again = "n"
    return play_again


# Menu for player's club choice:
# returns the number of swings the player took to get the ball in the hole, for their score calculation.
# inputs; player club selection & distance to the hole.
def club_selection_menu(prompt, ui):
    number_of_swings = 0
    distance_to_hole = HOLE_DISTANCE
    driver_average = 100
    iron_average = 30
    putting_threshold = 10
    putter_average = 10
    print(prompt)
    while distance_to_hole != 0:
        print(ui)
        user_input = input(">").lower()
        number_of_swings += 1
        # Select Driver:
        if user_input == "d":
            distance_to_hole = calculate_swing(driver_average, number_of_swings, distance_to_hole)
        # Select Iron:
        elif user_input == "i":
            distance_to_hole = calculate_swing(iron_average, number_of_swings, distance_to_hole)
        # Select Putter:
        elif user_input == "p":
            # When more than 10m from the hole:
            if distance_to_hole > putting_threshold:
                distance_to_hole = calculate_swing(putter_average, number_of_swings, distance_to_hole)
            # When less than 10m from the hole:
            else:
                distance_to_hole = calculate_putt(number_of_swings, distance_to_hole)
        else:
            print("Invalid club selection... AIR SWING! :(\n Your shot went 0m \n You are " +
                  str(distance_to_hole) + "m from the hole, after "
                  + str(number_of_swings) + " Swing/s.")
    return number_of_swings


# Calculation for normal shot distance:
# returns the remaining distance to the hole.
# inputs; club average, swings & distance to the hole.
def calculate_swing(average_distance, number_of_swings, distance_to_hole):
    hit_power = random.randint(HIT_POWER_MIN, HIT_POWER_MAX)
    shot_distance = int(average_distance * (hit_power / PERCENT))
    distance_to_hole -= shot_distance
    distance_to_hole = abs(distance_to_hole)
    print("Your shot went " + str(shot_distance) + "m\nYou are " + str(distance_to_hole) + "m from the hole, after " +
          str(number_of_swings) + " Swing/s.")
    return distance_to_hole


# Calculation for putting when within 10m of the hole:
# returns the remaining distance to the hole.
# inputs; swings & distance to the hole.
def calculate_putt(number_of_swings, distance_to_hole):
    hit_power = random.randint(HIT_POWER_MIN, HIT_POWER_MAX)
    putter_min_shot = 1
    if distance_to_hole == putter_min_shot:
        shot_distance = putter_min_shot
    else:
        shot_distance = int(distance_to_hole * (hit_power / PERCENT))
        while shot_distance < putter_min_shot:
            shot_distance = int(distance_to_hole * (hit_power / PERCENT))
    distance_to_hole -= shot_distance
    distance_to_hole = abs(distance_to_hole)
    print("Your shot went " + str(shot_distance) + "m\nYou are " + str(distance_to_hole) + "m from the hole, after "
          + str(number_of_swings) + " Swing/s.")
    return distance_to_hole


# Finds the players par and prints their par result after each game:
# inputs; par, game scores, players previous pars & number of swings taken by the player
def calculate_score(player_pars, game_scores, number_of_swings):
    par = PAR
    if number_of_swings < par:
        player_par = par - number_of_swings
        par_result = str(player_par) + " under par."
        print("Clunk… After", number_of_swings, "hits your ball is in the hole! Congratulations. You are", player_par,
              "under par for this hole.")
    elif number_of_swings == par:
        par_result = "On par."
        print("Clunk… After", number_of_swings, "hits your ball is in the hole! Not Bad. You are on par for this hole")
    else:
        player_par = number_of_swings - par
        par_result = str(player_par) + " over par."
        print("Clunk… After", number_of_swings, "hits your ball is in the hole! Oh dear... You are", player_par,
              "over par for this hole.")
    # keeps track of the players par result for each round:
    player_pars.append(par_result)
    # keeps track of the players score for each round:
    game_scores.append(number_of_swings)
    if len(game_scores) > 1:
        total_par = par*len(game_scores)
        if sum(game_scores) < total_par:
            difference = total_par - sum(game_scores)
            total_player_par = str(difference) + " under"
        elif total_par == sum(game_scores):
            total_player_par = "on"
        else:
            difference = sum(game_scores) - total_par
            total_player_par = str(difference) + " over"
        print("Your total score is " + str(sum(game_scores)) + " and you are " + total_player_par + " par after " +
              str(len(game_scores)) + " holes.")


main()
