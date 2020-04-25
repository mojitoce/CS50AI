from nim import train, play, play_two_ai

ai_one = train(10000)
# ai_two = train(100000)
play(ai_one)

#
# game_count = play_two_ai(ai_one, ai_two, 1000)
#
# print(game_count)
