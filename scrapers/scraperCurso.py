from lxml import html
import requests

url1 = "https://siga.ufrj.br/sira/repositorio-curriculo/80167CF7-3880-478C-8293-8E7D80CEDEBE.html"




def getListasDisciplinas(urls):
    l = []
    
    for url in urls:
        l.append(requests.get(url))
        
    return l

def getLinks(link):
    response =  requests.get(link)
    tree = html.fromstring(response.content)
    
    aElementList = tree.cssselect('body > table >  tr > td > table > tr > td > table > tr > td > a')
    l = []
    for element  in aElementList:
        
        if (('9999/9') in element.text):
            href =  element.get('href')
            linkDisciplina = 'https://siga.ufrj.br'+href.split('(\'')[-1].split('\')')[0]
            l.append(linkDisciplina.replace('temas/zire/frameConsultas.jsp?mainPage=/',''))
    return l
    
def getPageDisciplinaFromLink(linkCurso):
    response = requests.get(linkCurso)
    tree = html.fromstring(response.content)    
    link = 'https://siga.ufrj.br/sira/repositorio-curriculo/' +  tree.cssselect('#frameDynamic')[0].get('src')
    print(link)
    return requests.get(link).content



def getCodigoCurso(pageString):
    tree = html.fromstring(pageString)
    codElement = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(2) > td:nth-child(4)')[0]
    return codElement.text
  
def getNomeCurso(pageString):
    tree = html.fromstring(pageString)
    element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b')[0]
    return element.text
  
def getPeriodos(pageString):
    tree = html.fromstring(pageString)
    element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2)')[0]
    return element.text
  
  
  
def getAnoCurriculo(pageString):
    tree = html.fromstring(pageString)
    element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr.tableTitleBlue > td > center > b ')[0]
    return element.text.split('alunos de ')[1].split(' a ')[0].split('/')[0]

def getPeriodosMaximo(pageString):
    tree = html.fromstring(pageString)
    element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue2 > td:nth-child(2)')[0]
    return element.text.split(' ')[0]


def getDuracaoMinima(pageString):
    tree = html.fromstring(pageString)
    element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2) > table > tr > td > nobr')[0]
    return element.text.split(':')[1]

def getSituacao(pageString):
    tree = html.fromstring(pageString)
    element  =tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(4) > td:nth-child(2) > table > tr.tableBodyBlue2 > td:nth-child(2) >nobr')[0]
    return element.text

