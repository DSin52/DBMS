
import pandas as pd

paper_graph = {}
def readCitationFile(path):
    with open(path,'r') as file:
        for line in file:
            paper = line.split(' ')
            paper1 = str(paper[0])
            paper2 = str(paper[1])
            if paper1 in paper_graph:
                paper_graph[paper1]['cited'].append(paper2)
            else:
                paper_graph[paper1] = {'cited':[paper2]}


def readSLACFile(path):
    with open(path, 'r') as file:
        for line in file:
            token = line.split(' ')
            paper = str(token[0])
            date = str(token[1])

pd.DataFrame