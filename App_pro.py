if rejet:
        if alternative == "bilateral":
            conclusion = (
                f"Comme |Z_obs| = {abs(statistique):.4f} > {quantile:.4f}, "
                f"la statistique observée appartient à la zone de rejet, "
                f"on rejette H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion est statistiquement différente de {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
        elif alternative == "left":
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} < {quantile:.4f}, "
                f"la statistique observée appartient à la zone de rejet, "
                f"on rejette H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion est statistiquement inférieure à {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
        else:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} > {quantile:.4f}, "
                f"la statistique observée appartient à la zone de rejet, "
                f"on rejette H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion est statistiquement supérieure à {p0}. "
                f"On dispose donc de suffisamment de preuves statistiques pour rejeter H₀."
            )
    else:
        if alternative == "bilateral":
            conclusion = (
                f"Comme |Z_obs| = {abs(statistique):.4f} < {quantile:.4f}, "
                f"la statistique observée appartient à la zone de non rejet, "
                f"on ne rejette pas H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion n'est pas statistiquement différente de {p0}. "
                f"On n'a donc pas suffisamment de preuves statistiques pour conclure que la proportion est différente de {p0}."
            )
        elif alternative == "left":
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} > {quantile:.4f}, "
                f"la statistique observée appartient à la zone de non rejet, "
                f"on ne rejette pas H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion n'est pas statistiquement inférieure à {p0}. "
                f"On n'a donc pas suffisamment de preuves statistiques pour conclure que la proportion est inférieure à {p0}."
            )
        else:
            conclusion = (
                f"Comme Z_obs = {statistique:.4f} < {quantile:.4f}, "
                f"la statistique observée appartient à la zone de non rejet, "
                f"on ne rejette pas H₀ au seuil de {100*alpha:.0f}%. "
                f"La proportion n'est pas statistiquement supérieure à {p0}. "
                f"On n'a donc pas suffisamment de preuves statistiques pour conclure que la proportion est supérieure à {p0}."
            )
