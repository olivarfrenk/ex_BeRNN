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
trials_easy_preDF = pd.DataFrame(index = range(800), columns = range(3))

# Fill all rows for the four displays
for displays in range(1,5):
    if displays == 1:
        rangeList = [0,200]
    elif displays == 2:
        rangeList = [200,400]
    elif displays == 3:
        rangeList = [400,600]
    else:
        rangeList = [600,800]

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
                fieldNumberList = random.sample([2, 6, 10, 14, 18, 22, 26, 30], 3)
            elif displays == 2:
                fieldNumberList = random.sample([1, 5, 9, 13, 17, 21, 25, 29], 3)
            elif displays == 3:
                fieldNumberList = random.sample([4, 8, 12, 16, 20, 24, 28, 32], 3)
            else:
                fieldNumberList = random.sample([3, 7, 11, 15, 19, 23, 27, 31], 3)

            # Check that each stimulus position is at least five fields away from each other
            if abs(fieldNumberList[0] - fieldNumberList[1]) >= 6 and abs(fieldNumberList[0] - fieldNumberList[2]) >= 6 and \
                    abs(fieldNumberList[1] - fieldNumberList[2]) >= 6 and abs(fieldNumberList[1] - fieldNumberList[0]) <= 26 and \
                    abs(fieldNumberList[2] - fieldNumberList[0]) <= 26 and abs(fieldNumberList[2] - fieldNumberList[1]) <= 26:
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
            firstCurrentStim = df_stimList.sample()
            splitted_currentStim_color = firstCurrentStim.iloc[0, 0].split('_')[0]
            splitted_currentStim_form = firstCurrentStim.iloc[0, 0].split('_')[1].split('.')[0]
            if i == 0:
                if splitted_currentStim_color != c1 and splitted_currentStim_color != c2 and splitted_currentStim_color != c3 and\
                        splitted_currentStim_form != f1 and splitted_currentStim_form != f2 and splitted_currentStim_form != f3:
                    # add stim to trial df
                    trials_easy.loc[i,fieldNumberList[1]] = firstCurrentStim.iloc[0,0]
                    trials_easy_preDF.loc[i,1] = firstCurrentStim.iloc[0,0]
                    # save for next trial
                    trials_easy_preDF.loc[i+1,0] = firstCurrentStim.iloc[0,0]
                    # Second Stim --------------------------------------------------------------------------------------------------
                    # randomly choose a stim from general stimulus pool
                    secondCurrentStim = df_stimList.sample()
                    splitted_currentStim_color = secondCurrentStim.iloc[0, 0].split('_')[0]
                    splitted_currentStim_form = secondCurrentStim.iloc[0, 0].split('_')[1].split('.')[0]
                    if firstCurrentStim.iloc[0, 0] != secondCurrentStim.iloc[0, 0] and \
                            splitted_currentStim_color != c1 and splitted_currentStim_color != c2 and splitted_currentStim_color != c3 and \
                            splitted_currentStim_form != f1 and splitted_currentStim_form != f2 and splitted_currentStim_form != f3:
                        # add stim to trial df
                        trials_easy.loc[i, fieldNumberList[2]] = secondCurrentStim.iloc[0, 0]
                        trials_easy_preDF.loc[i, 2] = secondCurrentStim.iloc[0, 0]
                        # Save for next trial
                        trials_easy_preDF.loc[i + 1, 1] = secondCurrentStim.iloc[0, 0]
                        # colors to look for w.r.t. first Stim
                        [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                        # forms to look for w.r.t. first Stim
                        [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                        stimFound = True
                    else:
                        stimFound = False
                else:
                    stimFound = False

            else:
                if firstCurrentStim.iloc[0,0] != trials_easy_preDF.loc[i-1,0] and firstCurrentStim.iloc[0,0] != trials_easy_preDF.loc[i-1,1] and\
                    splitted_currentStim_color != c1 and splitted_currentStim_color != c2 and splitted_currentStim_color != c3 and \
                    splitted_currentStim_form != f1 and splitted_currentStim_form != f2 and splitted_currentStim_form != f3:
                    # add stim to trial df
                    trials_easy.loc[i,fieldNumberList[2]] = firstCurrentStim.iloc[0,0]
                    trials_easy_preDF.loc[i,2] = firstCurrentStim.iloc[0,0]
                    # colors to look for on next iteration w.r.t. first Stim
                    [c1, c2, c3] = colorDict[splitted_currentStim_color].split('-')
                    # forms to look for on next iteration w.r.t. first Stim
                    [f1, f2, f3] = formDict[splitted_currentStim_form].split('-')
                    # Save correct answer to real df
                    trials_easy.loc[i, 36] = trials_easy_preDF.loc[i, 2]

                    # Allocate the two stims from previous trial
                    trials_easy.loc[i, fieldNumberList[0]] = trials_easy_preDF.loc[i,0]
                    trials_easy.loc[i, fieldNumberList[1]] = trials_easy_preDF.loc[i,1]
                    # check for consecutive trial
                    if i != len(trials_easy_preDF)-1:
                        trials_easy_preDF.loc[i + 1,0] = trials_easy_preDF.loc[i, 1]
                        trials_easy_preDF.loc[i+1,1] = trials_easy_preDF.loc[i, 2]
                        stimFound = True
                    else:
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
    # Save correct answer for very first trial of a session
    trials_easy.iloc[start, 36] = 'noResponse'
    # Give 3 seconds preperation time for first trial
    trials_easy.iloc[start, 33] = 3000
    if start < 200:
        trials_easy.iloc[start, 0] = "Display 0.1 Anti".format(displays)
    elif start >= 200 and start < 400:
        trials_easy.iloc[start, 0] = "Display 0.2 Anti".format(displays)
    elif start >= 400 and start < 600:
        trials_easy.iloc[start, 0] = "Display 0.3 Anti".format(displays)
    else:
        trials_easy.iloc[start, 0] = "Display 0.4 Anti".format(displays)
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
trials_easy.to_excel('WM_Anti_trials_3stim_diffColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for normal - Only similiar colors in consecutive trials
# ======================================================================================================================
trials_normal = pd.DataFrame(index = range(800), columns = range(37))
trials_normal_preDF = pd.DataFrame(index = range(800), columns = range(3))

def assignFunc_color(color1, color2, color3, form1, form2, form3, fieldNumber, currentStim):
    if (splitted_currentStim_color == color1 and splitted_previousStim_form != splitted_currentStim_form or splitted_currentStim_color == color2 \
        or splitted_currentStim_color == color3) and splitted_currentStim_form != form1 and splitted_currentStim_form != form2 and\
            splitted_currentStim_form != form3:
        # append
        trials_normal.loc[i, fieldNumberList[fieldNumber]] = currentStim.iloc[0, 0]
        trials_normal_preDF.loc[i, fieldNumber] = currentStim.iloc[0, 0]
        # Save correct answer to real df
        trials_normal.loc[i, 36] = trials_normal_preDF.loc[i, fieldNumber]

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
for displays in range(1,5):
    if displays == 1:
        rangeList = [0,200]
    elif displays == 2:
        rangeList = [200,400]
    elif displays == 3:
        rangeList = [400,600]
    else:
        rangeList = [600,800]

    # Start loop trough rangelist
    for i in range(rangeList[0], rangeList[1]):
        fieldFound = False
        while fieldFound == False:
            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = random.sample([2, 6, 10, 14, 18, 22, 26, 30], 3)
            elif displays == 2:
                fieldNumberList = random.sample([1, 5, 9, 13, 17, 21, 25, 29], 3)
            elif displays == 3:
                fieldNumberList = random.sample([4, 8, 12, 16, 20, 24, 28, 32], 3)
            else:
                fieldNumberList = random.sample([3, 7, 11, 15, 19, 23, 27, 31], 3)

            # Check that each stimulus position is at least five fields away from each other
            if abs(fieldNumberList[0] - fieldNumberList[1]) >= 6 and abs(fieldNumberList[0] - fieldNumberList[2]) >= 6 and \
                    abs(fieldNumberList[1] - fieldNumberList[2]) >= 6 and abs(fieldNumberList[1] - fieldNumberList[0]) <= 26 and \
                    abs(fieldNumberList[2] - fieldNumberList[0]) <= 26 and abs(fieldNumberList[2] - fieldNumberList[1]) <= 26:
                fieldFound = True

        # Name all empty fields 000_000.png
        trials_normal.loc[i] = '000_000.png'
        # Assign Display variable
        trials_normal.iloc[i, 0] = "Display {} WM Anti".format(displays)
        # Add first stim to real df
        trials_normal.loc[i, fieldNumberList[0]] = previousStim
        # # Save correct answer to real df
        # trials_normal.loc[i, 36] = trials_normal_preDF.loc[i, 0]

        # colors to look for w.r.t. first Stim
        previousStim_color_colorDict = colorDict[splitted_previousStim_color]
        [c1, c2, c3] = previousStim_color_colorDict.split('-')
        # forms to look for w.r.t. first Stim
        previousStim_form_formDict = formDict[splitted_previousStim_form]
        [f1, f2, f3] = previousStim_form_formDict.split('-')

        # while loop until the right stimuli w.r.t. to the previous stim was found
        stimFound1 = False
        stimFound2 = False
        while stimFound1 == False or stimFound2 == False:

            # randomly choose a stim from general stimulus pool
            firstCurrentStim = df_stimList.sample()
            # split it up for comparison
            splitted_currentStim_color = firstCurrentStim.iloc[0, 0].split('_')[0]
            splitted_currentStim_form = firstCurrentStim.iloc[0, 0].split('_')[1].split('.')[0]
            if i == 0:
                stimFound1 = assignFunc_color(c1, c2, c3, f1, f2, f3, 1, firstCurrentStim)
            elif firstCurrentStim.iloc[0,0] != trials_normal_preDF.loc[i-1,1] and \
                    firstCurrentStim.iloc[0,0] != trials_normal_preDF.loc[i-1,2]:
                stimFound1 = assignFunc_color(c1, c2, c3, f1, f2, f3, 2, firstCurrentStim)
                trials_normal.loc[i, fieldNumberList[1]] = trials_normal_preDF.loc[i-1,2]

            # randomly choose a stim from general stimulus pool
            secondCurrentStim = df_stimList.sample()
            if firstCurrentStim.iloc[0,0] != secondCurrentStim.iloc[0,0]:
                # split it up for comparison
                string_currentStim = secondCurrentStim.iloc[0, 0]
                splitted_currentStim_color = string_currentStim.split('_')[0]
                splitted_currentStim_form = string_currentStim.split('_')[1].split('.')[0]
                if i == 0:
                    stimFound2 = assignFunc_color(c1, c2, c3, f1, f2, f3, 2, secondCurrentStim)
                else:
                    stimFound2 = True
            else:
                stimFound2 = False

        # Allocate stims for next iteration, if not at the end of df
        if i != len(trials_normal_preDF) - 1:
            previousStim = trials_normal_preDF.loc[i, 1]
            trials_normal_preDF.loc[i+1, 0] = trials_normal_preDF.loc[i, 1]
            trials_normal_preDF.loc[i+1, 1] = trials_normal_preDF.loc[i, 2]

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
    # Save correct answer for very first trial of a session
    trials_normal.iloc[start, 36] = 'noResponse'
    # Give 3 seconds preperation time for first trial
    trials_normal.iloc[start, 33] = 3000
    if start < 200:
        trials_normal.iloc[start, 0] = "Display 0.1 Anti".format(displays)
    elif start >= 200 and start < 400:
        trials_normal.iloc[start, 0] = "Display 0.2 Anti".format(displays)
    elif start >= 400 and start < 600:
        trials_normal.iloc[start, 0] = "Display 0.3 Anti".format(displays)
    else:
        trials_normal.iloc[start, 0] = "Display 0.4 Anti".format(displays)
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
trials_normal.to_excel('WM_Anti_trials_3stim_simColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for hard - Only similiar colors and forms in consecutive trials
# ======================================================================================================================
trials_hard = pd.DataFrame(index = range(800), columns = range(37))
trials_hard_preDF = pd.DataFrame(index = range(800), columns = range(3))

def assignFunc_form(form1, form2, form3, iter, fieldNumber, currentStim):
    if splitted_currentStim_form == form1 or splitted_currentStim_form == form2 or splitted_currentStim_form == form3:
        # add sampled stim to trial df
        trials_hard.loc[iter, fieldNumberList[fieldNumber]] = currentStim.iloc[0, 0]
        trials_hard_preDF.loc[iter, fieldNumber] = currentStim.iloc[0, 0]
        # check for consecutive trial
        if iter != len(trials_hard) - 1:
            trials_hard_preDF.loc[iter + 1, 0] = currentStim.iloc[0, 0]
        # Interrupt while loop
        stimFound = True
        return stimFound

    else:
        stimFound = False
        return stimFound

def assignFunc_color(color1, color2, color3, form1, form2, form3, i, fieldNumber, currentStim):
    if splitted_currentStim_color == color1 or splitted_currentStim_color == color2 or splitted_currentStim_color == color3:

        stimFound = assignFunc_form(form1, form2, form3, i, fieldNumber, currentStim)
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

# Fill all rows for the first 100 and second 100 (for distributing reasons on the two circles in gorilla)
for displays in range(1,5):
    if displays == 1:
        rangeList = [0,200]
    elif displays == 2:
        rangeList = [200,400]
    elif displays == 3:
        rangeList = [400,600]
    else:
        rangeList = [600,800]

    # Start loop trough rangelist
    for i in range(rangeList[0], rangeList[1]):
        fieldFound = False
        while fieldFound == False:
            # Sample a random number for every stimulus per trial for assigning them to their field in experiment space
            if displays == 1:
                fieldNumberList = random.sample([2, 6, 10, 14, 18, 22, 26, 30], 3)
            elif displays == 2:
                fieldNumberList = random.sample([1, 5, 9, 13, 17, 21, 25, 29], 3)
            elif displays == 3:
                fieldNumberList = random.sample([4, 8, 12, 16, 20, 24, 28, 32], 3)
            else:
                fieldNumberList = random.sample([3, 7, 11, 15, 19, 23, 27, 31], 3)

            # Check that each stimulus position is at least five fields away from each other
            if abs(fieldNumberList[0] - fieldNumberList[1]) >= 6 and abs(fieldNumberList[0] - fieldNumberList[2]) >= 6 and \
                    abs(fieldNumberList[1] - fieldNumberList[2]) >= 6 and abs(fieldNumberList[1] - fieldNumberList[0]) <= 26 and \
                    abs(fieldNumberList[2] - fieldNumberList[0]) <= 26 and abs(fieldNumberList[2] - fieldNumberList[1]) <= 26:
                fieldFound = True

        # Name all empty fields 000_000.png
        trials_hard.loc[i] = '000_000.png'
        # Assign Display variable
        trials_hard.iloc[i, 0] = "Display {} WM Anti".format(displays)
        # Add first stim to real df
        trials_hard.loc[i, fieldNumberList[0]] = previousStim

        # colors to look for w.r.t. first Stim
        previousStim_color_colorDict = colorDict[splitted_previousStim_color]
        [c1, c2, c3] = previousStim_color_colorDict.split('-')
        # forms to look for w.r.t. first Stim
        previousStim_form_formDict = formDict[splitted_previousStim_form]
        [f1, f2, f3] = previousStim_form_formDict.split('-')

        # while loop until the right stimuli w.r.t. to the previous stim was found
        stimFound1 = False
        stimFound2 = False
        while stimFound1 == False or stimFound2 == False:

            # randomly choose a stim from general stimulus pool
            firstCurrentStim = df_stimList.sample()
            # split it up for comparison
            splitted_currentStim_color = firstCurrentStim.iloc[0, 0].split('_')[0]
            splitted_currentStim_form = firstCurrentStim.iloc[0, 0].split('_')[1].split('.')[0]
            if i == 0:
                stimFound1 = assignFunc_color(c1, c2, c3, f1, f2, f3,i, 1, firstCurrentStim)
            elif firstCurrentStim.iloc[0,0] != trials_hard_preDF.loc[i-1,1] and \
                    firstCurrentStim.iloc[0,0] != trials_hard_preDF.loc[i-1,2]:
                stimFound1 = assignFunc_color(c1, c2, c3, f1, f2, f3,i, 2, firstCurrentStim)
                trials_hard.loc[i, fieldNumberList[1]] = trials_hard_preDF.loc[i - 1, 2]
                # Save correct answer to real df
                trials_hard.loc[i, 36] = trials_hard_preDF.loc[i, 2]

            # randomly choose a stim from general stimulus pool
            secondCurrentStim = df_stimList.sample()
            if firstCurrentStim.iloc[0,0] != secondCurrentStim.iloc[0,0]:
                # split it up for comparison
                string_currentStim = secondCurrentStim.iloc[0, 0]
                splitted_currentStim_color = string_currentStim.split('_')[0]
                splitted_currentStim_form = string_currentStim.split('_')[1].split('.')[0]
                if i == 0:
                    stimFound2 = assignFunc_color(c1, c2, c3, f1, f2, f3,i, 2, secondCurrentStim)
                else:
                    stimFound2 = True
            else:
                stimFound2 = False

        # Allocate stims for next iteration, if not at the end of df
        if i != len(trials_hard_preDF) - 1:
            previousStim = trials_hard_preDF.loc[i, 1]
            trials_hard_preDF.loc[i+1, 0] = trials_hard_preDF.loc[i, 1]
            trials_hard_preDF.loc[i+1, 1] = trials_hard_preDF.loc[i, 2]

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
    # Save correct answer for very first trial of a session
    trials_hard.iloc[start, 36] = 'noResponse'
    # Give 3 seconds preperation time for first trial
    trials_hard.iloc[start, 33] = 3000
    if start < 200:
        trials_hard.iloc[start, 0] = "Display 0.1 Anti".format(displays)
    elif start >= 200 and start < 400:
        trials_hard.iloc[start, 0] = "Display 0.2 Anti".format(displays)
    elif start >= 400 and start < 600:
        trials_hard.iloc[start, 0] = "Display 0.3 Anti".format(displays)
    else:
        trials_hard.iloc[start, 0] = "Display 0.4 Anti".format(displays)
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
trials_hard.to_excel('WM_Anti_trials_3stim_simColor_simForm.xlsx')



