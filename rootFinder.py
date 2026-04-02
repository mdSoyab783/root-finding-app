"""
╔══════════════════════════════════════════════════════════════╗
║   ROOT FINDING CALCULATOR                                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math, csv, time
from datetime import datetime

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

# ══════════════════════════════════════════════════════════════
#  DARK GOLD THEME  — Obsidian + Electric Gold + Teal
# ══════════════════════════════════════════════════════════════
T = {
    # Backgrounds — warm dark obsidian
    "bg_root":   "#1A1A2E",
    "bg_calc":   "#16213E",
    "bg_panel":  "#1E2A45",
    "bg_section":"#0F3460",
    "bg_input":  "#0A1628",
    "bg_output": "#1A1A2E",
    "bg_console":"#0D1B35",

    # Gold accent family
    "gold":      "#FFB800",
    "gold2":     "#FFC93C",
    "gold3":     "#FFD97D",
    "gold_dk":   "#A87700",
    "gold_glow": "#2A1F00",

    # Teal accent family
    "teal":      "#00E5CC",
    "teal2":     "#00B8A0",
    "teal_dk":   "#004A40",
    "teal_glow": "#001A16",

    # Red/orange for solve
    "crimson":   "#FF3D5A",
    "crimson2":  "#FF6B7A",
    "crimson_dk":"#8A0018",

    # Purple for methods
    "violet":    "#A855F7",
    "violet2":   "#C084FC",
    "violet_dk": "#3B0764",

    # LCD — cool blue-green
    "lcd_bg":    "#020F0D",
    "lcd_text":  "#00FFD4",
    "lcd_dim":   "#004A3A",

    # LED — warm gold
    "led_bg":    "#0A0800",
    "led_on":    "#FFB800",
    "led_bright":"#FFD97D",
    "led_dim":   "#2A1F00",

    # Buttons
    "btn_num":   "#1A1710",
    "btn_fn":    "#0D1A18",
    "btn_op":    "#1A1020",
    "btn_preset":"#100D1A",
    "btn_method":"#120A20",
    "btn_msel":  "#3B0764",
    "btn_exe":   "#8A1020",
    "btn_exe2":  "#B01830",
    "btn_clr":   "#1A0808",
    "btn_save":  "#081A14",

    # Text
    "t_white":   "#F5F0E8",
    "t_dim":     "#7A6A50",
    "t_gold":    "#FFB800",
    "t_teal":    "#00E5CC",
    "t_violet":  "#C084FC",
    "t_crimson": "#FF6B7A",
    "t_green":   "#4ADE80",
    "t_orange":  "#FB923C",

    # Borders
    "border":    "#2A2318",
    "border2":   "#1A1510",
    "b_gold":    "#FFB800",
    "b_teal":    "#00E5CC",
    "b_violet":  "#A855F7",
    "b_crimson": "#FF3D5A",
}

F = {
    "title":     ("Helvetica", 15, "bold"),
    "brand":     ("Helvetica", 18, "bold"),
    "model":     ("Courier New", 12, "bold"),
    "lcd_eq":    ("Courier New", 13, "bold"),
    "lcd_sm":    ("Courier New",  8),
    "led_big":   ("Courier New", 30, "bold"),
    "led_med":   ("Courier New", 12, "bold"),
    "led_sm":    ("Courier New",  9, "bold"),
    "btn":       ("Helvetica",   10, "bold"),
    "btn_sm":    ("Helvetica",    9, "bold"),
    "btn_xs":    ("Courier New",  8, "bold"),
    "entry":     ("Courier New", 11, "bold"),
    "lbl":       ("Helvetica",    9),
    "lbl_sm":    ("Helvetica",    8),
    "mono":      ("Courier New",  9),
    "mono_sm":   ("Courier New",  8),
    "tab":       ("Helvetica",    9, "bold"),
    "sec":       ("Helvetica",    7, "bold"),
    "heading":   ("Courier New", 10, "bold"),
}


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def _adj(col, d):
    try:
        r=int(col[1:3],16); g=int(col[3:5],16); b=int(col[5:7],16)
        return f"#{max(0,min(255,r+d)):02x}{max(0,min(255,g+d)):02x}{max(0,min(255,b+d)):02x}"
    except: return col

def hsep(parent, color, h=1, pady=0):
    tk.Frame(parent, bg=color, height=h).pack(fill="x", pady=pady)

def sec_lbl(parent, text, bg=None):
    tk.Label(parent, text=f"  ▸  {text}",
             font=F["sec"], bg=bg or T["bg_calc"],
             fg=T["t_dim"]).pack(anchor="w", padx=8, pady=(5,1))


# ══════════════════════════════════════════════════════════════
#  CANVAS BUTTON  (works on macOS)
# ══════════════════════════════════════════════════════════════
def cbutton(parent, text, face, fg, cmd=None,
            w=60, h=36, font=None, radius=4,
            border_col=None, tag=None):
    fnt  = font or F["btn_sm"]
    bcol = border_col or _adj(face, +40)
    cv   = tk.Canvas(parent, width=w, height=h,
                     bg=face, highlightthickness=1,
                     highlightbackground=bcol,
                     cursor="hand2")
    tid  = cv.create_text(w//2, h//2, text=text,
                           fill=fg, font=fnt,
                           anchor="center", justify="center")

    def _en(e):
        cv.config(bg=_adj(face,+22), highlightbackground=_adj(bcol,+30))
    def _lv(e):
        cv.config(bg=face, highlightbackground=bcol)
    def _pr(e):
        cv.config(bg=_adj(face,-18))
        cv.move(tid, 0, 1)
    def _rl(e):
        cv.config(bg=_adj(face,+22))
        cv.move(tid, 0, -1)
        if cmd: cmd()

    cv.bind("<Enter>",            _en)
    cv.bind("<Leave>",            _lv)
    cv.bind("<ButtonPress-1>",    _pr)
    cv.bind("<ButtonRelease-1>",  _rl)
    cv.tag_bind(tid,"<ButtonPress-1>",   _pr)
    cv.tag_bind(tid,"<ButtonRelease-1>", _rl)
    return cv


# ══════════════════════════════════════════════════════════════
#  NUMERICAL METHODS
# ══════════════════════════════════════════════════════════════
def safe_eval(expr, x):
    ns = {k: getattr(math,k) for k in dir(math) if not k.startswith("_")}
    ns["x"] = x
    return float(eval(expr, {"__builtins__":{}}, ns))

def derivative(expr, x, h=1e-7):
    return (safe_eval(expr,x+h)-safe_eval(expr,x-h))/(2*h)

def auto_bracket(expr, rng=(-20,20), n=600):
    xs = [rng[0]+i*(rng[1]-rng[0])/n for i in range(n+1)]
    vals=[]
    for xv in xs:
        try:    vals.append((xv, safe_eval(expr,xv)))
        except: vals.append((xv, None))
    for i in range(len(vals)-1):
        x0,f0=vals[i]; x1,f1=vals[i+1]
        if None in (f0,f1): continue
        if not(math.isfinite(f0) and math.isfinite(f1)): continue
        if f0*f1<0:
            a,b=round(x0,3),round(x1,3)
            return a,b,round((a+b)/2,3),True
    finite=[(x,f) for x,f in vals if f is not None and math.isfinite(f)]
    x0g=round(min(finite,key=lambda t:abs(t[1]))[0],3) if finite else 0.0
    return -1.0,1.0,x0g,False

def bisection(expr,a,b,tol,mx):
    st,fa,fb=[],safe_eval(expr,a),safe_eval(expr,b)
    if fa*fb>0: raise ValueError("f(a)·f(b) > 0 — no bracket.")
    for i in range(1,mx+1):
        c=(a+b)/2; fc=safe_eval(expr,c); err=abs(b-a)/2
        st.append((i,a,b,c,fc,err))
        if abs(fc)<tol or err<tol: return c,st
        if fa*fc<0: b,fb=c,fc
        else:       a,fa=c,fc
    return c,st

def newton_raphson(expr,x0,tol,mx):
    st,x=[],x0
    for i in range(1,mx+1):
        fx=safe_eval(expr,x); fpx=derivative(expr,x)
        if abs(fpx)<1e-14: raise ValueError("f'(x)≈0 — Newton failed.")
        xn=x-fx/fpx; err=abs(xn-x)
        st.append((i,x,fx,fpx,xn,err)); x=xn
        if err<tol and abs(fx)<tol: return x,st
    return x,st

def secant(expr,x0,x1,tol,mx):
    st=[]
    for i in range(1,mx+1):
        f0,f1=safe_eval(expr,x0),safe_eval(expr,x1)
        if abs(f1-f0)<1e-14: raise ValueError("Secant: division by zero.")
        x2=x1-f1*(x1-x0)/(f1-f0); err=abs(x2-x1)
        st.append((i,x0,x1,f0,f1,x2,err)); x0,x1=x1,x2
        if err<tol: return x2,st
    return x1,st

def false_pos(expr,a,b,tol,mx):
    st,fa,fb=[],safe_eval(expr,a),safe_eval(expr,b)
    if fa*fb>0: raise ValueError("f(a)·f(b) > 0 — no bracket.")
    for i in range(1,mx+1):
        c=b-fb*(b-a)/(fb-fa); fc=safe_eval(expr,c); err=abs(fc)
        st.append((i,a,b,c,fc,err))
        if abs(fc)<tol: return c,st
        if fa*fc<0: b,fb=c,fc
        else:       a,fa=c,fc
    return c,st


# ══════════════════════════════════════════════════════════════
#  ANIMATION HELPERS
# ══════════════════════════════════════════════════════════════
class Animator:
    """Simple value animator for smooth transitions."""
    def __init__(self, root):
        self.root = root
        self._jobs = {}

    def lerp_color(self, widget, attr, from_col, to_col,
                   duration=400, steps=20, done=None):
        key = id(widget)+hash(attr)
        if key in self._jobs:
            try: self.root.after_cancel(self._jobs[key])
            except: pass
        fr=int(from_col[1:3],16); fg=int(from_col[3:5],16); fb=int(from_col[5:7],16)
        tr=int(to_col[1:3],16);   tg=int(to_col[3:5],16);   tb=int(to_col[5:7],16)
        delay = duration // steps

        def _step(n):
            if n > steps:
                if done: done()
                return
            t = n/steps
            r=int(fr+(tr-fr)*t); g=int(fg+(tg-fg)*t); b=int(fb+(tb-fb)*t)
            col = f"#{r:02x}{g:02x}{b:02x}"
            try: widget.config(**{attr: col})
            except: return
            self._jobs[key] = self.root.after(delay, lambda: _step(n+1))
        _step(0)

    def pulse(self, widget, attr, col1, col2, times=3, period=300):
        """Flash a widget attribute between two colors (works for Label & Canvas)."""
        def _tog(n, cur):
            if n <= 0:
                try: widget.config(**{attr: col1})
                except: pass
                return
            try: widget.config(**{attr: cur})
            except: return
            nxt = col2 if cur == col1 else col1
            self.root.after(period//2, lambda: _tog(n-1, nxt))
        _tog(times*2, col1)

    def slide_in(self, frame, direction="down", duration=300):
        """Slide a frame into view."""
        pass  # placeholder for future use

    def typewriter(self, label, text, delay=40, done=None):
        """Animate text character by character."""
        def _type(i):
            if i > len(text):
                if done: done()
                return
            try: label.config(text=text[:i])
            except: return
            self.root.after(delay, lambda: _type(i+1))
        _type(0)

    def count_up(self, label, target, duration=800,
                 fmt="{:.8f}", prefix="", done=None):
        """Count up a number with animation."""
        steps = 30
        delay = duration // steps
        def _step(n):
            if n > steps:
                try: label.config(text=prefix + fmt.format(target))
                except: pass
                if done: done()
                return
            val = target * (n/steps)
            try: label.config(text=prefix + fmt.format(val))
            except: return
            self.root.after(delay, lambda: _step(n+1))
        _step(0)

    def blink_border(self, widget, color, times=3, speed=150):
        orig = widget.cget("highlightbackground")
        def _tog(n, show):
            if n<=0:
                try: widget.config(highlightbackground=orig)
                except: pass
                return
            col = color if show else orig
            try: widget.config(highlightbackground=col)
            except: return
            self.root.after(speed, lambda: _tog(n-1, not show))
        _tog(times*2, True)


# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════
class RootFinderApp:
    def __init__(self, root):
        self.root   = root
        self.anim   = Animator(root)
        self._result= self._steps = self._method = self._expr = None
        self._auto_job = None
        self._ab_lock  = False
        self._mbtn     = {}
        self._solving  = False

        root.title("fx-ROOT 991  ·  Numerical Methods  ·  23SMH-341")
        root.configure(bg=T["bg_root"])
        root.resizable(True, True)
        root.minsize(1100, 700)

        self._build()
        root.update_idletasks()
        sw,sh = root.winfo_screenwidth(), root.winfo_screenheight()
        w,h   = root.winfo_width(),       root.winfo_height()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        # startup animation
        self.root.after(200,  self._anim_startup)

    # ── STARTUP ANIMATION ─────────────────────────────────────
    def _anim_startup(self):
        # Animate the model name typewriter style
        self.anim.typewriter(self.lbl_model, "fx-ROOT 991", delay=60)
        # Pulse the border
        self.root.after(800, lambda: self.anim.blink_border(
            self._calc_border, T["b_gold"], times=2, speed=200))

    # ══════════════════════════════════════════════════════════
    def _build(self):
        desk = tk.Frame(self.root, bg=T["bg_root"], padx=14, pady=14)
        desk.pack(fill="both", expand=True)
        desk.columnconfigure(0, weight=0)
        desk.columnconfigure(1, weight=1)
        desk.rowconfigure(0, weight=1)
        self._build_calc(desk)
        self._build_output(desk)

    # ══════════════════════════════════════════════════════════
    #  CALCULATOR BODY
    # ══════════════════════════════════════════════════════════
    def _build_calc(self, parent):
        # Gold border wrapper
        wrap = tk.Frame(parent, bg=T["b_gold"], padx=2, pady=2)
        wrap.grid(row=0, column=0, sticky="ns", padx=(0,12))
        self._calc_border = wrap

        shell = tk.Frame(wrap, bg=T["bg_calc"])
        shell.pack(fill="both", expand=True)

        # ── HEADER ────────────────────────────────────────────
        hdr = tk.Frame(shell, bg=T["bg_calc"], pady=8)
        hdr.pack(fill="x", padx=12)

        # CU brand
        lf = tk.Frame(hdr, bg=T["bg_calc"])
        lf.pack(side="left")
        tk.Label(lf, text="CU", font=F["brand"],
                 bg=T["bg_calc"], fg=T["gold"]).pack(side="left")
        tk.Label(lf, text=" SCIENTIFIC",
                 font=("Helvetica",8), bg=T["bg_calc"],
                 fg=T["t_dim"]).pack(side="left", pady=(8,0))

        # model name — animated on startup
        self.lbl_model = tk.Label(hdr, text="",
                                   font=F["model"],
                                   bg=T["bg_calc"], fg=T["teal"])
        self.lbl_model.pack(side="left", padx=20)

        # right side: solar strip + dot
        rf = tk.Frame(hdr, bg=T["bg_calc"])
        rf.pack(side="right")
        self.dot = tk.Label(rf, text="●", font=("Helvetica",10),
                             bg=T["bg_calc"], fg=T["t_dim"])
        self.dot.pack(side="right", padx=(6,0))
        solar = tk.Frame(rf, bg=T["bg_calc"])
        solar.pack(side="right")
        cols = [T["gold_glow"], T["teal_dk"], T["gold_glow"],
                T["teal_dk"],   T["gold_glow"], T["teal_dk"],
                T["gold_glow"], T["teal_dk"]]
        for c in cols:
            tk.Frame(solar, bg=c, width=11,
                     height=18).pack(side="left", padx=1)

        # ── DUAL ACCENT LINES ─────────────────────────────────
        tk.Frame(shell, bg=T["gold"],  height=2).pack(fill="x")
        tk.Frame(shell, bg=T["teal"],  height=1).pack(fill="x")

        # ── LCD SCREEN ────────────────────────────────────────
        lcd_wrap = tk.Frame(shell, bg=T["bg_section"],
                             padx=8, pady=6)
        lcd_wrap.pack(fill="x")

        lcd_bz = tk.Frame(lcd_wrap, bg="#050A08", padx=3, pady=3,
                           highlightbackground=T["teal_dk"],
                           highlightthickness=1)
        lcd_bz.pack(fill="x")

        lcd = tk.Frame(lcd_bz, bg=T["lcd_bg"])
        lcd.pack(fill="x")

        sb = tk.Frame(lcd, bg=T["lcd_bg"])
        sb.pack(fill="x", padx=6, pady=(3,0))
        self.lbl_meth_lcd = tk.Label(sb, text="BISECTION",
                                      font=F["lcd_sm"],
                                      bg=T["lcd_bg"], fg=T["lcd_dim"])
        self.lbl_meth_lcd.pack(side="left")
        self.lbl_n_lcd = tk.Label(sb, text="n = --",
                                   font=F["lcd_sm"],
                                   bg=T["lcd_bg"], fg=T["lcd_dim"])
        self.lbl_n_lcd.pack(side="right")

        self.lbl_eq = tk.Label(lcd, text="f(x) = x**3 - x - 2",
                                font=F["lcd_eq"],
                                bg=T["lcd_bg"], fg=T["lcd_text"],
                                anchor="w")
        self.lbl_eq.pack(fill="x", padx=6, pady=(2,0))

        tk.Frame(lcd, bg=T["lcd_dim"], height=1).pack(fill="x", padx=6)

        ab_row = tk.Frame(lcd, bg=T["lcd_bg"])
        ab_row.pack(fill="x", padx=6, pady=(2,4))
        self.lbl_auto = tk.Label(ab_row, text="",
                                  font=F["lcd_sm"],
                                  bg=T["lcd_bg"], fg=T["lcd_dim"])
        self.lbl_auto.pack(side="left")
        self.lbl_conv_lcd = tk.Label(ab_row, text="",
                                      font=F["lcd_sm"],
                                      bg=T["lcd_bg"], fg=T["lcd_text"])
        self.lbl_conv_lcd.pack(side="right")

        # ── LED DISPLAY ───────────────────────────────────────
        led_wrap = tk.Frame(shell, bg=T["bg_section"], padx=8, pady=4)
        led_wrap.pack(fill="x")

        led_bz = tk.Frame(led_wrap, bg="#030200", padx=3, pady=3,
                           highlightbackground=T["gold_dk"],
                           highlightthickness=1)
        led_bz.pack(fill="x")

        led = tk.Frame(led_bz, bg=T["led_bg"])
        led.pack(fill="x")

        led_top = tk.Frame(led, bg=T["led_bg"])
        led_top.pack(fill="x", padx=10, pady=(5,0))
        tk.Label(led_top, text="ROOT  x =",
                 font=F["led_sm"], bg=T["led_bg"],
                 fg=T["led_dim"]).pack(side="left")
        self.lbl_conv_led = tk.Label(led_top, text="",
                                      font=F["led_sm"],
                                      bg=T["led_bg"], fg=T["t_green"])
        self.lbl_conv_led.pack(side="right")

        self.lbl_root = tk.Label(led,
                                  text="  -.  - - - - - - - - - -",
                                  font=F["led_big"],
                                  bg=T["led_bg"], fg=T["led_dim"],
                                  anchor="e")
        self.lbl_root.pack(fill="x", padx=10)

        led_bot = tk.Frame(led, bg=T["led_bg"])
        led_bot.pack(fill="x", padx=10, pady=(0,5))
        tk.Label(led_bot, text="f(root) =",
                 font=F["led_sm"], bg=T["led_bg"],
                 fg=T["led_dim"]).pack(side="left")
        self.lbl_froot = tk.Label(led_bot, text="---",
                                   font=F["led_sm"],
                                   bg=T["led_bg"], fg=T["gold"])
        self.lbl_froot.pack(side="left", padx=8)
        tk.Label(led_bot, text="iter =",
                 font=F["led_sm"], bg=T["led_bg"],
                 fg=T["led_dim"]).pack(side="right", padx=(0,4))
        self.lbl_itr = tk.Label(led_bot, text="--",
                                 font=F["led_med"],
                                 bg=T["led_bg"], fg=T["gold"])
        self.lbl_itr.pack(side="right")

        # ── INPUT FIELDS ──────────────────────────────────────
        tk.Frame(shell, bg=T["border"], height=1).pack(fill="x")
        iz = tk.Frame(shell, bg=T["bg_section"], padx=10, pady=6)
        iz.pack(fill="x")

        def mk_inp(lbl_txt, var, w=22):
            row = tk.Frame(iz, bg=T["bg_section"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=lbl_txt, font=F["lbl"], width=15,
                     bg=T["bg_section"], fg=T["t_dim"],
                     anchor="w").pack(side="left")
            e = tk.Entry(row, textvariable=var, font=F["entry"],
                         bg=T["bg_input"], fg=T["gold"],
                         insertbackground=T["gold2"],
                         selectbackground=T["gold_dk"],
                         relief="flat", bd=0, width=w,
                         highlightthickness=1,
                         highlightbackground=T["border"],
                         highlightcolor=T["gold"])
            e.pack(side="left", ipady=5)
            # animate focus
            e.bind("<FocusIn>",  lambda ev, en=e: en.config(
                highlightbackground=T["gold"],
                highlightthickness=2, fg=T["gold2"]))
            e.bind("<FocusOut>", lambda ev, en=e: en.config(
                highlightbackground=T["border"],
                highlightthickness=1, fg=T["gold"]))
            return e

        self.v_expr    = tk.StringVar(value="x**3 - x - 2")
        self.v_a       = tk.StringVar(value="1.0")
        self.v_b       = tk.StringVar(value="2.0")
        self.v_tol     = tk.StringVar(value="1e-6")
        self.v_maxiter = tk.StringVar(value="100")

        mk_inp("f(x)  =", self.v_expr, 24)
        self._ea = mk_inp("a / x₀  =", self.v_a)
        self._eb = mk_inp("b / x₁  =", self.v_b)
        mk_inp("Tolerance  =", self.v_tol)
        mk_inp("Max Iter  =", self.v_maxiter)

        self._hint_v = tk.StringVar(value="")
        tk.Label(iz, textvariable=self._hint_v,
                 font=F["lbl_sm"], bg=T["bg_section"],
                 fg=T["teal"], wraplength=340).pack(anchor="w")

        # ── Auto-bracket ──────────────────────────────────────
        self._auto_job = None; self._ab_lock = False

        def _run():
            expr = self.v_expr.get().strip()
            if len(expr) < 2:
                self.lbl_auto.config(text=""); return
            try:
                a,b,x0,found = auto_bracket(expr)
                self._ab_lock = True
                self.v_a.set(str(a)); self.v_b.set(str(b))
                self._ab_lock = False
                # animate: flash gold
                for e in [self._ea, self._eb]:
                    e.config(highlightbackground=T["gold"],
                              highlightthickness=2, fg=T["t_green"])
                self.root.after(1000, lambda: [
                    e.config(highlightbackground=T["border"],
                              highlightthickness=1, fg=T["gold"])
                    for e in [self._ea, self._eb]])
                self.lbl_auto.config(
                    text=f"✔  a={a}   b={b}   x₀≈{x0}" if found
                         else f"⚠  no bracket   x₀≈{x0}",
                    fg=T["lcd_text"] if found else T["t_orange"])
                self.lbl_eq.config(text=f"f(x) = {expr}")
                # animate LCD text color
                self.anim.lerp_color(self.lbl_eq, "fg",
                                      T["lcd_dim"], T["lcd_text"], 400)
            except:
                self._ab_lock = False
                self.lbl_auto.config(text="✗ invalid", fg=T["t_crimson"])

        def _sched(*_):
            if self._ab_lock: return
            if self._auto_job: self.root.after_cancel(self._auto_job)
            self._auto_job = self.root.after(600, _run)

        self.v_expr.trace_add("write", _sched)

        # ── METHOD BUTTONS ────────────────────────────────────
        tk.Frame(shell, bg=T["border"], height=1).pack(fill="x")
        sec_lbl(shell, "METHOD")

        mrow = tk.Frame(shell, bg=T["bg_calc"], padx=8)
        mrow.pack(fill="x", pady=(0,4))

        self.v_method = tk.StringVar(value="Bisection")
        for i,(lbl,val) in enumerate([
            ("BISEC","Bisection"),("NEWTON","Newton-Raphson"),
            ("SECANT","Secant"),("REG-F","False Position")]):
            b = cbutton(mrow, lbl, T["btn_method"], T["t_violet"],
                        cmd=lambda v=val: self._sel(v),
                        w=84, h=44, font=F["btn_sm"],
                        border_col=T["b_violet"])
            b.grid(row=0, column=i, padx=3, pady=3)
            self._mbtn[val] = b
        self._sel("Bisection")

        # ── FUNCTION KEYS ─────────────────────────────────────
        sec_lbl(shell, "FUNCTIONS")
        fr = tk.Frame(shell, bg=T["bg_calc"], padx=8)
        fr.pack(fill="x", pady=(0,2))
        fns=[("sin","sin(x)"),("cos","cos(x)"),("exp","exp(x)"),
             ("ln","log(x)"),("√","sqrt(x)"),("x²","x**2"),
             ("x³","x**3"),("π","pi")]
        for c,(lbl,fn) in enumerate(fns):
            cbutton(fr, lbl, T["btn_fn"], T["t_teal"],
                    cmd=lambda f=fn: self.v_expr.set(self.v_expr.get()+f),
                    w=50, h=32, font=F["btn_xs"],
                    border_col=T["teal_dk"]
                    ).grid(row=0, column=c, padx=2, pady=2)

        # ── PRESETS ───────────────────────────────────────────
        sec_lbl(shell, "QUICK EQUATIONS")
        pr = tk.Frame(shell, bg=T["bg_calc"], padx=8)
        pr.pack(fill="x", pady=(0,2))
        presets=[("x³-x-2","x**3-x-2"),("x²-4","x**2-4"),
                 ("cos-x","cos(x)-x"),("eˣ-3x","exp(x)-3*x**2"),
                 ("sin-x","sin(x)-x/2"),("x³+2x","x**3+2*x-1"),
                 ("x⁴-10","x**4-10"),("CLR","__CLR__")]
        for c,(lbl,ex) in enumerate(presets):
            isc = ex=="__CLR__"
            cbutton(pr, lbl,
                    T["btn_clr"] if isc else T["btn_preset"],
                    T["t_crimson"] if isc else T["t_violet"],
                    cmd=(lambda: self.v_expr.set("")) if isc
                        else (lambda e=ex: self.v_expr.set(e)),
                    w=50, h=30, font=F["btn_xs"],
                    border_col=T["b_crimson"] if isc else T["b_violet"]
                    ).grid(row=0, column=c, padx=2, pady=2)

        # ── NUMPAD ────────────────────────────────────────────
        sec_lbl(shell, "KEYPAD")
        kp = tk.Frame(shell, bg=T["bg_calc"], padx=8)
        kp.pack(fill="x", pady=(0,4))

        def ap(v): self.v_expr.set(self.v_expr.get()+v)
        def bk():  self.v_expr.set(self.v_expr.get()[:-1])

        krows = [
            [("7",T["btn_num"],T["t_white"],"7"),
             ("8",T["btn_num"],T["t_white"],"8"),
             ("9",T["btn_num"],T["t_white"],"9"),
             ("+",T["btn_op"], T["t_gold"]," + "),
             ("(",T["btn_op"], T["teal"],"("),
             (")",T["btn_op"], T["teal"],")"),
             ("**",T["btn_op"],T["t_violet"],"**"),
             ("DEL",T["btn_clr"],T["t_crimson"],"__DEL__")],
            [("4",T["btn_num"],T["t_white"],"4"),
             ("5",T["btn_num"],T["t_white"],"5"),
             ("6",T["btn_num"],T["t_white"],"6"),
             ("−",T["btn_op"], T["t_gold"]," - "),
             ("x",T["btn_fn"], T["t_teal"],"x"),
             ("e",T["btn_fn"], T["t_teal"],"e"),
             (".",T["btn_num"],T["t_white"],"."),
             ("AC",T["btn_clr"],T["t_crimson"],"__AC__")],
            [("1",T["btn_num"],T["t_white"],"1"),
             ("2",T["btn_num"],T["t_white"],"2"),
             ("3",T["btn_num"],T["t_white"],"3"),
             ("×",T["btn_op"], T["t_gold"]," * "),
             ("0",T["btn_num"],T["t_white"],"0"),
             ("-",T["btn_op"], T["t_gold"],"-"),
             ("÷",T["btn_op"], T["t_gold"]," / "),
             ("",  T["bg_calc"],T["bg_calc"],None)],
        ]
        for r,row in enumerate(krows):
            for c,(lbl,face,fg,val) in enumerate(row):
                if val is None: continue
                if val=="__DEL__": cmd=bk
                elif val=="__AC__": cmd=lambda: self.v_expr.set("")
                else: cmd=lambda v=val: ap(v)
                bc = T["b_crimson"] if "DEL" in lbl or "AC" in lbl else _adj(face,+35)
                cbutton(kp, lbl, face, fg, cmd=cmd,
                        w=50, h=34, font=F["btn_xs"],
                        border_col=bc
                        ).grid(row=r, column=c, padx=2, pady=2)

        # ── EXE BAR ───────────────────────────────────────────
        tk.Frame(shell, bg=T["gold"], height=2).pack(fill="x")
        exe = tk.Frame(shell, bg=T["bg_calc"], padx=8, pady=8)
        exe.pack(fill="x")

        # Animated SOLVE button
        self._solve_cv = cbutton(exe, "  ▶   EXE  /  SOLVE",
                                  T["btn_exe"], "#FFFFFF",
                                  cmd=self._solve,
                                  w=196, h=50,
                                  font=("Helvetica",11,"bold"),
                                  border_col=T["b_crimson"])
        self._solve_cv.pack(side="left", padx=(0,8))

        for lbl,face,fg,cmd in [
            ("CLR\nALL", T["btn_clr"], T["t_crimson"], self._clear_all),
            ("GRAPH",    T["btn_fn"],  T["t_teal"],    self._show_graph),
            ("TXT\nSAVE",T["btn_save"],T["t_green"],   self._export_txt),
            ("CSV\nSAVE",T["btn_save"],T["t_green"],   self._export_csv),
        ]:
            _f,_c,_cmd=face,fg,cmd
            cbutton(exe, lbl, _f, _c, cmd=_cmd,
                    w=56, h=50, font=F["btn_xs"],
                    border_col=_adj(_f,+40)
                    ).pack(side="left", padx=3)

        # ── FOOTER ────────────────────────────────────────────
        tk.Frame(shell, bg=T["gold_dk"], height=1).pack(fill="x")
        tk.Label(shell,
                 text="Chandigarh University  ·  BE CSE/IT 3rd Year  ·  Numerical Methods  ·  23SMH-341",
                 font=("Helvetica",7),
                 bg=T["bg_calc"], fg=T["t_dim"]).pack(pady=4)

    # ══════════════════════════════════════════════════════════
    #  OUTPUT PANEL
    # ══════════════════════════════════════════════════════════
    def _build_output(self, parent):
        # Teal border
        bwrap = tk.Frame(parent, bg=T["b_teal"], padx=2, pady=2)
        bwrap.grid(row=0, column=1, sticky="nsew")

        right = tk.Frame(bwrap, bg=T["bg_output"])
        right.pack(fill="both", expand=True)

        # title bar
        tbar = tk.Frame(right, bg=T["bg_output"])
        tbar.pack(fill="x")
        tk.Label(tbar, text="  ◈  OUTPUT CONSOLE",
                 font=("Helvetica",10,"bold"),
                 bg=T["bg_output"], fg="#FFD700").pack(side="left", pady=8)
        self.lbl_status = tk.Label(tbar, text="● READY",
                                    font=("Helvetica",8,"bold"),
                                    bg=T["bg_output"], fg=T["t_dim"])
        self.lbl_status.pack(side="right", padx=12)

        tk.Frame(right, bg=T["gold"], height=2).pack(fill="x")
        tk.Frame(right, bg=T["teal"], height=1).pack(fill="x")

        # notebook
        sty = ttk.Style(self.root)
        sty.theme_use("clam")
        sty.configure("O.TNotebook",
                       background=T["bg_output"], borderwidth=0)
        sty.configure("O.TNotebook.Tab",
                       background="#0F3460",
                       foreground="#8BAFD4",
                       font=F["tab"],
                       padding=[14,6])
        sty.map("O.TNotebook.Tab",
                background=[("selected", "#1B4F8A")],
                foreground=[("selected", "#FFD700")])
        sty.configure("O.TFrame", background=T["bg_output"])

        self.nb = ttk.Notebook(right, style="O.TNotebook")
        self.nb.pack(fill="both", expand=True)

        self.t_res = ttk.Frame(self.nb, style="O.TFrame")
        self.t_gr  = ttk.Frame(self.nb, style="O.TFrame")
        self.t_it  = ttk.Frame(self.nb, style="O.TFrame")
        self.t_err = ttk.Frame(self.nb, style="O.TFrame")

        self.nb.add(self.t_res, text="  RESULT  ")
        self.nb.add(self.t_gr,  text="  GRAPH  ")
        self.nb.add(self.t_it,  text="  ITERATIONS  ")
        self.nb.add(self.t_err, text="  ERROR ANALYSIS  ")

        self._mk_result()
        self._mk_graph()
        self._mk_iters()
        self._mk_error()

    # ── tabs ──────────────────────────────────────────────────
    def _mk_result(self):
        f = self.t_res
        self.res_txt = tk.Text(f, font=F["mono"],
                                bg=T["bg_console"], fg="#E8F4FD",
                                relief="flat", bd=0,
                                state="disabled", wrap="word",
                                padx=18, pady=14,
                                insertbackground=T["gold"],
                                selectbackground=T["gold_dk"])
        sb = tk.Scrollbar(f, command=self.res_txt.yview,
                           bg=T["bg_console"],
                           troughcolor=T["bg_section"], width=8)
        self.res_txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.res_txt.pack(fill="both", expand=True)
        for tag,col,fnt in [
            ("ROOT", "#FFD700",  ("Courier New",22,"bold")),
            ("OK",   "#00FF9F",  F["mono"]),
            ("ERR",  "#FF5F7E",  F["mono"]),
            ("HEAD", "#00E5FF",  F["heading"]),
            ("DIM",  "#8BAFD4",  F["mono"]),
            ("VAL",  "#FFC107",  F["mono"]),
            ("EQ",   "#64FFDA",  F["mono"]),
        ]:
            self.res_txt.tag_configure(tag, foreground=col, font=fnt)

    def _mk_graph(self):
        f = self.t_gr
        if not HAS_PLOT:
            tk.Label(f, text="pip install matplotlib numpy",
                     bg=T["bg_output"], fg=T["t_crimson"],
                     font=F["mono"]).pack(expand=True)
            return
        ctrl = tk.Frame(f, bg=T["bg_section"], pady=5)
        ctrl.pack(fill="x", padx=8, pady=(6,0))
        tk.Label(ctrl, text="  x range:", font=F["lbl"],
                 bg=T["bg_section"], fg=T["t_dim"]).pack(side="left")
        for attr,dv in [("_gxmin","-5"),("_gxmax","5")]:
            v = tk.StringVar(value=dv)
            setattr(self, attr+"_v", v)
            tk.Entry(ctrl, textvariable=v, font=F["entry"],
                     bg=T["bg_input"], fg=T["gold"],
                     insertbackground=T["gold"],
                     relief="flat", bd=0, width=5,
                     highlightthickness=1,
                     highlightbackground=T["border"],
                     highlightcolor=T["gold"]
                     ).pack(side="left", padx=4, ipady=4)
        cbutton(ctrl, "PLOT", T["btn_exe2"], "#FFF",
                cmd=self._plot_btn, w=64, h=30,
                font=F["btn_sm"],
                border_col=T["b_crimson"]).pack(side="left", padx=8)

        self.fig, self.ax = plt.subplots(facecolor=T["bg_output"])
        self.ax.set_facecolor(T["bg_console"])
        self.canvas = FigureCanvasTkAgg(self.fig, master=f)
        self.canvas.get_tk_widget().pack(fill="both", expand=True,
                                          padx=8, pady=8)

    def _mk_iters(self):
        f = self.t_it
        sty = ttk.Style(self.root)
        sty.configure("IT.Treeview",
                       background=T["bg_section"],
                       fieldbackground=T["bg_section"],
                       foreground="#E8F4FD", rowheight=24,
                       font=F["mono_sm"])
        sty.configure("IT.Treeview.Heading",
                       background=T["bg_console"],
                       foreground="#00E5FF", font=F["btn_sm"])
        sty.map("IT.Treeview",
                background=[("selected", T["gold_glow"])])
        frm = tk.Frame(f, bg=T["bg_output"])
        frm.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree = ttk.Treeview(frm, show="headings",
                                  style="IT.Treeview", height=32)
        vsb = ttk.Scrollbar(frm, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frm, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.tag_configure("e", background=T["bg_section"])
        self.tree.tag_configure("o", background=T["bg_input"])
        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def _mk_error(self):
        f = self.t_err
        self.err_txt = tk.Text(f, font=F["mono"],
                                bg=T["bg_console"], fg="#E8F4FD",
                                relief="flat", bd=0,
                                state="disabled", wrap="word",
                                padx=12, pady=8)
        sb = tk.Scrollbar(f, command=self.err_txt.yview,
                           bg=T["bg_console"],
                           troughcolor=T["bg_section"], width=8)
        self.err_txt.configure(yscrollcommand=sb.set)
        for tag,col in [("H","#00E5FF"),("V","#FFC107"),
                         ("G","#00FF9F"),("B","#FF5F7E"),
                         ("D","#8BAFD4")]:
            self.err_txt.tag_configure(tag, foreground=col)
        sb.pack(side="right", fill="y")
        self.err_txt.pack(fill="both", expand=True)
        if HAS_PLOT:
            self.efig,self.eax = plt.subplots(facecolor=T["bg_output"],
                                               figsize=(5,2.6))
            self.eax.set_facecolor(T["bg_console"])
            self.ecanv = FigureCanvasTkAgg(self.efig, master=f)
            self.ecanv.get_tk_widget().pack(fill="x", padx=8, pady=(0,8))

    # ══════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════
    def _sel(self, m):
        self.v_method.set(m)
        for v,b in self._mbtn.items():
            b.config(bg=T["btn_msel"] if v==m else T["btn_method"])
        hints = {
            "Newton-Raphson":"NR: uses x₀ (field a) — field b ignored.",
            "Secant":        "Secant: x₀ = a,  x₁ = b",
        }
        self._hint_v.set(hints.get(m,""))
        self.lbl_meth_lcd.config(text=m.upper()[:14])
        # animate: pulse the selected button
        btn = self._mbtn[m]
        self.anim.blink_border(btn, T["b_gold"], times=2, speed=120)

    def _w(self, wid, txt, tag=""):
        wid.configure(state="normal")
        wid.insert("end", txt, tag) if tag else wid.insert("end", txt)
        wid.configure(state="disabled")

    def _clr(self, w):
        w.configure(state="normal"); w.delete("1.0","end")
        w.configure(state="disabled")

    def _clear_all(self):
        self._clr(self.res_txt); self._clr(self.err_txt)
        for r in self.tree.get_children(): self.tree.delete(r)
        self.lbl_root.config(text="  -.  - - - - - - - - - -",
                              fg=T["led_dim"])
        self.lbl_froot.config(text="---")
        self.lbl_itr.config(text="--")
        self.lbl_n_lcd.config(text="n = --")
        self.lbl_conv_lcd.config(text="")
        self.lbl_conv_led.config(text="")
        self.lbl_status.config(text="● READY", fg=T["t_dim"])
        self._result=self._steps=self._method=self._expr=None
        # animate dot back to dim
        self.anim.lerp_color(self.dot, "fg", T["t_green"], T["t_dim"], 600)
        if HAS_PLOT:
            self.ax.cla();   self.canvas.draw()
            self.eax.cla();  self.ecanv.draw()

    # ── SOLVING ANIMATION ─────────────────────────────────────
    def _anim_solving(self):
        """Animate the SOLVE button and status while computing."""
        self.lbl_status.config(text="⟳ COMPUTING...", fg=T["teal"])
        # pulse the LED display
        self.anim.pulse(self.lbl_root, "fg", T["led_dim"], T["gold"],
                        times=2, period=300)
        # flash solve button border
        self.anim.blink_border(self._solve_cv, T["gold"], times=3, speed=150)

    def _anim_done(self, root_val, ok):
        """Animate result appearing after solve."""
        # count up the root value
        self.anim.count_up(self.lbl_root, root_val,
                            duration=600, fmt="{:+.8f}", prefix="  ")
        # power dot goes green
        self.anim.lerp_color(self.dot, "fg", T["t_dim"], T["t_green"], 400)
        # flash the LED border
        self.anim.blink_border(self.lbl_root, T["gold"] if ok else T["t_crimson"],
                                times=3, speed=120)
        # status label
        self.lbl_status.config(
            text="✔ CONVERGED" if ok else "⚠ LIMIT",
            fg=T["t_green"] if ok else T["t_orange"])

    # ══════════════════════════════════════════════════════════
    #  SOLVE
    # ══════════════════════════════════════════════════════════
    def _solve(self):
        self._clear_all()
        expr   = self.v_expr.get().strip()
        method = self.v_method.get()
        try:
            a   = float(self.v_a.get())
            b   = float(self.v_b.get())
            tol = float(self.v_tol.get())
            mx  = int(self.v_maxiter.get())
        except:
            messagebox.showerror("Input Error","Check parameters."); return

        self.lbl_eq.config(text=f"f(x) = {expr}")
        self._anim_solving()

        rt = self.res_txt
        W  = lambda t,tag="": self._w(rt,t,tag)

        W("━"*54+"\n","HEAD")
        W(f"  {method}\n","HEAD")
        W(f"  f(x) = {expr}\n","EQ")
        W("━"*54+"\n","HEAD")

        try: safe_eval(expr, a)
        except Exception as e:
            W(f"\n  ✗  Invalid expression:\n  {e}\n","ERR")
            self.lbl_status.config(text="✗ ERROR", fg=T["t_crimson"])
            return

        try:
            if   method=="Bisection":      root,st=bisection(expr,a,b,tol,mx)
            elif method=="Newton-Raphson": root,st=newton_raphson(expr,a,tol,mx)
            elif method=="Secant":         root,st=secant(expr,a,b,tol,mx)
            else:                          root,st=false_pos(expr,a,b,tol,mx)

            fr=safe_eval(expr,root); ok=abs(fr)<tol

            W(f"\n  ✔  ROOT FOUND\n\n","OK")
            W("  x  ≈  ","DIM")
            W(f"{root:.10f}\n","ROOT")
            W(f"\n  f(root)    =  ","DIM"); W(f"{fr:.6e}\n","VAL")
            W(f"  Iterations =  {len(st)}\n")
            W(f"  Tolerance  =  {tol}\n")
            W(f"  Method     =  {method}\n")
            W(f"\n  Converged? ","DIM")
            W("  ✔  YES\n\n" if ok else "  ✗  LIMIT REACHED\n\n",
              "OK" if ok else "ERR")

            # update static labels
            self.lbl_froot.config(text=f"{fr:.3e}")
            self.lbl_itr.config(text=str(len(st)))
            self.lbl_n_lcd.config(text=f"n={len(st)}")
            self.lbl_conv_lcd.config(
                text="✔ OK" if ok else "⚠ LIM",
                fg=T["lcd_text"] if ok else T["t_orange"])
            self.lbl_conv_led.config(
                text="✔ CONV" if ok else "⚠ LIM",
                fg=T["t_green"] if ok else T["t_crimson"])

            # ANIMATED result display
            self._anim_done(root, ok)

        except ValueError as e:
            W(f"\n  ✗  {e}\n","ERR")
            self.lbl_status.config(text="✗ ERROR", fg=T["t_crimson"])
            return
        except Exception as e:
            W(f"\n  ✗  {e}\n","ERR")
            self.lbl_status.config(text="✗ ERROR", fg=T["t_crimson"])
            return

        self._result=root; self._steps=st
        self._method=method; self._expr=expr

        self._fill_iters(st, method)
        self._fill_errors(st, root)
        self._do_plot()
        self.nb.select(self.t_res)

    # ── Iterations ────────────────────────────────────────────
    def _fill_iters(self, steps, method):
        for r in self.tree.get_children(): self.tree.delete(r)
        if method in ("Bisection","False Position"):
            cols=("Iter","a","b","c (mid)","f(c)","Error")
        elif method=="Newton-Raphson":
            cols=("Iter","xₙ","f(xₙ)","f'(xₙ)","xₙ₊₁","Error")
        else:
            cols=("Iter","x₀","x₁","f(x₀)","f(x₁)","x₂","Error")
        self.tree["columns"]=cols
        cw=max(90,760//len(cols))
        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=cw,anchor="center",minwidth=70)
        for i,row in enumerate(steps):
            fmt=tuple(f"{v:.8g}" if isinstance(v,float) else str(v) for v in row)
            self.tree.insert("","end",values=fmt,
                             tags=("e" if i%2==0 else "o",))

    # ── Error ─────────────────────────────────────────────────
    def _fill_errors(self, steps, root):
        et=self.err_txt
        W=lambda t,tag="": self._w(et,t,tag)
        errs=[r[-1] for r in steps]
        W("━"*50+"\n","H"); W("  ERROR ANALYSIS REPORT\n","H"); W("━"*50+"\n","H")
        W(f"\n  Method     : {self._method}\n")
        W(f"  Iterations : {len(steps)}\n")
        W(f"  Root       : ","D"); W(f"{root:.10f}\n","V")
        W(f"  f(root)    : ","D"); W(f"{safe_eval(self._expr,root):.4e}\n","V")
        W(f"\n  {'#':<5}{'Abs Error':<24}{'Rel Error':<24}\n","D")
        W("  "+"─"*48+"\n","D")
        for i,err in enumerate(errs,1):
            rel=abs(err/root) if root!=0 else float("inf")
            W(f"  {i:<5}{err:<24.6e}{rel:<24.6e}\n","G" if err<1e-4 else "B")
        W(f"\n  Init err   : {errs[0]:.6e}\n")
        W(f"  Final err  : {errs[-1]:.6e}\n","V")
        if len(errs)>1:
            W(f"  Reduction  : {errs[0]/(errs[-1]+1e-300):.2e}×\n","V")
        if HAS_PLOT and len(errs)>1:
            self.eax.cla()
            its=list(range(1,len(errs)+1))
            self.eax.semilogy(its,errs,color=T["gold"],
                               marker="o",markersize=4,
                               linewidth=2.2,label="Abs Error")
            self.eax.fill_between(its,errs,alpha=0.12,color=T["gold"])
            self.eax.set_title("Error Convergence",
                                color=T["t_dim"],fontsize=9,
                                fontfamily="Courier New")
            self.eax.set_xlabel("Iteration",color=T["t_dim"],fontsize=8)
            self.eax.set_ylabel("Error",    color=T["t_dim"],fontsize=8)
            self.eax.tick_params(colors=T["t_dim"],labelsize=7)
            for sp in self.eax.spines.values(): sp.set_color(T["border"])
            self.eax.legend(facecolor=T["bg_section"],
                             labelcolor=T["t_dim"],fontsize=8)
            self.eax.grid(True,color=T["border"],linewidth=0.4,ls="--")
            self.ecanv.draw()

    # ── Graph ─────────────────────────────────────────────────
    def _show_graph(self):
        if not self._expr:
            messagebox.showinfo("Graph","Solve first."); return
        self._do_plot(); self.nb.select(self.t_gr)

    def _plot_btn(self):
        if not self._expr:
            messagebox.showinfo("Graph","Solve first."); return
        self._do_plot(); self.nb.select(self.t_gr)

    def _do_plot(self):
        if not HAS_PLOT or not self._expr: return
        try:
            xmn=float(getattr(self,"_gxmin_v").get())
            xmx=float(getattr(self,"_gxmax_v").get())
        except: xmn,xmx=-5,5
        self.ax.cla()
        xs=np.linspace(xmn,xmx,700)
        ys=[]
        for xv in xs:
            try:    ys.append(safe_eval(self._expr,float(xv)))
            except: ys.append(float("nan"))
        ys=np.clip(np.array(ys),-1e4,1e4)
        self.ax.plot(xs,ys,color=T["teal"],linewidth=2.2,
                     label=f"f(x)={self._expr}")
        self.ax.fill_between(xs,ys,alpha=0.08,color=T["teal"])
        self.ax.axhline(0,color=T["border"],linewidth=0.8,ls="--")
        self.ax.axvline(0,color=T["border"],linewidth=0.8,ls="--")
        if self._result is not None:
            try:
                yr=safe_eval(self._expr,self._result)
                # vertical dashed drop line
                self.ax.plot([self._result,self._result],
                              [float(np.nanmin(ys)),yr],
                              color=T["gold"],linewidth=1,ls=":")
                self.ax.plot(self._result,yr,"o",
                              color=T["gold"],markersize=12,zorder=6,
                              label=f"root ≈ {self._result:.5f}")
                self.ax.annotate(f"  x ≈ {self._result:.5f}",
                                  xy=(self._result,yr),
                                  color=T["gold2"],fontsize=9,
                                  fontweight="bold",
                                  fontfamily="Courier New")
            except: pass
        self.ax.set_title(f"f(x) = {self._expr}",
                           color=T["t_dim"],fontsize=10,
                           fontfamily="Courier New")
        self.ax.set_xlabel("x",    color=T["t_dim"],fontsize=9)
        self.ax.set_ylabel("f(x)", color=T["t_dim"],fontsize=9)
        self.ax.tick_params(colors=T["t_dim"])
        for sp in self.ax.spines.values(): sp.set_color(T["border"])
        self.ax.legend(facecolor=T["bg_section"],
                        labelcolor=T["t_dim"],fontsize=9)
        self.ax.grid(True,color=T["border"],linewidth=0.5,ls="--")
        self.canvas.draw()

    # ── Export ────────────────────────────────────────────────
    def _lines(self):
        if not self._steps: return []
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        L=["="*60,
           "  ROOT FINDING CALCULATOR  ·  fx-ROOT 991  ·  CU",
           f"  Exported: {ts}","="*60,
           f"  Method  : {self._method}",
           f"  f(x)    : {self._expr}",
           f"  Root    : {self._result:.10f}",
           f"  f(root) : {safe_eval(self._expr,self._result):.4e}",
           f"  Iters   : {len(self._steps)}","",
           "ITERATIONS:", "-"*60]
        for r in self._steps:
            L.append("  "+"  |  ".join(
                f"{v:.8g}" if isinstance(v,float) else str(v) for v in r))
        L.append("="*60)
        return L

    def _export_txt(self):
        if not self._steps:
            messagebox.showwarning("Export","Solve first."); return
        p=filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text","*.txt")],
                                        initialfile="root_result.txt")
        if not p: return
        with open(p,"w") as f: f.write("\n".join(self._lines()))
        messagebox.showinfo("Saved",f"Saved:\n{p}")

    def _export_csv(self):
        if not self._steps:
            messagebox.showwarning("Export","Solve first."); return
        p=filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV","*.csv")],
                                        initialfile="root_result.csv")
        if not p: return
        with open(p,"w",newline="") as f:
            w=csv.writer(f)
            w.writerow(["Method",self._method])
            w.writerow(["f(x)",self._expr])
            w.writerow(["Root",self._result])
            w.writerow([])
            w.writerows(self._steps)
        messagebox.showinfo("Saved",f"Saved:\n{p}")


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = RootFinderApp(root)
    root.mainloop()
