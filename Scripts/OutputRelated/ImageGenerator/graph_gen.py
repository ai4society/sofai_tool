#
# This Python File generates the graphs with the solutions from the raw output files
#
# Run it with "python3 graph_gen.py Time Input".

import os
import re
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import functools
import glob
import math

acceptable_corr = 1.0

def getVarFromLine(line,varname):

#    print("Cond is </"+varname+">")
    if "</"+varname+">" in line:
        line = re.sub(r'.*</'+varname+'>([^<]+)</>.*',r'\1', line)
        return line.strip()
    return ''

def calculate_optimality(planLen,optLen,cor):
    
    #print(f"Plan len is {planLen} while optimal len is {optLen}",end="")

    planLen = int(planLen)
    optLen = int(optLen)

    if optLen == -1 or planLen == -1 or (float(cor) < acceptable_corr):
        #print(f" Optimality is {-1}")
        return -1

    diff = float(planLen-optLen)
    optimality = (diff / optLen)*100.0

    #print(f" Optimality is {optimality}")
    return optimality

def sol_reader(filename,rootFilename,suffix,domain_list):
    
    guard = False
    with open(filename) as myfile:
        for line in myfile:
            domain = getVarFromLine(line,"dmn")
            if domain in domain_list:
                guard = True
                break

    if guard:
        modfilename = rootFilename+'.csv'  # /home/user/somefile.jpg
        found_names = {}

        with open(modfilename, 'w') as f:
            print(f"Name,Time-{suffix},Corr-{suffix},Opt-{suffix},Sys-{suffix},Planner-{suffix}",file=f)
            with open(filename) as myfile:
                for line in myfile:
                    domain = getVarFromLine(line,"dmn")
                    if domain in domain_list:
                        problem = getVarFromLine(line,"pro")
                        
                        if (problem != ''):

                            #problem = getVarFromLine(line,"dmn") +"_"+ problem

                            if re.match(r"problem\_\d+\_\d+\_\d+\_\d+", problem):
                                problem = "gripper" + problem     
                            elif re.match(r"problem\_\d+\_\d\d\d", problem):
                                problem = "hanoi" + problem            
                            elif re.match(r"problem\_\d+\_\d+", problem):
                                problem = "zBW" + problem 

                            if problem in found_names.keys():
                                found_names[problem] = found_names[problem]+1
                            else:
                                found_names[problem] = 0

                            problem = problem + f"__{found_names[problem]}"

                            time = float(getVarFromLine(line,"sot")[:-1])
                            #time = float(getVarFromLine(line,"tim")[:-1])
                            if "could not be solved" in line or (float(getVarFromLine(line,"cor")) < acceptable_corr):
                                if "could not be solved" in line:
                                    cor = "0"
                                else:
                                    cor = getVarFromLine(line,"cor")
                                sys = "-1"
                                pla = "-1"
                                opt = "-1"
                            else:
                                cor = getVarFromLine(line,"cor")
                                sys = getVarFromLine(line,"sys")
                                pla = getVarFromLine(line,"pla")
                                planLen = getVarFromLine(line,"sollenght")
                                optLen = getVarFromLine(line,"optlen")
                                opt = calculate_optimality(planLen,optLen,cor)
                            time = time * 1000.00
                            print(f"{problem},{str(time)},{str(cor)},{str(opt)},{str(sys)},{str(pla)}",file=f)
                                #sys.exit()
            myfile.close()


        mydata = ['Name',f'Time-{suffix}',f'Corr-{suffix}',f'Opt-{suffix}',f'Sys-{suffix}',f'Planner-{suffix}']
        columns = mydata
        sort_order = mydata
        # Read a CSV file
        df = pd.read_csv(modfilename, usecols=columns)
        # sorting according to multiple columns
        df.sort_values(sort_order, ascending=True,inplace=True,na_position='first')
        df[f'Sys-{suffix}'] = df[f'Sys-{suffix}'].astype('Int64')
        df[f'Planner-{suffix}'] = df[f'Planner-{suffix}'].astype('Int64')
        df.to_csv(modfilename, index=False)
        return True
    else:
        return False

def loopPrintLaTeX(line,narg,tableFile):
    for i in range(narg):
        print(line,file=tableFile,end="")

def loopPrintLaTeXArray(line_before,endline,endSequence,array,tableFile):
    for elem in array[:-1]:
        print(line_before + str(elem),file=tableFile,end=endline)
    print(line_before + str(array[-1]),file=tableFile,end=endSequence)
    

if __name__ == '__main__':

    domain_separate = False
    tot_domain_list = ['blocksworld-4ops', 'ferry', 'hanoi', 'gripper-strips', 'miconic', 'driverlog', 'rocket']
    #tot_domain_list = [ 'ferry', 'hanoi', 'gripper-strips', 'miconic', 'driverlog']
    tot_domain_list = ['briefcase']

    domain_list = []
    iter_domain = 0

    while iter_domain < len(tot_domain_list):
        if domain_separate:
            domain_list.clear()
            domain_list.append(tot_domain_list[iter_domain])
        else:
            domain_list = tot_domain_list
            iter_domain = len(tot_domain_list)


        plotting_val = sys.argv[1]
        print(f"Plotting value is \"{plotting_val}\"")

        inputFolder = sys.argv[2]
        solutionfilesExt=".sol"

        narg = len(glob.glob1(inputFolder,f"*{solutionfilesExt}"))
        # list to store files
        solFiles = []
        # Iterate directory
        for file in os.listdir(inputFolder):
            # check only text files
            if file.endswith(f"{solutionfilesExt}"):
                solFiles.append(f"{inputFolder}/{file}")

            solFiles.sort()
        print("Files to analize are: " +  str(solFiles))


        filenames = []
        rootFilenames = []
        modfilenames = []
        dataFrames=[]
        suffixes=[]
        count = 0
        decrease_n_arg = 0
        while count < narg:
            temp = solFiles[count]
            tmp_filename = temp
            tmp_rootFilename = (os.path.splitext(temp)[0])
            tmp_suffix = (os.path.basename(tmp_rootFilename))
            print("Temp is " +  str(temp))
            if(sol_reader(tmp_filename,tmp_rootFilename,tmp_suffix,domain_list)):
                filenames.append(temp)
                rootFilenames.append(os.path.splitext(temp)[0])
                suffixes.append(os.path.basename(rootFilenames[count]))
                modfilenames.append(rootFilenames[count]+'.csv')
                dataFrames.append(pd.read_csv(modfilenames[count]).reset_index(drop=True))
                path, rootFilenames[count] = os.path.split(rootFilenames[count])
            else:
                decrease_n_arg +=1
            count += 1

        narg = narg - decrease_n_arg
        if narg <= 0:
            sys.exit()
        merged_df = functools.reduce(lambda left, right: pd.merge(left,right,on='Name'), dataFrames)

        merged_path="Output/Merged/"
        Path(merged_path).mkdir(parents=True,exist_ok=True)
        
        merged_name = merged_path+"merged.csv"
        merged_df.to_csv(merged_name, encoding='utf-8', index=False)



        plt.rcParams["figure.figsize"] = [14.00, 8.00]
        plt.rcParams["figure.autolayout"] = True
        # Make a list of columns

        # mydata = ["Fast Downward",'SOFAIxPlansformers','SOFAIxPlanning', 'Jaccard']

        mydata=[]
        for elem in suffixes:
            mydata.append(plotting_val+'-'+elem)

        columns = mydata

        styles = ['o', 'x', '^', 'h' , 'D']

        df = pd.read_csv(merged_name, usecols=columns)

        if plotting_val == "Time":
            df[columns] = df[columns] / 1000

        # Plot the lines
        df.plot(y=columns, style=styles, figsize=(12,4),color=['limegreen','tab:blue','tab:orange','tab:red','black',])
        #plt.title(plotting_val + " comparsion between Fast and Slow Arch. and FD", weight='bold')
        # label the x and y axes
        plt.xlabel('Instances', weight='bold', size='large')
        if plotting_val == "Time":
            plt.ylabel(plotting_val + (" (s)"), weight='bold', size='large')
        else:
            plt.ylabel(plotting_val, weight='bold', size='large')
        #plt.legend(['Jac','Plf','SOFAIxPlanning','FD'])

        #n_inst = 100
        #plt.axvspan(0, 99, color='red', alpha=0.2)
        #plt.axvspan(100, 199, color='green', alpha=0.2)
        #plt.axvspan(200, 299, color='yellow', alpha=0.2)
        #plt.axvspan(300, 399, color='blue', alpha=0.2)
        #plt.axvspan(400, 499, color='orange', alpha=0.2)

        plt.legend(prop={'size': 18})
        plt.legend(labels=suffixes)
        #plt.xlim(1, 240)
        #plt.ylim(1, 900000)

        #plt.yscale('log')
        if domain_separate:
            plt.savefig("Output/"+plotting_val+f"_{domain_list[0]}"+"-Plot.png")
        else:
            plt.savefig("Output/"+plotting_val+"-Plot.png")



        nRows = len(df)+1
        countCases = 0
        col_numbers = 5
        merged_name_formula = merged_path+"merged_formulae.csv"
        
        for suffix in suffixes:
            merged_df[f'Sys-{suffix}'] = merged_df[f'Sys-{suffix}'].astype('Int64')
            merged_df[f'Planner-{suffix}'] = merged_df[f'Planner-{suffix}'].astype('Int64')  
                
        merged_df.to_csv(merged_name_formula, encoding='utf-8', index=False)
        chrOrd = ord('A')
        extraChar = ''
        formula_row = "\"=SUBTOTAL(3,"+chr(chrOrd)+"2:"+chr(chrOrd)+str(nRows) +")\","
        chrOrd+=1
        internal_counter = 0
        extraCounter=0
        while countCases < narg:
            if internal_counter < 3:
                formula_row += "\"=SUBTOTAL(1,"+extraChar+chr(chrOrd)+"2:"+extraChar+chr(chrOrd)+str(nRows) +")\","
                internal_counter+=1
                if chrOrd<90:
                    chrOrd+=1
                else:
                    chrOrd = ord('A')
                    extraChar = chr(ord('A')+extraCounter)
                    extraCounter+=1
            
            elif internal_counter == 3:
                formula_row += "\"=COUNTIF("+extraChar+chr(chrOrd)+"2:"+extraChar+chr(chrOrd)+str(nRows) +",1)\""
                internal_counter+=1
                if chrOrd<90:
                    chrOrd+=1
                else:
                    chrOrd = ord('A')
                    extraChar = chr(ord('A')+extraCounter)
                    extraCounter+=1
                    
            elif internal_counter == 4:
                formula_row += "," #For Empty column -- Type of system 2 does not have an aggregate
                internal_counter=0
                if chrOrd<90:
                    chrOrd+=1
                else:
                    chrOrd = ord('A')
                    extraChar = chr(ord('A')+extraCounter)
                    extraCounter+=1
            
                if countCases < narg:
                    formula_row += ","
                else:
                    formula_row += "\n"
                
                countCases+=1

        f = open(merged_name_formula, "a")
        f.write(formula_row)
        f.close()

        #Create LaTeX Table
        if domain_separate:
            extension="5"
            table_path="Output/Table_"+f"{domain_list[0]}/"
            table_filename = "table_"+f"{domain_list[0]}{extension}.tex"
        else:
            table_path="Output/Table/"
            table_filename = "table.tex"


        Path(table_path).mkdir(parents=True,exist_ok=True)

        with open(table_path+table_filename, "w") as tableFile:
            #Preamble
            print('\\documentclass[12pt,a4paper]{standalone}\n\\usepackage{hhline}\n\\usepackage{tabularx}\n\\usepackage[table]{xcolor}\n\\definecolor{lightgray}{gray}{0.9}\n\\begin{document}',file=tableFile)
            
            #Tabular declaration
            print('\t\\begin{tabular}{||l',file=tableFile,end="")
            loopPrintLaTeX('|c',narg,tableFile)
            print('||}',file=tableFile)

            #Approaches row
            print('\t\t\\hhline{~|t:',file=tableFile,end="")
            loopPrintLaTeX('=',narg,tableFile)
            print(':t|}',file=tableFile)
            print("\t\t\\multicolumn{1}{c||}{} & \multicolumn{1}{c|}", file=tableFile,end="")
            loopPrintLaTeXArray("{\\texttt{","}} & ","}}\\\\\n",suffixes,tableFile)
            print('\t\t\\hhline{|t:=:b:',file=tableFile,end="")
            loopPrintLaTeX('=',narg,tableFile)
            print(':t}',file=tableFile)

            #Number of plans Section

            solved_plans_stats = []
            correct_plans_stats = []
            partial_plans_stats = []
            partial_plansArr = []
            max_solved_plans = -1
            index_max = []
            count_plans = 0
            nInstances = nRows-1
            dictValues = {}
            for suff in suffixes:
                
                dictValues.clear()
                dictValues = merged_df[f'Corr-{suff}'].value_counts().to_dict()

                if 0.0 in dictValues.keys():
                    failed_plans = dictValues[0.0]
                else:
                    failed_plans = 0

                if 1.0 in dictValues.keys():
                    correct_plans = dictValues[1.0]
                else:
                    correct_plans = 0


                solved_plans = nInstances - failed_plans
                partial_plans = solved_plans - correct_plans

                if solved_plans > max_solved_plans:
                    max_solved_plans = solved_plans
                    index_max.clear()
                    index_max.append(count_plans)
                elif solved_plans == max_solved_plans:
                    index_max.append(count_plans)

                solved_plans_stats.append(f"{solved_plans} ({(solved_plans / nInstances)*100.0:.2f}\%)")
                correct_plans_stats.append(f"{correct_plans} ({(correct_plans / nInstances)*100.0:.2f}\%)")
                partial_plans_stats.append(f"{partial_plans} ({(partial_plans / nInstances)*100.0:.2f}\%)")
                partial_plansArr.append(partial_plans)

                count_plans += 1

            for c in index_max:
                solved_plans_stats[c] = "\\textbf{"+solved_plans_stats[c]+"}"



            optimalPlans=[]
            maxOptimal=0
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] < 1].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)

                tmp_optimal = cleaned_df[f'Sys-{suff}'].count()
                if tmp_optimal > maxOptimal:
                    maxOptimal = tmp_optimal

                optimalPlans.append(tmp_optimal)
            
            


            print("\t\t%Number of Plans", file=tableFile)
            print("\t\tPlans & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",solved_plans_stats,tableFile)


            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            #print("\t\t\\quad Complete & ", file=tableFile,end="")
            #loopPrintLaTeXArray(""," & ","\\\\\n",correct_plans_stats,tableFile)

            #print('\t\t\\hhline{||',file=tableFile,end="")
            #loopPrintLaTeX('-',narg+1,tableFile)
            #print('||}',file=tableFile)

            #print("\t\t\\quad Partial & ", file=tableFile,end="")
            #loopPrintLaTeXArray(""," & ","\\\\\n",partial_plans_stats,tableFile)

            print("\t\t\\rowcolor{lightgray}\\quad Optimal & ", file=tableFile,end="")
            optimalPlans_print = []
            for elem in optimalPlans:
                if elem > 0:
                    if elem == maxOptimal:
                        optimalPlans_print.append("\\textbf{" + f"{elem} ({(elem / nInstances)*100.0:.2f}\%)" + "}")
                    else:
                        optimalPlans_print.append(f"{elem} ({(elem / nInstances)*100.0:.2f}\%)")

                else:
                    optimalPlans_print.append(f"0 (0.00\%)")

            loopPrintLaTeXArray(""," & ","\\\\\n",optimalPlans_print,tableFile)

            print('\t\t\\hhline{|:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':|}',file=tableFile)

            #S1 Plans
            sys1PlansArr = []
            sys1PlanClean = []
            sys2PlansArr = []
            sys2PlanClean = []

            for suff in suffixes:
                dictValues = merged_df[f'Sys-{suff}'].value_counts().to_dict()

            
                if -1 in dictValues.keys():
                    failedPlans = dictValues[-1]
                else:
                    failedPlans = 0

                if 1 in dictValues.keys():
                    sys1Plans = dictValues[1]
                else:
                    sys1Plans = 0

                if 2 in dictValues.keys():
                    sys2Plans = dictValues[2]
                else:
                    sys2Plans = 0

                sys1PlansArr.append(f"{sys1Plans} ({(sys1Plans / nInstances)*100.0:.2f}\%)")
                sys1PlanClean.append(sys1Plans)
                sys2PlansArr.append(f"{sys2Plans} ({(sys2Plans / nInstances)*100.0:.2f}\%)")
                sys2PlanClean.append(sys2Plans)


            print("\t\t\\texttt{S1} Plans & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",sys1PlansArr,tableFile)

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)



            sys1_completePlans = []
            c = 0
            while c in range(len(partial_plansArr)):
                sys1_completePlans.append(int(sys1PlanClean[c])-int(partial_plansArr[c]))
                c+=1

            #print("\t\t\\quad Complete & ", file=tableFile,end="")
            
            #sys1_complete_stats = []
            #for elem in sys1_completePlans:
            #    sys1_complete_stats.append(f"{elem} ({(elem / nInstances)*100.0:.2f}\%)")
            #loopPrintLaTeXArray(""," & ","\\\\\n",sys1_complete_stats,tableFile)

            #print('\t\t\\hhline{||',file=tableFile,end="")
            #loopPrintLaTeX('-',narg+1,tableFile)
            #print('||}',file=tableFile)

            #print("\t\t\\quad Partial & ", file=tableFile,end="")
            #sys1_partial_stats = []
            #for elem in partial_plansArr:
            #    sys1_partial_stats.append(f"{elem} ({(elem / nInstances)*100.0:.2f}\%)")
            #loopPrintLaTeXArray(""," & ","\\\\\n",sys1_partial_stats,tableFile)


            #print('\t\t\\hhline{||',file=tableFile,end="")
            #loopPrintLaTeX('-',narg+1,tableFile)
            #print('||}',file=tableFile)


            sys1_optimalPlans=[]
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] != 1].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)

                sys1_optimalPlans.append(cleaned_df[f'Sys-{suff}'].count())
            
            print("\t\t\\rowcolor{lightgray}\\quad Optimal & ", file=tableFile,end="")
            sys1_optimalPlans_print = []
            countOpt=0
            for elem in sys1_optimalPlans:
                if elem > 0:
                    sys1_optimalPlans_print.append(f"{elem} ({(elem / float(sys1PlanClean[countOpt]))*100.0:.2f}\%)")
                else:
                    sys1_optimalPlans_print.append(f"0 (0.00\%)")

                countOpt+=1
            loopPrintLaTeXArray(""," & ","\\\\\n",sys1_optimalPlans_print,tableFile)

            print('\t\t\\hhline{|:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':|}',file=tableFile)


            print("\t\t\\texttt{S2} Plans & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",sys2PlansArr,tableFile)

            sys2_optimalPlans=[]
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Planner-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] != 2].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)
                sys2_optimalPlans.append(cleaned_df[f'Sys-{suff}'].count())

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\t\\rowcolor{lightgray}\\quad Optimal & ", file=tableFile,end="")
            sys2_optimalPlans_print = []
            optCount=0
            for elem in sys2_optimalPlans:
                if elem > 0 and float(sys2PlanClean[optCount]) > 0:
                    sys2_optimalPlans_print.append(f"{elem} ({(elem / sys2PlanClean[optCount])*100.0:.2f}\%)")
                else:
                    sys2_optimalPlans_print.append(f"0 (0.00\%)")
                optCount+=1

            loopPrintLaTeXArray(""," & ","\\\\\n",sys2_optimalPlans_print,tableFile)


            FD_uses = []
            FD_uses_clean =[]
            LPG_uses = []
            LPG_uses_clean =[]
            PFLPG_uses = []
            PFLPG_uses_clean =[]

            dictValues.clear()
            for suff in suffixes:
        
                df_Sys2_cleaned = merged_df
                df_Sys2_cleaned = df_Sys2_cleaned[ (df_Sys2_cleaned[f'Sys-{suff}'] == 2) ]
                dictValues = df_Sys2_cleaned[f'Planner-{suff}'].value_counts().to_dict()
            
                if 1 in dictValues.keys():
                    fdPlans = dictValues[1]
                else:
                    fdPlans = 0

                if 2 in dictValues.keys():
                    lpgPlans = dictValues[2]
                else:
                    lpgPlans = 0

                if 3 in dictValues.keys():
                    pfLpgPlans = dictValues[3]
                else:
                    pfLpgPlans = 0

                FD_uses.append(f"{fdPlans} ({(fdPlans / nInstances)*100.0:.2f}\%)")
                FD_uses_clean.append(float(fdPlans))
                LPG_uses.append(f"{lpgPlans} ({(lpgPlans / nInstances)*100.0:.2f}\%)")
                LPG_uses_clean.append(float(lpgPlans))
                PFLPG_uses.append(f"{pfLpgPlans} ({(pfLpgPlans / nInstances)*100.0:.2f}\%)")
                PFLPG_uses_clean.append(float(pfLpgPlans))

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\\quad FD & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",FD_uses,tableFile)

            FD_optimalPlans=[]
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Planner-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] != 2].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Planner-{suff}'] != 1].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)
                FD_optimalPlans.append(cleaned_df[f'Sys-{suff}'].count())

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\t\\rowcolor{lightgray}\\quad\\quad Optimal & ", file=tableFile,end="")
            fd_optimalPlans_print = []
            optCount=0
            for elem in FD_optimalPlans:
                if elem > 0 and float(FD_uses_clean[optCount]) > 0:
                    fd_optimalPlans_print.append(f"{elem} ({(elem / FD_uses_clean[optCount])*100.0:.2f}\%)")
                else:
                    fd_optimalPlans_print.append(f"0 (0.00\%)")
                optCount+=1

            loopPrintLaTeXArray(""," & ","\\\\\n",fd_optimalPlans_print,tableFile)

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\\quad LPG & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",LPG_uses,tableFile)

            LPG_optimalPlans=[]
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Planner-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] != 2].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Planner-{suff}'] != 2].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)
                LPG_optimalPlans.append(cleaned_df[f'Sys-{suff}'].count())

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\t\\rowcolor{lightgray}\\quad\\quad Optimal & ", file=tableFile,end="")
            lpg_optimalPlans_print = []
            optCount=0
            for elem in LPG_optimalPlans:
                if elem > 0 and float(LPG_uses_clean[optCount]) > 0:
                    lpg_optimalPlans_print.append(f"{elem} ({(elem / LPG_uses_clean[optCount])*100.0:.2f}\%)")
                else:
                    lpg_optimalPlans_print.append(f"0 (0.00\%)")
                optCount+=1
            loopPrintLaTeXArray(""," & ","\\\\\n",lpg_optimalPlans_print,tableFile)


            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\\quad PF + LPG & ", file=tableFile,end="")
            loopPrintLaTeXArray(""," & ","\\\\\n",PFLPG_uses,tableFile)


            PFLPG_optimalPlans=[]
            for suff in suffixes:
                cleaned_df = merged_df[[f'Sys-{suff}',f'Planner-{suff}',f'Opt-{suff}']]
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Sys-{suff}'] != 2].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Planner-{suff}'] != 3].index)
                cleaned_df = cleaned_df.drop(cleaned_df[cleaned_df[f'Opt-{suff}'] > 0].index)
                PFLPG_optimalPlans.append(cleaned_df[f'Sys-{suff}'].count())

            print('\t\t\\hhline{||',file=tableFile,end="")
            loopPrintLaTeX('-',narg+1,tableFile)
            print('||}',file=tableFile)

            print("\t\t\t\\rowcolor{lightgray}\\quad\\quad Optimal & ", file=tableFile,end="")
            pflpg_optimalPlans_print = []
            optCount=0
            for elem in PFLPG_optimalPlans:
                if elem > 0 and float(PFLPG_uses_clean[optCount]) > 0:
                    pflpg_optimalPlans_print.append(f"{elem} ({(elem / PFLPG_uses_clean[optCount])*100.0:.2f}\%)")
                else:
                    pflpg_optimalPlans_print.append(f"0 (0.00\%)")
                optCount+=1
            loopPrintLaTeXArray(""," & ","\\\\\n",pflpg_optimalPlans_print,tableFile)

            print('\t\t\\hhline{|:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':|}',file=tableFile)



            print("\t\tTime (avg) & ", file=tableFile,end="")
            timeArr = []
            minTime = sys.maxsize
            index_min = []
            count_time = 0
            for suff in suffixes:
                timeAvg = merged_df[f'Time-{suff}'].mean()/1000


                if timeAvg < minTime:
                    minTime = timeAvg
                    index_min.clear()
                    index_min.append(count_time)
                elif minTime == timeAvg:
                    index_min.append(count_time)
                count_time +=1

                timeArr.append(f"{timeAvg:.3f}s")

            for c in index_min:
                timeArr[c] = "\\textbf{"+timeArr[c]+"}"
            loopPrintLaTeXArray(""," & ","\\\\\n",timeArr,tableFile)

            print('\t\t\\hhline{|:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':|}',file=tableFile)


            print("\t\tCorrectness (avg) & ", file=tableFile,end="")
            corrArr = []
            maxCorr = -1
            index_max = []
            count_corr = 0
            for suff in suffixes:
                corrAvg = merged_df[f'Corr-{suff}'].mean()

                if corrAvg > maxCorr:
                    maxCorr = corrAvg
                    index_max.clear()
                    index_max.append(count_corr)
                elif minTime == maxCorr:
                    index_max.append(count_corr)
                count_corr +=1

                corrArr.append(f"{corrAvg:.3f}")

            for c in index_max:
                corrArr[c] = "\\textbf{"+corrArr[c]+"}"
            loopPrintLaTeXArray(""," & ","\\\\\n",corrArr,tableFile)

            print('\t\t\\hhline{|:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':|}',file=tableFile)



            print("\t\tOptimality (avg) & ", file=tableFile,end="")
        


            df_cleaned = merged_df
          #  for suff in suffixes:
          #      df_cleaned = df_cleaned[ (df_cleaned[f'Opt-{suff}'] >= 0) ]
            


            optArr = []
            minOpt = sys.maxsize
            index_min = []
            count_opt = 0
            for suff in suffixes:
                optAvg = df_cleaned[f'Opt-{suff}'].mean()

                if optAvg < minOpt:
                    minOpt = optAvg
                    index_min.clear()
                    index_min.append(count_opt)
                elif minOpt == optAvg:
                    index_max.append(count_opt)
                
                count_opt +=1
            
                
                if math.isnan(optAvg):
                    optArr.append(f"-")
                else:
                    optArr.append(f"+{optAvg:.2f}\%")

            for c in index_min:
                optArr[c] = "\\textbf{"+optArr[c]+"}"
            loopPrintLaTeXArray(""," & ","\\\\\n",optArr,tableFile)

            print('\t\t\\hhline{|b:',file=tableFile,end="")
            loopPrintLaTeX('=',narg+1,tableFile)
            print(':b|}',file=tableFile)


            print('\t\\end{tabular}\n\\end{document}',file=tableFile)


        with open(table_path+table_filename, 'r') as file:
            data = file.read()
            data = data.replace("_", "\\_")
            data = data.replace("0 (0.00\%)", "--")


        with open(table_path+table_filename, 'w') as file:
            file.write(data)
    
        iter_domain+=1
