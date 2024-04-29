import pandas as pd
import os
import random
import math
from itertools import combinations

# Direct to project file
os.getcwd()
os.chdir('./Relational Processing Ctx 2')

# Create general stimulus pool
AllStimuli = pd.read_excel('AllStimuli.xlsx', engine='openpyxl')
# Concatenate all columns from AllStimuli into one united column
stimList = []
for iter in range(len(AllStimuli.columns)):
    currentList = AllStimuli.iloc[:, iter].tolist()
    stimList = stimList + currentList

df_stimList = pd.DataFrame(stimList)

# Create dictionary for colors with their similar connections
colorDict = {
    'yellow': 'yellow-amber-lime',
    'amber': 'amber-yellow-orange',
    'orange': 'orange-amber-rust',
    'rust': 'rust-orange-red',
    'red': 'red-rust-magenta',
    'magenta': 'magenta-red-purple',
    'purple': 'purple-magenta-violet',
    'violet': 'violet-purple-blue',
    'blue': 'blue-violet-moss',
    'moss': 'moss-blue-green',
    'green': 'green-moss-lime',
    'lime': 'lime-green-yellow'
}
formDict = {
    'triangle': 'triangle-pentagon-pentagon',
    'pentagon': 'pentagon-triangle-heptagon',
    'heptagon': 'heptagon-pentagon-nonagon',
    'nonagon': 'nonagon-heptagon-circle',
    'circle': 'circle-nonagon-nonagon'
}

# co: Functions for nonSimiliarity #####################################################################################

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name

def form_nonSimiliarity(form1, form2, form3, otherStim_form, otherStim, stimList):
    if otherStim_form != form1 and otherStim_form != form2 and otherStim_form != form3:
        # append
        stimList.append(otherStim)
        stimFound = True
        return stimFound
    else:
        stimFound = False
        return stimFound

def color_nonSimiliarity(color1, color2, color3, form1, form2, form3, otherStim_color, otherStim_form, otherStim, stimList):
    if otherStim_color != color1 and otherStim_color != color2 and otherStim_color != color3:
        stimFound = form_nonSimiliarity(form1, form2, form3, otherStim_form, otherStim, stimList)
        return stimFound
    else:
        stimFound = False
        return stimFound

def create_RPCtx2_nonSimiliarity_trials(numTrials, numStim, dataFrame):

    for displays in range(1, 5):
        if displays == 1:
            rangeList = [0, int(numTrials / 4)]
        elif displays == 2:
            rangeList = [int(numTrials / 4), int(numTrials / 2)]
        elif displays == 3:
            rangeList = [int(numTrials / 2), int(numTrials / 2) + int(numTrials / 4)]
        else:
            rangeList = [int(numTrials / 2) + int(numTrials / 4), numTrials]

        for iter in range(rangeList[0], rangeList[1]):
            # Allocate list for the stimuli presented in one trial
            stimList = []
            # first stim is sampled
            firstStim = df_stimList.sample()
            splitted_firstStim_color = firstStim.iloc[0, 0].split('_')[0]
            splitted_firstStim_form = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
            # colors to look for w.r.t. first Stim
            [c1, c2, c3] = colorDict[splitted_firstStim_color].split('-')
            # forms to look for w.r.t. first Stim
            [f1, f2, f3] = formDict[splitted_firstStim_form].split('-')
            # Append first stim to list of 3 stimuli in total for one trial
            stimList.append(firstStim)

            for i in range(numStim - math.ceil(numStim/2)):
                # Find otherStim that has similiar form
                stimFound = False
                while stimFound == False:
                    secondStim = df_stimList.sample()
                    splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # compare new sampled stim with firstStim
                    if splitted_secondStim_form == splitted_firstStim_form and splitted_secondStim_color != c1 and \
                            splitted_secondStim_color != c2 and splitted_secondStim_color != c3:
                        stimList.append(secondStim)
                        stimFound = True

            # Find stim that has similiar form like otherStim
            for i in range(numStim - (math.floor(numStim/2) + 1)):
                stimFound = False
                while stimFound == False:
                    thirdStim = df_stimList.sample()
                    splitted_thirdStim_color = thirdStim.iloc[0, 0].split('_')[0]
                    splitted_thirdStim_form = thirdStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # compare new sampled stim with firstStim form
                    stimFound = color_nonSimiliarity(c1, c2, c3, f1, f2, f3, splitted_thirdStim_color, splitted_thirdStim_form, thirdStim, stimList)

            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = combinations([2, 6, 10, 14, 18, 22, 26, 30], 5)
            elif displays == 2:
                fieldNumberList = combinations([1, 5, 9, 13, 17, 21, 25, 29], 5)
            elif displays == 3:
                fieldNumberList = combinations([4, 8, 12, 16, 20, 24, 28, 32], 5)
            else:
                fieldNumberList = combinations([3, 7, 11, 15, 19, 23, 27, 31], 5)

            # Assign empty fields on current trial
            dataFrame.loc[iter] = '000_000.png'
            # Assign Display variable
            dataFrame.iloc[iter,0] = "Display {} RP Ctx2".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomList = random.choice(list(fieldNumberList))
            randomFieldNumbers = random.sample(randomList, numStim)
            for i in range(len(stimList)):
                dataFrame.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answers to real df
            for stimIter in range(numStim-(math.ceil(numStim/2) - 1)):
                dataFrame.loc[iter, 36+stimIter] = stimList[stimIter].iloc[0, 0]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataFrame.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataFrame.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataFrame.iloc[iter, 35] = 1

    # Give columns the right names
    if len(dataFrame.columns) == 38:
        dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                             'Field 8', 'Field 9', \
                             'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                             'Field 17', 'Field 18', 'Field 19', \
                             'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                             'Field 27', 'Field 28', 'Field 29', \
                             'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                             'TrialRandomisation', 'CorrectAnswer1', 'CorrectAnswer2']
    elif len(dataFrame.columns) == 39:
        dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                             'Field 8', 'Field 9', \
                             'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                             'Field 17', 'Field 18', 'Field 19', \
                             'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                             'Field 27', 'Field 28', 'Field 29', \
                             'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                             'TrialRandomisation', 'CorrectAnswer1', 'CorrectAnswer2', 'CorrectAnswer3']

    dataFrameName = get_df_name(dataFrame)
    # Save df as spreadsheet
    dataFrame.to_excel('{}.xlsx'.format(dataFrameName))


# ======================================================================================================================
# Create 800 trials for 3stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_3stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(38))
# create trials
create_RPCtx2_nonSimiliarity_trials(numTrials, 3, RP_Ctx2_trials_3stim_nonSimiliar)

# ======================================================================================================================
# Create 800 trials for 4stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_4stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(39))
# create trials
create_RPCtx2_nonSimiliarity_trials(numTrials, 4, RP_Ctx2_trials_4stim_nonSimiliar)

# ======================================================================================================================
# Create 800 trials for 5stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_5stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(39))
# create trials
create_RPCtx2_nonSimiliarity_trials(numTrials, 5, RP_Ctx2_trials_5stim_nonSimiliar)


# co: Functions for similiarity ########################################################################################

def form_similiarity(form2, form3, otherStim_form, otherStim, stimList):
    if otherStim_form == form2 or otherStim_form == form3:
        # append
        stimList.append(otherStim)
        stimFound = True
        return stimFound
    else:
        stimFound = False
        return stimFound

def color_similiarity(color1, color2, color3, form2, form3, otherStim_color, otherStim_form, otherStim, stimList):
    if otherStim_color == color1 or otherStim_color == color2 or otherStim_color == color3:
        stimFound = form_similiarity(form2, form3, otherStim_form, otherStim, stimList)
        return stimFound
    else:
        stimFound = False
        return stimFound

def create_RPCtx2_similiarity_trials(numTrials, numStim, dataFrame):

    for displays in range(1, 5):
        if displays == 1:
            rangeList = [0, int(numTrials / 4)]
        elif displays == 2:
            rangeList = [int(numTrials / 4), int(numTrials / 2)]
        elif displays == 3:
            rangeList = [int(numTrials / 2), int(numTrials / 2) + int(numTrials / 4)]
        else:
            rangeList = [int(numTrials / 2) + int(numTrials / 4), numTrials]

        for iter in range(rangeList[0], rangeList[1]):
            # Allocate list for the stimuli presented in one trial
            stimList = []
            # first stim is sampled
            firstStim = df_stimList.sample()
            splitted_firstStim_color = firstStim.iloc[0, 0].split('_')[0]
            splitted_firstStim_form = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
            # colors to look for w.r.t. first Stim
            [c1, c2, c3] = colorDict[splitted_firstStim_color].split('-')
            # forms to look for w.r.t. first Stim
            [f1, f2, f3] = formDict[splitted_firstStim_form].split('-')
            # Append first stim to list of 3 stimuli in total for one trial
            stimList.append(firstStim)

            for i in range(numStim - math.ceil(numStim/2)):
                # Find otherStim that has similiar form
                stimFound = False
                while stimFound == False:
                    secondStim = df_stimList.sample()
                    splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # compare new sampled stim with firstStim
                    if splitted_secondStim_form == splitted_firstStim_form and (splitted_secondStim_color == c1 or \
                            splitted_secondStim_color == c2 or splitted_secondStim_color == c3):
                        stimList.append(secondStim)
                        stimFound = True

            # Find stim that has similiar form like otherStim
            for i in range(numStim - (math.floor(numStim/2) + 1)):
                stimFound = False
                while stimFound == False:
                    thirdStim = df_stimList.sample()
                    splitted_thirdStim_color = thirdStim.iloc[0, 0].split('_')[0]
                    splitted_thirdStim_form = thirdStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # compare new sampled stim with firstStim form
                    stimFound = color_similiarity(c1, c2, c3, f2, f3, splitted_thirdStim_color, splitted_thirdStim_form, thirdStim, stimList)

            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = combinations([2, 6, 10, 14, 18, 22, 26, 30], 5)
            elif displays == 2:
                fieldNumberList = combinations([1, 5, 9, 13, 17, 21, 25, 29], 5)
            elif displays == 3:
                fieldNumberList = combinations([4, 8, 12, 16, 20, 24, 28, 32], 5)
            else:
                fieldNumberList = combinations([3, 7, 11, 15, 19, 23, 27, 31], 5)

            # Assign empty fields on current trial
            dataFrame.loc[iter] = '000_000.png'
            # Assign Display variable
            dataFrame.iloc[iter,0] = "Display {} RP Ctx2".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomList = random.choice(list(fieldNumberList))
            randomFieldNumbers = random.sample(randomList, numStim)
            for i in range(len(stimList)):
                dataFrame.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answers to real df
            for stimIter in range(numStim-(math.ceil(numStim/2) - 1)):
                dataFrame.loc[iter, 36+stimIter] = stimList[stimIter].iloc[0, 0]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataFrame.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataFrame.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataFrame.iloc[iter, 35] = 1

    # Give columns the right names
    if len(dataFrame.columns) == 38:
        dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6',
                             'Field 7',
                             'Field 8', 'Field 9', \
                             'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                             'Field 17', 'Field 18', 'Field 19', \
                             'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                             'Field 27', 'Field 28', 'Field 29', \
                             'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                             'TrialRandomisation', 'CorrectAnswer1', 'CorrectAnswer2']
    elif len(dataFrame.columns) == 39:
        dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6',
                             'Field 7',
                             'Field 8', 'Field 9', \
                             'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                             'Field 17', 'Field 18', 'Field 19', \
                             'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                             'Field 27', 'Field 28', 'Field 29', \
                             'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                             'TrialRandomisation', 'CorrectAnswer1', 'CorrectAnswer2', 'CorrectAnswer3']

    dataFrameName = get_df_name(dataFrame)
    # Save df as spreadsheet
    dataFrame.to_excel('{}.xlsx'.format(dataFrameName))


# ======================================================================================================================
# Create 800 trials for 3stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_3stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(38))
# create trials
create_RPCtx2_similiarity_trials(numTrials, 3, RP_Ctx2_trials_3stim_similiar)

# ======================================================================================================================
# Create 800 trials for 4stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_4stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(39))
# create trials
create_RPCtx2_similiarity_trials(numTrials, 4, RP_Ctx2_trials_4stim_similiar)

# ======================================================================================================================
# Create 800 trials for 5stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx2_trials_5stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(39))
# create trials
create_RPCtx2_similiarity_trials(numTrials, 5, RP_Ctx2_trials_5stim_similiar)