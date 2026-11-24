"""A simple desktop AI chat assistant (Jarvis).

Needs an OpenAI API key in the OPENAI_API_KEY environment variable.
Uses only Python's standard library, including tkinter for the window.
"""

import json
import os
import threading
import urllib.error
import urllib.request
import tkinter as tk
from tkinter import messagebox


API_URL = "https://api.openai.com/v1/responses"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
INSTRUCTIONS = (
    "You are Jarvis, a friendly and helpful assistant. "
    "Answer clearly and naturally. If you are unsure, say so."
)


class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis - AI Chat")
        self.root.geometry("760x620")
        self.root.minsize(520, 420)
        self.root.configure(bg="#101820")
        self.history = []
        self.busy = False

        header = tk.Frame(root, bg="#101820", padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(
            header, text="JARVIS", bg="#101820", fg="#69d9ff",
            font=("Segoe UI", 20, "bold")
        ).pack(side="left")
        tk.Label(
            header, text="AI CHAT ASSISTANT", bg="#101820", fg="#a9bac6",
            font=("Segoe UI", 10)
        ).pack(side="left", padx=12, pady=(6, 0))
        tk.Button(
            header, text="New chat", command=self.new_chat,
            bg="#243440", fg="white", activebackground="#344c5c",
            activeforeground="white", relief="flat", padx=12, pady=6
        ).pack(side="right")

        self.chat = tk.Text(
            root, wrap="word", state="disabled", bg="#17232d", fg="#edf5fa",
            insertbackground="white", relief="flat", padx=18, pady=16,
            font=("Segoe UI", 11), spacing1=4, spacing3=10
        )
        self.chat.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self.chat.tag_configure("you", foreground="#69d9ff", font=("Segoe UI", 10, "bold"))
        self.chat.tag_configure("jarvis", foreground="#8fe3a1", font=("Segoe UI", 10, "bold"))
        self.chat.tag_configure("body", foreground="#edf5fa")
        self.chat.tag_configure("note", foreground="#a9bac6", font=("Segoe UI", 10, "italic"))

        bottom = tk.Frame(root, bg="#101820", padx=14, pady=(0, 14))
        bottom.pack(fill="x")
        self.entry = tk.Text(
            bottom, height=3, wrap="word", bg="#243440", fg="white",
            insertbackground="white", relief="flat", padx=12, pady=10,
            font=("Segoe UI", 11)
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.enter_to_send)
        self.entry.bind("<Shift-Return>", lambda event: None)
        self.send_button = tk.Button(
            bottom, text="Send", command=self.send_message,
            bg="#087eaa", fg="white", activebackground="#0b98ca",
            activeforeground="white", relief="flat", padx=18, pady=10,
            font=("Segoe UI", 10, "bold")
        )
        self.send_button.pack(side="right", padx=(10, 0), anchor="s")

        self.add_line("Jarvis", "Hello! Ask me a question to get started.", "jarvis")
        if not os.getenv("OPENAI_API_KEY"):
            self.add_line(
                "Setup", "Add your OpenAI API key to OPENAI_API_KEY, then restart this app.", "note"
            )

    def add_line(self, speaker, text, tag):
        self.chat.configure(state="normal")
        self.chat.insert("end", speaker + "\n", tag)
        self.chat.insert("end", text + "\n\n", "body" if tag != "note" else "note")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def enter_to_send(self, event):
        if not (event.state & 0x0001):  # Shift+Enter inserts a new line.
            self.send_message()
            return "break"

    def send_message(self):
        if self.busy:
            return
        message = self.entry.get("1.0", "end").strip()
        if not message:
            return
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            messagebox.showinfo(
                "API key needed",
                "Set the OPENAI_API_KEY environment variable, then restart Jarvis."
            )
            return

        self.entry.delete("1.0", "end")
        self.add_line("You", message, "you")
        self.history.append({"role": "user", "content": message})
        self.busy = True
        self.send_button.configure(state="disabled", text="...")
        self.add_line("Jarvis", "Thinking...", "note")
        threading.Thread(target=self.ask_api, args=(api_key,), daemon=True).start()

    def ask_api(self, api_key):
        payload = {
            "model": MODEL,
            "instructions": INSTRUCTIONS,
            "input": self.history,
        }
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
            answer = "\n".join(
                part["text"]
                for item in result.get("output", [])
                if item.get("type") == "message"
                for part in item.get("content", [])
                if part.get("type") == "output_text" and "text" in part
            ).strip()
            if not answer:
                answer = "I couldn't find a text answer in the API response."
            self.history.append({"role": "assistant", "content": answer})
            self.root.after(0, self.finish_reply, answer, None)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            self.root.after(0, self.finish_reply, None, f"API error ({error.code}): {detail}")
        except urllib.error.URLError as error:
            self.root.after(0, self.finish_reply, None, f"Connection problem: {error.reason}")
        except Exception as error:
            self.root.after(0, self.finish_reply, None, f"Something went wrong: {error}")

    def finish_reply(self, answer, error):
        # Remove the temporary “Thinking...” message before showing the result.
        self.chat.configure(state="normal")
        content = self.chat.get("1.0", "end-1c")
        marker = "Jarvis\nThinking...\n\n"
        if content.endswith(marker):
            self.chat.delete(f"end-{len(marker)}c", "end-1c")
        self.chat.configure(state="disabled")
        if error:
            # Remove this unanswered turn from the conversation so it can be retried.
            if self.history and self.history[-1].get("role") == "user":
                self.history.pop()
            self.add_line("Jarvis", error, "note")
        else:
            self.add_line("Jarvis", answer, "jarvis")
        self.busy = False
        self.send_button.configure(state="normal", text="Send")
        self.entry.focus_set()

    def new_chat(self):
        if self.busy:
            return
        self.history.clear()
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self.add_line("Jarvis", "New chat started. What would you like to ask?", "jarvis")


if __name__ == "__main__":
    window = tk.Tk()
    app = JarvisApp(window)
    window.mainloop()
