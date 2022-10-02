"""
author: johncoderdev
creation date: 02/10/2022
license: MIT
github repository: https://github.com/JohnCoderDev/tester-mc102.git
"""
from sys import argv
from subprocess import Popen, PIPE
from glob import glob
from os.path import basename, exists, isdir

def verifyPaths(*paths):
    """
    Levanta uma exceção se algum caminho passado
    não for encontrado.
    """
    for path in paths:
        if not exists(path):
            raise FileNotFoundError(
                f'\033[31marquivo \'{path}\' não foi encontrado.\033[m'
            )

def verifyDir(*paths):
    """
    Verifica se o caminho especificado é um diretório
    e se existe. Levanta uma exceção caso não.
    """
    for path in paths:
        if not isdir(path):
            raise FileNotFoundError(
                f'\033[31mpasta \'{path}\' não foi encontrada.\033[m'
            )

class Tester:
    """
    Classe do Tester que será usado para
    fazer os testes.
    """
    def __init__(self, programToBeTested: str, directoryWithAnswers: str) -> None:
        if not programToBeTested.endswith('.py'): programToBeTested += '.py'
        self.programToBeTested = programToBeTested
        self.directoryWithAnswers = directoryWithAnswers

        try:
            verifyPaths(self.programToBeTested)
            verifyDir(self.directoryWithAnswers)
            
        except FileNotFoundError as error:
            print(str(error))
            exit()
    
    def setProgramToBeTested(self, newProgram: str) -> None:
        """
        Muda o programa que será testado.
        """
        if not newProgram.endswith('.py'): newProgram += '.py'

        try:
            verifyPaths(newProgram)
            self.programToBeTested = newProgram

        except FileNotFoundError as error:
            print(f'\033[31m{str(error.args)}\033[m')

    def setDirectoryWithAnswers(self, directoryWithAnswers: str):
        """
        Permite mudar o diretório em que as respostas se encontram.
        """
        try:
            verifyDir(directoryWithAnswers)
            self.directoryWithAnswers = directoryWithAnswers
        
        except FileNotFoundError as error:
            print(str(error))
    
    def verifyAnswer(self, inputFilePath: str, outputFilePath: str) -> tuple:
        """
        Verifica a resposta com base nos arquivos
        de input e output passados.
        """
        command = f'python {self.programToBeTested}'

        process = Popen(
            command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            encoding='ISO-8859-1'
        )

        try:
            if not inputFilePath.endswith('.in'): inputFilePath += '.in'
            if not outputFilePath.endswith('.out'): outputFilePath += '.out'

            with open(inputFilePath, 'r') as inputFile:
                inputText = ''.join(inputFile.readlines())
            
            with open(outputFilePath, 'r', encoding='utf-8') as outputFile:
                expectedOutput = ''.join(outputFile.readlines())
                expectedOutput = expectedOutput.split('\n')

            process.communicate(inputText)
            output, error = process.communicate()
            output = output.split('\n')

            if error != '':
                raise RuntimeError(
                    f'\033[41mocorreu um problema na execução do programa:\033[0m\n' + 
                    f'\033[31m{error}\033[m'
                )
            
            incorrectAnswers = [
                output[answer] for answer in range(len(output))
                if not output[answer] in expectedOutput
            ]

            return output, expectedOutput, incorrectAnswers

        except FileNotFoundError as error:
            print(f'\033[31mnão foi possível encontrar {error.filename}.\033[m')
            return None

        except RuntimeError as error:
            print(str(error))
            return None

    def verifyAllAnswers(self) -> None:
        """
        Função para verificar as respostas no diretório especificado.
        """
        inputFilesInDirectory = [
            filename.replace('.in', '') for filename in 
            glob(self.directoryWithAnswers + '/*.in')
        ]

        for filename in inputFilesInDirectory:
            result = self.verifyAnswer(filename, filename)

            if result is None: continue

            output, expectedOutput, incorrectAnswers = result

            if not incorrectAnswers:
                print(f'\033[32mO teste {filename} está correto.\033[m')
                continue

            print(f'\033[31mO teste {filename} está incorreto.\033[m\n')
            print('\033[1mResultado esperado:\033[m\n')
            
            # printa as respostas esperadas
            for expectedAnswer in expectedOutput:
                
                if not expectedAnswer in output:
                    print(f'\033[32m{expectedAnswer}\033[m')
                    continue
                
                print(expectedAnswer)
            
            print('\033[1m\nResultado obtido:\033[m\n')

            # printa as respostas obtidas do programa
            for answer in output:
                
                if answer in incorrectAnswers:
                    print(f'\033[31m{answer}\033[m')
                    continue

                print(f'\033[32m{answer}\033[m')

if __name__ == '__main__':
    
    if len(argv) != 3:
        print(
            '\033[31mpara usar este programa, você deve ' + 
            'digitar o comando da seguinte forma:\033[m\n' + 
            f'python {basename(__file__)} \033[33m ' + 
            '<nome do arquivo> <pasta com as respostas>\033[m'
        )
        exit()

    tester = Tester(argv[1], argv[2])
    tester.verifyAllAnswers()