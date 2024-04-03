import pandas as pd
import os
import random

# Direct to project file
os.getcwd()
os.chdir('./Working Memory')

def get_fieldNumbers():
    fieldFound = False
    while fieldFound == False:
        # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
        if displays == 1:
            fieldNumberList = random.sample([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32], 2)
        else:
            fieldNumberList = random.sample([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31], 2)
        # Check that each stimulus position is at least five fields away from each other
        if abs(fieldNumberList[0] - fieldNumberList[1]) >= 6 and abs(fieldNumberList[1] - fieldNumberList[0]) <= 26:
            fieldFound = True

    return fieldNumberList

def get_stimPair():
    # Pull first stim
    firstStim = df_stimList.sample().iloc[0,0]
    # trials_easy_preDF.loc[0, 0] = firstStim.iloc[0, 0]
    # Split information
    splitted_firstStim_color = firstStim.split('_')[0]
    splitted_firstStim_form = firstStim.split('_')[1].split('.')[0]
    # colors to look for w.r.t. first Stim
    [c1, c2, c3] = colorDict[splitted_firstStim_color].split('-')
    # forms to look for w.r.t. first Stim
    [f1, f2, f3] = formDict[splitted_firstStim_form].split('-')
    # Pull second stim first time
    secondStim = df_stimList.sample().iloc[0,0]
    splitted_secondStim_color = secondStim.split('_')[0]
    splitted_secondStim_form = secondStim.split('_')[1].split('.')[0]
    # Check for unsimiliarity
    while splitted_secondStim_color == splitted_firstStim_color or splitted_secondStim_color == c2 or splitted_secondStim_color == c3 \
            or splitted_secondStim_form == splitted_firstStim_form or splitted_secondStim_form == f2 or splitted_secondStim_form == f3:
        # Pull second stim second time if stims are too similiar or even
        secondStim = df_stimList.sample().iloc[0,0]
        splitted_secondStim_color = secondStim.split('_')[0]
        splitted_secondStim_form = secondStim.split('_')[1].split('.')[0]

    return firstStim, secondStim

# ======================================================================================================================
# todo Working memory task (2-back)
# ======================================================================================================================
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

# ======================================================================================================================
# Create 800 trials for easy - all stimuli in consecutive trial allowed
# ======================================================================================================================
trials_easy = pd.DataFrame(index = range(800), columns = range(37))
# First stim pair ######################################################################################################
# Create stims and fieldNumbers
displays = 1
firstStim, secondStim = get_stimPair()
fieldNumberList = get_fieldNumbers()
# Set all fields to 0
trials_easy.loc[0, 1:32] = '000_000.png'
# Assign Display variable
trials_easy.iloc[0, 0] = "Display 0.1"
# Add first stim to real df
trials_easy.loc[0, fieldNumberList[0]] = firstStim
trials_easy.loc[0, fieldNumberList[1]] = secondStim
# Add random fixation cross time and after response time
fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
trials_easy.iloc[0, 33] = fixation_cross_time[0]
after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
trials_easy.iloc[0, 34] = after_response_time[0]
# Save correct answer to real df
trials_easy.loc[0, 36] = 'noResponse'
# Second stim pair #####################################################################################################
# Create stims and fieldNumbers
thirdStim, fourthStim = get_stimPair()
fieldNumberList = get_fieldNumbers()
# Set all fields to 0
trials_easy.loc[1, 1:32] = '000_000.png'
# Assign Display variable
trials_easy.iloc[1, 0] = "Display 0.1"
# Add first stim to real df
trials_easy.loc[1, fieldNumberList[0]] = firstStim
trials_easy.loc[1, fieldNumberList[1]] = secondStim
# Add random fixation cross time and after response time
fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
trials_easy.iloc[1, 33] = fixation_cross_time[0]
after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
trials_easy.iloc[1, 34] = after_response_time[0]
# Save correct answer to real df
trials_easy.loc[1, 36] = 'noResponse'
########################################################################################################################
# Fill all rows for the first 400 and second 800 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [2,400]
    else:
        rangeList = [400,800]
    # Loop through rangelist
    for i in range(rangeList[0], rangeList[1]):
        # Create stims and fieldNumbers
        fifthStim, sixthStim = get_stimPair()
        fifthStim == firstStim # Manually create match, equals also the right current response
        # Store the right stims to current index in rangelist
        fieldNumberList = get_fieldNumbers()
        print('Pair found!')
        # Set all fields to 0
        trials_easy.loc[i,0:32] = '000_000.png'
        # Assign Display variable
        trials_easy.iloc[i,0] = "Display {} WM".format(displays)
        # Add first stim to real df
        trials_easy.loc[i,fieldNumberList[0]] = fifthStim
        trials_easy.loc[i,fieldNumberList[1]] = sixthStim
        # Save correct response to real df
        trials_easy.loc[i,36] = fifthStim
        # Reallocate the stim pair order
        firstStim = thirdStim
        secondStim = fourthStim
        thirdStim = fifthStim
        fourthStim = sixthStim
        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_easy.iloc[i, 33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_easy.iloc[i, 34] = after_response_time[0]
########################################################################################################################
# Add start trials and Block Randomization
sessionSize = 40
for j in range(20):
    start = sessionSize * j
    end = sessionSize * (j+1)
    if start < 400:
        trials_easy.iloc[start, 0] = "Display 0.1"
        trials_easy.iloc[start+1, 0] = "Display 0.1"
        # Save correct answer for very first trial of a session
        trials_easy.iloc[start, 36] = 'noResponse'
        trials_easy.iloc[start+1, 36] = 'noResponse'
    else:
        trials_easy.iloc[start, 0] = "Display 0.2"
        trials_easy.iloc[start+1, 0] = "Display 0.2"
        # Save correct answer for very first trial of a session
        trials_easy.iloc[start, 36] = 'noResponse'
        trials_easy.iloc[start+1, 36] = 'noResponse'
    for i in range(len(trials_easy)):
        if i in range(start,end):
            trials_easy.iloc[i, 35] = j
# Name columns
trials_easy.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'BlockRandomisation', 'CorrectAnswer']

# Save df as spreadsheet
trials_easy.to_excel('WM_2back_trials_diffColor_diffForm.xlsx')


