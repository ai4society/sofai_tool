import re
import sys

def getPlan(planFilename):
    with open(planFilename) as file:
        for line in file:
            if "(:solution" in line:
                return re.sub(r'.*\(:solution (.*)\).*',r'\1', line)


if __name__ == "__main__":
   
    prompt = sys.argv[1]
    planFilename = sys.argv[2]
    outfolder = sys.argv[3]
    
    csvFilename=outfolder+"rocketTrainingSet.csv"
    prompt = prompt.replace('\n',' ')
    

    with open(csvFilename,'a+') as f:
        f.write(f'\"{prompt}\", \"{getPlan(planFilename)}\"')
    
    with open(csvFilename, 'r') as file:
        data = file.read()
        data = data.replace(',\"','\"')
        data = data.replace('\"\"','\"\n\"')
        data = data.replace('(','')
        data = data.replace(')','')

    with open(csvFilename,'w') as f:
        f.write(data)