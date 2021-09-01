from lxml import html
import requests


def getListasDisciplinas(urls):
    l = []
    
    for url in urls:
        l.append(requests.get(url))
        
    return l

def getLinks(link):
    print('Pegando Links dos cursos na pagina da graduacao')
    response =  requests.get(link)
    tree = html.fromstring(response.content)
    
    aElementList = tree.cssselect('body > table >  tr > td > table > tr > td > table > tr > td > a')
    l = []
    
    for element  in aElementList:
        
        if (('9999/9') in element.text):
            href =  element.get('href')
            linkCurso = 'https://siga.ufrj.br'+href.split('(\'')[-1].split('\')')[0]
            linkCurso=  linkCurso.replace('temas/zire/frameConsultas.jsp?mainPage=/','')
            print('Url Curso  = ' + linkCurso )
            l.append(linkCurso)
    
    print('Encontrados ',len(l),' cursos.')
    return l
    
def getPageCursoFromLink(linkCurso):
    print ('Extraindo html curso')
    response = requests.get(linkCurso)
    tree = html.fromstring(response.content)    
    link = 'https://siga.ufrj.br/sira/repositorio-curriculo/' +  tree.cssselect('#frameDynamic')[0].get('src')
    print(link)
    return requests.get(link).content



def getCodigoCurso(pageString):
    tree = html.fromstring(pageString)
    codElement = ''
    elements = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(2) > td:nth-child(4)')

    if (len(elements)> 0):
        codElement = elements[0] 
        print ('Codigo Curso: ', codElement.text)
        return codElement.text

    elements = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(4)')

    if (len(elements)> 0):
        codElement = elements[0] 
        print ('Codigo Curso: ', codElement.text)
        return codElement.text
    print ('Codigo Curso Nao Achado ')
    return ''

def getSituacao(pageString):
    tree = html.fromstring(pageString)
    elements  =tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(4) > td:nth-child(2) > table > tr.tableBodyBlue2 > td:nth-child(2) >nobr')
    situacao = ''
    
    if(len(elements)>0):
        situacao =  elements[0].text
    
    elements  =tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody >   tr:nth-child(5) > td:nth-child(2) > table > tr.tableBodyBlue2 > td:nth-child(2) >nobr')
    
    if(len(elements)>0):
        situacao =  elements[0].text
    
    
    print('Situacao: ', situacao)
    return situacao
    



def getNomeCurso(pageString):
    tree = html.fromstring(pageString)
    element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b')[0]
    nomeCurso = element.text.replace('Curso de Graduação em ','')
    print('Nome Curso: ',nomeCurso)
    return nomeCurso
  
def getPeriodos(pageString):
    tree = html.fromstring(pageString)
    elements = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2)')
    duracao = ''
    element = None
    
    if (len(elements)> 0):
        element = elements[0]

        duracao = element.text.split(' ')[0]
    else:
        elements = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2)')
        element = elements[0]
        duracao =  element.text.split(' ')[0]
        
    print('Duracao Recomendada: ',duracao )
    
   
    return duracao
  
  
  
  
def getAnoCurriculo(pageString):
    tree = html.fromstring(pageString)
    try:
        element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr.tableTitleBlue > td > center > b ')[0]
    except:
        element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitleBlue > td > center > b ')[0]
    
    print('Ano Curriculo: ', element.text.split('alunos de ')[1].split(' a ')[0].split('/')[0])
    return element.text.split('alunos de ')[1].split(' a ')[0].split('/')[0]

def getPeriodosMaximo(pageString):
    tree = html.fromstring(pageString)
    try:
        element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue2 > td:nth-child(2)')[0]
    except:
        element = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody >  tr:nth-child(4) > td:nth-child(1) > table > tr.tableBodyBlue2 > td:nth-child(2)')[0]
        
    print('Duracao Maxima: ' ,element.text)
  
    return element.text.split(' ')[0]


def getDuracaoMinima(pageString):
    tree = html.fromstring(pageString)
    try:
        element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr.tableTitle > td > center > b > tr:nth-child(3) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2) > table > tr > td > nobr')[0]
    except:
        element  = tree.cssselect('body > table > tbody > tr:nth-child(1) > td > table > tr > td > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tr.tableBodyBlue1 > td:nth-child(2) > table > tr > td > nobr')[0]
    
    
    
    
    print('Duracao Minima: ', element.text.split(':')[1], ' anos.')
    return element.text.split(':')[1]


page = getPageCursoFromLink(getLinks('https://siga.ufrj.br/sira/repositorio-curriculo/80167CF7-3880-478C-8293-8E7D80CEDEBE.html')[1])


# element = tree.cssselect('body > table > tbody > tr > td > table')
# el.cssselect('tr.tableTitle > td > center > b')

def getTabelas(pageString): # iterar entre segundo e penultimo
    tree = html.fromstring(pageString)
    elements  =tree.cssselect('body > table > tbody > tr > td > table')
    return elements
 
def getCabecalhoTabelaDisciplinas(tableElement):
    cabecalho = tableElement.cssselect('tr.tableTitle > td > center > b')[0].text
    print (cabecalho) 
    return cabecalho

def getLinhas(tableElement):
    return tableElement.cssselect('tr')


def getInformacoesDisciplina(linhas):
    print('Parseando linhas')    
    for i in range (3,len(linhas)-1):
       
        if(len(linhas[i].cssselect('td > a'))==0):
               
            break
            
        print('Linha: ', html.tostring(linhas[i]) )
        codigo = linhas[i].cssselect('td > a')[0].text.strip()
        print ('Codigo: ',codigo )        
        nome = linhas[i].cssselect('td')[1].text
        print ('Nome: ',nome)
        creditos = linhas[i].cssselect('td')[2].text
        print ('Creditos: ',creditos)
        cargaTeorica = linhas[i].cssselect('td')[3].text
        print ('Carga Teorica: ',cargaTeorica)
        cargaPratica = linhas[i].cssselect('td')[4].text
        print ('Carga Pratica: ',cargaPratica)
        requisitos = linhas[i].cssselect('td')[6].text.strip()
        print ('Requisitos: ', requisitos)    

def main():

    urlInicial = "https://siga.ufrj.br/sira/repositorio-curriculo/80167CF7-3880-478C-8293-8E7D80CEDEBE.html"
    linksCursos = getLinks(urlInicial)
    atual = 1
    
    for i in range(len(linksCursos)):
        
        link = linksCursos[i]
        print('Manipulando Curso ',i+1,'/',len(linksCursos))
        page = getPageCursoFromLink(link)
        nomeCurso = getNomeCurso(page)
        codigo = getCodigoCurso(page)
        situacao = getSituacao(page)      
        duracao = getPeriodos(page)
        duracaoMin = getDuracaoMinima(page)
        duracaoMax = getPeriodosMaximo(page)
        ano = getAnoCurriculo(page)
        tabelas = getTabelas(page)
        
        for indexTabela in range(1,len(tabelas)-3):
            print('Manipulando Curso ',i+1,'/',len(linksCursos))
            if('Para fazer jus ao grau e diploma, o aluno dever' in str(html.tostring(tabelas[indexTabela]))):
                break
            print('Tabelas ', indexTabela,'/',len(tabelas))
            tabela = tabelas[indexTabela]
            cabecalho =  getCabecalhoTabelaDisciplinas(tabela)
            getInformacoesDisciplina(tabela.cssselect('tr'))
        
main()    

    