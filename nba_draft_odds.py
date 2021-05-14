#NBA DRAFT ODDS CALCULATOR

import copy

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

def new_ball_odds(picked, current_odds):
    new_odds = current_odds.copy()
    for pick in picked:
        new_odds[pick] = 0

    return new_odds

def get_next_pick_chance(team_spot, odds):
    return odds[team_spot]/sum(odds)


if __name__ == "__main__":
    #Remember pick 1 would be index 0. So I add padding at 0
    Ball_Odds = [0, 140, 140, 140, 125, 105, 90, 75, 60, 45, 30, 20, 15, 10, 5]
    t_arr = ['Rockets', 'Pistons', 'Thunder', 'Magic', 'Wolves', '', '', '', '', '', '', '', '', '']
    Current_odds = copy.deepcopy(Ball_Odds)
    teams = [{"name":t_arr[0], "position":1}, {"name":t_arr[1], "position":2}, {"name":t_arr[2], "position":3}, {"name":t_arr[3], "position":4},
        {"name":t_arr[4], "position":5}, {"name":t_arr[5], "position":6}, {"name":t_arr[6], "position":7}, {"name":t_arr[7], "position":8},
        {"name":t_arr[8], "position":9}, {"name":t_arr[9], "position":10}, {"name":t_arr[10], "position":11}, {"name":t_arr[11], "position":12},
        {"name":t_arr[12], "position":13}, {"name":t_arr[13], "position":14}]
    tied_odds = ties([[3,4], [5,6], [9,10], [12,13]], Current_odds)
    current_sum = sum(tied_odds)

    first_pick_odds = []
    for team in teams:
        first_pick_odds.append(get_next_pick_chance(team['position'], tied_odds))

    #right now if gets fun

    #PICK FIRST
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

    odds_thunder_1st = sum([sitc['odds'] for sitc in fourth if \
    
    #chance = get_next_pick_chance(3, tied_odds)
    print(fourth)

  
    
    

