"""Symbolic and numerical checks of the derived and adapted equations of Chapter 3.
Run: python3 REM_FINAL_THESIS/verification/verify_equations.py
Each check prints PASS or FAIL. Checks concern internal mathematical consistency only;
they do not verify what a cited source prints."""
import sympy as sp, numpy as np, sys
ok = True
def check(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name); ok &= bool(cond)

p, C_miss, C_FA, C_mod, C_esc, r = sp.symbols('p C_miss C_FA C_mod C_esc r', positive=True)
# Table 3.13 losses
L = {'allow': (0, C_miss), 'modify': (C_mod, r*C_miss), 'escalate': (C_esc, C_esc), 'block': (C_FA, 0)}
R = {v: (1-p)*l0 + p*l1 for v, (l0, l1) in L.items()}                      # Eq. 3.6

# Eq. 3.5: law of total expectation under A-Mod
check('Eq 3.5  E[loss|Modify,y=1] = r*C_miss', sp.simplify(r*C_miss + (1-r)*0 - L['modify'][1]) == 0)
# Eq. 3.6 affine in p
check('Eq 3.6  R(v) affine in p for every v', all(sp.degree(sp.expand(R[v]), p) <= 1 for v in R))
# Eq. 3.8 general indifference point
L0v, L1v, L0w, L1w = sp.symbols('L0v L1v L0w L1w', real=True)
Rv = (1-p)*L0v + p*L1v; Rw = (1-p)*L0w + p*L1w
D0 = L0w - L0v; D1 = L1v - L1w
sol = sp.solve(sp.Eq(Rv, Rw), p)
check('Eq 3.8  pi = D0/(D0+D1)', len(sol) == 1 and sp.simplify(sol[0] - D0/(D0+D1)) == 0)
check('Eq 3.8  R(v)-R(v\') = -D0 + p(D0+D1)', sp.simplify((Rv-Rw) - (-D0 + p*(D0+D1))) == 0)
# Eq. 3.9 Allow-Block threshold
pstar = sp.solve(sp.Eq(R['allow'], R['block']), p)[0]
check('Eq 3.9  p* = C_FA/(C_FA+C_miss)', sp.simplify(pstar - C_FA/(C_FA+C_miss)) == 0)
# Eq. 3.10 escalation feasibility: max over p of min(R_allow, R_block) = C_FA C_miss/(C_FA+C_miss)
peak = sp.simplify(R['allow'].subs(p, pstar))
check('Eq 3.10 max_p min(R_A,R_B) = C_FA*C_miss/(C_FA+C_miss)', sp.simplify(peak - C_FA*C_miss/(C_FA+C_miss)) == 0)
rng = np.random.default_rng(0); good = True
for _ in range(2000):   # numerical check of the iff in Eq. 3.10 over {Allow, Escalate, Block}
    cfa, cm, ce = rng.uniform(0.1, 10, 3)
    ps = np.linspace(0, 1, 4001)
    sel = np.any(ce < np.minimum(ps*cm, (1-ps)*cfa))
    good &= (sel == (ce < cfa*cm/(cfa+cm)))
check('Eq 3.10 Escalate selectable iff C_esc < C_FA C_miss/(C_FA+C_miss) (2000 random structures)', good)
check('Eq 3.10 symmetric case reduces to C_esc < C/2', sp.simplify((C_FA*C_miss/(C_FA+C_miss)).subs({C_FA: C_miss}) - C_miss/2) == 0)
# Dominance check text: R(Modify)-R(Block)
check('Sec 3.7.5 R(Mod)-R(Block) = (1-p)(C_mod-C_FA) + p r C_miss',
      sp.simplify(R['modify'] - R['block'] - ((1-p)*(C_mod-C_FA) + p*r*C_miss)) == 0)
# Eq. 3.3 monotone and rank-preserving for gamma1 > 0; Kull equivalence: beta calibration with a=b on p~=sigmoid(s)
s, g1, g0 = sp.symbols('s gamma_1 gamma_0', real=True)
sig = lambda z: 1/(1+sp.exp(-z))
check('Eq 3.3  d p/d s = g1 p(1-p) > 0 when g1 > 0', sp.simplify(sp.diff(sig(g1*s+g0), s) - g1*sig(g1*s+g0)*(1-sig(g1*s+g0))) == 0)
a, c = sp.symbols('a c', real=True)
pt = sig(s)
beta_map = 1/(1 + 1/(sp.exp(c) * pt**a / (1-pt)**a))     # beta calibration with a = b
check('Kull eq. beta(a=b) on sigmoid(s) == sigmoid(a s + c)', sp.simplify(sp.logcombine(sp.log(beta_map/(1-beta_map)) - (a*s + c), force=True)) == 0)
# Eq. 3.11-3.12 completeness
d = 5; beta = sp.symbols('b1:%d' % (d+1)); x = sp.symbols('x1:%d' % (d+1)); xb = sp.symbols('m1:%d' % (d+1)); b0 = sp.Symbol('b0')
phi = [beta[i]*(x[i]-xb[i]) for i in range(d)]; phi0 = b0 + sum(beta[i]*xb[i] for i in range(d))
check('Eq 3.12 phi0 + sum phi_i = s_t', sp.simplify(phi0 + sum(phi) - (b0 + sum(beta[i]*x[i] for i in range(d)))) == 0)
# Eq. 3.21 log-loss equals negated averaged unpenalised term of Eq. 3.2
# Eqs. 3.20-3.21 and 3.14: implementation against a direct transcription of the printed formula
sys.path.insert(0, '.')
from rem.evaluation.probabilistic import expected_calibration_error, log_loss
from rem.algorithms.a1 import operating_threshold
yy = rng.integers(0, 2, 500); pp = rng.uniform(0, 1, 500); pp[:5] = 0.0
M = 10; ece = 0.0
for m in range(1, M + 1):
    idx = (pp > (m-1)/M) & (pp <= m/M) if m > 1 else (pp <= 1/M)   # p = 0 assigned to bin 1 (Ch. 3)
    if idx.any(): ece += idx.sum()/len(pp) * abs(yy[idx].mean() - pp[idx].mean())
check('Eq 3.20 ECE implementation == formula (M=10, random data)', abs(expected_calibration_error(yy, pp, M) - ece) < 1e-12)
eps = 1e-6; pc = np.clip(pp, eps, 1-eps)
ll = -np.mean(yy*np.log(pc) + (1-yy)*np.log(1-pc))
check('Eq 3.21 log-loss implementation == formula (clip 1e-6)', abs(log_loss(yy, pp, eps) - ll) < 1e-12)
ben = rng.uniform(0, 1, 300)
for alpha in (0.01, 0.05, 0.2):
    th = operating_threshold(ben, alpha)
    cands = sorted(set(ben))
    direct = min(t for t in cands if np.mean(ben >= t) <= alpha) if any(np.mean(ben >= t) <= alpha for t in cands) else None
    check(f'Eq 3.14 theta(alpha={alpha}) implementation == min over observed values', direct is not None and abs(th - direct) < 1e-12)
# Penalty scale correspondence (Ch. 3 R2 / Ch. 4): lambda*||b||^2 == (lambda_impl/2)*||b||^2 iff lambda = lambda_impl/2
lam, lam_i, bb = sp.symbols('lambda lambda_impl bb', positive=True)
check('Eq 3.2  lambda = lambda_impl/2 maps the two objectives', sp.simplify(lam*bb - (lam_i/2)*bb).subs(lam, lam_i/2) == 0)
# Pre-registered tier thresholds quoted in Ch. 5/6: C_FA=1, C_miss=10 -> 1/11; C_miss=20 -> 1/21
check('Ch5 tier-3 Allow-Block point 1/11', pstar.subs({C_FA: 1, C_miss: 10}) == sp.Rational(1, 11))
check('Ch5 tier-4 Allow-Block point 1/21', pstar.subs({C_FA: 1, C_miss: 20}) == sp.Rational(1, 21))
# Eq. 3.15-3.16 Bernoulli LLR and CUSUM: LLR of Bernoulli pmf
e, q0, q1 = sp.symbols('e q0 q1', positive=True)
llr = sp.log((q1**e*(1-q1)**(1-e))/(q0**e*(1-q0)**(1-e)))
target = e*sp.log(q1/q0) + (1-e)*sp.log((1-q1)/(1-q0))
check('Eq 3.15 Bernoulli LLR (e=0,1)', all(sp.simplify(sp.expand_log((llr-target).subs(e, k), force=True)) == 0 for k in (0, 1)))
print('ALL PASS' if ok else 'SOME FAILED'); sys.exit(0 if ok else 1)
