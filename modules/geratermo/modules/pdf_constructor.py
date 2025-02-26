from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, gray
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, ListFlowable, ListItem, Spacer
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PageObject
from datetime import datetime
import re, os, random, segno, socket

def obter_ip():
    try:
        return socket.gethostbyname(socket.gethostname())  # Obtém o IP da máquina
    except Exception as e:
        print(f"Erro ao obter IP: {e}")
        return None

class PdfConstructor:
    def __init__(self, first_paragraph: str, title: str, data: dict):
        self.numero = random.randint(1000000, 9999999)
        # self.criar_qr(self.numero)
        self.title = title
        self.base_color = Color(0.0, 0.50196, 0.50196)
        self.template_pdf = "template.pdf"
        self.temp_pdf = "temp.pdf"
        self.export_folder = "export"
        if obter_ip() == "172.20.1.108":
            self.export_folder = "/var/www/files"
        self.first_paragraph = first_paragraph
        self.text_list = [
            "O equipamento deverá ser usado ÚNICO e EXCLUSIVAMENTE a serviço da SMECICT tendo em vista a atividade a ser exercida pelo USUÁRIO;",
            "Ficará o USUÁRIO responsável pelo uso e conservação do equipamento, responsabilizando-se, também, pelo pagamento dos danos causados ao aparelho por negligência ou imprudência, sem prejuízo dos procedimentos disciplinares cabíveis.",
            "O USUÁRIO tem somente a DETENÇÃO, tendo em vista o uso exclusivo para a prestação de serviços profissionais e NÃO a PROPRIEDADE do equipamento, sendo terminantemente proibido o empréstimo, aluguel ou cessão deste a terceiros;",
            "O USUÁRIO compromete-se a devolver o equipamento em perfeito estado, considerado o desgaste natural, quando solicitado pela Administração da SMECICT;",
            "A SMECICT não poderá ser, de qualquer forma, responsabilizada pelo uso indevido, seja para fins ilícitos ou não. Ocorrendo tal conduta, o profissional do magistério poderá sofrer sanções administrativas junto à SMECICT, além das sanções penais cabíveis;",
            "Em caso de dano, perda ou roubo, o USUÁRIO deverá comunicar imediatamente à autoridade policial e a SMECICT, por escrito, para que sejam efetuadas as devidas providências, devendo ainda efetuar o registro do boletim de ocorrência junto à autoridade policial e encaminhar para a Administração da SMECICT;",
            "Caso o profissional se desvincule da Unidade Escolar ou da Rede Municipal de Ensino de Saquarema, deverá devolver de imediato o mesmo para a SMECICT."
        ]
        self.user_name = self.extract_first_and_second_name(data["nome"])
        self.first_name = data["nome"].split()[0]
        self.text_list = [self.apply_bold(text, data) for text in self.text_list]

        self.export_pdf = os.path.join(self.export_folder, f"{self.numero}.pdf")

        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)
        
        # Criar PDF temporário
        self.criar_pdf_temp(self.temp_pdf)
        
        # Mesclar com template
        self.merge_pdf(self.template_pdf, self.temp_pdf, self.export_pdf)

    def criar_qr(self, numero:int):
        url = ""
        if obter_ip() == "172.20.1.108":
            url = f"http://172.20.1.108/files/{numero}"
        self.test = segno.make(url)
        self.test.save(f"termo_qr_{numero}.png", scale=2)

    def extract_first_and_second_name(self, full_name):
        conectores = ["de", "da", "das", "do", "dos"]
        partes = full_name.split()

        if len(partes) == 1:
            return partes[0]

        if len(partes) >= 3 and partes[1].lower() in conectores:
            return f"{partes[0]} {partes[1]} {partes[2]}"

        return f"{partes[0]} {partes[1]}"

    def apply_bold(self, text: str, data: dict):
        bold_terms = ["SMECICT", "USUÁRIO", "ÚNICO", "EXCLUSIVAMENTE", "DETENÇÃO", "NÃO", "PROPRIEDADE"]
        for term in bold_terms:
            text = re.sub(f'(?i)({term})', r'<b>\1</b>', text)
        return text
    
    def get_current_date(self):
        meses = {
            "January": "Janeiro", "February": "Fevereiro", "March": "Março",
            "April": "Abril", "May": "Maio", "June": "Junho",
            "July": "Julho", "August": "Agosto", "September": "Setembro",
            "October": "Outubro", "November": "Novembro", "December": "Dezembro"
        }
        data_atual = datetime.now()
        mes_em_portugues = meses[data_atual.strftime("%B")]
        return data_atual.strftime(f"%d de {mes_em_portugues} de %Y")
    
    def desenhar_logos(self, c):
        largura, altura = A4
        # Inserir imagem no cabeçalho
        largura_imagem = 66  # Ajuste conforme necessário
        altura_imagem = 66    # Ajuste conforme necessário
        x_imagem = 20         # Posição X da imagem
        y_imagem = altura - 80  # Posição Y (ajustada para caber no cabeçalho)
        base_x = 105
        base_y = 40

        img_path = f"termo_qr_{self.numero}.png"

        # Abrir a imagem com PIL
        img = Image.open(img_path)

        # Esticar a imagem sem suavização (modo Nearest)
        new_width = img.width
        new_height = img.height

        img_resized = img.resize((new_width, new_height), Image.NEAREST)  # Mantém os pixels nítidos

        # Converter para ImageReader
        img_reader = ImageReader(img_resized)

        # Imagens
        # c.drawImage("saquarema_logo.png", x_imagem, y_imagem, width=largura_imagem, height=altura_imagem, mask='auto')
        # c.drawImage("logo_prefeitura_transp.png", x_imagem + 430, y_imagem + 10, width=(1800/6)/2.5, height=(601/6)/2.5, mask='auto')
        # c.drawImage("logo_educacao.png", x_imagem + 440, 34, width=(2778/30), height=(642/30), mask='auto')
        # c.drawImage("logo_sub_branco.png", x_imagem + 440, 8, width=(2210/30), height=(690/30), mask='auto')
        c.drawImage(img_reader, (largura - new_width) - 30, altura - (6 * cm), new_width, new_height, mask='auto')

    def criar_pdf_temp(self, nome_arquivo):
        largura, altura = A4  
        c = canvas.Canvas(nome_arquivo, pagesize=A4)

        # Estilos de texto
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=24,
            alignment=1,  
            spaceAfter=20,
            bold=True
        )
        custom_style = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=4,
            leading=14
        )
        custom_style2 = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
        )

        list_style = ParagraphStyle(
            "ListStyle",
            parent=styles["Normal"],
            fontSize=12,  
            leading=14,
            alignment=4  
        )

        base_sign_y = 8.6
        y_signature = base_sign_y * cm
        y_temp = (base_sign_y - 0.4) * cm
        x_positions = [1.2 * cm, 8 * cm, 15 * cm]
        for x in x_positions:
            c.line(x, y_signature, x + 5 * cm, y_signature)

        c.setFillColor("black")
        labels = [self.user_name, "Secretária de Educação", "Sub. de Tecnologia"]
        x_temp = 3.8
        c.setFont("Helvetica", 10)
        c.drawCentredString(x_temp * cm, y_temp, labels[0])
        c.drawCentredString(largura / 2, y_temp, labels[1])
        c.drawCentredString(largura - (x_temp * cm), y_temp, labels[2])

        title_paragraph = Paragraph(f"<b>{self.title}</b>", title_style)
        text_paragraph = Paragraph(self.first_paragraph, custom_style)
        timestamp = Paragraph(f"Saquarema, {self.get_current_date()}", custom_style2)

        list_items = [ListItem(Paragraph(f". {item}", list_style)) for i, item in enumerate(self.text_list)]
        numbered_list = ListFlowable(list_items, bulletType='1')

        frame = Frame(1 * cm, 5.5 * cm, 19 * cm, 20 * cm, showBoundary=False)
        frame.addFromList([title_paragraph, Spacer(1, 20), text_paragraph, Spacer(1, 20), numbered_list, Spacer(1, 20), timestamp], c)

        separator_y = 6.5
        c.setStrokeColor(gray)
        c.setDash(3, 3)
        c.line(1.2 * cm, separator_y * cm, 20 * cm, separator_y * cm)

        c.setDash(1, 0)
        c.setFont("Helvetica", 12)
        c.drawCentredString(largura / 2, (separator_y - 1.2) * cm, "Equipamento devolvido no dia _____ de _______________ de 202___")

        base_sign_y2 = 3.8
        c.setStrokeColor("black")
        y_signature2 = base_sign_y2 * cm
        y_temp2 = (base_sign_y2 - 0.4) * cm
        x_positions2 = [1.2 * cm, 8 * cm, 15 * cm]
        for x in x_positions2:
            c.line(x, y_signature2, x + 5 * cm, y_signature2)

        c.setFillColor("black")
        x_temp2 = 3.8
        c.setFont("Helvetica", 10)
        c.drawCentredString(x_temp2 * cm, y_temp2, labels[0])
        c.drawCentredString(largura / 2, y_temp2, labels[1])
        c.drawCentredString(largura - (x_temp2 * cm), y_temp2, labels[2])


        c.setFillColor(gray)
        # self.desenhar_logos(c)
        c.setFont("Helvetica", 8)
        c.drawString(505, altura - (6 * cm), f"Doc Nº{self.numero}")

        c.save()
        # self.delete_qr()

    def delete_qr(self):
        os.remove(f"termo_qr_{self.numero}.png")

    def merge_pdf(self, template_path, content_path, output_path):
        template_reader = PdfReader(template_path)
        content_reader = PdfReader(content_path)
        writer = PdfWriter()

        for i in range(len(template_reader.pages)):
            template_page = template_reader.pages[i]
            if i < len(content_reader.pages):
                content_page = content_reader.pages[i]
                template_page.merge_page(content_page)  # Mesclar conteúdo com template
            
            writer.add_page(template_page)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)
    
    def get_pdf_number(self):
        return self.numero
