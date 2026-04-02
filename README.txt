╔══════════════════════════════════════════════════════════════╗
║         ROOT FINDING CALCULATOR APP                          ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DESCRIPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  A fully-featured GUI-based Nonlinear Equation Solver
  built with Python and Tkinter. Uses four classical
  root-finding numerical methods to solve f(x) = 0.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [1] Root-Finding Methods:
      ✔  Bisection Method
      ✔  Newton-Raphson Method
      ✔  Secant Method
      ✔  False Position (Regula Falsi) Method

  [2] Extra Features:
      ✔  Graph / Plot of equation with root marker
      ✔  Step-by-step Iterations Table
      ✔  Error Analysis Display (with convergence plot)
      ✔  Export results to TXT and CSV files

  [3] Modern Colorful UI (Tkinter + Matplotlib)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Python  3.8 or higher

  Built-in (no install needed):
    - tkinter
    - math
    - csv

  Install with pip:
    pip install matplotlib numpy

  Command to install all at once:
    pip install matplotlib numpy


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW TO RUN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Step 1:  Install dependencies
           pip install matplotlib numpy

  Step 2:  Run the application
           python root_finding_calculator.py

  Step 3:  Enter an equation in f(x) form, e.g.
           x**3 - x - 2
           sin(x) - x/2
           exp(x) - 3*x

  Step 4:  Choose a method and set parameters, click SOLVE


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  EQUATION FORMAT (supported syntax)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  x**2          → x squared
  x**3          → x cubed
  sin(x)        → sine
  cos(x)        → cosine
  tan(x)        → tangent
  exp(x)        → e^x
  log(x)        → natural log (ln)
  log10(x)      → log base 10
  sqrt(x)       → square root
  pi            → π = 3.14159...
  e             → Euler's number

  Examples:
    x**3 - x - 2
    cos(x) - x
    x**2 - 4
    exp(x) - 3*x**2
    sin(x)*x - 1


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  METHODS — PARAMETER GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Bisection / False Position:
    a = lower bracket (f(a) and f(b) must have opposite signs)
    b = upper bracket

  Newton-Raphson:
    a = initial guess x₀
    b = (ignored)

  Secant:
    a = x₀  (first initial point)
    b = x₁  (second initial point)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROJECT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  root_finding_calculator.py   ← Main application file
  README.txt                   ← This file


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STUDENT INFO (fill before submission)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Name      : ______________________________
  Roll No.  : ______________________________
  Section   : ______________________________
  Semester  : 5th / 6th  (3rd Year)
  Subject   : Numerical Methods (23SMH-341)
  Project # : 3 — Root Finding Calculator App

══════════════════════════════════════════════════════════════
