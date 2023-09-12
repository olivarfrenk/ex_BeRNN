import pandas as pd
import os
import random

# Direct to project file
os.getcwd()
os.chdir('./Working Memory Anti')


# ======================================================================================================================
# todo Twin memory task
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
trials_easy_preDF = pd.DataFrame(index = range(800), columns = range(2))

# Fill all rows for the first 400 and second 800 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [0,400]
    else:
        rangeList = [400,800]

    # Pull first stim
    currentStim = df_stimList.sample()
    trials_easy_preDF.loc[0, 0] = currentStim.iloc[0, 0]
    # Split information
    splitted_currentStim_color = currentStim.iloc[0, 0].split('_')[0]
    splitted_currentStim_form = currentStim.iloc[0, 0].split('_')[1].split('.')[0]
    # colors to look for w.r.t. first Stim
    [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
    # forms to look for w.r.t. first Stim
    [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')

    # Start loop trough rangelist
    for i in range(rangeList[0],rangeList[1]):
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

        # Name all empty fields 000_000.png
        trials_easy.loc[i] = '000_000.png'
        # Assign Display variable
        trials_easy.iloc[i, 0] = "Display {} WM Anti".format(displays)
        # Add first stim to real df
        trials_easy.loc[i, fieldNumberList[0]] = trials_easy_preDF.loc[i, 0]

        # randomly choose a stim from general stimulus pool
        stimFound = False
        while stimFound == False:
            currentStim = df_stimList.sample()
            splitted_currentStim_color = currentStim.iloc[0, 0].split('_')[0]
            splitted_currentStim_form = currentStim.iloc[0, 0].split('_')[1].split('.')[0]
            if i == 0:
                if splitted_currentStim_color != c1 and splitted_currentStim_color != c2 and splitted_currentStim_color != c3 and\
                        splitted_currentStim_form != f1 and splitted_currentStim_form != f2 and splitted_currentStim_form != f3:
                    # add stim to trial df
                    trials_easy.loc[i,fieldNumberList[1]] = currentStim.iloc[0,0]
                    trials_easy_preDF.loc[i,1] = currentStim.iloc[0,0]
                    # Save correct answer to real df
                    trials_easy.loc[i, 36] = trials_easy_preDF.loc[i, 1]
                    # check for consecutive trial
                    if i != len(trials_easy_preDF)-1:
                        trials_easy_preDF.loc[i+1,0] = currentStim.iloc[0,0]

                        # colors to look for w.r.t. first Stim
                        [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                        # forms to look for w.r.t. first Stim
                        [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                        stimFound = True
                    else:
                        # colors to look for w.r.t. first Stim
                        [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                        # forms to look for w.r.t. first Stim
                        [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                        stimFound = True
                else:
                    stimFound = False
            else:
                if currentStim.iloc[0,0] != trials_easy_preDF.loc[i,0] and currentStim.iloc[0,0] != trials_easy_preDF.loc[i-1,0] and \
                        splitted_currentStim_color != c1 and splitted_currentStim_color != c2 and splitted_currentStim_color != c3 and \
                        splitted_currentStim_form != f1 and splitted_currentStim_form != f2 and splitted_currentStim_form != f3:
                    # add stim to trial df
                    trials_easy.loc[i,fieldNumberList[1]] = currentStim.iloc[0,0]
                    trials_easy_preDF.loc[i,1] = currentStim.iloc[0,0]
                    # Save correct answer to real df
                    trials_easy.loc[i, 36] = trials_easy_preDF.loc[i, 1]
                    # check for consecutive trial
                    if i != len(trials_easy_preDF)-1:
                        trials_easy_preDF.loc[i+1,0] = currentStim.iloc[0,0]
                        # Save correct answer to real df
                        trials_easy.loc[i, 36] = trials_easy_preDF.loc[i, 1]

                        # colors to look for w.r.t. first Stim
                        [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                        # forms to look for w.r.t. first Stim
                        [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                        stimFound = True
                    else:
                        # Save correct answer to real df
                        trials_easy.loc[i, 36] = trials_easy_preDF.loc[i, 1]

                        # colors to look for w.r.t. first Stim
                        [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                        # forms to look for w.r.t. first Stim
                        [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                        stimFound = True
                else:
                    stimFound = False

            # Add random fixation cross time
            fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
            trials_easy.iloc[i, 33] = fixation_cross_time[0]
            # Add random after response time
            after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
            trials_easy.iloc[i, 34] = after_response_time[0]

# Add Block Randomization
sessionSize = 40
for j in range(20):
    start = sessionSize * j
    end = sessionSize * (j+1)
    if start < 400:
        trials_easy.iloc[start, 0] = "Display 0.1".format(displays)
        # Save correct answer for very first trial of a session
        trials_easy.iloc[start, 36] = 'noResponse'
    else:
        trials_easy.iloc[start, 0] = "Display 0.2".format(displays)
        # Save correct answer for very first trial of a session
        trials_easy.iloc[start, 36] = 'noResponse'
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
trials_easy.to_excel('WM_Anti_trials_diffColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for normal - Only similiar colors in consecutive trials
# ======================================================================================================================
trials_normal = pd.DataFrame(index = range(800), columns = range(37))
trials_normal_preDF = pd.DataFrame(index = range(800), columns = range(2))

def assignFunc_color(color1, color2, color3, form1, form2, form3):
    if (splitted_currentStim_color == color1 and splitted_previousStim_form != splitted_currentStim_form or splitted_currentStim_color == color2 \
        or splitted_currentStim_color == color3) and splitted_currentStim_form != form1 and splitted_currentStim_form != form2 and\
            splitted_currentStim_form != form3:
        # append
        trials_normal.loc[i, fieldNumberList[1]] = currentStim.iloc[0, 0]
        trials_normal_preDF.loc[i, 1] = currentStim.iloc[0, 0]
        # Save correct answer to real df
        trials_normal.loc[i, 36] = trials_normal_preDF.loc[i, 1]

        if i != len(trials_normal) - 1:
            trials_normal_preDF.loc[i + 1, 0] = currentStim.iloc[0, 0]

        stimFound = True
        return stimFound

    else:
        stimFound = False
        return stimFound

# Allocate first previous stim
previousStim = df_stimList.sample().iloc[0, 0]
trials_normal_preDF.loc[0,0] = previousStim
# split it up for comparison
splitted_previousStim_color = previousStim.split('_')[0]
splitted_previousStim_form = previousStim.split('_')[1].split('.')[0]

# Fill all rows for the first 100 and second 100 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [0,400]
    else:
        rangeList = [400,800]

    # Start loop trough rangelist
    for i in range(rangeList[0], rangeList[1]):
        fieldFound = False
        while fieldFound == False:
            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = random.sample([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32], 2)
            else:
                fieldNumberList = random.sample([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31], 2)
            # Check that each stimulus position is at least five fields away from each other
            if abs(fieldNumberList[0] - fieldNumberList[1]) >= 6 and abs(
                    fieldNumberList[1] - fieldNumberList[0]) <= 26:
                fieldFound = True

        # Name all empty fields 000_000.png
        trials_normal.loc[i] = '000_000.png'
        # Assign Display variable
        trials_normal.iloc[i, 0] = "Display {} WM Anti".format(displays)
        # Add first stim to real df
        trials_normal.loc[i, fieldNumberList[0]] = trials_normal_preDF.loc[i, 0]

        # colors to look for w.r.t. first Stim
        previousStim_color_colorDict = colorDict[splitted_previousStim_color]
        [c1, c2, c3] = previousStim_color_colorDict.split('-')
        # forms to look for w.r.t. first Stim
        previousStim_form_formDict = formDict[splitted_previousStim_form]
        [f1, f2, f3] = previousStim_form_formDict.split('-')

        # while loop until the right stimuli w.r.t. to the previous stim was found
        stimFound = False
        while stimFound == False:
            # randomly choose a stim from general stimulus pool
            currentStim = df_stimList.sample()
            # split it up for comparison
            string_currentStim = currentStim.iloc[0, 0]
            splitted_currentStim_color = string_currentStim.split('_')[0]
            splitted_currentStim_form = string_currentStim.split('_')[1].split('.')[0]

            if i == 0:
                stimFound = assignFunc_color(c1, c2, c3, f1, f2, f3)
            elif currentStim.iloc[0,0] != trials_normal_preDF.loc[i-1,0]:
                stimFound = assignFunc_color(c1, c2, c3, f1, f2, f3)

        # the current stim is the previous for the next iteration in the for loop
        previousStim = trials_normal_preDF.loc[i, 1]
        # split it up for comparison
        splitted_previousStim_color = previousStim.split('_')[0]
        splitted_previousStim_form = previousStim.split('_')[1].split('.')[0]

        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_normal.iloc[i, 33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_normal.iloc[i, 34] = after_response_time[0]

# Add Block Randomization
sessionSize = 40
for j in range(20):
    start = sessionSize * j
    end = sessionSize * (j+1)
    if start < 400:
        trials_normal.iloc[start, 0] = "Display 0.1".format(displays)
        # Save correct answer for very first trial of a session
        trials_normal.iloc[start, 36] = 'noResponse'
    else:
        trials_normal.iloc[start, 0] = "Display 0.2".format(displays)
        # Save correct answer for very first trial of a session
        trials_normal.iloc[start, 36] = 'noResponse'
    for i in range(len(trials_normal)):
        if i in range(start,end):
            trials_normal.iloc[i, 35] = j
# Name columns
trials_normal.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'BlockRandomisation', 'CorrectAnswer']
# Save df as spreadsheet
trials_normal.to_excel('WM_Anti_trials_simColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for hard - Only similiar colors and forms in consecutive trials
# ======================================================================================================================
# Create empty trials hard df
trials_hard = pd.DataFrame(index = range(800), columns = range(37))
trials_hard_preDF = pd.DataFrame(index = range(800), columns = range(2))

# Define functions
def assignFunc_form(form1, form2, form3, iter):
    if splitted_currentStim_form == form1 or splitted_currentStim_form == form2 or splitted_currentStim_form == form3:
        # add sampled stim to trial df
        trials_hard.loc[iter, fieldNumberList[1]] = currentStim.iloc[0, 0]
        trials_hard_preDF.loc[iter, 1] = currentStim.iloc[0, 0]
        # Save correct answer to real df
        trials_hard.loc[iter, 36] = trials_hard_preDF.loc[iter, 1]
        # check for consecutive trial
        if iter != len(trials_hard) - 1:
            trials_hard_preDF.loc[iter + 1, 0] = currentStim.iloc[0, 0]
        # Interrupt while loop
        stimFound = True
        return stimFound

    else:
        stimFound = False
        return stimFound

def assignFunc_color(color1, color2, color3, form1, form2, form3, i):
    if splitted_currentStim_color == color1 or splitted_currentStim_color == color2 or splitted_currentStim_color == color3:

        stimFound = assignFunc_form(form1, form2, form3, i)
        return stimFound

    else:
        stimFound = False
        return stimFound

# Allocate first previous stim
previousStim = df_stimList.sample().iloc[0, 0]
trials_hard_preDF.loc[0,0] = previousStim
# split it up for comparison
splitted_previousStim_color = previousStim.split('_')[0]
splitted_previousStim_form = previousStim.split('_')[1].split('.')[0]

for displays in range(1,3):
    if displays == 1:
        rangeList = [0,400]
    else:
        rangeList = [400,800]

    # Start loop trough rangelist
    for i in range(rangeList[0], rangeList[1]):
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

        # Name all empty fields 000_000.png
        trials_hard.loc[i] = '000_000.png'
        # Assign Display variable
        trials_hard.iloc[i, 0] = "Display {} WM Anti".format(displays)
        # Add first stim to real df
        trials_hard.loc[i, fieldNumberList[0]] = trials_hard_preDF.loc[i, 0]

        # colors to look for w.r.t. previous Stim
        outPrevious_colorDict = colorDict[splitted_previousStim_color]
        [c1, c2, c3] = outPrevious_colorDict.split('-')
        # forms to look for w.r.t. previous Stim
        outPrevious_formDict = formDict[splitted_previousStim_form]
        [f1, f2, f3] = outPrevious_formDict.split('-')

        # .. until right stim according to the previous stim conditions was found
        stimFound = False
        while stimFound == False:
            # randomly choose a stim from general stimulus pool
            currentStim = df_stimList.sample()
            # split it up for comparison
            splitted_currentStim_color = currentStim.iloc[0,0].split('_')[0]
            splitted_currentStim_form = currentStim.iloc[0,0].split('_')[1].split('.')[0]

            # Apply function for finding right consecutive stimulus
            if i == 0 and currentStim.iloc[0,0] != trials_hard_preDF.loc[i,0]:
                stimFound = assignFunc_color(c1, c2, c3, f1, f2, f3, i)
            elif currentStim.iloc[0,0] != trials_hard_preDF.loc[i,0]:
                stimFound = assignFunc_color(c1, c2, c3, f1, f2, f3, i)

        # At the end allocate previous stim for next for loop
        previousStim = trials_hard_preDF.iloc[i, 1]
        # split it up for comparison
        splitted_previousStim_color = previousStim.split('_')[0]
        splitted_previousStim_form = previousStim.split('_')[1].split('.')[0]

        # Add random fixation cross time
        fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
        trials_hard.iloc[i, 33] = fixation_cross_time[0]
        # Add random after response time
        after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
        trials_hard.iloc[i, 34] = after_response_time[0]

# Add Block Randomization
sessionSize = 40
for j in range(20):
    start = sessionSize * j
    end = sessionSize * (j+1)
    if start < 400:
        trials_hard.iloc[start, 0] = "Display 0.1".format(displays)
        # Save correct answer for very first trial of a session
        trials_hard.iloc[start, 36] = 'noResponse'
    else:
        trials_hard.iloc[start, 0] = "Display 0.2".format(displays)
        # Save correct answer for very first trial of a session
        trials_hard.iloc[start, 36] = 'noResponse'
    for i in range(len(trials_hard)):
        if i in range(start,end):
            trials_hard.iloc[i, 35] = j
# Name columns
trials_hard.columns = ['display', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7',
                     'Field 8', 'Field 9', \
                     'Field 10', 'Field 11', 'Field 12', 'Field 13', 'Field 14', 'Field 15', 'Field 16',
                     'Field 17', 'Field 18', 'Field 19', \
                     'Field 20', 'Field 21', 'Field 22', 'Field 23', 'Field 24', 'Field 25', 'Field 26',
                     'Field 27', 'Field 28', 'Field 29', \
                     'Field 30', 'Field 31', 'Field 32', 'FixationCrossTime', 'AfterResponseTime',
                     'BlockRandomisation', 'CorrectAnswer']
# Save df as spreadsheet
trials_hard.to_excel('WM_Anti_trials_simColor_simForm.xlsx')


