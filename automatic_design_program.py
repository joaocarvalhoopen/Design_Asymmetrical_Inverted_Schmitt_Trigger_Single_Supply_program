##############################################################
#                                                            #
#                   Automatic design of an                   #
#  Asymmetrical Inverted Schmitt-Trigger with Single Supply  #
#                   for E24 resistors scale                  #
#                   with tolerance analysis                  #
#                                                            #
##############################################################
# Author:  Joao Nuno Carvalho                                #
# Date:    2019.08.30                                        #
# License: MIT Open Source License                           #
# Description: This is a simple program to make the          #
#              automatic design of an Asymmetrical Inverted  #
#              Schmitt-Trigger with Single Supply, with      #
#              resistors from E24 scale. Typically used for  #
#              1%, but in this case used for 5% or 0.1% .    #
#              The input is V_supply, V_low_threshold,       #
#              V_high_threshold and Resistor_tolerance_perc. #
#              It works by making the full search of all     #
#              combinations of values from E24 to identify   #
#              the best ones.                                #
#              In this way it speeds up immensely the manual #
#              experimentation. It also makes resistor       #
#              tolerance analysis. Please see the schematic  #
#              diagram on the GitHub page.                   #
##############################################################

#######
# Please fill the following 4 program variables to your
# specification, see schematic diagram.

# VCC voltage in volts.
VCC = 5.0
# Input Voltage low threshold in volts.  
V_low_threshold_target = 0.555
# Input Voltage high threshold in volts.  
V_high_threshold_target = 0.575
# Resistor tolerance percentage 5.0%, 1.0%, 0.1%, one of this values [5.0, 1.0, 0.1].
Resistor_tolerance_perc = 1.0


#######
# Start of program.
import math

# E24 Standard resistor series.
E24_values = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2,
              2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1,
              5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

# The scales of the resistor values so that an OpAmp circuit is stable,
# normally are between 1K and 100K, but I use a extended version from
# 100 Ohms to 1MOhms.
scales = [100, 1000, 10000, 100000]

def consistency_testing(VCC, V_low_threshold_target, V_high_threshold_target):
    passed_tests = True
    if  not ( 0 < VCC):
        print("Error in specification VCC, it has to be: 0 < VCC")
        passed_tests = False
    if  not (V_low_threshold_target < V_high_threshold_target):
        print("Error in specification, it has to be: V_low_threshold_target < V_high_threshold_target")
        passed_tests = False   
    if  not (0 <= V_low_threshold_target <= VCC):
        print("Error in specification, it has to be: 0 <= V_low_threshold_target <= VCC")
        passed_tests = False
    if  not (0 <= V_high_threshold_target <= VCC):
        print("Error in specification, it has to be: 0 <= V_high_threshold_target <= VCC")
        passed_tests = False
    if  Resistor_tolerance_perc not in [5.0, 1.0, 0.1]:
        print("Error in specification Resistor_tolerance_perc, it has to be: 5.0, 1.0 or 0.1")
        passed_tests = False
    return passed_tests
    
def expansion_of_E24_values_for_range(E24_values, scales):
    values_list = []
    for scale in scales:
        for val in E24_values:
            value = val * scale 
            values_list.append(value)
    return values_list

def calc_voltage_thresholds_for_circuit(VCC, R1, R2, R3):
    V_low_threshold  = 0.0
    V_high_threshold = 0.0

    # Calc V_low_threshold.
    R_total_low = (R2 * R3) / float((R2 + R3))
    V_low_threshold = VCC * R_total_low / float((R1 + R_total_low)) 

    # Calc V_high_threshold.
    R_total_high = (R1 * R3) / float((R1 + R3))
    V_high_threshold = VCC * R2 / float((R2 + R_total_high)) 

    return (V_low_threshold, V_high_threshold)

def calc_square_distance_error(V_low_threshold_target, V_high_threshold_target,
                               V_low_threshold_obtained, V_high_threshold_obtained):
    res = math.sqrt( math.pow(V_low_threshold_target - V_low_threshold_obtained, 2) + 
                     math.pow(V_high_threshold_target - V_high_threshold_obtained, 2) )
    return res

def full_search_of_resister_values(values_list, VCC, V_low_threshold_target, V_high_threshold_target):
    best_error = 1000000000.0
    best_V_low_threshold  = -1000.0 
    best_V_high_threshold = -1000.0
    best_R1 = -1000.0
    best_R2 = -1000.0
    best_R3 = -1000.0
    for R1 in values_list:
        for R2 in values_list:
            for R3 in values_list:
                res = calc_voltage_thresholds_for_circuit(VCC, R1, R2, R3)
                V_low_threshold_obtained, V_high_threshold_obtained = res
                error = calc_square_distance_error(V_low_threshold_target, V_high_threshold_target,
                                                   V_low_threshold_obtained, V_high_threshold_obtained)
                if error < best_error:
                    best_error = error
                    best_V_low_threshold = V_low_threshold_obtained
                    best_V_high_threshold = V_high_threshold_obtained
                    best_R1 = R1
                    best_R2 = R2
                    best_R3 = R3
                    
    return (best_error, best_V_low_threshold, best_V_high_threshold, best_R1, best_R2, best_R3)

def expand_resistor_vals_tolerance(R_val, Resistor_tolerance_perc):
    resistor_vals = []
    delta = R_val * Resistor_tolerance_perc * 0.01
    resistor_vals.append(R_val - delta)
    resistor_vals.append(R_val)
    resistor_vals.append(R_val + delta)
    return resistor_vals

def calc_absolute_distance_error(V_low_threshold_target, V_high_threshold_target,
                                 V_low_threshold_obtained, V_high_threshold_obtained):
    res = (math.fabs(V_low_threshold_target - V_low_threshold_obtained) 
            + math.fabs(V_high_threshold_target - V_high_threshold_obtained)) 
    return res

def worst_tolerance_resistor_analysis(VCC, V_low_threshold_target, V_high_threshold_target,
                             R1_nominal, R2_nominal, R3_nominal, Resistor_tolerance_perc):
    worst_error = 0.0
    worst_V_low_threshold  = 0.00000001 
    worst_V_high_threshold = 0.00000001
    R1_values = expand_resistor_vals_tolerance(R1_nominal, Resistor_tolerance_perc)
    R2_values = expand_resistor_vals_tolerance(R2_nominal, Resistor_tolerance_perc)
    R3_values = expand_resistor_vals_tolerance(R3_nominal, Resistor_tolerance_perc)
    for R1 in R1_values:
        for R2 in R2_values:
            for R3 in R3_values:
                res = calc_voltage_thresholds_for_circuit(VCC, R1, R2, R3)
                V_low_threshold_obtained, V_high_threshold_obtained = res
                error = calc_absolute_distance_error(V_low_threshold_target, V_high_threshold_target,
                                                     V_low_threshold_obtained, V_high_threshold_obtained)
                if error > worst_error:
                    worst_error = error
                    worst_V_low_threshold = V_low_threshold_obtained
                    worst_V_high_threshold = V_high_threshold_obtained
                    
    return (worst_error, worst_V_low_threshold, worst_V_high_threshold)

def main():
    print("##############################################################")
    print("#                                                            #")
    print("#                   Automatic design of an                   #")
    print("#  Asymmetrical Inverted Schmitt-Trigger with Single Supply  #")
    print("#                   for E24 resistors scale                  #")
    print("#                   with tolerance analysis                  #")
    print("#                                                            #")
    print("##############################################################")
    print("")
    print("### Specification:")
    print("VCC: ", VCC, " Volts")
    print("V_low_threshold_target:  ", V_low_threshold_target, " Volts")
    print("V_high_threshold_target: ", V_high_threshold_target, " Volts")
    print("Resistor_tolerance_perc: ", Resistor_tolerance_perc, " %")
    print("")

    passed_tests = consistency_testing(VCC, V_low_threshold_target, V_high_threshold_target)
    if passed_tests == False:
        return

    values_list = expansion_of_E24_values_for_range(E24_values, scales)
    res = full_search_of_resister_values(values_list, VCC, V_low_threshold_target, V_high_threshold_target)
    best_error, V_low_threshold_obtained, V_high_threshold_obtained, best_R1, best_R2, best_R3 = res

    print("### Solution")
    print("Best_error: ", best_error)
    print("V_low_threshold_obtained:  ", V_low_threshold_obtained, " Volts,    delta: ",
          math.fabs(V_low_threshold_target - V_low_threshold_obtained), " Volts" )
    print("V_high_threshold_obtained: ", V_high_threshold_obtained, " Volts,    delta: ",
          math.fabs(V_high_threshold_target - V_high_threshold_obtained), " Volts" )
    print("Best_R1: ", best_R1, " Ohms 1%")
    print("Best_R2: ", best_R2, " Ohms 1%")
    print("Best_R3: ", best_R3, " Ohms 1%")
    print("")

    res = worst_tolerance_resistor_analysis(VCC, V_low_threshold_target, V_high_threshold_target,
                             best_R1, best_R2, best_R3, Resistor_tolerance_perc)
    worst_error, worst_V_low_threshold_obtained, worst_V_high_threshold_obtained = res
    print("### Resistor tolerance analysis")
    print("Worst_error: ", worst_error)
    print("Worst V_low_threshold_obtained:  ", worst_V_low_threshold_obtained, " Volts,    delta: ",
          math.fabs(V_low_threshold_target - worst_V_low_threshold_obtained), " Volts" )
    print("Worst V_high_threshold_obtained: ", worst_V_high_threshold_obtained, " Volts,    delta: ",
          math.fabs(V_high_threshold_target - worst_V_high_threshold_obtained), " Volts" )


if __name__ == "__main__":
    main()


