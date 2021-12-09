from tkinter import messagebox

"""[Classes para a manipulação de notificações]
"""

class Notificacao():
    """[Representa os tipos de notificações que serão exibidas pelo sistema]
    """
    @staticmethod
    def notif_info(*, titulo='Informação', msg='Você tem uma notificação.')-> None:
        messagebox.showinfo(titulo, msg)

    @staticmethod
    def notif_erro(*, titulo='ERRO', msg='Ocorreu um erro!')-> None:
        messagebox.showerror(titulo, msg)

    @staticmethod
    def pergu_ok_cancel(*, titulo='Responda', msg='Deseja continuar?')-> bool:
        resp = messagebox.askokcancel(titulo, msg)
        return resp
