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
        self.task = ''
        self.view = 'all'
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name TEXT, status TEXT)')
        self.results = self.db_execute('SELECT * FROM tasks')
        self.main_page()

    # gerando um banco de dados
    def db_execute(self, query, params=[]):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall() 

    # verificando se os valores estão (complete ou incomplete)
    def checked(self, e):
        is_checked = e.control.value
        label = e.control.label

        if is_checked:
            self.db_execute('UPDATE tasks SET status = "complete" WHERE name = ?', params=[label])
        else:
            self.db_execute('UPDATE tasks SET status = "incomplete" WHERE name = ?', params=[label])

        if self.view == 'all':
            self.results = self.db_execute('SELECT * FROM tasks')
        else:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = ?', params=[self.view])

        self.update_task_list()

    # deletando uma tarefa
    def delete_task(self, e):
        label = e.control.data
        self.db_execute('DELETE FROM tasks WHERE name = ?', params=[label])
        self.results = self.db_execute('SELECT * FROM tasks')
        self.update_task_list()

    # gerando as funções de tarefas
    def task_container(self):
        return ft.Container(
            height=self.page.height * 0.8,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Checkbox(
                                label=res[0],
                                on_change=self.checked,
                                value=True if res[1] == 'complete' else False
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=self.delete_task,
                                data=res[0]  # Passa o nome da tarefa como dado
                            )
                        ]
                    )
                    for res in self.results
                ]
            )
        )
    
    # salvando os valores
    def set_value(self, e):
        self.task = e.control.value
        print(self.task)

    # passando informações pros botões
    def add(self, e, input_task):
        name = self.task
        status = 'incomplete'

        if name:
            self.db_execute('INSERT INTO tasks VALUES(?,?)', params=[name, status])
            input_task.value = ''
            self.results = self.db_execute('SELECT * FROM tasks')
            self.update_task_list()

    def update_task_list(self):
        tasks = self.task_container()
        self.page.controls[2] = tasks  # Atualiza o terceiro controle
        self.page.update()

    def tabs_changed(self, e):
        if e.control.selected_index == 0:
            self.results = self.db_execute('SELECT * FROM tasks')
            self.view = 'all'
        elif e.control.selected_index == 1:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"')
            self.view = 'incomplete'
        elif e.control.selected_index == 2:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "complete"')
            self.view = 'complete'

        self.update_task_list()

    # criando os botões das tarefas
    def main_page(self):
        input_task = ft.TextField(
            hint_text='Digite aqui uma tarefa',
            expand=True,
            on_change=self.set_value
        )

        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.add(e, input_task)
                )
            ]
        )

        tabs = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text='Todos'),
                ft.Tab(text='Em andamento'),
                ft.Tab(text='Finalizados')
            ]
        )

        tasks = self.task_container()

        # adicionando os botões e funções
        self.page.add(input_bar, tabs, tasks)

# inicializando o projeto
ft.app(target=ToDo)
