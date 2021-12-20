from pathlib import Path
from notific import *

"""[Classes para a manipulação de arquivos de registro txt, Arquivos docx e de imagem e Diretórios]
"""

class Registro():
    """[Representa um arquivo de registro de tipo txt]
    """
    
    diret_registro = Path('caminhos').absolute() # Caminho da pasta que armazena todos os registros

    def __init__(self, nome_reg:str, tipo='arquivos'):
        """[Método construtor da instãncia Registro]

        Args:
            nome_reg (str): [Nome do arquivo de registro]
            tipo (str, optional): [Tipo de registro, pode ser 'arquivos', ou 'diretoris', indicando quetipo de caminho ele registra]. Defaults to 'arquivos'.
        """
        
        self.nome_reg = Path(nome_reg)
        self.tipo = tipo
        # Une caminho_do_diretorio/nome_registor.txt
        self.registro = self.diret_registro.joinpath(self.nome_reg) 
           

    def criar_dir_reg(self) -> None:
        """[Cria o diretório dos registros caso este não exista]
        """

        # Armazena o caminho do diretório de registro em uma variável
        diret = self.diret_registro

        # Se o diretório de registros não existir, cria o mesmo
        if not diret.exists():
            diret.mkdir()


    def criar_reg(self) -> None:
        """[Cria um arquivo de registro, caso este não exista.]
        """
        
        # Se o arquivo de registro não existe:
        if not self.registro.exists():
            # Simplifica jogando o caminho em uma variável
            registro = self.registro

            # Se o tipo do registro for válido:
            if self.tipo in ['arquivos', 'diretorios']:
                        

                # Númere de linhas de aviso, para quando
                # o registro estiver vazio
                l_aviso = 0

                # 1 linha de aviso para registro de arquivos
                # e 2 linhas para registro de diretórios
                l_aviso = 1 if self.tipo == 'arquivos' else 2

                # Insira as linhas de aviso:
                with open(registro, 'a+', encoding='utf-8') as arq:
                    for c in range(l_aviso):
                        arq.write('Caminho não registrado\n')


    def registrar_arq(self, tupla_caminhos) -> None:
        """[Realiza o registro de uma tupla de caminhos de arquivos 
        que pode conter um ou mais caminhos]

        Args:
            lista_caminhos ([tuple]): [tupla de caminhos de arquivos]
        """
        # Cria o diretório de registro e o registro
        # caso os mesmos não existam
        self.criar_dir_reg()
        self.criar_reg()


        registro = self.registro

        # Lista que irá contar os caminhos
        lista_cam = list()

        # Laço para inserir quebra de linha em cada
        # caminho da tupla e inseri-los na lista
        for cam in tupla_caminhos:
            lista_cam.append(fr"{cam}"+'\n')

        # Abre o arquivo de registro e registra os caminhos,
        # um em cada linha do arquivo
        with open(registro, 'w+', encoding='utf-8') as arq:
            arq.writelines(lista_cam)

        
    def registrar_dir(self, linha:int, caminho:str) -> None:
        """[Realiza o registro de um único caminho de diretório]

        Args:
            linha (int): [Linha do registro onde será inserido o caminho].
            caminho (str): [Caminho do diretório].
        """
        
        # Cria o diretório de registro e o registro
        # caso os mesmos não existam
        self.criar_dir_reg()
        self.criar_reg()

        registro = self.registro

        # Abre o registro para leitura
        with open(registro, 'r+', encoding='utf-8') as arq:
                # Passa os caminhos do arquivo para uma lista
                lista_linhas = arq.readlines()

                # Substitui o caminho contido no índice 'linha' pela a string 'caminho'
                lista_linhas.pop(linha) 
                lista_linhas.insert(linha, f"{caminho}\n") #\n para quebra de linha

        # Insere a lista_linhas modificada no registro
        with open(registro, 'w+', encoding='utf-8') as arq:
            arq.writelines(lista_linhas)


    def consultar(self) -> tuple:
        """[Consulta o registro]

        Returns:
            tuple: [Retorna uma tupla contendo todos os caminhos de 
            diretórios ou arquivos contidos no registro]
        """

        # Cria o diretório de registro e o registro
        # caso os mesmos não existam
        self.criar_dir_reg()
        self.criar_reg()

        registro = self.registro


        # Abre o arquivo e realiza uma leitura de todas as listas
        with open(registro, 'r+', encoding='utf-8') as arq:
            lista_caminhos = arq.readlines() # Retorna uma lista de strings

        # Converte a lista de caminhos em uma tupla e retorna
        return tuple(lista_caminhos)

    
class Arquivo():

    registro = Registro('reg_arq.txt', tipo='arquivos')

    def __init__(self, caminho:str):
        """[Representa um arquivo]

        Args:
            caminho (str): [Caminho absoluto do arquivo]
        """
        
        # Converte o caminho em um objeto Path 
        # extraí o caminho absoluto se necessário
        self.caminho_abs = Path(caminho).absolute()
        self.nome = self.caminho_abs.name   # Nome original do arquivo
        # Caminho absoluto da cópia pdf que será gerada
        #self.cam_abs_pdf = self.caminho_abs.with_suffix('.pdf')
        self.extensao = self.caminho_abs.suffix  # Extensão do arquivo
        self.dir_atual = self.caminho_abs.parent


    def euma_imagem(self) -> bool:
        """[Verifica se um objeto é ou não uma imagem]

        Returns:
            [bool]: [Retorna True se o objeto for uma imagem, e False, caso não.]
        """

        if self.extensao in ['.png', '.jpg', '.jpeg', '.svg']:
            return True

        else:
            return False

    def eum_docx(self)-> bool:
        """[Verifica se um objeto é ou não um docx]

        Returns:
            [bool]: [Retorna True se o objeto for um docx, e False, caso não.]
        """
        if self.extensao in ['.docx']:
            return True
        
        else:
            return False

    def e_valido(self) -> bool:
        """[Verifica se um objeto é válido para o sistema]

        Returns:
            [bool]: [Retorna True se o objeto for uma imagem ou um docx, e False, caso não.]
        """
            
        if self.eum_docx() or self.euma_imagem():
            return True

        else:
            return False

    @classmethod
    def consultar_reg(cls) -> bool:
        """[Retorna os caminhos contidos no registro de arquivos

        Returns:
            [tuple]: [Caminhos contidos no registro de arquivos]
        """
        caminhos = cls.registro.consultar()
        return caminhos

    def converter_docx(self, dir_dest:Path) -> None:
        """[Cria uma cópia pdf de um arquivo docx, depois aloca essa cópia
        para o diretório de destino]

        Args:
            arq (Path): [Caminho absoluto do arquivo docx]
            dir_dest (Path): [Diretório onde será armazenado o pdf]
        """

        from sys import platform  # Descobre o sistema operacional

        # Sistema operacional em que este código está rodando
        plataforma = platform
    
        # Pega o caminho absoluto do diretório atual do arquivo docx
        dir_atual = self.dir_atual
        
        
        # Deduz qual será o caminho absoluto atual da cópia pdf
        # Esse método Path retorna um novo objeto Path porém com o sulfixo  
        # (extensão de arquivo)_alterado
        cam_abs_pdf = self.caminho_abs.with_suffix('.pdf')

        # Deduz qual será o novo  caminho absoluto do arquivo pdf que será criado
        # Esse método Path retorna um novo objeto Path que é a 
        # junção de dois objetos Path A e B. 
        # sintaxe: A.joinpath(B)
        novo_cam_abs_pdf = dir_dest.joinpath(cam_abs_pdf.name)
 
        # Se o sistema operacional for linux
        # ATENÇÃO! Será necessário ter o pacote abword instalado no linux
        # Use sudo apt-get install abword
        if plataforma == 'linux':

            from os import system  # lib do sistema
            import shutil  # Lib para mover arquivos de um diretório para outro

            # Cria uma cópia pdf do docx na mesma pasta
            system(fr"cd '{dir_atual}' && abiword --to=pdf {self.nome}")

            
            # Move o arquivo pdf do seu caminho absoluto atual para um novo caminho absoluto
            # mudando também o seu nome
            shutil.move(cam_abs_pdf, novo_cam_abs_pdf)

        # Se o sistema operacional for windows
        elif plataforma == 'win32':

            from docx2pdf import convert # Lib docx2pdf só funciona no windows
  
            # Converte o arquivo docx em pdf
            # Recebe como arqumentos (caminho absoluto do arquivo docx, novo caminho absoluto para o pdf)
            convert(self.caminho_abs, novo_cam_abs_pdf)     

    def converter_imagem(self, dir_dest:Path) -> None:
        """[Converte arquivos de imagem para PDF]

        Args:
            arq (Path): [Caminho absoluto do arquivo de imagem]
            dir_dest (Path): [Diretório onde será armazenado o PDF]
        """
        
        from PIL import Image # Lib para tratamento de imagens
        import img2pdf  # Lib para conversão de imagens em pdf


        # Deduz qual será o caminho absoluto atual da cópia pdf
        # Esse método Path retorna um novo objeto Path porém com o sulfixo  
        # (extensão de arquivo)_alterado
        cam_abs_pdf = self.caminho_abs.with_suffix('.pdf')

        # Deduz qual será o novo  caminho absoluto do arquivo pdf que será criado
        # Esse método Path retorna um novo objeto Path que é a 
        # junção de dois objetos Path A e B. 
        # sintaxe: A.joinpath(B)
        novo_cam_abs_pdf = dir_dest.joinpath(cam_abs_pdf.name)

        # Importa a imagem
        imagem = Image.open(self.caminho_abs)
        # Converte o arquivo de imagem em bytes de pdf
        # Para pegar o caminho do arquivo de imagem usamo .filename
        bytes_pdf = img2pdf.convert(imagem.filename)

        # Cria um arquivo pdf e o abre para escrita de arquivo binário (wb)
        with open(novo_cam_abs_pdf, "wb") as novo_pdf:
            # Escreve no arquivo pdf os bytes da nossa imagem:
            novo_pdf.write(bytes_pdf)

    def ConvereterPDF_arq(self, diretorio_destino:str) -> None:
        """[Realiza a conversão de arquivos docx e de imagem para pdf.
        Para isso, chama métodos especídicos para a conversão de cada tipo de arquivo]

        Args:
            diretorio_destino (str): [Diretório onde será armazenado o pdf]
        """
        
        if self.e_valido():
            # Verifica se o arquivo é um docx ou uma imagem
            # E chama a função específica para convertê-lo
            
            if self.eum_docx():
                self.converter_docx(Path(diretorio_destino))
                
            elif self.euma_imagem():
                self.converter_imagem(Path(diretorio_destino))
            

class Diretorio():
    
    # Instancia o Registro da classe diretório
    registro = Registro('reg_dir.txt', tipo='diretorios')

    def __init__(self, caminho:str):
        """[Método construtor da instância de Diretorio]

        Args:
            caminho (str): [Caminho absoluto do diretório]
            eum_dir_destino (bool, optional): [Define se o diretório é um diretório de destino, se não for, então ele é considerado um diretório de origem.]. Defaults to False.
        """
        
        self.caminho_abs = Path(caminho)
        self.nome = self.caminho_abs.name
    
    def listar_arquivos(self) -> tuple:
        """[Lista o caminho absoluto de todos os arquivos contidos no diretório]

            Returns:
                [tuple]: [Uma tupla contendo os caminhos abolutos dos arquivos contidos no direório]
        """
        
        diretorio = self.caminho_abs

        lista_arq = list() # Lista de arquivos
        # Itera sobre o diretório inserindo os caminhos
        # absolutos dos arquivos contidos nele em uma lista
        for arq in diretorio.glob('*'):
            lista_arq.append(str(arq.absolute()))
            
        # Converte a lista de arquivos em tupla e retorna
        return tuple(lista_arq)

    def salvar_caminho(self, linha) -> None:
        """[Salva o caminho absoluto do diretório em um registro]
        """
        
        # Efetua o registro
        # OBS: O método registrar aceita apenas strings como argumento
        self.registro.registrar_dir(linha, self.caminho_abs)  

    @classmethod
    def consultar_reg(cls) -> tuple:
        """[Retorna os caminhos contidos no registro de diretórios]

        Returns:
            [tuple]: [Caminhos contidos no registro de diretórios]
        """

        caminhos = cls.registro.consultar()
        return caminhos

    def converterPDF_dir(self, dir_dest) -> None:
        """[Realiza a conversão dos arquivos que estão dentro do diretório para pdf]

        Args:
            dir_dest (str): [Diretório onde os pdfs serão armazenados]
        """
        
        c = 0
        # Percorre todos os arquivos do diretório
        for arq in self.listar_arquivos():
            
            # Transforma-os em um objeto Arquivo
            arq = Arquivo(arq)

            # Se o arquivo for válido:
            if arq.e_valido():
                c += 1
                # Converte-o
                arq.ConvereterPDF_arq(dir_dest)
            

        else:
            if c > 0:
                Notificacao.notif_info(titulo='Sucesso', msg=f'{c} arquivos foram convertidos com sucesso!')
            else:
                Notificacao.notif_erro(msg='Nenhum arquivo foi converdito, verifique se há no diretório algum arquivo docx ou de imagem.')
