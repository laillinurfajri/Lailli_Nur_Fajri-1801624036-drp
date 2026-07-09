# settings.py
# ==============================================================================
# MOODIARY - SETTINGS & PREFERENCES CENTER (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import core.i18n as language
import core.database as database


from core.theme import (
    BG_PINK, BG_CARD_YELLOW, BG_WHITE,
    PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER,
    SECONDARY_PINK,
    ACCENT_PINK, ACCENT_DARK,
    TEXT_DARK, TEXT_MUTED,
    BORDER_YELLOW,
    BTN_SAVE, BTN_DELETE,
    FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY, FONT_SMALL,
    center_window, configure_ttk_styles, create_back_header
)




def render_settings(parent_container, current_username=None, callback_refresh_lang=None, callback_refresh_user=None, on_back_callback=None):
    """
    Merender antarmuka Pengaturan di dalam parent_container (Single-Window).
    """
    configure_ttk_styles()


    # ==================================
    # HEADER DENGAN TOMBOL KEMBALI
    # ==================================
    create_back_header(
        parent_container,
        language.get_text("settings_header_title"),
        language.get_text("settings_header_sub"),
        on_back_callback
    )


    # WRAPPER CONTENT DENGAN 2 KOLOM (KIRI & KANAN)
    content_area = tk.Frame(parent_container, bg=BG_PINK)
    content_area.pack(fill="both", expand=True, padx=36, pady=16)


    col_left = tk.Frame(content_area, bg=BG_PINK)
    col_left.pack(side="left", fill="both", expand=True, padx=(0, 12))


    col_right = tk.Frame(content_area, bg=BG_PINK)
    col_right.pack(side="left", fill="both", expand=True, padx=(12, 0))


    # =========================================================
    # KOLOM KIRI 1: BAHASA
    # =========================================================
    card_lang = tk.Frame(
        col_left,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        highlightbackground=BORDER_YELLOW,
        highlightthickness=1
    )
    card_lang.pack(fill="x", pady=(0, 16))


    tk.Label(
        card_lang,
        text=language.get_text("settings_lang_card_title"),
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", padx=20, pady=(16, 8))


    lang_var = tk.StringVar(value=language.LANG)


    radio_frame = tk.Frame(card_lang, bg=BG_CARD_YELLOW)
    radio_frame.pack(fill="x", padx=20, pady=(4, 18))


    def ganti_bahasa():
        bahasa_baru = lang_var.get()
        language.set_language(bahasa_baru)
        if callback_refresh_lang:
            callback_refresh_lang()
        # Segera muat ulang antarmuka pengaturan dengan bahasa baru
        for child in parent_container.winfo_children():
            child.destroy()
        render_settings(parent_container, current_username, callback_refresh_lang, callback_refresh_user, on_back_callback)
        messagebox.showinfo(
            language.get_text("success"),
            language.get_text("settings_lang_changed_msg")
        )


    tk.Radiobutton(
        radio_frame,
        text=language.get_text("lang_id"),
        variable=lang_var,
        value="ID",
        bg=BG_CARD_YELLOW,
        font=FONT_BODY,
        cursor="hand2",
        command=ganti_bahasa
    ).pack(side="left", padx=(0, 24))


    tk.Radiobutton(
        radio_frame,
        text=language.get_text("lang_en"),
        variable=lang_var,
        value="EN",
        bg=BG_CARD_YELLOW,
        font=FONT_BODY,
        cursor="hand2",
        command=ganti_bahasa
    ).pack(side="left")


    # =========================================================
    # KOLOM KIRI 2: PRIVASI & BACKUP DATA
    # =========================================================
    card_data = tk.Frame(
        col_left,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        highlightbackground=BORDER_YELLOW,
        highlightthickness=1
    )
    card_data.pack(fill="x", pady=(0, 16))


    tk.Label(
        card_data,
        text=language.get_text("settings_privacy_card_title"),
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", padx=20, pady=(16, 6))


    tk.Label(
        card_data,
        text=language.get_text("settings_privacy_desc"),
        font=FONT_SMALL,
        bg=BG_CARD_YELLOW,
        fg=TEXT_MUTED,
        wraplength=420,
        justify="left"
    ).pack(anchor="w", padx=20, pady=(0, 14))


    # Tombol Export & Import JSON
    json_frame = tk.Frame(card_data, bg=BG_CARD_YELLOW)
    json_frame.pack(fill="x", padx=20, pady=(0, 14))


    def aksi_export_json():
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Export Database JSON"
        )
        if path:
            database.export_user_data_to_json(path)
            messagebox.showinfo(
                language.get_text("export_success_title"),
                language.get_text("export_success_msg", path=path)
            )


    def aksi_import_json():
        path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            title="Import Database JSON"
        )
        if path:
            konf = messagebox.askyesno(
                language.get_text("import_confirm_title"),
                language.get_text("import_confirm_msg")
            )
            try:
                database.import_user_data_from_json(path, replace_existing=konf)
                messagebox.showinfo(
                    language.get_text("import_success_title"),
                    language.get_text("import_success_msg")
                )
            except Exception as e:
                messagebox.showerror(
                    language.get_text("import_error_title"),
                    language.get_text("import_error_msg", err=str(e))
                )


    tk.Button(
        json_frame,
        text=language.get_text("settings_btn_export"),
        command=aksi_export_json,
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 9, "bold"),
        fg=TEXT_DARK,
        bd=1,
        relief="solid",
        cursor="hand2",
        padx=14,
        pady=7
    ).pack(side="left", padx=(0, 12))


    tk.Button(
        json_frame,
        text=language.get_text("settings_btn_import"),
        command=aksi_import_json,
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 9, "bold"),
        fg=TEXT_DARK,
        bd=1,
        relief="solid",
        cursor="hand2",
        padx=14,
        pady=7
    ).pack(side="left")


    # Separator
    tk.Frame(card_data, bg=BORDER_YELLOW, height=1).pack(fill="x", padx=20, pady=10)


    def reset_data_user():
        konfirmasi = messagebox.askyesno(
            language.get_text("reset_warn_title"),
            language.get_text("reset_warn_msg")
        )
        if not konfirmasi:
            return


        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM journal")
        cursor.execute("DELETE FROM mood")
        cursor.execute("DELETE FROM todo")
        cursor.execute("DELETE FROM wish")
        conn.commit()
        conn.close()


        messagebox.showinfo(
            language.get_text("reset_done_title"),
            language.get_text("reset_done_msg")
        )


    tk.Button(
        card_data,
        text=language.get_text("settings_btn_reset"),
        command=reset_data_user,
        bg=BTN_DELETE,
        activebackground="#EF9A9A",
        font=("Segoe UI", 9, "bold"),
        fg=TEXT_DARK,
        bd=1,
        relief="solid",
        cursor="hand2",
        pady=9
    ).pack(fill="x", padx=20, pady=(4, 18))


    # =========================================================
    # KOLOM KANAN: MANAJEMEN AKUN & KEAMANAN
    # =========================================================
    card_account = tk.Frame(
        col_right,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        highlightbackground=BORDER_YELLOW,
        highlightthickness=1
    )
    card_account.pack(fill="both", expand=True, pady=(0, 16))


    tk.Label(
        card_account,
        text=language.get_text("settings_account_card_title"),
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", padx=20, pady=(16, 4))


    tk.Label(
        card_account,
        text=language.get_text("settings_active_account", name=current_username or '-'),
        font=("Segoe UI", 10, "bold"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", padx=20, pady=(0, 14))


    # Bagian Ganti Username
    tk.Label(
        card_account,
        text=language.get_text("settings_change_username_lbl"),
        font=("Segoe UI", 9, "bold"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", padx=20, pady=(0, 6))


    form_u = tk.Frame(card_account, bg=BG_CARD_YELLOW)
    form_u.pack(fill="x", padx=20, pady=(0, 16))


    entry_new_user = tk.Entry(form_u, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1, width=24)
    entry_new_user.pack(side="left", ipady=4, padx=(0, 10))


    def simpan_username():
        nama_baru = entry_new_user.get().strip()
        if not nama_baru:
            messagebox.showwarning("Peringatan", "Username baru tidak boleh kosong.")
            return


        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET username=? WHERE username=?",
                (nama_baru, current_username)
            )
            conn.commit()
            conn.close()


            # Rename file database agar data dipertahankan
            database.rename_user_db(current_username, nama_baru)


            if callback_refresh_user:
                callback_refresh_user(nama_baru)


            messagebox.showinfo("Berhasil", f"🎉 Username berhasil diperbarui menjadi '{nama_baru}'!\nSeluruh data Anda telah dipertahankan.")
            if on_back_callback:
                on_back_callback()
        except sqlite3.IntegrityError:
            conn.close()
            messagebox.showerror("Error", "Username tersebut sudah digunakan oleh pengguna lain.")


    tk.Button(
        form_u,
        text=language.get_text("settings_btn_save_username"),
        command=simpan_username,
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 9, "bold"),
        fg=TEXT_DARK,
        bd=1,
        relief="solid",
        cursor="hand2",
        padx=14,
        pady=5
    ).pack(side="left")


    # Separator
    tk.Frame(card_account, bg=BORDER_YELLOW, height=1).pack(fill="x", padx=20, pady=12)


    # Bagian Ganti Password
    tk.Label(
        card_account,
        text=language.get_text("settings_change_password_lbl"),
        font=("Segoe UI", 9, "bold"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", padx=20, pady=(0, 10))


    form_p = tk.Frame(card_account, bg=BG_CARD_YELLOW)
    form_p.pack(fill="x", padx=20, pady=(0, 20))


    tk.Label(form_p, text=language.get_text("settings_old_password_lbl"), font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=6)
    entry_old_pass = tk.Entry(form_p, show="•", font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1, width=26)
    entry_old_pass.grid(row=0, column=1, padx=12, pady=6, ipady=4)


    tk.Label(form_p, text=language.get_text("settings_new_password_lbl"), font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_MUTED).grid(row=1, column=0, sticky="w", pady=6)
    entry_new_pass = tk.Entry(form_p, show="•", font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1, width=26)
    entry_new_pass.grid(row=1, column=1, padx=12, pady=6, ipady=4)


    tk.Label(form_p, text=language.get_text("settings_conf_password_lbl"), font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=6)
    entry_conf_pass = tk.Entry(form_p, show="•", font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1, width=26)
    entry_conf_pass.grid(row=2, column=1, padx=12, pady=6, ipady=4)


    def simpan_password():
        old_p = entry_old_pass.get().strip()
        new_p = entry_new_pass.get().strip()
        conf_p = entry_conf_pass.get().strip()


        if not old_p or not new_p or not conf_p:
            messagebox.showwarning("Peringatan", "Harap isi semua kolom password lama dan baru.")
            return


        if len(new_p) < 6:
            messagebox.showwarning("Peringatan", "Password baru minimal 6 karakter.")
            return


        if new_p != conf_p:
            messagebox.showwarning("Peringatan", "Konfirmasi password baru tidak cocok.")
            return


        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (current_username, old_p)
        )
        row = cursor.fetchone()
        if not row:
            conn.close()
            messagebox.showerror("Gagal", "Password lama yang Anda masukkan salah.")
            return


        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_p, current_username)
        )
        conn.commit()
        conn.close()


        entry_old_pass.delete(0, tk.END)
        entry_new_pass.delete(0, tk.END)
        entry_conf_pass.delete(0, tk.END)
        messagebox.showinfo("Berhasil", "🎉 Password akun berhasil diubah dengan aman!")


    tk.Button(
        form_p,
        text=language.get_text("settings_btn_save_password"),
        command=simpan_password,
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 10, "bold"),
        fg=ACCENT_PINK,
        bd=1,
        relief="solid",
        cursor="hand2",
        pady=8
    ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 0))




def buka_pengaturan(root_win, current_username=None, callback_refresh_lang=None, callback_refresh_user=None, on_back_callback=None):
    # Backward compatible call / single-window support
    if isinstance(root_win, tk.Frame):
        render_settings(root_win, current_username, callback_refresh_lang, callback_refresh_user, on_back_callback)
    else:
        win = tk.Toplevel(root_win)
        win.title(f"{language.get_text('settings_header_title')} - Moodiary")
        win.configure(bg=BG_PINK)
        center_window(win, 680, 640)
        render_settings(win, current_username, callback_refresh_lang, callback_refresh_user, None)

