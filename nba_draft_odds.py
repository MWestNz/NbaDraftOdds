#NBA DRAFT ODDS CALCULATOR

import copy

#Fixes the odds off lottery balls where there is a tie, #FIXME as of now doesn't do the coin flip, just splits balls down the middle
def ties(tie_list, odds):
    tied_odds = odds.copy()
    for tie in tie_list:
        summ = 0
        for i in tie:
            summ += tied_odds[i]
        new_odd = summ/len(tie)

        for ii in tie:
            tied_odds[ii] = new_odd

    return tied_odds

#After a lottery pick remove the chance of that team picking again
def new_ball_odds(picked, current_odds):
    new_odds = current_odds.copy()
    for pick in picked:
        new_odds[pick] = 0

    return new_odds

#The chance of a team picking next
def get_next_pick_chance(team_spot, odds):
    return odds[team_spot]/sum(odds)

#Calculates the list of possible top 4 picks based on lottery odds. #FIXME Currently uses globals defined in main. 
def get_top_4_odds():

    first = []
    second = []
    third = []
    fourth = []
    for team in teams:
        first.append({'picks':{'1st':team}, 'odds':first_pick_odds[team['position']-1]})
    
    for possible in first:
        new_odds = new_ball_odds([possible['picks']['1st']['position']], tied_odds)
        
        for team in teams:
            second_odds = (get_next_pick_chance(team['position'], new_odds))
            if second_odds > 0:
                poss2 = copy.deepcopy(possible)
                poss2['picks']['2nd'] = team
                poss2['odds'] = second_odds * poss2['odds']
                second.append(poss2)
    
    for possible in second:
        newer_odds = new_ball_odds([possible['picks']['1st']['position'], possible['picks']['2nd']['position']], tied_odds)

        for team in teams:
            third_odds = (get_next_pick_chance(team['position'], newer_odds))
            if third_odds > 0:
                poss3 = copy.deepcopy(possible)
                poss3['picks']['3rd'] = team
                poss3['odds'] = third_odds * poss3['odds']
                third.append(poss3)

    for possible in third:
        newest_odds = new_ball_odds([possible['picks']['1st']['position'], possible['picks']['2nd']['position'],
                                    possible['picks']['3rd']['position']], tied_odds)

        for team in teams:
            fourth_odds = (get_next_pick_chance(team['position'], newest_odds))
            if fourth_odds > 0:
                poss4 = copy.deepcopy(possible)
                poss4['picks']['4th'] = team
                poss4['odds'] = fourth_odds * poss4['odds']
                fourth.append(poss4)

    return fourth

#Get the remaining lottery picks for all possible top 4 combinations. #FIXME Add in ties.
def get_rest_odds(odds_list, ties, t_arr, tied_odds):
    for item in odds_list:
        left = list(range(14))
        left.append(14)
        left.pop(0)
        selected = [item['picks']['1st']['position'], item['picks']['2nd']['position'], item['picks']['3rd']['position'], item['picks']['4th']['position']]
        for s in selected:
            left.remove(s)
        picks = ['5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th']
        for ii in range(len(left)):
            item['picks'][picks[ii]] = {'name':teams[left[ii]-1]['name'], 'position':teams[left[ii]-1]['position']}
        
    return odds_list

#Get the sum off all chances given set conditions.
def odds_of_result(odds_list, with_dict, without_dict=[], one_of_list=[]):
    #Each object in the param dicts has a team and a pick
    
    def test_conds(sitch):
        ret = True
        if with_dict != []:
            #All of these
            for item in with_dict:
                ret = sitch['picks'][item['pick']]['name'] == item['name']
                if ret == False:
                    return ret
        if without_dict != []:
            #None of these
            for item in without_dict:
                ret = sitch['picks'][item['pick']]['name'] != item['name']
                if ret == False:
                    return ret
        if one_of_list != []:
            #At least one of these.
            ret = False
            for item in one_of_list:
                ret = sitch['picks'][item['pick']]['name'] == item['name']
                if ret == True:
                    return ret
        return ret

    odds = sum([sitc['odds'] for sitc in odds_list if test_conds(sitc)])
    return odds

if __name__ == "__main__":
    #Remember pick 1 would be index 0. So I add padding at 0. These are the base odds before ties.
    Ball_Odds = [0, 140, 140, 140, 125, 105, 90, 75, 60, 45, 30, 20, 15, 10, 5]

    #This is the current order of the teams, ignoring ties which I have semi implemented, but not the coin toss if both the tied teams miss top 4.
    t_arr = ['Rockets', 'Pistons', 'Thunder', 'Magic', 'Wolves', 'Cavs', 'Raptors', 'Bulls', 'Pelicans', 'Kings', 'Wizards',
            'Spurs', 'Pacers', 'Grizz']
    #List of teams tied, and the places. Bit untidy but works for now.
    ties_list = [[3,4], [5,6], [9,10], [12,13]] 
    #make a copy incase we do multiple calculations in one run. And calclulate the current ties.
    current_odds = copy.deepcopy(Ball_Odds)
    tied_odds = ties(ties_list, current_odds)

    #Set up teams object, little bit ugly, will be a better way of doing this but just want to get something working for now.
    teams = [{"name":t_arr[0], "position":1}, {"name":t_arr[1], "position":2}, {"name":t_arr[2], "position":3}, {"name":t_arr[3], "position":4},
        {"name":t_arr[4], "position":5}, {"name":t_arr[5], "position":6}, {"name":t_arr[6], "position":7}, {"name":t_arr[7], "position":8},
        {"name":t_arr[8], "position":9}, {"name":t_arr[9], "position":10}, {"name":t_arr[10], "position":11}, {"name":t_arr[11], "position":12},
        {"name":t_arr[12], "position":13}, {"name":t_arr[13], "position":14}]
    
    #Get odds for the first pick.
    first_pick_odds = []
    for team in teams:
        first_pick_odds.append(get_next_pick_chance(team['position'], tied_odds))

    #Get the list off possible top 4 picks and the odds of each situation
    odds_list = get_top_4_odds()

    #Populate the rest of the lottery in ranking order. (#TODO This currently takes in Ties but doesn't use that parameter)
    rest = get_rest_odds(odds_list, ties, t_arr, tied_odds)
    

    #OPTIONS SECTION
    on_list = [
        {'name':'Thunder', 'pick':'1st'},
        {'name':'Rockets', 'pick':'5th'}
    ]
    odds_of_1_5 = odds_of_result(rest, on_list, [], []) #Chance of Thunder getting 1 and 5

    on_list = [
        {'name':'Thunder', 'pick':'2nd'},
        {'name':'Rockets', 'pick':'5th'}
    ]
    
    odds_of_2_5 = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'3rd'},
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_3_5 = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'4th'},
        {'name':'Rockets', 'pick':'5th'}
    ]
   
    odds_of_4_5 = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'1st'}
    ]
    one_of_list = [
        {'name':'Rockets', 'pick':'2nd'},
        {'name':'Rockets', 'pick':'3rd'},
        {'name':'Rockets', 'pick':'4th'}
    ]
    odds_of_1_alone = odds_of_result(rest, on_list, [], one_of_list)

    on_list = [
        {'name':'Thunder', 'pick':'2nd'}
    ]
    one_of_list = [
        {'name':'Rockets', 'pick':'1st'},
        {'name':'Rockets', 'pick':'3rd'},
        {'name':'Rockets', 'pick':'4th'}
    ]
    odds_of_2_alone = odds_of_result(rest, on_list, [], one_of_list)

    on_list = [
        {'name':'Thunder', 'pick':'3rd'}
    ]
    one_of_list = [
        {'name':'Rockets', 'pick':'1st'},
        {'name':'Rockets', 'pick':'2nd'},
        {'name':'Rockets', 'pick':'4th'}
    ]
    odds_of_3_alone = odds_of_result(rest, on_list, [], one_of_list)

    on_list = [
        {'name':'Thunder', 'pick':'4th'}
    ]
    one_of_list = [
        {'name':'Rockets', 'pick':'1st'},
        {'name':'Rockets', 'pick':'2nd'},
        {'name':'Rockets', 'pick':'3rd'}
    ]
    odds_of_4_alone = odds_of_result(rest, on_list, [], one_of_list)

    on_list = [
        {'name':'Thunder', 'pick':'5th'}
    ]
    
    odds_of_5_alone = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'6th'},
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_6_5 = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'7th'},
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_7_5 = odds_of_result(rest, on_list)

    on_list = [
        {'name':'Thunder', 'pick':'6th'}
    ]
    off_list = [
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_6_alone = odds_of_result(rest, on_list, off_list)

    on_list = [
        {'name':'Thunder', 'pick':'7th'}
    ]
    off_list = [
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_7_alone = odds_of_result(rest, on_list, off_list)

    on_list = [
        {'name':'Thunder', 'pick':'8th'},
        {'name':'Rockets', 'pick':'5th'}
    ]

    odds_of_8_5 = odds_of_result(rest, on_list)

    #Simple print output for now.

    print("Thunder Pick:")
    print(f"1st: alone: {100*odds_of_1_alone:.2f}% and with 5: {100*odds_of_1_5:.2f}%")
    print(f"2nd: alone: {100*odds_of_2_alone:.2f}% and with 5: {100*odds_of_2_5:.2f}%")
    print(f"3rd: alone: {100*odds_of_3_alone:.2f}% and with 5: {100*odds_of_3_5:.2f}%")
    print(f"4th: alone: {100*odds_of_4_alone:.2f}% and with 5: {100*odds_of_4_5:.2f}%")
    print(f"5th: alone: {100*odds_of_5_alone:.2f}")
    print(f"6th: alone: {100*odds_of_6_alone:.2f}% and with 5: {100*odds_of_6_5:.2f}%")
    print(f"7th: alone: {100*odds_of_7_alone:.2f}% and with 5: {100*odds_of_7_5:.2f}%")
    print(f"8 with 5: {100*odds_of_8_5:.2f}%")

  
    
    

