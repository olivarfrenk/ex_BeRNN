import pandas as pd
import os
import random

# Direct to project file
os.getcwd()
os.chdir('./Executive Function Anti')

# Create general stimulus pool
AllStimuli = pd.read_excel('AllStimuli.xlsx', engine='openpyxl')
# Concatenate all columns from AllStimuli into one united column
stimList = []
for iter in range(len(AllStimuli.columns)):
    currentList = AllStimuli.iloc[:, iter].tolist()
    stimList = stimList + currentList

df_stimList = pd.DataFrame(stimList)

# Create dictionaries
greenResp_dict = {
    'up': 'D',
    'down': 'U',
    'left': 'R',
    'right': 'L'
}
redResp_dict = {
    'up': 'U',
    'down': 'D',
    'left': 'L',
    'right': 'R'
}
color_dict = {
    'green': 'red',
    'red': 'green'
}
direction_dict = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

# ======================================================================================================================
# Create 200 trials for easy - same color, same direction
# ======================================================================================================================
trials_easy = pd.DataFrame(index = range(800), columns = range(37))

for displays in range(1,3):
    if displays == 1:
        rangeList = [0, int(800/2)]
    else:
        rangeList = [int(800/2), 800]

    for i in range(rangeList[0],rangeList[1]):
        # select rangeList according to display
        if displays == 1: # Display 1
            [w,x,y,z,a],[dis] = random.sample(
                        [[[32, 6, 12, 18, 24],[1]], [[2, 8, 14, 20, 26],[2]], [[4, 10, 16, 22, 28],[3]], [[6, 12, 18, 24, 30],[4]],
                         [[8, 14, 20, 26, 32],[5]], [[10, 16, 22, 28, 2],[6]], \
                         [[12, 18, 24, 30, 4],[7]], [[14, 20, 26, 32, 6],[8]], [[16, 22, 28, 2, 8],[9]], [[18, 24, 30, 4, 10],[10]],
                         [[20, 26, 32, 6, 12],[11]], [[22, 28, 2, 8, 14],[12]], \
                         [[24, 30, 4, 10, 16],[13]], [[26, 32, 6, 12, 18],[14]], [[28, 2, 8, 14, 20],[15]], [[30, 4, 10, 16, 22],[16]]], 1)[0]
        elif displays == 2: # Display 2
            [w,x,y,z,a],[dis] = random.sample(
                        [[[1, 7, 13, 19, 25],[17]], [[3, 9, 15, 21, 27],[18]], [[5, 11, 17, 23, 29],[19]], [[7, 13, 19, 25, 31],[20]],
                         [[9, 15, 21, 27, 1],[21]], [[11, 17, 23, 29, 3],[22]], \
                         [[13, 19, 25, 31, 5],[23]], [[15, 21, 27, 1, 7],[24]], [[17, 23, 29, 3, 9],[25]], [[19, 25, 31, 5, 11],[26]],
                         [[21, 27, 1, 7, 13],[27]], [[23, 29, 3, 9, 15],[28]], \
                         [[25, 31, 5, 11, 17],[29]], [[27, 1, 7, 13, 19],[30]], [[29, 3, 9, 15, 21],[31]], [[31, 5, 11, 17, 23],[32]]], 1)[0]

        # Randomly choose a stim from general stimulus pool
        centralStim = df_stimList.sample()
        splitted_centralStim_color = centralStim.iloc[0, 0].split('_')[0]
        splitted_centralStim_direction = centralStim.iloc[0, 0].split('_')[1].split('.')[0]

        # Random decision when no-go trial is presented (1/3 of all trials)
        ratio_list = [1, 2, 3, 4, 5] # co: ratio of 1/5 (Price et al., 2015)
        ratio = random.sample(ratio_list, 1)

        if ratio[0] == 1:
            splitted_otherStim_color = splitted_centralStim_color
            splitted_otherStim_direction = 'X'
            otherStim = splitted_otherStim_color + '_' + splitted_otherStim_direction + '.png'
        else:
            otherStim = centralStim.iloc[0, 0]
            splitted_otherStim_direction = otherStim.split('_')[1].split('.')[0]

        # Assign empty fields on current trial
        trials_easy.loc[i] = '000_000.png'
        # Fill the cells for correct and wrong answers
        trials_easy.loc[i, w] = otherStim
        trials_easy.loc[i, x] = otherStim
        trials_easy.loc[i, y] = centralStim.iloc[0, 0]
        trials_easy.loc[i, z] = otherStim
        trials_easy.loc[i, a] = otherStim
        # Save correct answer to real df
        if splitted_centralStim_color == 'green' and splitted_otherStim_direction != 'X':
            trials_easy.loc[i, 36] = greenResp_dict[splitted_centralStim_direction]
        elif splitted_centralStim_color == 'red' and splitted_otherStim_direction != 'X':
            trials_easy.loc[i, 36] = redResp_dict[splitted_centralStim_direction]
        elif splitted_otherStim_direction == 'X':
            trials_easy.loc[i, 36] = 'noResponse'

        # Assign Display variable
        trials_easy.iloc[i,0] = "Display {}".format(dis)
        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_easy.iloc[i, 33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_easy.iloc[i, 34] = after_response_time[0]
        # Add Trial Randomization
        trials_easy.iloc[i, 35] = 1

# Give columns the right names
trials_easy.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'TrialRandomisation', 'CorrectAnswer']
# Save df as spreadsheet
trials_easy.to_excel('EF_Anti_trials_sameColor_sameDirect.xlsx')


# ======================================================================================================================
# Create 200 trials for normal - diff color, same direction
# ======================================================================================================================
trials_normal = pd.DataFrame(index = range(800), columns = range(37))

for displays in range(1,3):
    if displays == 1:
        rangeList = [0, int(800/2)]
    else:
        rangeList = [int(800/2), 800]

    for i in range(rangeList[0],rangeList[1]):
        # select rangeList according to display
        if displays == 1: # Display 1
            [w,x,y,z,a],[dis] = random.sample(
                        [[[32, 6, 12, 18, 24],[1]], [[2, 8, 14, 20, 26],[2]], [[4, 10, 16, 22, 28],[3]], [[6, 12, 18, 24, 30],[4]],
                         [[8, 14, 20, 26, 32],[5]], [[10, 16, 22, 28, 2],[6]], \
                         [[12, 18, 24, 30, 4],[7]], [[14, 20, 26, 32, 6],[8]], [[16, 22, 28, 2, 8],[9]], [[18, 24, 30, 4, 10],[10]],
                         [[20, 26, 32, 6, 12],[11]], [[22, 28, 2, 8, 14],[12]], \
                         [[24, 30, 4, 10, 16],[13]], [[26, 32, 6, 12, 18],[14]], [[28, 2, 8, 14, 20],[15]], [[30, 4, 10, 16, 22],[16]]], 1)[0]
        elif displays == 2: # Display 2
            [w,x,y,z,a],[dis] = random.sample(
                        [[[1, 7, 13, 19, 25],[17]], [[3, 9, 15, 21, 27],[18]], [[5, 11, 17, 23, 29],[19]], [[7, 13, 19, 25, 31],[20]],
                         [[9, 15, 21, 27, 1],[21]], [[11, 17, 23, 29, 3],[22]], \
                         [[13, 19, 25, 31, 5],[23]], [[15, 21, 27, 1, 7],[24]], [[17, 23, 29, 3, 9],[25]], [[19, 25, 31, 5, 11],[26]],
                         [[21, 27, 1, 7, 13],[27]], [[23, 29, 3, 9, 15],[28]], \
                         [[25, 31, 5, 11, 17],[29]], [[27, 1, 7, 13, 19],[30]], [[29, 3, 9, 15, 21],[31]], [[31, 5, 11, 17, 23],[32]]], 1)[0]

        # Randomly choose a stim from general stimulus pool
        centralStim = df_stimList.sample()
        splitted_centralStim_color = centralStim.iloc[0, 0].split('_')[0]
        splitted_centralStim_direction = centralStim.iloc[0, 0].split('_')[1].split('.')[0]

        # Random decision when no-go trial is presented (1/3 of all trials)
        ratio_list = [1, 2, 3, 4, 5] # co: ratio of 1/5 (Price et al., 2015)
        ratio = random.sample(ratio_list, 1)

        if ratio[0] == 1:
            splitted_otherStim_color = color_dict[splitted_centralStim_color]
            splitted_otherStim_direction = 'X'
            otherStim = splitted_otherStim_color + '_' + splitted_otherStim_direction + '.png'
        else:
            splitted_otherStim_color = color_dict[splitted_centralStim_color]
            splitted_otherStim_direction = splitted_centralStim_direction
            otherStim = splitted_otherStim_color + '_' + splitted_otherStim_direction + '.png'

        # Assign empty fields on current trial
        trials_normal.loc[i] = '000_000.png'
        # Fill the cells for correct and wrong answers
        trials_normal.loc[i, w] = otherStim
        trials_normal.loc[i, x] = otherStim
        trials_normal.loc[i, y] = centralStim.iloc[0, 0]
        trials_normal.loc[i, z] = otherStim
        trials_normal.loc[i, a] = otherStim
        # Save correct answer to real df
        if splitted_centralStim_color == 'green' and splitted_otherStim_direction != 'X':
            trials_normal.loc[i, 36] = greenResp_dict[splitted_centralStim_direction]
        elif splitted_centralStim_color == 'red' and splitted_otherStim_direction != 'X':
            trials_normal.loc[i, 36] = redResp_dict[splitted_centralStim_direction]
        elif splitted_otherStim_direction == 'X':
            trials_normal.loc[i, 36] = 'noResponse'

        # Assign Display variable
        trials_normal.iloc[i,0] = "Display {}".format(dis)
        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_normal.iloc[i,33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_normal.iloc[i,34] = after_response_time[0]
        # Add Trial Randomization
        trials_normal.iloc[i,35] = 1

# Give columns the right names
trials_normal.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'TrialRandomisation', 'CorrectAnswer']
# Save df as spreadsheet
trials_normal.to_excel('EF_Anti_trials_diffColor_sameDirect.xlsx')


# ======================================================================================================================
# Create 200 trials for normal - diff color, diff direction
# ======================================================================================================================
trials_hard = pd.DataFrame(index = range(800), columns = range(37))

for displays in range(1,3):
    if displays == 1:
        rangeList = [0, int(800/2)]
    else:
        rangeList = [int(800/2), 800]

    for i in range(rangeList[0],rangeList[1]):
        # select rangeList according to display
        if displays == 1: # Display 1
            [w,x,y,z,a],[dis] = random.sample(
                        [[[32, 6, 12, 18, 24],[1]], [[2, 8, 14, 20, 26],[2]], [[4, 10, 16, 22, 28],[3]], [[6, 12, 18, 24, 30],[4]],
                         [[8, 14, 20, 26, 32],[5]], [[10, 16, 22, 28, 2],[6]], \
                         [[12, 18, 24, 30, 4],[7]], [[14, 20, 26, 32, 6],[8]], [[16, 22, 28, 2, 8],[9]], [[18, 24, 30, 4, 10],[10]],
                         [[20, 26, 32, 6, 12],[11]], [[22, 28, 2, 8, 14],[12]], \
                         [[24, 30, 4, 10, 16],[13]], [[26, 32, 6, 12, 18],[14]], [[28, 2, 8, 14, 20],[15]], [[30, 4, 10, 16, 22],[16]]], 1)[0]
        elif displays == 2: # Display 2
            [w,x,y,z,a],[dis] = random.sample(
                        [[[1, 7, 13, 19, 25],[17]], [[3, 9, 15, 21, 27],[18]], [[5, 11, 17, 23, 29],[19]], [[7, 13, 19, 25, 31],[20]],
                         [[9, 15, 21, 27, 1],[21]], [[11, 17, 23, 29, 3],[22]], \
                         [[13, 19, 25, 31, 5],[23]], [[15, 21, 27, 1, 7],[24]], [[17, 23, 29, 3, 9],[25]], [[19, 25, 31, 5, 11],[26]],
                         [[21, 27, 1, 7, 13],[27]], [[23, 29, 3, 9, 15],[28]], \
                         [[25, 31, 5, 11, 17],[29]], [[27, 1, 7, 13, 19],[30]], [[29, 3, 9, 15, 21],[31]], [[31, 5, 11, 17, 23],[32]]], 1)[0]

        # Randomly choose a stim from general stimulus pool
        centralStim = df_stimList.sample()
        splitted_centralStim_color = centralStim.iloc[0, 0].split('_')[0]
        splitted_centralStim_direction = centralStim.iloc[0, 0].split('_')[1].split('.')[0]

        # Random decision when no-go trial is presented (1/3 of all trials)
        ratio_list = [1, 2, 3, 4, 5] # co: ratio of 1/5 (Price et al., 2015)
        ratio = random.sample(ratio_list, 1)

        if ratio[0] == 1:
            splitted_otherStim_color = color_dict[splitted_centralStim_color]
            splitted_otherStim_direction = 'X'
            otherStim = splitted_otherStim_color + '_' + splitted_otherStim_direction + '.png'
        else:
            splitted_otherStim_color = color_dict[splitted_centralStim_color]
            splitted_otherStim_direction = direction_dict[splitted_centralStim_direction]
            otherStim = splitted_otherStim_color + '_' + splitted_otherStim_direction + '.png'

        # Assign empty fields on current trial
        trials_hard.loc[i] = '000_000.png'
        # Fill the cells for correct and wrong answers
        trials_hard.loc[i, w] = otherStim
        trials_hard.loc[i, x] = otherStim
        trials_hard.loc[i, y] = centralStim.iloc[0, 0]
        trials_hard.loc[i, z] = otherStim
        trials_hard.loc[i, a] = otherStim
        # Save correct answer to real df
        if splitted_centralStim_color == 'green' and splitted_otherStim_direction != 'X':
            trials_hard.loc[i, 36] = greenResp_dict[splitted_centralStim_direction]
        elif splitted_centralStim_color == 'red' and splitted_otherStim_direction != 'X':
            trials_hard.loc[i, 36] = redResp_dict[splitted_centralStim_direction]
        elif splitted_otherStim_direction == 'X':
            trials_hard.loc[i, 36] = 'noResponse'

        # Assign Display variable
        trials_hard.iloc[i,0] = "Display {}".format(dis)
        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_hard.iloc[i,33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_hard.iloc[i,34] = after_response_time[0]
        # Add Trial Randomization
        trials_hard.iloc[i,35] = 1

# Give columns the right names
trials_hard.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'TrialRandomisation', 'CorrectAnswer']
# Save df as spreadsheet
trials_hard.to_excel('EF_Anti_trials_diffColor_diffDirect.xlsx')