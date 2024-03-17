import sys
import random
import time
from threading import Timer

random.seed(0)

class TimeProxy:
    def __init__(self, game, time_sec=60):
        self.game = game
        self.time_sec = time_sec
        self.end_time = time.time() + time_sec
        self.timer = None

    def timer_logic(self):
        if self.game.winner == False:
            self.timer = Timer(self.end_time - time.time(), self.time_up)
            self.timer.start()
        elif self.game.winner == True:
            self.timer.cancel()

    def time_up(self):
        print(f"\nTime is up {self.time_sec} sec have passed.")
        self.game.end_game()
        sys.exit("The game is over")

class Player:
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.sp = "Human"

    def roll_dice(self):
        return random.randint(1, 6)

    def hold(self, temp_score):
        self.score += temp_score
        print(f"\n{self.sp} p{self.id} holds, Current score: {self.score}")
        if self.score >= 100:
            print(f"\n{self.sp} p{self.id} wins!")
            game.winner = True
            game.time_proxy.timer_logic()
            sys.exit("The game is over")

class Robot(Player):
    def __init__(self, id):
        super().__init__(id)
        self.sp = "Robot"
        self.temp_score = 0

    def big_brain(self):
        logic = min(25, 100 - self.score)
        temp_score = 0 
        while temp_score < logic:
            dice_roll = self.roll_dice()
            print(f"\n{self.sp} p{self.id} rolled a {dice_roll}")
            temp_score += dice_roll

            if dice_roll == 1:
                print("A 1 was rolled. Temp score reset to 0.")
                return

        self.score += temp_score
        self.hold(self.temp_score)
        return 

class PlayerFactory:
    def human(player_id):
        return Player(player_id)

    def robot(player_id):
        return Robot(player_id)

class PigGame:
    def __init__(self, time_sec, sp1=Player, sp2=Player):
        self.p = [sp1, sp2]
        self.curr_p = 0
        self.temp_score = 0
        self.winner = False
        self.time_proxy = TimeProxy(self, time_sec)

    def switch_player(self):
        self.curr_p = (self.curr_p + 1) % 2
        self.temp_score = 0

    def end_game(self):
        for player in self.p:
            print(f"\n{player.sp} p{player.id} final score: {player.score}")
        self.winner = True
        if self.p[0].score > self.p[1].score:
            print(f"\n{self.p[0].sp} p{self.p[0].id} wins!")
        else:
            print(f"\n{self.p[1].sp} p{self.p[1].id} wins!")
        sys.exit("The game is over")

    def start(self):
        self.time_proxy.timer_logic()
        while not self.winner:
            print(f"\n{self.p[self.curr_p].sp} p{self.p[self.curr_p].id}'s Current Score: {self.p[self.curr_p].score}")
            if self.p[self.curr_p].sp == "Robot":
                print("\nRobot turn")
                self.p[self.curr_p].big_brain()
                print("\nRobot turn over")
                self.switch_player()
            else:
                choice = input("Enter 'r' to roll the dice or 'h' to hold: ")
                if choice == 'r':
                    dice_roll = self.p[self.curr_p].roll_dice()
                    print(f"\n{self.p[self.curr_p].sp} p{self.p[self.curr_p].id} rolled a {dice_roll}")
                    if dice_roll == 1:
                        print("A 1 was rolled. Temp score reset to 0.")
                        self.switch_player()
                    else:
                        self.temp_score += dice_roll
                        print(f"Temp score: +{self.temp_score} Temp total: {self.p[self.curr_p].score + self.temp_score}")

                elif choice == 'h':
                    self.p[self.curr_p].hold(self.temp_score)
                    self.switch_player()
                else:
                    print("\nInvalid choice. Please try again.")

def user_inputs():
    user_change = input("Change default time? (y/n): ")
    time_change = 60
    if user_change == "y":
        time_change = int(input("Enter time in sec: "))
        if time_change not in range(1, 1000):
            raise Exception(f"Time must be greater than 0")

    spchoice = {
        ("H"): PlayerFactory.human,
        ("R"): PlayerFactory.robot
    }
    players = []
    for id_count in range(1, 3):
        choice = input("Human player or robot? (H/R) ")
        if choice.upper() in spchoice:
            players.append(spchoice[choice.upper()](id_count))
        else:
            raise Exception(f"Bad input")

    return time_change, players[0], players[1]

if __name__ == "__main__":
    time_change, sp1, sp2 = user_inputs()
    game = PigGame(time_change, sp1, sp2)
    game.start()
