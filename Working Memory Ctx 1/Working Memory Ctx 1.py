import pandas as pd
import os
import random

# Direct to project file
os.getcwd()
os.chdir('./Working Memory Ctx 1')

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

# Create general stimulus pool
AllStimuli = pd.read_excel('AllStimuli.xlsx', engine='openpyxl')
# Concatenate all columns from AllStimuli into one united column
stimList = []
for iter in range(len(AllStimuli.columns)):
    currentList = AllStimuli.iloc[:, iter].tolist()
    stimList = stimList + currentList

df_stimList = pd.DataFrame(stimList)


# ======================================================================================================================
# Create 800 trials for easy - diff colors and diff forms
# ======================================================================================================================
trials_easy = pd.DataFrame(index = range(800), columns = range(37))

def nonSimiliarity(color1, color2, color3, form1, form2, form3):
    stimFound = False
    while stimFound == False:
        stim = df_stimList.sample()
        splitted_stim_color = stim.iloc[0, 0].split('_')[0]
        splitted_stim_form = stim.iloc[0, 0].split('_')[1].split('.')[0]
        if splitted_stim_color != color1 and splitted_stim_color != color2 and splitted_stim_color != color3 and \
                splitted_stim_form != form1 and splitted_stim_form != form2 and splitted_stim_form != form3:
            stimFound = True
            return stimFound, stim

# Name all empty fields 000_000.png
trials_easy.loc[0] = '000_000.png'
# Add random fixation cross time
fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
trials_easy.iloc[0, 33] = fixation_cross_time[0]
# Add random after response time
after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
trials_easy.iloc[0, 34] = after_response_time[0]

# Pull very first stim
firstStim = df_stimList.sample()
# Split information
splitted_firstStim_color = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_form = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color].split('-')
[first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form].split('-')
# Write firstStim into df
trials_easy.loc[0,16] = firstStim.iloc[0,0]

# Get second non-similiar stim
stimFound, secondStim = nonSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
# Split information
splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color].split('-')
[second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form].split('-')
# Write secondStim into df
trials_easy.loc[0,32] = firstStim.iloc[0,0]

# Fill all rows for the first 400 and second 400 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [1,400]
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
        trials_easy.loc[i] = '000_000.png'
        # Assign Display variable
        trials_easy.iloc[i, 0] = "Display {} WM Ctx1".format(displays)

        # Create subsequently connected trials
        ratioMatches = random.sample([0, 1], 1)
        if ratioMatches[0] == 0:
            diffFound = False
            while diffFound == False:
                # Create two new stims
                firstStim = df_stimList.sample()
                firstStim_currentTrial_color = firstStim.iloc[0, 0].split('_')[0]

                secondStim = df_stimList.sample()
                secondStim_currentTrial_color = secondStim.iloc[0, 0].split('_')[0]
                # Save correct answer
                trials_easy.iloc[i, 36] = 'Match'

                if firstStim_currentTrial_color == splitted_firstStim_color_memory and secondStim_currentTrial_color == splitted_secondStim_color_memory or \
                        firstStim_currentTrial_color == splitted_secondStim_color_memory and secondStim_currentTrial_color == splitted_firstStim_color_memory:
                    # Save the new found trial in memory for consecutive trial
                    splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
                    splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
                    splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors and forms to look for w.r.t. first Stim
                    [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
                    [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')
                    # colors and forms to look for w.r.t. second Stim
                    [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
                    [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
                    # Write stims into df
                    trials_easy.loc[i,fieldNumberList[0]] = firstStim.iloc[0, 0]
                    trials_easy.loc[i,fieldNumberList[1]] = secondStim.iloc[0, 0]
                    diffFound = True
                else:
                    diffFound = False

        else:
            global_stimFound = False
            while global_stimFound == False:
                # Create two new stims
                stimFound, firstStim = nonSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
                # Save the new found trial in memory for consecutive trial
                splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
                splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]

                stimFound, secondStim = nonSimiliarity(second_c1, second_c2, second_c3, second_f1, second_f2, second_f3)
                # Save the new found trial in memory for consecutive trial
                splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
                splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]

                if splitted_firstStim_color_memory != second_c1 and splitted_secondStim_color_memory != first_c1:
                    global_stimFound = True

            # colors and forms to look for w.r.t. first Stim
            [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
            [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')
            # colors and forms to look for w.r.t. second Stim
            [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
            [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
            # Save correct answer
            trials_easy.iloc[i, 36] = 'Mismatch'
            # Write stims into df
            trials_easy.loc[i, fieldNumberList[0]] = firstStim.iloc[0, 0]
            trials_easy.loc[i, fieldNumberList[1]] = secondStim.iloc[0, 0]

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
        trials_easy.iloc[start, 0] = "Display 0.1 Ctx1".format(displays)
        # Save correct answer for very first trial of a session
        trials_easy.iloc[start, 36] = 'noResponse'
    else:
        trials_easy.iloc[start, 0] = "Display 0.2 Ctx1".format(displays)
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
# # Save df as spreadsheet
trials_easy.to_excel('WM_Ctx1_trials_diffColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for normal - sim colors and diff forms
# ======================================================================================================================
trials_normal = pd.DataFrame(index = range(800), columns = range(37))

def colorSimiliarity(color1, color2, color3, form1, form2, form3):
    stimFound = False
    while stimFound == False:
        stim = df_stimList.sample()
        splitted_stim_color = stim.iloc[0, 0].split('_')[0]
        splitted_stim_form = stim.iloc[0, 0].split('_')[1].split('.')[0]
        if (splitted_stim_color != color1 or splitted_stim_color == color2 or splitted_stim_color == color3) and \
                splitted_stim_form != form1 and splitted_stim_form != form2 and splitted_stim_form != form3:
            stimFound = True
            return stimFound, stim

# Name all empty fields 000_000.png
trials_normal.loc[0] = '000_000.png'
# Add random fixation cross time
fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
trials_normal.iloc[0, 33] = fixation_cross_time[0]
# Add random after response time
after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
trials_normal.iloc[0, 34] = after_response_time[0]

# Pull very first stim
firstStim = df_stimList.sample()
# Split information
splitted_firstStim_color = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_form = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color].split('-')
[first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form].split('-')
# Write firstStim into df
trials_normal.loc[0,16] = firstStim.iloc[0,0]

# Get second non-similiar stim
stimFound, secondStim = colorSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
# Split information
splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color].split('-')
[second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form].split('-')
# Write secondStim into df
trials_normal.loc[0,32] = firstStim.iloc[0,0]

# Fill all rows for the first 400 and second 400 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [1,400]
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
        trials_normal.loc[i] = '000_000.png'
        # Assign Display variable
        trials_normal.iloc[i, 0] = "Display {} WM Ctx1".format(displays)

        # Create subsequently connected trials
        ratioMatches = random.sample([0, 1], 1)
        if ratioMatches[0] == 0:
            diffFound = False
            while diffFound == False:
                # Create two new stims
                firstStim = df_stimList.sample()
                firstStim_currentTrial_color = firstStim.iloc[0, 0].split('_')[0]

                secondStim = df_stimList.sample()
                secondStim_currentTrial_color = secondStim.iloc[0, 0].split('_')[0]
                # Save correct answer
                trials_normal.iloc[i, 36] = 'Match'

                if firstStim_currentTrial_color == splitted_firstStim_color_memory and secondStim_currentTrial_color == splitted_secondStim_color_memory or \
                        firstStim_currentTrial_color == splitted_secondStim_color_memory and secondStim_currentTrial_color == splitted_firstStim_color_memory:
                    # Save the new found trial in memory for consecutive trial
                    splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
                    splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
                    splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors and forms to look for w.r.t. first Stim
                    [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
                    [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')
                    # colors and forms to look for w.r.t. second Stim
                    [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
                    [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
                    # Write stims into df
                    trials_normal.loc[i,fieldNumberList[0]] = firstStim.iloc[0, 0]
                    trials_normal.loc[i,fieldNumberList[1]] = secondStim.iloc[0, 0]
                    diffFound = True
                else:
                    diffFound = False

        else:
            # Create two new stims
            stimFound, firstStim = colorSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
            # Save the new found trial in memory for consecutive trial
            splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
            splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
            # colors and forms to look for w.r.t. first Stim
            [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
            [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')

            stimFound, secondStim = colorSimiliarity(second_c1, second_c2, second_c3, second_f1, second_f2, second_f3)
            # Save the new found trial in memory for consecutive trial
            splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
            splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
            # colors and forms to look for w.r.t. second Stim
            [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
            [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
            # Save correct answer
            trials_normal.iloc[i, 36] = 'Mismatch'
            # Write stims into df
            trials_normal.loc[i, fieldNumberList[0]] = firstStim.iloc[0, 0]
            trials_normal.loc[i, fieldNumberList[1]] = secondStim.iloc[0, 0]

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
        trials_normal.iloc[start, 0] = "Display 0.1 Ctx1".format(displays)
        # Save correct answer for very first trial of a session
        trials_normal.iloc[start, 36] = 'noResponse'
    else:
        trials_normal.iloc[start, 0] = "Display 0.2 Ctx1".format(displays)
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
# # Save df as spreadsheet
trials_normal.to_excel('WM_Ctx1_trials_simColor_diffForm.xlsx')


# ======================================================================================================================
# Create 800 trials for hard - sim colors and sim forms
# ======================================================================================================================
trials_hard = pd.DataFrame(index = range(800), columns = range(37))

def colorAndFormSimiliarity(color1, color2, color3, form1, form2, form3):
    stimFound = False
    while stimFound == False:
        stim = df_stimList.sample()
        splitted_stim_color = stim.iloc[0, 0].split('_')[0]
        splitted_stim_form = stim.iloc[0, 0].split('_')[1].split('.')[0]
        if (splitted_stim_color != color1 or splitted_stim_color == color2 or splitted_stim_color == color3) and \
                (splitted_stim_form == form1 or splitted_stim_form == form2 or splitted_stim_form == form3):
            stimFound = True
            return stimFound, stim

# Name all empty fields 000_000.png
trials_hard.loc[0] = '000_000.png'
# Add random fixation cross time
fixation_cross_time = random.sample([100, 200, 300, 400, 500], 1)
trials_hard.iloc[0, 33] = fixation_cross_time[0]
# Add random after response time
after_response_time = random.sample([600, 700, 800, 900, 1000], 1)
trials_hard.iloc[0, 34] = after_response_time[0]

# Pull very first stim
firstStim = df_stimList.sample()
# Split information
splitted_firstStim_color = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
splitted_firstStim_form = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color].split('-')
[first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form].split('-')
# Write firstStim into df
trials_hard.loc[0,16] = firstStim.iloc[0,0]

# Get second non-similiar stim
stimFound, secondStim = colorAndFormSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
# Split information
splitted_secondStim_color = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
splitted_secondStim_form = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
# colors and forms to look for w.r.t. first Stim
[second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color].split('-')
[second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form].split('-')
# Write secondStim into df
trials_hard.loc[0,32] = firstStim.iloc[0,0]

# Fill all rows for the first 400 and second 400 (for distributing reasons on the two circles in gorilla)
for displays in range(1,3):
    if displays == 1:
        rangeList = [1,400]
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
        trials_hard.iloc[i, 0] = "Display {} WM Ctx1".format(displays)

        # Create subsequently connected trials
        ratioMatches = random.sample([0, 1], 1)
        if ratioMatches[0] == 0:
            diffFound = False
            while diffFound == False:
                # Create two new stims
                firstStim = df_stimList.sample()
                firstStim_currentTrial_color = firstStim.iloc[0, 0].split('_')[0]

                secondStim = df_stimList.sample()
                secondStim_currentTrial_color = secondStim.iloc[0, 0].split('_')[0]
                # Save correct answer
                trials_hard.iloc[i, 36] = 'Match'

                if firstStim_currentTrial_color == splitted_firstStim_color_memory and secondStim_currentTrial_color == splitted_secondStim_color_memory or \
                        firstStim_currentTrial_color == splitted_secondStim_color_memory and secondStim_currentTrial_color == splitted_firstStim_color_memory:
                    # Save the new found trial in memory for consecutive trial
                    splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
                    splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
                    splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors and forms to look for w.r.t. first Stim
                    [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
                    [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')
                    # colors and forms to look for w.r.t. second Stim
                    [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
                    [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
                    # Write stims into df
                    trials_hard.loc[i,fieldNumberList[0]] = firstStim.iloc[0, 0]
                    trials_hard.loc[i,fieldNumberList[1]] = secondStim.iloc[0, 0]
                    diffFound = True
                else:
                    diffFound = False

        else:
            diffFound = False
            while diffFound == False:
                # Create two new stims
                stimFound, firstStim = colorAndFormSimiliarity(first_c1, first_c2, first_c3, first_f1, first_f2, first_f3)
                firstStim_currentTrial_color = firstStim.iloc[0, 0].split('_')[0]

                stimFound, secondStim = colorAndFormSimiliarity(second_c1, second_c2, second_c3, second_f1, second_f2, second_f3)
                secondStim_currentTrial_color = secondStim.iloc[0, 0].split('_')[0]

                if firstStim_currentTrial_color != splitted_firstStim_color_memory and firstStim_currentTrial_color != splitted_secondStim_color_memory or \
                        secondStim_currentTrial_color != splitted_firstStim_color_memory and secondStim_currentTrial_color != splitted_secondStim_color_memory:

                    # Save the new found trial in memory for consecutive trial
                    splitted_firstStim_color_memory = firstStim.iloc[0, 0].split('_')[0]
                    splitted_firstStim_form_memory = firstStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors and forms to look for w.r.t. first Stim
                    [first_c1, first_c2, first_c3] = colorDict[splitted_firstStim_color_memory].split('-')
                    [first_f1, first_f2, first_f3] = formDict[splitted_firstStim_form_memory].split('-')

                    # Save the new found trial in memory for consecutive trial
                    splitted_secondStim_color_memory = secondStim.iloc[0, 0].split('_')[0]
                    splitted_secondStim_form_memory = secondStim.iloc[0, 0].split('_')[1].split('.')[0]
                    # colors and forms to look for w.r.t. second Stim
                    [second_c1, second_c2, second_c3] = colorDict[splitted_secondStim_color_memory].split('-')
                    [second_f1, second_f2, second_f3] = formDict[splitted_secondStim_form_memory].split('-')
                    # Save correct answer
                    trials_hard.iloc[i, 36] = 'Mismatch'
                    # Write stims into df
                    trials_hard.loc[i, fieldNumberList[0]] = firstStim.iloc[0, 0]
                    trials_hard.loc[i, fieldNumberList[1]] = secondStim.iloc[0, 0]
                    # Stop loop
                    diffFound = True

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
        trials_hard.iloc[start, 0] = "Display 0.1 Ctx1".format(displays)
        # Save correct answer for very first trial of a session
        trials_hard.iloc[start, 36] = 'noResponse'
    else:
        trials_hard.iloc[start, 0] = "Display 0.2 Ctx1".format(displays)
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
# # Save df as spreadsheet
trials_hard.to_excel('WM_Ctx1_trials_simColor_simForm.xlsx')