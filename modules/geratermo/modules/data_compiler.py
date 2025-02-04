class DataCompiler:
    msgs = []
    def set_data(self, data:dict) -> None:
        data_valid = self.analyse_data(data)
        if data_valid:
            self.data = data.copy()

    def analyse_data(self, data:dict) -> bool:
        if "cpf" not in data:
            data.setdefault("cpf", "-")
        if "celular" not in data:
            data.setdefault("celular", "-")

        if "serial" in data and "nome" in data and "matricula" in data:
            return True
    
        if not "serial" in data:
            self.msgs.append("Serial não informado!")
        if not "nome" in data:
            self.msgs.append("Nome não informado!")
        if not "matricula" in data:
            self.msgs.append("Matrícula não informada!")

        return False

    def get_data(self):
        if hasattr(self, "data"):
            return self.data
        
        for msg in self.msgs:
            print("[ATENÇÃO]", msg)

        return "Invalid data!"
    
    def define_first_paragraph(self):
        return f"""A SMECICT, entrega neste ato o Chromebook, no de série: <b>{self.data['serial']}</b>, ao profissional do magistério de nome <b>{self.data['nome']}</b>, matrícula n° <b>{self.data['matricula']}</b>, CPF n° <b>{self.data['cpf']}</b> portando o celular de n° <b>{self.data['celular']}</b> doravante denominado simplesmente “<b>USUÁRIO</b>” sob as seguintes condições:"""