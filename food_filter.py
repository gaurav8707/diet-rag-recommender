def filter_foods(df, condition, allergies):
    filtered = df.copy()

    # Fuzzy match condition using keyword split
    condition_keywords = condition.lower().split()

    def keyword_match(s):
        if not isinstance(s, str):
            return False
        s = s.lower()
        return any(kw in s for kw in condition_keywords)

    if "Suitable For" in df.columns:
        filtered = filtered[filtered["Suitable For"].apply(keyword_match)]

    if "Avoid For" in df.columns:
        filtered = filtered[~filtered["Avoid For"].apply(keyword_match)]

    # Filter by allergens
    if allergies and "Allergens" in df.columns:
        pattern = "|".join(allergy.lower() for allergy in allergies)
        filtered = filtered[~filtered["Allergens"].astype(str).str.lower().str.contains(pattern, na=False)]

    return filtered[["Food Name", "Category"]].dropna().head(10).to_dict(orient="records")
