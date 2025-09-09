import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import pandas as pd
from PIL import Image, ImageTk

# ======================
# CONFIG BASE DE DATOS
# ======================
def init_db():
    conn = sqlite3.connect("clinic.db")
    cur = conn.cursor()

    # Tabla de pacientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        primer_nombre TEXT,
        segundo_nombre TEXT,
        primer_apellido TEXT,
        segundo_apellido TEXT,
        cedula_tipo TEXT,
        cedula_numero TEXT,
        fecha_nacimiento TEXT,
        edad INTEGER,
        telefono_contacto TEXT,
        telefono_domicilio TEXT,
        direccion TEXT,
        seguro TEXT,
        poliza TEXT,
        responsable TEXT,
        antecedentes TEXT
    )
    """)

    # Tabla de citas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        especialidad TEXT,
        fecha TEXT,
        hora TEXT,
        doctor TEXT,
        motivo TEXT,
        FOREIGN KEY(paciente_id) REFERENCES patients(id)
    )
    """)

    conn.commit()
    conn.close()

# ======================
# LOGIN
# ======================
def attempt_login(user, pwd, root):
    if user == "mariana" and pwd == "1234":
        root.destroy()
        open_main_app()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# ======================
# APP PRINCIPAL
# ======================
def open_main_app():
    app = tk.Tk()
    app.title("Base de Datos Mariana Nuñez C.A")
    app.geometry("1000x700")
    app.configure(bg="#e6ecf0")

    # LOGO
    try:
        logo = Image.open("logo.png")  # usa el logo que adjuntaste
        logo = logo.resize((120, 120))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(app, image=logo_img, bg="#e6ecf0").pack(pady=5)
    except:
        tk.Label(app, text="LOGO", bg="#e6ecf0", font=("Arial", 16)).pack()

    # Título
    tk.Label(app, text="📋 Sistema de Gestión de Pacientes y Citas",
             font=("Arial", 18, "bold"), fg="white", bg="#2c3e50", pady=10).pack(fill="x")

    notebook = ttk.Notebook(app)
    
    notebook.pack(expand=True, fill="both")

    # ======================
    # FRAME PACIENTES
    # ======================
    frame_pacientes = tk.Frame(notebook, bg="#e6ecf0")
    notebook.add(frame_pacientes, text="Pacientes")

    tk.Label(frame_pacientes, text="Registro de Pacientes",
             font=("Arial", 14, "bold"), bg="#e6ecf0").pack(pady=10)

    form_frame = tk.Frame(frame_pacientes, bg="#e6ecf0")
    form_frame.pack()

    labels = ["Primer Nombre", "Segundo Nombre", "Primer Apellido", "Segundo Apellido",
              "Tipo Cédula (V/E)", "Número de Cédula", "Fecha Nacimiento", "Edad",
              "Teléfono Contacto", "Teléfono Domicilio", "Dirección",
              "Seguro", "Póliza", "Responsable", "Antecedentes Médicos"]

    entries = {}
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, bg="#e6ecf0").grid(row=i, column=0, sticky="w", pady=2)
        if label == "Fecha Nacimiento":
            entry = DateEntry(form_frame, width=18, background="blue", foreground="white", date_pattern="yyyy-mm-dd")
        elif label == "Tipo Cédula (V/E)":
            entry = ttk.Combobox(form_frame, values=["V", "E"], width=17)
        elif label == "Seguro":
            entry = ttk.Combobox(form_frame, values=["Particular", "Mercantil Seguros", "La Previsora",
                                                     "Seguros Caracas", "MAPFRE", "Humanitas"], width=17)
        else:
            entry = tk.Entry(form_frame, width=20)
        entry.grid(row=i, column=1, pady=2)
        entries[label] = entry

    def guardar_paciente():
        data = [e.get() for e in entries.values()]
        conn = sqlite3.connect("clinic.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
            cedula_tipo, cedula_numero, fecha_nacimiento, edad, telefono_contacto, telefono_domicilio,
            direccion, seguro, poliza, responsable, antecedentes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Paciente registrado correctamente")

    tk.Button(frame_pacientes, text="Guardar Paciente", bg="#2980b9", fg="white",
              command=guardar_paciente).pack(pady=10)

    # ======================
    # FRAME CITAS
    # ======================
    frame_citas = tk.Frame(notebook, bg="#e6ecf0")
    notebook.add(frame_citas, text="Citas")

    tk.Label(frame_citas, text="Agendar Cita Médica",
             font=("Arial", 14, "bold"), bg="#e6ecf0").pack(pady=10)

    citas_frame = tk.Frame(frame_citas, bg="#e6ecf0")
    citas_frame.pack()

    tk.Label(citas_frame, text="Paciente ID:", bg="#e6ecf0").grid(row=0, column=0, pady=5)
    paciente_id_entry = tk.Entry(citas_frame)
    paciente_id_entry.grid(row=0, column=1, pady=5)

    tk.Label(citas_frame, text="Especialidad:", bg="#e6ecf0").grid(row=1, column=0, pady=5)
    especialidad_cb = ttk.Combobox(citas_frame, values=[
        "Medicina Interna", "Medicina General", "Endocrinología", "Gastroenterología",
        "Dermatología", "Neurología", "Cardiología", "Otorrinolaringología",
        "Pediatría", "Neumología", "Urología", "Nefrología"])
    especialidad_cb.grid(row=1, column=1, pady=5)

    tk.Label(citas_frame, text="Fecha:", bg="#e6ecf0").grid(row=2, column=0, pady=5)
    fecha_cita = DateEntry(citas_frame, width=18, background="blue", foreground="white", date_pattern="yyyy-mm-dd")
    fecha_cita.grid(row=2, column=1, pady=5)

    tk.Label(citas_frame, text="Hora:", bg="#e6ecf0").grid(row=3, column=0, pady=5)
    hora_cb = ttk.Combobox(citas_frame, values=["09:00 AM", "10:00 AM", "11:00 AM",
                                                "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM"])
    hora_cb.grid(row=3, column=1, pady=5)

    tk.Label(citas_frame, text="Doctor:", bg="#e6ecf0").grid(row=4, column=0, pady=5)
    doctor_entry = tk.Entry(citas_frame)
    doctor_entry.grid(row=4, column=1, pady=5)

    tk.Label(citas_frame, text="Motivo:", bg="#e6ecf0").grid(row=5, column=0, pady=5)
    motivo_entry = tk.Entry(citas_frame)
    motivo_entry.grid(row=5, column=1, pady=5)

    def guardar_cita():
        conn = sqlite3.connect("clinic.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO appointments (paciente_id, especialidad, fecha, hora, doctor, motivo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (paciente_id_entry.get(), especialidad_cb.get(), fecha_cita.get(),
              hora_cb.get(), doctor_entry.get(), motivo_entry.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Cita agendada correctamente")

    tk.Button(frame_citas, text="Guardar Cita", bg="#2980b9", fg="white",
              command=guardar_cita).pack(pady=10)

    # ======================
    # EXPORTAR A EXCEL
    # ======================
    def exportar_excel():
        conn = sqlite3.connect("clinic.db")
        df = pd.read_sql_query("SELECT * FROM patients", conn)
        conn.close()
        df.to_excel("pacientes.xlsx", index=False)
        messagebox.showinfo("Exportado", "Datos exportados a pacientes.xlsx")

    tk.Button(app, text="Exportar Pacientes a Excel", bg="#27ae60", fg="white",
              command=exportar_excel).pack(pady=10)

    # COPYRIGHT
    tk.Label(app, text="© 2025 Mariana Nuñez 30079653",
             bg="#2c3e50", fg="white").pack(fill="x", side="bottom")

    app.mainloop()

# ======================
# LOGIN SCREEN
# ======================
def main():
    init_db()
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x250")
    root.configure(bg="#34495e")

    tk.Label(root, text="Usuario:", fg="white", bg="#34495e").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Contraseña:", fg="white", bg="#34495e").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Ingresar", bg="#2980b9", fg="white",
              command=lambda: attempt_login(username_entry.get(), password_entry.get(), root)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
