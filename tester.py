
# author: johncoderdev
# creation date: 01/10/2022
# license: MIT
# github repository:

# imports
from sys import argv
from subprocess import Popen, PIPE
from glob import glob
from os.path import basename, exists

from pynvim import encoding

# função para verificar se a resposta bate com 
# o resultado esperado
def verifyAnswer(programName, inputPath, outputPath) -> tuple:    
    """
    Está é uma função para testar o programa passado como
    argumento. O seu retorno normal será uma tupla que 
    conterá a saída esperada, a saída obtida, e as respostas
    que não bateram. Caso contrário, retorna o erro obtido
    na execução do programa.
    (param) programName: nome do arquivo '.py' que será testado.
    (param) inputPath: caminho até o arquivo que contém as entradas do programa.
    (param) outputPath: caminho até o arquivo que contém as saídas esperadas para o programa.
    """
    command = f'python {programName}'
    # Roda a execução do programa
    process = Popen(command, 
                    stdout=PIPE,
                    stdin=PIPE,
                    stderr=PIPE,
                    encoding='ISO-8859-1')
        
    with open(inputPath, 'r') as inputFile:
        inputText = ''.join(inputFile.readlines())

    # roda o programa passando as entradas
    process.communicate(input=inputText)
    # pega a saida do programa
    programOutput, error = process.communicate()

    # retorna o erro do progama caso exista
    if error != '': return error

    programOutput = programOutput.split('\n')

    # caso não tenha dado erro, compara a saída
    # do programa com a resposta esperada
    with open(outputPath, 'r', encoding='utf-8') as outputFile:
        expectedOutput = ''.join(outputFile.readlines())
        expectedOutput = expectedOutput.split('\n')

    incorrectAnswers = [
        programOutput[a] for a in range(len(programOutput))
        if programOutput[a] not in expectedOutput
    ]
    
    return programOutput, expectedOutput, incorrectAnswers

# Verifica se os caminhos passados existem
def verifyPaths(*paths):
    """
    Função para verificar se os caminhos existem. Caso
    não exista o caminho especificado, retorna um erro.
    (param) *paths: caminhos a serem avaliados.
    """
    for path in paths:
        if not exists(path):
            raise FileNotFoundError(
                '\033[31mnão foi possível encontrar ' + 
                f'\033[36m{path}\033[m'
            )

def verifyAllAnswers(programName: str, directoryWithAnswers: str):
    """
    Função para verificar as respostas do programa com base
    nos arquivos presentes em um diretório com as respostas.
    (param) programName: nome do programa a ser testado.
    (param) directoryWithAnswers: caminho do diretório que contém as respostas.
    """
    filesInDirectory = glob(directoryWithAnswers + '/*.in')
    filesPrefixes = [fn.replace('.in', '') for fn in filesInDirectory]
    
    for filePrefix in filesPrefixes:
        try:
            inputFile = glob(f'{filePrefix}.in')[0]
            outputFile = glob(f'{filePrefix}.out')[0]
        
        except IndexError:
            print(f'\033[31mnão foi possível encontrar o teste {filePrefix}\033[m')
            continue

        result = verifyAnswer(programName, inputFile, outputFile) 

        if type(result) is str:
            print(f'\033[41mocorreu um erro na execução do programa:\033[m')
            print(f'\033[31m{result}\033[m')
            continue

        programOutput, expectedOutput, incorrectAnswer = result

        # caso não haja respostas incorretas
        if not incorrectAnswer:
            print(f'\033[32mO teste {filePrefix} está correto\033[m')
            continue
        
        print(f'\033[31m\033[1mO teste {filePrefix} está incorreto\033[m\n')

        # printa as respostas esperadas
        print('\033[1mResposta esperada:\033[m\n')
        for line in expectedOutput:
            
            if line not in programOutput:
                print(f'\033[32m{line}\033[m')
                continue
            
            print(line)
        
        # Printa as respostas do programa
        print('\n\033[1mResposta obtida:\033[m\n')
        for line in programOutput:
            if line in incorrectAnswer:
                print(f'\033[31m{line}\033[m')
                continue

            print(f'\033[32m{line}\033[m')
        


if __name__ == "__main__":
    try:
        # verifica se o comando foi digitado corretamente
        if len(argv) != 3:
            print('\033[33mPara usar este programa,' +
                'você deve digitar o comando da ' + 
                'seguinte forma:\n' +
                f'\033[mpython {basename(__file__)} ' +
                '\033[36m<nome do arquivo> <pasta com as respostas>\033[m')
            exit()
        
        programToBeTested = argv[1] if argv[1].endswith('.py') else f'{argv[1]}.py'
        directoryWithAnswers = argv[2]

        verifyPaths(programToBeTested, directoryWithAnswers)
        verifyAllAnswers(programToBeTested, directoryWithAnswers)

    except FileNotFoundError as e:
        print(e.__str__())

    except ValueError as e:
        print(e.__str__())