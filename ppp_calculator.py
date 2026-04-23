"""
Purchasing Power Parity (PPP) Calculator
Data: IMF World Economic Outlook, April 2025
PPP factors stored in data/ppp_data.json — update that file to refresh data.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "ppp_data.json"

HEADER_BG  = "#1e3a5f"
HEADER_FG  = "white"
HEADER_SUB = "#90cdf4"
APP_BG     = "#f0f4f8"
CARD_BG    = "#ffffff"
RESULT_BG  = "#ebf8ff"
RESULT_FG  = "#1a365d"
ACCENT     = "#2b6cb0"
MUTED      = "#718096"
DARK       = "#1a202c"
BORDER     = "#e2e8f0"
SEP        = "#bee3f8"


def load_data() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt(symbol: str, amount: float) -> str:
    """Format a currency amount with symbol and thousand separators."""
    return f"{symbol}{amount:,.2f}"


class PPPCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PPP Calculator")
        self.geometry("680x640")
        self.minsize(600, 580)
        self.configure(bg=APP_BG)

        try:
            raw = load_data()
        except FileNotFoundError:
            messagebox.showerror(
                "Data file missing",
                f"Could not find:\n{DATA_PATH}\n\nMake sure data/ppp_data.json exists."
            )
            self.destroy()
            return
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON error", f"Could not parse data file:\n{e}")
            self.destroy()
            return

        self.meta        = raw["metadata"]
        self.country_map = {c["country"]: c for c in raw["countries"]}
        self.countries   = sorted(self.country_map.keys())

        self._setup_styles()
        self._build_ui()
        self._set_defaults()

    # ── Styles ────────────────────────────────────────────────────────────────

    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure("TFrame",            background=APP_BG)
        s.configure("Card.TFrame",       background=CARD_BG,   relief="flat")
        s.configure("TLabelframe",       background=CARD_BG,   relief="groove", borderwidth=1)
        s.configure("TLabelframe.Label", background=CARD_BG,   font=("Segoe UI", 10, "bold"), foreground=DARK)
        s.configure("TLabel",            background=CARD_BG,   font=("Segoe UI", 10), foreground=DARK)
        s.configure("Muted.TLabel",      background=CARD_BG,   font=("Segoe UI", 9),  foreground=MUTED)
        s.configure("TRadiobutton",      background=CARD_BG,   font=("Segoe UI", 10), foreground=DARK)
        s.configure("TCombobox",         font=("Segoe UI", 10))
        s.configure("TEntry",            font=("Segoe UI", 11))
        s.configure(
            "Calc.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 9),
            background=ACCENT,
            foreground="white",
            borderwidth=0,
        )
        s.map("Calc.TButton",
              background=[("active", "#2c5282"), ("pressed", "#1a365d")],
              foreground=[("active", "white")])

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        body = tk.Frame(self, bg=APP_BG, padx=20, pady=16)
        body.pack(fill="both", expand=True)
        self._build_source_card(body)
        self._build_target_card(body)
        self._build_calc_button(body)
        self._build_results_card(body)

    def _build_header(self):
        hdr = tk.Frame(self, bg=HEADER_BG, padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Purchasing Power Parity Calculator",
                 font=("Segoe UI", 16, "bold"), bg=HEADER_BG, fg=HEADER_FG).pack()
        tk.Label(hdr,
                 text=f"Data: {self.meta['source']}  |  Year: {self.meta['year']}",
                 font=("Segoe UI", 9), bg=HEADER_BG, fg=HEADER_SUB).pack(pady=(2, 0))

    def _build_source_card(self, parent):
        lf = ttk.LabelFrame(parent, text="  Source — Your Country & Salary  ", padding=14)
        lf.pack(fill="x", pady=(0, 10))

        # Country row
        ttk.Label(lf, text="Country:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.src_var = tk.StringVar()
        src_cb = ttk.Combobox(lf, textvariable=self.src_var, values=self.countries,
                              state="readonly", width=32)
        src_cb.grid(row=0, column=1, sticky="w")
        src_cb.bind("<<ComboboxSelected>>", lambda _: self._on_country_change())

        self.src_currency_var = tk.StringVar()
        ttk.Label(lf, textvariable=self.src_currency_var, style="Muted.TLabel").grid(
            row=0, column=2, padx=(12, 0), sticky="w")

        # Salary row
        ttk.Label(lf, text="Salary:").grid(row=1, column=0, sticky="w", pady=(12, 0), padx=(0, 8))

        salary_f = ttk.Frame(lf)
        salary_f.grid(row=1, column=1, columnspan=2, sticky="w", pady=(12, 0))

        self.salary_var = tk.StringVar()
        entry = ttk.Entry(salary_f, textvariable=self.salary_var, width=18)
        entry.pack(side="left", padx=(0, 14))
        entry.bind("<Return>", lambda _: self._calculate())

        self.period_var = tk.StringVar(value="yearly")
        ttk.Radiobutton(salary_f, text="Yearly",  variable=self.period_var, value="yearly" ).pack(side="left", padx=(0, 6))
        ttk.Radiobutton(salary_f, text="Monthly", variable=self.period_var, value="monthly").pack(side="left")

    def _build_target_card(self, parent):
        lf = ttk.LabelFrame(parent, text="  Target — Compare To  ", padding=14)
        lf.pack(fill="x", pady=(0, 14))

        ttk.Label(lf, text="Country:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.tgt_var = tk.StringVar()
        tgt_cb = ttk.Combobox(lf, textvariable=self.tgt_var, values=self.countries,
                              state="readonly", width=32)
        tgt_cb.grid(row=0, column=1, sticky="w")
        tgt_cb.bind("<<ComboboxSelected>>", lambda _: self._on_country_change())

        self.tgt_currency_var = tk.StringVar()
        ttk.Label(lf, textvariable=self.tgt_currency_var, style="Muted.TLabel").grid(
            row=0, column=2, padx=(12, 0), sticky="w")

    def _build_calc_button(self, parent):
        btn_frame = tk.Frame(parent, bg=APP_BG)
        btn_frame.pack(fill="x", pady=(0, 14))
        ttk.Button(btn_frame, text="Calculate PPP Equivalent  ▶",
                   command=self._calculate, style="Calc.TButton").pack()

    def _build_results_card(self, parent):
        lf = ttk.LabelFrame(parent, text="  Results  ", padding=14)
        lf.pack(fill="both", expand=True)

        inner = tk.Frame(lf, bg=RESULT_BG, padx=16, pady=14, relief="flat")
        inner.pack(fill="both", expand=True)
        inner.columnconfigure(1, weight=1)

        # Your salary row
        tk.Label(inner, text="Your Salary:", font=("Segoe UI", 10),
                 bg=RESULT_BG, fg=MUTED, width=17, anchor="w").grid(row=0, column=0, sticky="w")
        self.res_src_var = tk.StringVar(value="—")
        tk.Label(inner, textvariable=self.res_src_var,
                 font=("Segoe UI", 11, "bold"), bg=RESULT_BG, fg=DARK).grid(
            row=0, column=1, sticky="w", padx=8)

        # PPP equivalent row
        tk.Label(inner, text="PPP Equivalent:", font=("Segoe UI", 10),
                 bg=RESULT_BG, fg=MUTED, width=17, anchor="w").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.res_tgt_var = tk.StringVar(value="—")
        tk.Label(inner, textvariable=self.res_tgt_var,
                 font=("Segoe UI", 14, "bold"), bg=RESULT_BG, fg=ACCENT).grid(
            row=1, column=1, sticky="w", padx=8, pady=(10, 0))

        # Separator
        tk.Frame(inner, bg=SEP, height=1).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=12)

        # Explanation
        self.res_note_var = tk.StringVar(
            value="Select source and target countries, enter a salary, then click Calculate.")
        tk.Label(inner, textvariable=self.res_note_var,
                 font=("Segoe UI", 9), bg=RESULT_BG, fg=MUTED,
                 wraplength=560, justify="left").grid(
            row=3, column=0, columnspan=2, sticky="w")

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _set_defaults(self):
        if "United States" in self.countries:
            self.src_var.set("United States")
        if "India" in self.countries:
            self.tgt_var.set("India")
        self._on_country_change()

    def _on_country_change(self):
        for country_var, label_var in [
            (self.src_var, self.src_currency_var),
            (self.tgt_var, self.tgt_currency_var),
        ]:
            name = country_var.get()
            if name in self.country_map:
                c = self.country_map[name]
                label_var.set(f"{c['symbol']}  {c['currency_name']}  ({c['currency']})")
            else:
                label_var.set("")

    def _calculate(self):
        src_name = self.src_var.get()
        tgt_name = self.tgt_var.get()

        if not src_name or not tgt_name:
            messagebox.showwarning("Missing selection", "Please select both a source and target country.")
            return

        raw = self.salary_var.get().replace(",", "").strip()
        if not raw:
            messagebox.showwarning("Missing salary", "Please enter a salary amount.")
            return

        try:
            salary = float(raw)
        except ValueError:
            messagebox.showerror("Invalid input", "Salary must be a number, e.g. 50000 or 4166.67")
            return

        if salary <= 0:
            messagebox.showerror("Invalid input", "Salary must be greater than zero.")
            return

        is_monthly = self.period_var.get() == "monthly"
        yearly  = salary * 12 if is_monthly else salary
        monthly = salary / 12 if not is_monthly else salary

        src = self.country_map[src_name]
        tgt = self.country_map[tgt_name]

        # Core PPP conversion:  equivalent = salary × (target_ppp / source_ppp)
        ratio       = tgt["ppp_factor"] / src["ppp_factor"]
        tgt_yearly  = yearly  * ratio
        tgt_monthly = monthly * ratio

        ss, ts = src["symbol"], tgt["symbol"]
        sc, tc = src["currency"], tgt["currency"]

        self.res_src_var.set(
            f"{fmt(ss, yearly)} / year     {fmt(ss, monthly)} / month"
        )
        self.res_tgt_var.set(
            f"{fmt(ts, tgt_yearly)} / year     {fmt(ts, tgt_monthly)} / month"
        )

        # Explanation note
        if ratio >= 1:
            rel = f"{ratio:.3f}× the nominal amount in {tgt_name}"
        else:
            rel = f"{1/ratio:.3f}× less in nominal terms in {tgt_name}"

        note = (
            f"PPP ratio ({tgt_name} ÷ {src_name}): {ratio:.4f}\n"
            f"Earning {fmt(ss, yearly)}/yr in {src_name} ({sc}) has the same purchasing power as "
            f"{fmt(ts, tgt_yearly)}/yr in {tgt_name} ({tc}).\n"
            f"Conversion: {fmt(ss, yearly)} ÷ {src['ppp_factor']} × {tgt['ppp_factor']} = {fmt(ts, tgt_yearly)}\n"
            f"Source: {self.meta['source']} (year: {self.meta['year']})"
        )
        self.res_note_var.set(note)


if __name__ == "__main__":
    app = PPPCalculatorApp()
    app.mainloop()
