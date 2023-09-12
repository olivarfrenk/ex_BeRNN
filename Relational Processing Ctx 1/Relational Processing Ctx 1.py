import pandas as pd
import os
import random

# Direct to project file
os.getcwd()
os.chdir('./Relational Processing Ctx 1')

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

def create_RPCtx1_nonSimiliarity_trials(numTrials, numStim, otherStimNumber, dataFrame):
    for displays in range(1,3):
        if displays == 1:
            rangeList = [0, int(numTrials/2)]
        else:
            rangeList = [int(numTrials/2), numTrials]

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

            for i in range(otherStimNumber):
                # sample otherStims
                stimFound = False
                while stimFound == False:
                    secondStim = df_stimList.sample()
                    splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors to look for w.r.t. second Stim
                    [c1_2, c2_2, c3_2] = colorDict[splitted_firstStim_color].split('-')
                    # compare new sampled stim with firstStim
                    stimFound = color_nonSimiliarity(c1, c2, c3, f1, f2, f3, splitted_secondStim_color, splitted_secondStim_form, secondStim, stimList)

                for i in range(numStim-2*otherStimNumber):
                    stimFound = False
                    while stimFound == False:
                        otherStim = df_stimList.sample()
                        splitted_otherStim_color = otherStim.iloc[0, 0].split('_')[0]
                        splitted_otherStim_form = otherStim.iloc[0, 0].split('_')[1].split('.')[0]

                        if splitted_otherStim_form == splitted_secondStim_form and splitted_otherStim_color != c1_2 and \
                                splitted_otherStim_color != c2_2 and splitted_otherStim_color != c3_2:
                            stimList.append(otherStim)
                            stimFound = True

            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = random.sample(
                    [[32, 6, 12, 18, 24], [2, 8, 14, 20, 26], [4, 10, 16, 22, 28], [6, 12, 18, 24, 30],
                     [8, 14, 20, 26, 32], [10, 16, 22, 28, 2], \
                     [12, 18, 24, 30, 4], [14, 20, 26, 32, 6], [16, 22, 28, 2, 8], [18, 24, 30, 4, 10],
                     [20, 26, 32, 6, 12], [22, 28, 2, 8, 14], \
                     [24, 30, 4, 10, 16], [26, 32, 6, 12, 18], [28, 2, 8, 14, 20], [30, 4, 10, 16, 22]], 1)[0]
                # fieldList = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
            else:
                fieldNumberList = random.sample(
                    [[1, 7, 13, 19, 25], [3, 9, 15, 21, 27], [5, 11, 17, 23, 29], [7, 13, 19, 25, 31],
                     [9, 15, 21, 27, 1], [11, 17, 23, 29, 3], \
                     [13, 19, 25, 31, 5], [15, 21, 27, 1, 7], [17, 23, 29, 3, 9], [19, 25, 31, 5, 11],
                     [21, 27, 1, 7, 13], [23, 29, 3, 9, 15], \
                     [25, 31, 5, 11, 17], [27, 1, 7, 13, 19], [29, 3, 9, 15, 21], [31, 5, 11, 17, 23]], 1)[0]
                # fieldList = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]

            # Assign empty fields on current trial
            dataFrame.loc[iter] = '000_000.png'
            # Assign Display variable
            dataFrame.iloc[iter,0] = "Display {} RP Ctx1".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomFieldNumbers = random.sample(fieldNumberList, numStim)
            for i in range(len(stimList)):
                dataFrame.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answer to real df
            dataFrame.loc[iter, 36] = stimList[0].iloc[0, 0]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataFrame.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataFrame.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataFrame.iloc[iter, 35] = 1

    # Give columns the right names
    dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                         'Field 8', 'Field 9', \
                         'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                         'Field 17', 'Field 18', 'Field 19', \
                         'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                         'Field 27', 'Field 28', 'Field 29', \
                         'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                         'TrialRandomisation', 'CorrectAnswer1']

    dataFrameName = get_df_name(dataFrame)
    # Save df as spreadsheet
    dataFrame.to_excel('{}.xlsx'.format(dataFrameName))


# ======================================================================================================================
# Create 800 trials for 3stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_3stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_nonSimiliarity_trials(numTrials, 3, 1, RP_Ctx1_trials_3stim_nonSimiliar)

# ======================================================================================================================
# Create 800 trials for 4stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_4stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_nonSimiliarity_trials(numTrials, 4, 1, RP_Ctx1_trials_4stim_nonSimiliar)

# ======================================================================================================================
# Create 800 trials for 5stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_5stim_nonSimiliar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_nonSimiliarity_trials(numTrials, 5, 2, RP_Ctx1_trials_5stim_nonSimiliar)


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

def create_RPCtx1_similiarity_trials(numTrials, numStim, otherStimNumber, dataFrame):
    for displays in range(1,3):
        if displays == 1:
            rangeList = [0, int(numTrials/2)]
        else:
            rangeList = [int(numTrials/2), numTrials]

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

            for i in range(otherStimNumber):
                # sample otherStims
                stimFound = False
                while stimFound == False:
                    secondStim = df_stimList.sample()
                    splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors to look for w.r.t. second Stim
                    [c1_2, c2_2, c3_2] = colorDict[splitted_firstStim_color].split('-')
                    # compare new sampled stim with firstStim
                    stimFound = color_similiarity(c1, c2, c3, f2, f3, splitted_secondStim_color,
                                                     splitted_secondStim_form, secondStim, stimList)

                for i in range(numStim - 2 * otherStimNumber):
                    stimFound = False
                    while stimFound == False:
                        otherStim = df_stimList.sample()
                        splitted_otherStim_color = otherStim.iloc[0, 0].split('_')[0]
                        splitted_otherStim_form = otherStim.iloc[0, 0].split('_')[1].split('.')[0]

                        if splitted_otherStim_form == splitted_secondStim_form and splitted_otherStim_color != c1_2 and \
                                (splitted_otherStim_color == c2_2 or splitted_otherStim_color == c3_2):
                            stimList.append(otherStim)
                            stimFound = True

            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = random.sample(
                    [[32, 6, 12, 18, 24], [2, 8, 14, 20, 26], [4, 10, 16, 22, 28], [6, 12, 18, 24, 30],
                     [8, 14, 20, 26, 32], [10, 16, 22, 28, 2], \
                     [12, 18, 24, 30, 4], [14, 20, 26, 32, 6], [16, 22, 28, 2, 8], [18, 24, 30, 4, 10],
                     [20, 26, 32, 6, 12], [22, 28, 2, 8, 14], \
                     [24, 30, 4, 10, 16], [26, 32, 6, 12, 18], [28, 2, 8, 14, 20], [30, 4, 10, 16, 22]], 1)[0]
                # fieldList = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
            else:
                fieldNumberList = random.sample(
                    [[1, 7, 13, 19, 25], [3, 9, 15, 21, 27], [5, 11, 17, 23, 29], [7, 13, 19, 25, 31],
                     [9, 15, 21, 27, 1], [11, 17, 23, 29, 3], \
                     [13, 19, 25, 31, 5], [15, 21, 27, 1, 7], [17, 23, 29, 3, 9], [19, 25, 31, 5, 11],
                     [21, 27, 1, 7, 13], [23, 29, 3, 9, 15], \
                     [25, 31, 5, 11, 17], [27, 1, 7, 13, 19], [29, 3, 9, 15, 21], [31, 5, 11, 17, 23]], 1)[0]
                # fieldList = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]

            # Assign empty fields on current trial
            dataFrame.loc[iter] = '000_000.png'
            # Assign Display variable
            dataFrame.iloc[iter,0] = "Display {} RP Ctx1".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomFieldNumbers = random.sample(fieldNumberList, numStim)
            for i in range(len(stimList)):
                dataFrame.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answer to real df
            dataFrame.loc[iter, 36] = stimList[0].iloc[0, 0]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataFrame.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataFrame.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataFrame.iloc[iter, 35] = 1

    # Give columns the right names
    dataFrame.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                         'Field 8', 'Field 9', \
                         'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                         'Field 17', 'Field 18', 'Field 19', \
                         'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                         'Field 27', 'Field 28', 'Field 29', \
                         'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                         'TrialRandomisation', 'CorrectAnswer1']

    dataFrameName = get_df_name(dataFrame)
    # Save df as spreadsheet
    dataFrame.to_excel('{}.xlsx'.format(dataFrameName))


# ======================================================================================================================
# Create 800 trials for 3stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_3stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_similiarity_trials(numTrials, 3, 1, RP_Ctx1_trials_3stim_similiar)

# ======================================================================================================================
# Create 800 trials for 4stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_4stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_similiarity_trials(numTrials, 4, 1, RP_Ctx1_trials_4stim_similiar)

# ======================================================================================================================
# Create 800 trials for 5stim_nonSimiliar
# ======================================================================================================================
# create empty df
numTrials = 800
RP_Ctx1_trials_5stim_similiar = pd.DataFrame(index=range(numTrials), columns=range(37))
# create trials
create_RPCtx1_similiarity_trials(numTrials, 5, 2, RP_Ctx1_trials_5stim_similiar)