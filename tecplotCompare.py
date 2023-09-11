import pandas as pd

file_path_main = './plots/smallestJet2.tec'
file_path_ref = './plots/nojet.tec'
new_file_path = './plots/smallestJet2_modified.tec'


with open(file_path_main, 'r') as mainFile, open(file_path_ref, 'r') as refFile, open(new_file_path, 'w') as modified:
    # Writing the first and modified second lines to the new file
    first_line = mainFile.readline().strip()
    variables_line = mainFile.readline().strip()
    third_line = mainFile.readline().strip()
    refFile.readline()
    refFile.readline()
    refFile.readline()


    preview_lines = [first_line, variables_line, third_line]

    variables = variables_line.split('"')[1::2]  # Extracting the variable names
    press_column_index = variables.index("Press")
    Rho_column_index = variables.index("Rho  ")
    MA_column_index = variables.index("Ma   ")

    # Step 3: Preparing the modified second line to include "NEWVAR"
    modified_second_line = variables_line.strip() + ',      "rho_dif",      "Ma_dif,      "Pa_dif"'

    modified.write(first_line + '\n')
    modified.write(modified_second_line + '\n')
    modified.write(third_line + '\n')
    
    # Iterate through the remaining lines
    for line1, line2 in zip(mainFile, refFile):
        stripped_lineMain = line1.strip()
        stripped_lineRef = line2.strip()
        # If line starts with "ZONE", copy it as-is
        if stripped_lineMain.startswith("ZONE"):
            modified.write(stripped_lineMain + '\n')
        else:
            # Split the line into individual values
            mainValues = stripped_lineMain.split()
            refValues = stripped_lineRef.split()
            ratio_pressure_percent = abs((float(mainValues[press_column_index]) - float(refValues[press_column_index])) / ((float(refValues[press_column_index]) + float(mainValues[press_column_index]) +1/100000000000)/2)*100)
            ratio_Rho_percent = abs((float(mainValues[Rho_column_index]) - float(refValues[Rho_column_index])) / ((float(refValues[Rho_column_index]) + float(mainValues[Rho_column_index]) +1/100000000000)/2)*100)
            ratio_Ma_percent = abs((float(mainValues[MA_column_index]) - float(refValues[MA_column_index])) / ((float(refValues[MA_column_index]) + float(mainValues[MA_column_index]) +1/100000000000)/2)*100)
            # Add the value for "NEWVAR" column and join them back
            rho_dif = 1
            ma_dif = 2
            modified_line = '\t'.join(mainValues + ["{:.6E}".format(ratio_Rho_percent)] + ["{:.6E}".format(ratio_Ma_percent)] + ["{:.6E}".format(ratio_pressure_percent)]) + '\n'
            modified.write(modified_line)

new_file_path