import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm


st.set_page_config(page_title="Test sur une proportion", layout="wide")


def format_percent_clean(alpha: float) -> str:
    """
    Formate alpha en pourcentage sans décimales inutiles.
    Exemples :
    0.05   -> 5%
    0.025  -> 2.5%
    0.1234 -> 12.34%
    """
    val = 100 * alpha
    if abs(val - round(val)) < 1e-10:
        return f"{int(round(val))}%"
    txt = f"{val:.2f}".rstrip("0").rstrip(".")
    return f"{txt}%"


def format_prob_clean(x: float) -> str:
    """
    Formate une probabilité décimale sans zéros inutiles.
    Exemples :
    0.025 -> 0.025
    0.05  -> 0.05
    0.5   -> 0.5
    """
    return f"{x:.4f}".rstrip("0").rstrip(".")


def test_proportion_general(
    p0: float,
    n: int,
    alpha: float = 0.05,
    alternative: str = "bilateral",
    x: int | None = None,
    p_hat: float | None = None,
):
    if not (0 < alpha < 1):
        raise ValueError("Le niveau alpha doit être strictement compris entre 0 et 1.")

    if not (0 < p0 < 1):
        raise ValueError("La proportion théorique p0 doit être strictement comprise entre 0 et 1.")

    if n <= 0:
        raise ValueError("La taille de l'échantillon n doit être strictement positive.")

    if alternative not in {"bilateral", "left", "right"}:
        raise ValueError("Le type d'alternative est invalide.")

    source = ""

    if x is not None:
        if x < 0 or x > n:
            raise ValueError("x doit être compris entre 0 et n.")
        p_hat = x / n
        source = "effectif observé"
    elif p_hat is not None:
        if not (0 <= p_hat <= 1):
            raise ValueError("La proportion estimée doit être comprise entre 0 et 1.")
        source = "proportion estimée"
    else:
        raise ValueError("Il faut fournir soit x, soit p̂.")

    erreur_standard = math.sqrt(p0 * (1 - p0) / n)
    variance_sous_H0 = p0 * (1 - p0) / n
    statistique = (p_hat - p0) / erreur_standard

    alpha_label = format_percent_clean(alpha)
    alpha_sur_2_label = format_prob_clean(alpha / 2)
    alpha_label_prob = format_prob_clean(alpha)
    un_moins_alpha_label = format_prob_clean(1 - alpha)

    if alternative == "bilateral":
        quantile = norm.ppf(1 - alpha / 2)
        rejet = abs(statistique) > quantile
        p_value = 2 * (1 - norm.cdf(abs(statistique)))
        H1 = f"p \\neq {p0}"
        etiquette_quantile = f"z_{{\\alpha/2}} = z_{{{alpha_sur_2_label}}}"

        if rejet:
            conclusion = (
                f"Comme |Z_obs| = {abs(statistique):.4f} > {quantile:.4f} = z_(α/2), "
                f"la statistique observée appartient à la zone de rejet. "
                f"On rejette donc H₀ au seuil de {alpha_label}. "
                f"La proportion est statistiquement différente de {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
        else:
            conclusion = (
                f"Comme |Z_obs| = {abs(statistique):.4f} < {quantile:.4f} = z_(α/2), "
                f"la statistique observée appartient à la zone de non rejet. "
                f"On ne rejette pas donc H₀ au seuil de {alpha_label}. "
                f"La proportion n'est pas statistiquement différente de {p0}."
            )

    elif alternative == "left":
        quantile = norm.ppf(alpha)
        rejet = statistique < quantile
        p_value = norm.cdf(statistique)
        H1 = f"p < {p0}"
        etiquette_quantile = f"z_{{\\alpha}} = z_{{{alpha_label_prob}}}"

        if rejet:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} < {quantile:.4f} = z_(α), "
                f"la statistique observée appartient à la zone de rejet. "
                f"On rejette donc H₀ au seuil de {alpha_label}. "
                f"La proportion est statistiquement inférieure à {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
        else:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} > {quantile:.4f} = z_(α), "
                f"la statistique observée appartient à la zone de non rejet. "
                f"On ne rejette pas donc H₀ au seuil de {alpha_label}. "
                f"La proportion n'est pas statistiquement inférieure à {p0}."
            )

    else:
        quantile = norm.ppf(1 - alpha)
        rejet = statistique > quantile
        p_value = 1 - norm.cdf(statistique)
        H1 = f"p > {p0}"
        etiquette_quantile = f"z_{{1-\\alpha}} = z_{{{un_moins_alpha_label}}}"

        if rejet:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} > {quantile:.4f} = z_(1-α), "
                f"la statistique observée appartient à la zone de rejet. "
                f"On rejette donc H₀ au seuil de {alpha_label}. "
                f"La proportion est statistiquement supérieure à {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
        else:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} < {quantile:.4f} = z_(1-α), "
                f"la statistique observée appartient à la zone de non rejet. "
                f"On ne rejette pas donc H₀ au seuil de {alpha_label}. "
                f"La proportion n'est pas statistiquement supérieure à {p0}."
            )

    return {
        "source": source,
        "n": n,
        "x": x,
        "p_hat": p_hat,
        "p0": p0,
        "alpha": alpha,
        "alpha_label": alpha_label,
        "alternative": alternative,
        "nom_statistique": "Z",
        "statistique_test": statistique,
        "quantile_critique": quantile,
        "p_value": p_value,
        "rejet_H0": rejet,
        "H1": H1,
        "conclusion": conclusion,
        "erreur_standard": erreur_standard,
        "variance_sous_H0": variance_sous_H0,
        "loi": "Normale asymptotique",
        "etiquette_quantile": etiquette_quantile
    }


def tracer_distribution_proportion(resultats: dict):
    statistique = resultats["statistique_test"]
    quantile = resultats["quantile_critique"]
    alpha = resultats["alpha"]
    alternative = resultats["alternative"]
    nom_stat = resultats["nom_statistique"]

    borne = max(4, abs(statistique) + 1, abs(quantile) + 1)
    x = np.linspace(-borne, borne, 3000)
    y = norm.pdf(x)

    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(x, y, color="black", linewidth=1.5)

    alpha_pct = format_percent_clean(alpha)
    alpha_half_pct = format_percent_clean(alpha / 2)
    non_rejet_pct = format_percent_clean(1 - alpha)

    if alternative == "bilateral":
        mask_L = x <= -quantile
        mask_C = (x >= -quantile) & (x <= quantile)
        mask_R = x >= quantile

        ax.fill_between(
            x, 0, y, where=mask_L, color="gray", alpha=0.5,
            label=f"Zone de rejet (α/2 = {alpha_half_pct})"
        )
        ax.fill_between(x, 0, y, where=mask_R, color="gray", alpha=0.5)
        ax.fill_between(
            x, 0, y, where=mask_C, color="lightblue", alpha=0.3,
            label=f"Zone de non-rejet ({non_rejet_pct})"
        )

        ax.axvline(-quantile, color="black", linewidth=1.2, linestyle="--")
        ax.axvline(quantile, color="black", linewidth=1.2, linestyle="--")

        ax.text(-quantile - 0.5, max(y) * 0.12, alpha_half_pct, fontsize=9, ha="center", color="dimgray")
        ax.text(quantile + 0.5, max(y) * 0.12, alpha_half_pct, fontsize=9, ha="center", color="dimgray")

        ax.text(-borne * 0.72, max(y) * 0.25, "Rejet\nH₀", fontsize=10, ha="center", va="center", color="dimgray")
        ax.text(borne * 0.72, max(y) * 0.25, "Rejet\nH₀", fontsize=10, ha="center", va="center", color="dimgray")
        ax.text(0, max(y) * 0.55, f"Non-rejet de H₀\n({non_rejet_pct})",
                fontsize=10, ha="center", va="center", color="steelblue", fontweight="bold")

        ax.set_xticks([-quantile, 0, quantile])
        ax.set_xticklabels([f"{-quantile:.2f}", "0", f"{quantile:.2f}"])

    elif alternative == "left":
        mask_L = x <= quantile
        mask_C = x >= quantile

        ax.fill_between(
            x, 0, y, where=mask_L, color="gray", alpha=0.5,
            label=f"Zone de rejet (α = {alpha_pct})"
        )
        ax.fill_between(
            x, 0, y, where=mask_C, color="lightblue", alpha=0.3,
            label=f"Zone de non-rejet ({non_rejet_pct})"
        )

        ax.axvline(quantile, color="black", linewidth=1.2, linestyle="--")
        ax.text(quantile - 0.5, max(y) * 0.12, alpha_pct, fontsize=9, ha="center", color="dimgray")

        ax.text(-borne * 0.72, max(y) * 0.25, "Rejet\nH₀", fontsize=10, ha="center", va="center", color="dimgray")
        ax.text(borne * 0.25, max(y) * 0.55, f"Non-rejet de H₀\n({non_rejet_pct})",
                fontsize=10, ha="center", va="center", color="steelblue", fontweight="bold")

        ax.set_xticks([quantile, 0])
        ax.set_xticklabels([f"{quantile:.2f}", "0"])

    else:
        mask_C = x <= quantile
        mask_R = x >= quantile

        ax.fill_between(
            x, 0, y, where=mask_R, color="gray", alpha=0.5,
            label=f"Zone de rejet (α = {alpha_pct})"
        )
        ax.fill_between(
            x, 0, y, where=mask_C, color="lightblue", alpha=0.3,
            label=f"Zone de non-rejet ({non_rejet_pct})"
        )

        ax.axvline(quantile, color="black", linewidth=1.2, linestyle="--")
        ax.text(quantile + 0.5, max(y) * 0.12, alpha_pct, fontsize=9, ha="center", color="dimgray")

        ax.text(borne * 0.72, max(y) * 0.25, "Rejet\nH₀", fontsize=10, ha="center", va="center", color="dimgray")
        ax.text(-borne * 0.25, max(y) * 0.55, f"Non-rejet de H₀\n({non_rejet_pct})",
                fontsize=10, ha="center", va="center", color="steelblue", fontweight="bold")

        ax.set_xticks([0, quantile])
        ax.set_xticklabels(["0", f"{quantile:.2f}"])

    ax.axvline(statistique, color="red", linewidth=1.8, linestyle="-",
               label=f"{nom_stat}_obs = {statistique:.4f}")

    decalage = 0.12 if statistique <= 0 else -0.12
    align = "left" if statistique <= 0 else "right"

    ax.text(
        statistique + decalage,
        max(y) * 0.45,
        f"{nom_stat}_obs = {statistique:.4f}",
        fontsize=9,
        ha=align,
        va="center",
        color="red",
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="red",
            linewidth=0.7,
            alpha=0.9,
        ),
    )

    if alternative == "bilateral":
        titre_test = f"Test bilatéral : H₀ : p = {resultats['p0']} contre H₁ : p ≠ {resultats['p0']}"
    elif alternative == "left":
        titre_test = f"Test unilatéral gauche : H₀ : p = {resultats['p0']} contre H₁ : p < {resultats['p0']}"
    else:
        titre_test = f"Test unilatéral droit : H₀ : p = {resultats['p0']} contre H₁ : p > {resultats['p0']}"

    ax.set_title(
        f"{titre_test}\nLoi normale asymptotique (α = {alpha_pct}, z_obs = {statistique:.4f})",
        fontsize=11
    )
    ax.set_xlabel("z")
    ax.set_ylabel("Densité")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9, edgecolor="gray")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


st.title("Application Streamlit : test sur une proportion")

st.markdown(
    """
Cette application permet d'effectuer un test asymptotique sur une proportion.

Deux possibilités d'entrée :

- **Nombre de personnes possédant le caractère \(x\)**
- **Proportion estimée dans l’échantillon \(\hat p\)**
"""
)

col1, col2 = st.columns(2)

with col1:
    mode_entree = st.selectbox(
        "Choix de l'entrée",
        [
            "Nombre de personnes possédant le caractère x",
            "Proportion estimée dans l’échantillon p̂"
        ]
    )

    p0 = st.number_input(
        "Valeur sous H₀ : p₀",
        min_value=0.0001,
        max_value=0.9999,
        value=0.25,
        step=0.01,
        format="%.4f"
    )

    n = st.number_input(
        "Taille de l'échantillon n",
        min_value=1,
        value=545,
        step=1
    )

    alpha = st.number_input(
        "Niveau du test α",
        min_value=0.001,
        max_value=0.50,
        value=0.05,
        step=0.01
    )

    alternative_label = st.selectbox(
        "Type de test",
        [
            "Bilatéral : H₁ : p ≠ p₀",
            "Unilatéral gauche : H₁ : p < p₀",
            "Unilatéral droit : H₁ : p > p₀",
        ],
    )

    alternative_map = {
        "Bilatéral : H₁ : p ≠ p₀": "bilateral",
        "Unilatéral gauche : H₁ : p < p₀": "left",
        "Unilatéral droit : H₁ : p > p₀": "right",
    }
    alternative = alternative_map[alternative_label]

with col2:
    x = None
    p_hat = None

    if mode_entree == "Nombre de personnes possédant le caractère x":
        x = st.number_input(
            "Nombre de personnes possédant le caractère x",
            min_value=0,
            max_value=int(n),
            value=117,
            step=1
        )
    else:
        p_hat = st.number_input(
            "Proportion estimée dans l’échantillon p̂",
            min_value=0.0,
            max_value=1.0,
            value=117 / 545,
            step=0.01,
            format="%.4f"
        )

st.markdown("---")

if st.button("Effectuer le test"):
    try:
        resultats = test_proportion_general(
            p0=p0,
            n=int(n),
            alpha=alpha,
            alternative=alternative,
            x=int(x) if x is not None else None,
            p_hat=p_hat,
        )

        st.subheader("Résultats numériques")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("n", f"{resultats['n']}")
        c2.metric("p̂", f"{resultats['p_hat']:.4f}")
        c3.metric("Z", f"{resultats['statistique_test']:.4f}")
        c4.metric("p-value", f"{resultats['p_value']:.4f}")

        if resultats["x"] is not None:
            st.write(f"**Nombre de personnes possédant le caractère :** {resultats['x']}")
        st.write(f"**Erreur standard sous H₀ :** {resultats['erreur_standard']:.6f}")
        st.write(f"**Quantile critique :** {resultats['quantile_critique']:.4f}")
        st.write(f"**Loi utilisée :** {resultats['loi']}")

        st.subheader("Présentation détaillée du test")

        st.markdown("**Proportion observée dans l’échantillon :**")
        if resultats["x"] is not None:
            st.latex(
                rf"\hat{{p}} = \frac{{{resultats['x']}}}{{{resultats['n']}}} \approx {resultats['p_hat']:.4f}"
            )
        else:
            st.latex(
                rf"\hat{{p}} \approx {resultats['p_hat']:.4f}"
            )

        st.markdown(f"**Test sur la proportion au niveau α = {resultats['alpha_label']}**")

        st.markdown("**i) Les hypothèses du test :**")
        st.latex(rf"H_0 :\ p = {resultats['p0']}")
        st.write("contre")
        st.latex(rf"H_1 :\ {resultats['H1']}")

        st.markdown("**ii) Statistique de test : loi et calcul**")
        st.write("Sous H₀, par approximation normale :")
        st.latex(
            rf"Z = \frac{{\hat{{p}} - p_0}}{{\sqrt{{\dfrac{{p_0(1-p_0)}}{{n}}}}}}"
            rf"\sim_{{H_0}} \mathcal{{N}}(0,1), \qquad p_0 = {resultats['p0']}"
        )

        st.write("Calculons la statistique de test :")
        st.latex(
            rf"Z_{{obs}} = \frac{{{resultats['p_hat']:.4f} - {resultats['p0']}}}"
            rf"{{\sqrt{{\dfrac{{{resultats['p0']} \times (1-{resultats['p0']})}}{{{resultats['n']}}}}}}}"
        )
        st.latex(
            rf"= \frac{{{resultats['p_hat'] - resultats['p0']:.4f}}}"
            rf"{{\sqrt{{{resultats['variance_sous_H0']:.6f}}}}}"
        )
        st.latex(
            rf"= \frac{{{resultats['p_hat'] - resultats['p0']:.4f}}}{{{resultats['erreur_standard']:.5f}}}"
            rf"\approx {resultats['statistique_test']:.4f}"
        )

        st.markdown("**iii) Règle de décision**")

        if resultats["alternative"] == "bilateral":
            st.latex(
                rf"\text{{On rejette }} H_0 \text{{ si }} |Z_{{obs}}| > z_{{\alpha/2}} = z_{{{format_prob_clean(resultats['alpha']/2)}}} = {resultats['quantile_critique']:.4f}"
            )
            symbole = ">" if resultats["rejet_H0"] else "<"
            st.latex(
                rf"|Z_{{obs}}| = {abs(resultats['statistique_test']):.4f} {symbole} {resultats['quantile_critique']:.4f}"
            )

        elif resultats["alternative"] == "left":
            st.latex(
                rf"\text{{On rejette }} H_0 \text{{ si }} Z_{{obs}} < z_{{\alpha}} = z_{{{format_prob_clean(resultats['alpha'])}}} = {resultats['quantile_critique']:.4f}"
            )
            symbole = "<" if resultats["rejet_H0"] else ">"
            st.latex(
                rf"Z_{{obs}} = {resultats['statistique_test']:.4f} {symbole} {resultats['quantile_critique']:.4f}"
            )

        else:
            st.latex(
                rf"\text{{On rejette }} H_0 \text{{ si }} Z_{{obs}} > z_{{1-\alpha}} = z_{{{format_prob_clean(1-resultats['alpha'])}}} = {resultats['quantile_critique']:.4f}"
            )
            symbole = ">" if resultats["rejet_H0"] else "<"
            st.latex(
                rf"Z_{{obs}} = {resultats['statistique_test']:.4f} {symbole} {resultats['quantile_critique']:.4f}"
            )

        st.markdown("**Conclusion :**")
        st.write(resultats["conclusion"])

        st.subheader("Graphique de la distribution du test")
        fig = tracer_distribution_proportion(resultats)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur : {e}")
