import re
import sys

def getPlan(planFilename):
    with open(planFilename, 'r') as file:
        data = file.read()
        data = re.sub(r';.*$','', data)
        data = data.replace('\n\n','\n')
        data = data.replace('\n',',')
        return data

if __name__ == "__main__":
   
    prompt = sys.argv[1]
    planFilename = sys.argv[2]
    outfolder = sys.argv[3]
    
    csvFilename=outfolder+"bwTrainingSet.csv"
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