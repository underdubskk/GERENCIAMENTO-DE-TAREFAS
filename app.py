# importando o flet e sqlite
import flet as ft
import sqlite3

# chamando a janela do flet
class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        # dando os atributos dela
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width = 350
        self.page.window_height = 500
        self.page.window_resizable = False
        self.page.window_always_on_top = True
        self.page.title = 'ToDo App'
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name, status)')
        self.main_page()

    # gerando um banco de dados
    def db_execute(self, query, params = []):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall() 

    # gerando às funções de tarefas
    def task_container(self):
        return ft.Container(
            height = self.page.height * 0.8,
            content =  ft.Column(
                controls = [
                    ft.Checkbox(label = 'Tarefa 1', value = True)
                ]
            )
        )

    # criando os botões das tarefas
    def main_page(self):
        input_task = ft.TextField(hint_text = 'Digite aqui uma tarefa', expand = True)

        input_bar = ft.Row(
            controls = [
                input_task,
                ft.FloatingActionButton(icon = ft.icons.ADD)
            ]
        )

        tabs = ft.Tabs(
            selected_index = 0,
            tabs = [
                ft.Tab(text = 'Todos'),
                ft.Tab(text = 'Em andamento'),
                ft.Tab(text = 'Finalizados')
            ] 
        )

        tasks = self.task_container()

        # adicionando ob botões e funções
        self.page.add(input_bar, tabs, tasks)
        





# inicializando o projeto
ft.app(target = ToDo)