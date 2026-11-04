from tkinter import ttk


class PainelLista(ttk.LabelFrame):
    def __init__(self, janela_pai, titulo, colunas, acoes):
        super().__init__(janela_pai, text=titulo, padding=8)
        self.__itens = {}
        self.__ao_selecionar = lambda: None
        self.__criar_tabela(colunas)
        self.__criar_botoes(acoes)

    def vincular_selecao(self, ao_selecionar):
        self.__ao_selecionar = ao_selecionar

    def preencher(self, itens, para_valores):
        selecionado = self.item_selecionado()
        self.__tabela.delete(*self.__tabela.get_children())
        self.__itens = {}
        for indice, item in enumerate(itens):
            identificador = str(indice)
            self.__itens[identificador] = item
            self.__tabela.insert("", "end", iid=identificador, values=para_valores(item))
            if item == selecionado:
                self.__tabela.selection_set(identificador)

    def item_selecionado(self):
        selecao = self.__tabela.selection()
        if not selecao:
            return None
        return self.__itens.get(selecao[0])

    def selecionar_primeiro(self):
        filhos = self.__tabela.get_children()
        if filhos:
            self.__tabela.selection_set(filhos[0])

    def __criar_tabela(self, colunas):
        nomes = [titulo for titulo, _ in colunas]
        area = ttk.Frame(self)
        area.pack(fill="both", expand=True)
        self.__tabela = ttk.Treeview(area, columns=nomes, show="headings", selectmode="browse")
        for titulo, largura in colunas:
            self.__tabela.heading(titulo, text=titulo, anchor="w")
            self.__tabela.column(titulo, width=largura, anchor="w")
        self.__tabela.bind("<<TreeviewSelect>>", lambda _: self.__ao_selecionar())
        rolagem = ttk.Scrollbar(area, orient="vertical", command=self.__tabela.yview)
        self.__tabela.configure(yscrollcommand=rolagem.set)
        rolagem.pack(side="right", fill="y")
        self.__tabela.pack(side="left", fill="both", expand=True)

    def __criar_botoes(self, acoes):
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(8, 0))
        for texto, comando in acoes:
            ttk.Button(barra, text=texto, command=comando).pack(side="left", padx=(0, 4))
