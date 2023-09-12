import pandas as pd
import os
import random
import math

# Direct to project file
os.getcwd()
os.chdir('./Decision Making Anti')

# Create general stimulus pool
AllStimuli = pd.read_excel('AllStimuli.xlsx', engine='openpyxl')
# Concatenate all columns from AllStimuli into one united column
stimList = []
for iter in range(len(AllStimuli.columns)):
    currentList = AllStimuli.iloc[:, iter].tolist()
    stimList = stimList + currentList
df_stimList = pd.DataFrame(stimList)

# create dictionaries
strengthDict = {
    'lowest' : 'lowest-low-low',
    'low' : 'low-lowest-high',
    'strong' : 'strong-low-strongest',
    'strongest' : 'strongest-strong-strong'
}
answerDict = {
    'up' : 'U',
    'down' : 'D',
    'left' : 'L',
    'right' : 'R'
}

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name

# todo: nonSimiliar
def createDMAntiSheets_nonSimiliar(numTrials, dataframe, numStim):
    # Fill all rows for the first 100 and second 100 (for distributing reasons on the two circles in gorilla)
    for displays in range(1, 3):
        if displays == 1:
            rangeList = [0, int(numTrials/2)]
        else:
            rangeList = [int(numTrials/2),numTrials]

        for iter in range(rangeList[0], rangeList[1]):
            # Allocate list for the stimuli presented in one trial
            stimList = []
            # Randomly choose a stim from general stimulus pool as the right direction stim
            firstStim = df_stimList.sample()
            firstStimStim_direction = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
            firstStimStim_strength = firstStim.iloc[0, 0].split('_')[0]
            [s1, s2, s3] = strengthDict[firstStimStim_strength].split('-')
            stimList.append(firstStim)
            if numStim == 5:
                stimList.append(firstStim)

            # Choose other Stim
            stimFound = False
            while stimFound == False:
                otherStim = df_stimList.sample()
                otherStim_direction = otherStim.iloc[0, 0].split('_')[1].split('.')[0]  # co: CorrectAnswer
                otherStim_strength = otherStim.iloc[0, 0].split('_')[0]
                if otherStim_direction != firstStimStim_direction and otherStim_strength != s1 and otherStim_strength != s2 and \
                        otherStim_strength != s3:

                    for i in range(math.floor(numStim/2)+1):
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
            else:
                fieldNumberList = random.sample(
                    [[1, 7, 13, 19, 25], [3, 9, 15, 21, 27], [5, 11, 17, 23, 29], [7, 13, 19, 25, 31],
                     [9, 15, 21, 27, 1], [11, 17, 23, 29, 3], \
                     [13, 19, 25, 31, 5], [15, 21, 27, 1, 7], [17, 23, 29, 3, 9], [19, 25, 31, 5, 11],
                     [21, 27, 1, 7, 13], [23, 29, 3, 9, 15], \
                     [25, 31, 5, 11, 17], [27, 1, 7, 13, 19], [29, 3, 9, 15, 21], [31, 5, 11, 17, 23]], 1)[0]

            # Assign empty fields on current trial
            dataframe.loc[iter] = '000_000.png'
            # Assign Display variable
            dataframe.iloc[iter, 0] = "Display {} DM Anti".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomFieldNumbers = random.sample(fieldNumberList, numStim)
            for i in range(len(stimList)):
                dataframe.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answer to real df
            dataframe.loc[iter, 36] = answerDict[stimList[0].iloc[0, 0].split('_')[1].split('.')[0]]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataframe.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataframe.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataframe.iloc[iter, 35] = 1

    # Give columns the right names
    dataframe.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                           'Field 8', 'Field 9', \
                           'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                           'Field 17', 'Field 18', 'Field 19', \
                           'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                           'Field 27', 'Field 28', 'Field 29', \
                           'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                           'TrialRandomisation', 'CorrectAnswer']

    dataFrameName = get_df_name(dataframe)
    # Save df as spreadsheet
    dataframe.to_excel('{}.xlsx'.format(dataFrameName))

# ======================================================================================================================
# Create 800 trials for easy - 3stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_3stim_nonSimiliar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 3
# create trials
createDMAntiSheets_nonSimiliar(numTrials, DM_Anti_trials_3stim_nonSimiliar, numStim)

# ======================================================================================================================
# Create 800 trials for normal - 4stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_4stim_nonSimiliar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 4
# create trials
createDMAntiSheets_nonSimiliar(numTrials, DM_Anti_trials_4stim_nonSimiliar, numStim)

# ======================================================================================================================
# Create 800 trials for hard - 5stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_5stim_nonSimiliar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 5
# create trials
createDMAntiSheets_nonSimiliar(numTrials, DM_Anti_trials_5stim_nonSimiliar, numStim)



# todo: similiar
def createDMAntiSheets_similiar(numTrials, dataframe, numStim):
    # Fill all rows for the first 100 and second 100 (for distributing reasons on the two circles in gorilla)
    for displays in range(1, 3):
        if displays == 1:
            rangeList = [0, int(numTrials/2)]
        else:
            rangeList = [int(numTrials/2),numTrials]

        for iter in range(rangeList[0], rangeList[1]):
            # Allocate list for the stimuli presented in one trial
            stimList = []
            # Randomly choose a stim from general stimulus pool as the right direction stim
            firstStim = df_stimList.sample()
            firstStimStim_direction = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
            firstStimStim_strength = firstStim.iloc[0, 0].split('_')[0]
            [s1, s2, s3] = strengthDict[firstStimStim_strength].split('-')
            stimList.append(firstStim)
            if numStim == 5:
                stimList.append(firstStim)

            # Choose other Stim
            stimFound = False
            while stimFound == False:
                otherStim = df_stimList.sample()
                otherStim_direction = otherStim.iloc[0, 0].split('_')[1].split('.')[0]  # co: CorrectAnswer
                otherStim_strength = otherStim.iloc[0, 0].split('_')[0]
                if otherStim_direction != firstStimStim_direction and (otherStim_strength == s1 or otherStim_strength == s2 or \
                        otherStim_strength == s3):

                    for i in range(math.floor(numStim/2)+1):
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
            else:
                fieldNumberList = random.sample(
                    [[1, 7, 13, 19, 25], [3, 9, 15, 21, 27], [5, 11, 17, 23, 29], [7, 13, 19, 25, 31],
                     [9, 15, 21, 27, 1], [11, 17, 23, 29, 3], \
                     [13, 19, 25, 31, 5], [15, 21, 27, 1, 7], [17, 23, 29, 3, 9], [19, 25, 31, 5, 11],
                     [21, 27, 1, 7, 13], [23, 29, 3, 9, 15], \
                     [25, 31, 5, 11, 17], [27, 1, 7, 13, 19], [29, 3, 9, 15, 21], [31, 5, 11, 17, 23]], 1)[0]

            # Assign empty fields on current trial
            dataframe.loc[iter] = '000_000.png'
            # Assign Display variable
            dataframe.iloc[iter, 0] = "Display {} DM Anti".format(displays)
            # Assign every stim to its field according to the sampled random numbers in fieldNumberList
            randomFieldNumbers = random.sample(fieldNumberList, numStim)
            for i in range(len(stimList)):
                dataframe.iloc[iter, randomFieldNumbers[i]] = stimList[i].iloc[0, 0]
            # Save correct answer to real df
            dataframe.loc[iter, 36] = answerDict[stimList[0].iloc[0, 0].split('_')[1].split('.')[0]]
            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            dataframe.iloc[iter, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            dataframe.iloc[iter, 34] = after_response_time[0]
            # Add Trial Randomization
            dataframe.iloc[iter, 35] = 1

    # Give columns the right names
    dataframe.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                           'Field 8', 'Field 9', \
                           'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                           'Field 17', 'Field 18', 'Field 19', \
                           'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                           'Field 27', 'Field 28', 'Field 29', \
                           'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                           'TrialRandomisation', 'CorrectAnswer']

    dataFrameName = get_df_name(dataframe)
    # Save df as spreadsheet
    dataframe.to_excel('{}.xlsx'.format(dataFrameName))

# ======================================================================================================================
# Create 800 trials for easy - 3stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_3stim_similiar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 3
# create trials
createDMAntiSheets_similiar(numTrials, DM_Anti_trials_3stim_similiar, numStim)

# ======================================================================================================================
# Create 800 trials for normal - 4stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_4stim_similiar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 4
# create trials
createDMAntiSheets_similiar(numTrials, DM_Anti_trials_4stim_similiar, numStim)

# ======================================================================================================================
# Create 800 trials for hard - 5stim nonSimiliar
# ======================================================================================================================
numTrials = 800
DM_Anti_trials_5stim_similiar = pd.DataFrame(index = range(800), columns = range(37))
numStim = 5
# create trials
createDMAntiSheets_similiar(numTrials, DM_Anti_trials_5stim_similiar, numStim)