"""Make equations and symbols render in Word (R2 formatting fix).

1. Display equations of Chapter 3 ($$ ... $$ (3.n)) were written with Unicode
   symbols inside TeX delimiters; pandoc cannot convert them to Word equations,
   so they rendered as blank lines. Each is replaced by hand-written LaTeX with
   the same content (checked by equation number).
2. Inline symbols written as x_{t}, C_{miss}(k), x^{ctx}_{1} are converted to
   pandoc subscript/superscript markup (x~t~, C~miss~, x^ctx^~1~), outside code.
3. In Chapters 1, 4, 5 and 6 a whitelist of plain symbols (λ_impl, C_miss, ...)
   is converted the same way.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "revision_R2", "chapters_md")

EQ = {
    "3.1": r"s_t = \beta_0 + \beta^{\top} x_t, \qquad \tilde{p}_t = \sigma(s_t) = \frac{1}{1+\exp(-s_t)}",
    "3.2": r"(\hat{\beta}_0, \hat{\beta}) = \arg\max_{\beta_0,\beta} \sum_{i \in D_{\mathrm{fit}}} \left[ y_i \ln \tilde{p}_i + (1-y_i)\ln(1-\tilde{p}_i) \right] - \lambda \lVert \beta \rVert_2^2",
    "3.3": r"p_t = \sigma(\gamma_1 s_t + \gamma_0), \qquad \gamma_1 > 0",
    "3.4": r"(\hat{\gamma}_1, \hat{\gamma}_0) = \arg\min_{\gamma_1,\gamma_0} \; -\sum_{i \in D_{\mathrm{cal}}} \left[ y_i \ln p_i + (1-y_i)\ln(1-p_i) \right]",
    "3.5": r"L(\mathrm{Modify},1,k) = r_{\mathrm{mod}}(k)\, C_{\mathrm{miss}}(k) + \bigl(1-r_{\mathrm{mod}}(k)\bigr)\cdot 0 = r_{\mathrm{mod}}(k)\, C_{\mathrm{miss}}(k)",
    "3.6": r"R_t(v) = (1-p_t)\, L(v,0,k_t) + p_t\, L(v,1,k_t), \qquad v \in \mathcal{V}(a_t)",
    "3.7": r"v_t = \arg\min_{v \in \mathcal{V}(a_t)} R_t(v)",
    "3.8": r"\pi_{v,v'}(k) = \frac{\Delta_0}{\Delta_0 + \Delta_1}",
    "3.9": r"p^{*}_k = \frac{C_{\mathrm{FA}}(k)}{C_{\mathrm{FA}}(k) + C_{\mathrm{miss}}(k)}",
    "3.10": r"C_{\mathrm{esc}} < \frac{C_{\mathrm{FA}}(k)\, C_{\mathrm{miss}}(k)}{C_{\mathrm{FA}}(k) + C_{\mathrm{miss}}(k)}",
    "3.11": r"\phi_{t,i} = \beta_i \,(x_{t,i} - \bar{x}_i),\; i = 1,\dots,d; \qquad \phi_0 = \beta_0 + \beta^{\top}\bar{x}",
    "3.12": r"\phi_0 + \sum_{i=1}^{d} \phi_{t,i} = s_t",
    "3.13": r"\Phi_J = \sum_{i \in I_J} \phi_{t,i}, \qquad J \in \{\mathrm{ctx}, \mathrm{beh}, \mathrm{act}\}",
    "3.14": r"\theta(\alpha) = \min\{\theta : \mathrm{FPR}_{\mathrm{val}}(\theta) \le \alpha\}, \qquad \mathrm{FPR}_{\mathrm{val}}(\theta) = \frac{\left|\{ i \in D^{\mathrm{benign}}_{\mathrm{val}} : p_i \ge \theta \}\right|}{\left|D^{\mathrm{benign}}_{\mathrm{val}}\right|}",
    "3.15": r"\ell_t = e_t \ln\frac{q_1}{q_0} + (1-e_t) \ln\frac{1-q_1}{1-q_0}",
    "3.16": r"G_t = \max(0,\, G_{t-1} + \ell_t), \qquad G_0 = 0",
    "3.17": r"T_A = \min\{ t : G_t \ge h_G \}",
    "3.18": r"\mathrm{FA}_{\mathrm{ep}}(h_G) = \frac{\left|\{ j \in E_{\mathrm{ben}} : \max_t G^{(j)}_t \ge h_G \}\right|}{\left|E_{\mathrm{ben}}\right|}",
    "3.19": r"\tau_d = T_A - \nu, \qquad T_A \ge \nu",
    "3.20": r"\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \left| \bar{y}(B_m) - \bar{p}(B_m) \right|, \qquad B_m = \{ i : (m-1)/M < p_i \le m/M \}",
    "3.21": r"\mathrm{LL} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \ln p_i + (1-y_i)\ln(1-p_i) \right]",
    "3.22": r"\bar{L}(L_e) = \frac{1}{N} \sum_{i=1}^{N} L_e(v_i, y_i, k_i)",
}


def esc(t):
    return t.replace("\\", "\\\\").replace(" ", "\\ ").replace("*", "\\*").replace("~", "\\~").replace("^", "\\^")


TOKEN = re.compile(r"((?:_\{[^{}\n]*\}|\^\{[^{}\n]*\})+)")


def inline(line):
    def conv(m):
        out = []
        for part in re.findall(r"[_^]\{[^{}\n]*\}", m.group(1)):
            body = esc(part[2:-1])
            out.append(f"~{body}~" if part[0] == "_" else f"^{body}^")
        return "".join(out)
    # leave inline code spans untouched
    pieces = re.split(r"(`[^`]*`)", line)
    return "".join(p if p.startswith("`") else TOKEN.sub(conv, p) for p in pieces)


WHITELIST = [("λ_impl", "λ~impl~"), ("C_miss", "C~miss~"), ("C_FA", "C~FA~"), ("C_mod", "C~mod~"), ("C_esc", "C~esc~"),
             ("α_blk", "α~blk~"), ("α_mod", "α~mod~"), ("k_D2", "k~D2~"), ("r_mod", "r~mod~"), ("𝒯_R", "𝒯~R~"),
             ("D_train", "D~train~"), ("θ(α_blk)", "θ(α~blk~)")]


def plain(line):
    pieces = re.split(r"(`[^`]*`)", line)
    res = []
    for p in pieces:
        if not p.startswith("`"):
            for a, b in WHITELIST:
                p = p.replace(a, b)
        res.append(p)
    return "".join(res)


def process(path, ch3):
    lines = open(path, encoding="utf-8").read().split("\n")
    out, fenced, n_eq = [], False, 0
    for ln in lines:
        if ln.startswith("```"):
            fenced = not fenced
            out.append(ln)
            continue
        if fenced:
            out.append(ln)
            continue
        m = re.match(r"^\$\$ (.*) \$\$ \((3\.\d+)\)\s*$", ln)
        if ch3 and m:
            num = m.group(2)
            out.append(f"$$ {EQ[num]} \\qquad ({num}) $$")
            n_eq += 1
            continue
        out.append(inline(ln) if ch3 else plain(ln))
    open(path, "w", encoding="utf-8").write("\n".join(out))
    return n_eq


if __name__ == "__main__":
    n = process(os.path.join(D, "CHAPTER3_METHODOLOGY_R2.md"), True)
    print("Chapter 3 display equations converted:", n)
    if n != 22:
        sys.exit("expected 22 equations")
    for f in ("CHAPTER1_INTRODUCTION_R2.md", "CHAPTER4_IMPLEMENTATION_R2.md", "CHAPTER5_RESULTS_R2.md",
              "CHAPTER6_DISCUSSION_CONCLUSION_R2.md"):
        process(os.path.join(D, f), False)
    print("inline symbols converted")
