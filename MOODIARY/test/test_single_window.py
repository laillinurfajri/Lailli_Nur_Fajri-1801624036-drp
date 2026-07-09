# tests/test_single_window.py
import tkinter as tk
import pytest
from views.daily_journal_view import render_daily_journal
from views.mood_tracker_view import render_mood_tracker
from views.todo_list_view import render_todo_list
from views.wish_list_view import render_wish_list
from views.quotes_view import render_quote
from views.analytics_view import render_statistik
from views.settings_view import render_settings
from views.register_view import render_register
import core.database as database




def test_single_window_renderers():
    database.init_db()
    database.set_active_user("test_user_sw")


    root = tk.Tk()
    root.withdraw()


    try:
        container = tk.Frame(root)
        container.pack()


        renderers = [
            render_daily_journal,
            render_mood_tracker,
            render_todo_list,
            render_wish_list,
            render_quote,
            render_statistik,
            lambda c, on_back_callback: render_settings(c, "test_user_sw", None, None, on_back_callback),
            render_register
        ]


        for renderer in renderers:
            for widget in container.winfo_children():
                widget.destroy()


            renderer(container, on_back_callback=lambda: None)
            assert len(container.winfo_children()) > 0, "Renderer harus membuat widget anak di dalam kontainer."


    finally:
        root.destroy()
