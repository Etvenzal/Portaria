import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime
import os
import json

DADOS_ARQUIVO = "registros.txt"

def salvar_registro(tipo, nome, celular, whatsapp):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    registro = {
        "tipo": tipo,
        "nome": nome,
        "celular": celular,
        "whatsapp": whatsapp,
        "data_hora": data_hora
    }
    with open(DADOS_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro) + "\n")

def gerar_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Relatório de Entrada - {data}", ln=True, align="C")

    tipos = {"Associado": [], "Aluno": [], "Day Use": [], "Vôlei": []}

    if not os.path.exists(DADOS_ARQUIVO):
        messagebox.showerror("Erro", "Nenhum dado encontrado para gerar o PDF.")
        return

    with open(DADOS_ARQUIVO, "r", encoding="utf-8") as f:
        for linha in f:
            registro = json.loads(linha)
            data_registro = registro["data_hora"].split(" ")[0]
            if data_registro == data:
                if registro["tipo"] in tipos:
                    tipos[registro["tipo"]].append(registro)

    pdf.set_font("Arial", "", 12)
    for tipo, pessoas in tipos.items():
        if pessoas:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"- {tipo}s", ln=True)
            pdf.set_font("Arial", "", 12)
            for pessoa in pessoas:
                linha = f"{pessoa['nome']} - {pessoa['celular']} - {pessoa['data_hora'].split(' ')[1]}"
                if pessoa["whatsapp"].lower() == "sim":
                    celular_limpo = ''.join(filter(str.isdigit, pessoa["celular"]))
                    link = f"https://wa.me/55{celular_limpo}"
                    linha += f" - WhatsApp: {link}"
                pdf.cell(0, 10, linha, ln=True)

    nome_arquivo = f"Relatorio_Entrada_{data.replace('/', '-')}.pdf"
    pdf.output(nome_arquivo)
    messagebox.showinfo("Sucesso", f"PDF gerado com sucesso: {nome_arquivo}")

def enviar_dados():
    tipo = tipo_var.get()
    nome = nome_entry.get()
    celular = celular_entry.get()
    whatsapp = whatsapp_var.get()

    if not nome or not celular:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    salvar_registro(tipo, nome, celular, whatsapp)
    nome_entry.delete(0, tk.END)
    celular_entry.delete(0, tk.END)
    whatsapp_var.set("Não")
    messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")

def gerar_pdf_gui():
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    gerar_pdf(data_hoje)

# Interface Gráfica
janela = tk.Tk()
janela.title("Controle de Portaria")
janela.geometry("400x300")

tk.Label(janela, text="Tipo de Entrada:").pack()
tipo_var = tk.StringVar(janela)
tipo_var.set("Associado")
tk.OptionMenu(janela, tipo_var, "Associado", "Aluno", "Day Use", "Vôlei").pack()

tk.Label(janela, text="Nome:").pack()
nome_entry = tk.Entry(janela)
nome_entry.pack()

tk.Label(janela, text="Celular (com DDD):").pack()
celular_entry = tk.Entry(janela)
celular_entry.pack()

tk.Label(janela, text="É WhatsApp?").pack()
whatsapp_var = tk.StringVar(janela)
whatsapp_var.set("Não")
tk.OptionMenu(janela, whatsapp_var, "Sim", "Não").pack()

tk.Button(janela, text="Registrar Entrada", command=enviar_dados).pack(pady=10)
tk.Button(janela, text="Gerar PDF de Hoje", command=gerar_pdf_gui).pack(pady=5)

janela.mainloop()
