from tkinter import *
from tkinter import ttk
# Lib para manipulação de caminhos
from pathlib import Path

import dir_arq, notific


class Funcs_Auxiliares():
    def rm_quebra_linha(self, iteravel) -> tuple:
        import re

        novo_iteravel = list()
        for string in iteravel:

            novo_iteravel.append(re.sub("[\n]$", "", string))

        return tuple(novo_iteravel)

    def validar_caminho(self, caminho) -> bool:
        """[Verifica se um caminho de arquivo ou diretório é válido para este sistema conversor PDF]

        Args:
            caminho ([str]): [Caminho de diretório ou arquivo]

        Returns:
            bool: [Retorna True se ele for válido, senão, retorna False]
        """

        # Objeto Path
        cam = Path(caminho)

        # Lista de tipos de caminhos que existem porém são inválidos para o sistema
        lista_invalido = ['', '.', '/', '//', '///']
    

        # Verifica se o sistema existe E que não está na lista de inválidos:
        if cam.exists() and not str(cam) in lista_invalido:

            return True

        else:
            return False

    def consultar_entry(self, entry) -> tuple:
        """[Extrai os caminhos contidos na entry]

        Args:
            entry (Tk.Entry): [Caixa de texto tkinter]

        Returns:
            tuple: [Retorna uma tupla de strings contendo caminhos de arquivo ou diretórios]
        """

        # Lib para expressões regulares
        import re

        # Conteúdo da entry formato (str)
        texto = entry.get()

        # Lista que conterá os caminhos extraídos do conteúdo da entry
        lista_cam = list()

        # Retorna as virgulas encontradas no texto
        virgulas = re.sub('[^,$]', "", texto)
        num_virgulas = len(virgulas) # Número de vírgulas encontrads

        # Se não houver nenhuma vírgula:
        if num_virgulas == 0:
            # Insira a string única na lista
            lista_cam.append(texto)
              
        # Senão, foi encontrada ao menos uma vírgula:
        else:

            #Converte a string 'texto' em uma lista]
            # usando as vírgulas da string como separador
            lista_cam = texto.split(', ')
        

        # Retorna uma tupla contendo os caminhos consultados na entry
        return tuple(lista_cam)

    def inserir_iteravel(self, iteravel, entry):
        # Laço para inserir os caminhos do iteravel
            # na entry
            for cam in iteravel:
                # Se o caminho não for o último do iteravel:
                if cam != iteravel[-1]:
                    # Insere o caminho com uma vírgula
                    entry.insert(END, cam+', ')

                # Senão, insere o caminho sem vírgula
                else:
                    entry.insert(END, cam)

class Funcs(Funcs_Auxiliares):
    """[Classe Mãe de Funcs_Partial. Representa as funções principais do sistema]
    """

    def salvar(self, entry):
        """[Função para salvar o caminho contido na entry]

        Args:
            entry (Tk.Entry): [Caixa de texto Tk]
        """

        # Consulta o conteúdo da entry:
        tupla_cam = self.consultar_entry(entry)

        # Flag para indicar se todos os caminhos foram
        # salvos com sucesso!
        ok = False

        # Laço para validar os caminhos da entry
        for cam in tupla_cam:
            caminho = Path(cam)

            # Se o caminho não for válido:
            if not self.validar_caminho(caminho):
                notific.Notificacao.notif_erro(msg=fr"Caminho não encontrado! Verifique se todos os arquivos ou diretórios informados existem.")
                return False


        # Se a entry pertence á aba1 que é a aba de arquivos:
        if entry == self.entry_ab1:
            
            # Salva a lista de caminho no registro de arquivos
            registro_arq = dir_arq.Arquivo.registro
            registro_arq.registrar_arq(tupla_cam)

            # Sucesso!
            ok = True

        # Senão, ela pertence à uma das abas de diretório
        else:
            
            # Define em que linha do registro o caminho será salvo:
            if entry == self.entry_ab2:
                linha = 0
            elif entry == self.entry_ab3:
                linha = 1

            # Converte o caminho em um obejeto Diretório
            # OBS: Deduz-se que haverá apenas um caminho de diretório na tupla
            # logo, extraímos o caminho que está no primeiro índice:
            diret = dir_arq.Diretorio(str(tupla_cam[0]))
            # Salva o caminho do diretório na linha
            diret.salvar_caminho(linha)

            # Sucesso!
            ok = True
        
        # Se a flag é positiva:
        if ok:
            notific.Notificacao.notif_info(titulo='SUCESSO', msg='Caminho salvo com sucesso!')

    def limpar(self, entry):
        """[Limpa o conteúdo de uma entry tkinter]

        Args:
            entry (Tk.Entry): [Caixa de texto Tk]
        """
        # Conteúdo da entry (str)
        conteudo = entry.get()

        # Se a entry não estiver vazia:
        if conteudo:
            entry.delete(0, END)
    
    def selecionar(self, entry):
        """[Abre uma interface para que o usuário possa selecionar arquivos]
        Args:
            entry (Tk.Entry): [Caixa de texto tkinter]
                e_diretorio (bool): [Determina se o conteúdo da entry se refere à um diretório,
                se for False, então deduz que ser refere à um ou mais arquivos]
        """
        from tkinter import filedialog
        
        entry.delete(0, END)
        # Se o caminho contido na entry for referente à um diretório:
        if entry == self.entry_ab2 or entry == self.entry_ab3:
        
            # Retorna o caminho do diretório em formato de string
            cam = filedialog.askdirectory()

            # Insere o(s) caminho(s) na entry
            entry.insert(0, cam)

        # Senão, o caminho é de um arquivo:
        else:
            # Retorna uma tupla de strings com os caminhos dos arquivos
            tupla = filedialog.askopenfilenames()

            self.inserir_iteravel(tupla, entry)

    def converter(self, entry):
        """[Converte os arquivos em pdf, consultando o caminho dos arquivos
        ou do diretório que contem os arquivos na entry]

        Args:
            entry (Tk.Entry): [Caixa de texto tkinter]
        """

        # Consulta o caminho contino na entry
        tupla_caminhos = self.consultar_entry(entry)

        for cam in tupla_caminhos:
            if not self.validar_caminho(cam):
                
                # Exiba uma notificação de erro:
                notific.Notificacao.notif_erro(msg='Diretório de destino não encontrado!')
                return False

        # Consulto a entry_ab3 que conterá o diretório de destino dos arquivos
        tupla_dest = self.consultar_entry(self.entry_ab3)

        # Extrai o caminho da tupla
        destino = tupla_dest[0]

        # Se a entry que foi consultada for da aba1 (aba de arquivos):
        if entry == self.entry_ab1:
            
            # Laço para converter todos os arquivos que
            # foram selecionados na aba1
            for i, cam in enumerate(tupla_caminhos):
                
                # Instancia o objeto Arquivo
                arq = dir_arq.Arquivo(cam)
                # Converte o arquivo passando o seu novo nome e o deu sestino
                arq.ConvereterPDF_arq(destino)

            
        # Senão, se a entry que foi consultada for da aba2 (aba de diretórios):
        elif entry == self.entry_ab2:

            # Extrái o único caminho que está na tupla:
            cam = tupla_caminhos[0]
    
            # Instancia o objeto Diretório
            diretorio = dir_arq.Diretorio(cam)
            # Converte os arquivos no diretório passando caminho de destino dos mesmos
            diretorio.converterPDF_dir(destino)


class Funcs_Partial(Funcs):
    """[Classe filha de Funcs. Representa as funções parciais das funções principais contidas em Funcs]
    """
    
# Parciais de salvamento
    def prtl_salv_ab1(self):
        from functools import partial
        func = partial(self.salvar, self.entry_ab1)
        func()

    def prtl_salv_ab2(self):
        from functools import partial
        func = partial(self.salvar, self.entry_ab2)
        func()

    def prtl_salv_ab3(self):
        from functools import partial
        func = partial(self.salvar, self.entry_ab3)
        func()

# Parciais de limpeza
    def prtl_limp_ab1(self):
        from functools import partial
        func = partial(self.limpar, self.entry_ab1)
        func()

    def prtl_limp_ab2(self):
        from functools import partial
        func = partial(self.limpar, self.entry_ab2)
        func()

    def prtl_limp_ab3(self):
        from functools import partial
        func = partial(self.limpar, self.entry_ab3)
        func()

# Parciais de seleção
    def prtl_selec_ab1(self):
        from functools import partial
        func = partial(self.selecionar, self.entry_ab1)
        func()

    def prtl_selec_ab2(self):
        from functools import partial
        func = partial(self.selecionar, self.entry_ab2)
        func()

    def prtl_selec_ab3(self):
        from functools import partial
        func = partial(self.selecionar, self.entry_ab3)
        func()

# Parciais de conversão

    def prtl_convert_arq(self):
        from functools import partial
        #func = partial(self.converter, self.entry_ab1)
        func = partial(self.converter, self.entry_ab1)
        func()

    def prtl_convert_dir(self):
        from functools import partial
        #func = partial(self.converter, self.entry_ab1)
        func = partial(self.converter, self.entry_ab2)
        func()



class App(Funcs_Partial):
    """[Classe para representar a interface gráfica]
    """

    def __init__(self):
        # Crio o nosso objeto root
        self.root = Tk()
        self.tela()
        self.frame_tela()
        self.widgets_frame()
        self.preencher_entry()
        self.root.mainloop()

    def tela(self):
        """[Configurações da tela]
        """
        self.root.title("Conversor PDF")
        self.root.geometry("650x300")
        self.root.resizable(True, True)

    def frame_tela(self):
        # Sintaxes:
        # Frame(conteiner, border, cor de fundo, cor da borda, grossura da borda)
        # frame.place(relativoX, relativoY, largura relativa, altura relativa)
        self.frame = Frame(self.root, bd=4)
        self.frame.place(relx=0.02, rely=0.03, relwidth=0.98, relheight=0.95)

    def widgets_frame(self):
        # Abas
        self.abas = ttk.Notebook(self.frame)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba3 = Frame(self.abas)

        # Nome das abas
        self.abas.add(self.aba1, text="Arquivos")
        self.abas.add(self.aba2, text="Pasta")
        self.abas.add(self.aba3, text="Destino")

        # Aloca as abas
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        # Imagens:
        self.img_arquivo = PhotoImage(file="imagens/img_arquivo.png")
        self.img_diretorio = PhotoImage(file="imagens/img_diretorio.png")
        self.img_excluir = PhotoImage(file="imagens/img_excluir.png")


        # Aba "Arquivos"-------------------------------------------
        # Label e entry e botões do Caminho de arquivos
        self.lb_arq = Label(self.aba1, text="Caminho do arquivo") 
        self.lb_arq.place(relx=0, rely=0.1)
        self.entry_ab1 = Entry(self.aba1)
        self.entry_ab1.place(relx=0, rely=0.2, relwidth=0.8)
        self.bt_selecarq = Button(self.aba1, text=None, image= self.img_arquivo, command=self.prtl_selec_ab1)
        self.bt_selecarq.place(relx=0.8, rely=0.2, relwidth=0.07, relheight=0.1)
        
        # Botões principais:
        self.bt_limpar = Button(self.aba1, text=None, image= self.img_excluir, command=self.prtl_limp_ab1)
        self.bt_limpar.place(relx=0.94, rely=0, relwidth=0.06, relheight=0.13)

        self.bt_salvar = Button(self.aba1, text="Salvar", command=self.prtl_salv_ab1)
        self.bt_salvar.place(relx=0.53, rely=0.85, relwidth=0.2, relheight=0.13)
        self.bt_converter = Button(self.aba1, text="Converter", bd=2, activebackground="grey", command=self.prtl_convert_arq)
        self.bt_converter.place(relx=0.74, rely=0.85, relwidth=0.2, relheight=0.13)


        # Aba "Diretório"-------------------------------------------
        # Label e entry e botões do Caminho da pasta de origem
        self.lb_dir_ori = Label(self.aba2, text="Caminho da Pasta de Origem") 
        self.lb_dir_ori.place(relx=0, rely=0.1)
        self.entry_ab2 = Entry(self.aba2)
        self.entry_ab2.place(relx=0, rely=0.2, relwidth=0.8)
        self.bt_selecdir_ori = Button(self.aba2, text=None, image= self.img_diretorio, command=self.prtl_selec_ab2)
        self.bt_selecdir_ori.place(relx=0.8, rely=0.2, relwidth=0.07, relheight=0.1)
        
        # Botões principais:
        self.bt_limpar = Button(self.aba2, text=None, image= self.img_excluir, command=self.prtl_limp_ab2)
        self.bt_limpar.place(relx=0.94, rely=0, relwidth=0.06, relheight=0.13)

        self.bt_salvar = Button(self.aba2, text="Salvar", command=self.prtl_salv_ab2)
        self.bt_salvar.place(relx=0.53, rely=0.85, relwidth=0.2, relheight=0.13)
        self.bt_converter = Button(self.aba2, text="Converter", bd=2, activebackground="grey", command=self.prtl_convert_dir)
        self.bt_converter.place(relx=0.74, rely=0.85, relwidth=0.2, relheight=0.13)


        # Aba "Destino"-------------------------------------------
        # Label e entry do caminho da dir de destino:
        self.lb_dir_dest = Label(self.aba3, text="Caminho da Pasta de Destino") 
        self.lb_dir_dest.place(relx=0, rely=0.1)
        self.entry_ab3 = Entry(self.aba3)
        self.entry_ab3.place(relx=0, rely=0.2, relwidth=0.8)
        self.bt_selecdir_dest = Button(self.aba3, text=None, image=self.img_diretorio, command=self.prtl_selec_ab3)
        self.bt_selecdir_dest.place(relx=0.8, rely=0.2, relwidth=0.07, relheight=0.1)

        # Botões principais:
        self.bt_limpar = Button(self.aba3, text=None, image= self.img_excluir, command=self.prtl_limp_ab3)
        self.bt_limpar.place(relx=0.94, rely=0, relwidth=0.06, relheight=0.13)

        self.bt_salvar = Button(self.aba3, text="Salvar", command=self.prtl_salv_ab3)
        self.bt_salvar.place(relx=0.74, rely=0.85, relwidth=0.2, relheight=0.13)


    def preencher_entry(self):
        """[Preenche as entrys com os caminhos contidos nos seus respectivos registros txt]
        """

        # Preenche a aba 1 ---------------

        # Consulta o registro de arquivos que retorna uma tupla
        # com os caminhos de arquivos
        tupla_arqs = dir_arq.Arquivo.consultar_reg()
        # Remove as quebras de linha dos caminhos
        tupla_arqs = self.rm_quebra_linha(tupla_arqs)
        
        # Insere a tupla na entry_ab1
        self.inserir_iteravel(tupla_arqs, self.entry_ab1)

        # Preenche as abas 2 e 3---------------
        # Consulta o registro de diretórios que retorna uma tupla
        # com os caminhos dos diretórios de origem e de destino
        tupla_dirs = dir_arq.Diretorio.consultar_reg()
        # Remove as quebras de linha dos caminhos
        tupla_dirs = self.rm_quebra_linha(tupla_dirs)

        # Insere os caminhos nas respectivas abas
        # Sendo que o caminho do diretório de o

        self.entry_ab2.insert(0, tupla_dirs[0])
        self.entry_ab3.insert(0, tupla_dirs[1])

App()
