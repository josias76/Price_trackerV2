import pandas as pd
import os

def get_product_data(file_path, filters=None):
    """
    Lit les données d'un fichier Excel et retourne un DataFrame, avec filtrage optionnel.
    """
    try:
        df = pd.read_excel(file_path)
        
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    # Convertir la colonne en string pour la recherche insensible à la casse
                    df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return None

def list_data_structure(base_path):
    """
    Parcourt le répertoire de base et retourne une structure arborescente des dossiers et fichiers Excel.
    Chaque nœud contient 'name', 'type' ('folder' ou 'file'), et 'path' (pour les fichiers).
    Les dossiers contiennent une liste 'children'.
    """
    structure = []
    for item_name in sorted(os.listdir(base_path)):
        item_path = os.path.join(base_path, item_name)
        if os.path.isdir(item_path):
            # C'est un dossier, récursion
            children = list_data_structure(item_path)
            if children: # N'ajouter que les dossiers non vides
                structure.append({
                    "name": item_name,
                    "type": "folder",
                    "children": children
                })
        elif os.path.isfile(item_path) and item_name.endswith(".xlsx"):
            # C'est un fichier Excel
            structure.append({
                "name": item_name,
                "type": "file",
                "path": item_path
            })
    return structure


# Exemple d'utilisation (pour les tests)
if __name__ == '__main__':
    # Créez un exemple de structure de fichiers pour tester
    os.makedirs('data/Assurance/Auto', exist_ok=True)
    os.makedirs('data/Manufacturing/Alimentaire/Generale', exist_ok=True)

    # Créez des fichiers Excel factices
    df_auto = pd.DataFrame({'Date': pd.to_datetime(['2023-01-01', '2023-01-02']), 'Prix': [100, 105]})
    df_auto.to_excel('data/Assurance/Auto/prime_assurance.xlsx', index=False)

    df_lait = pd.DataFrame({'Date': pd.to_datetime(['2023-01-01', '2023-01-02']), 'Prix': [1.2, 1.25]})
    df_lait.to_excel('data/Manufacturing/Alimentaire/Generale/lait.xlsx', index=False)

    base_data_path = 'data'
    data_structure = list_data_structure(base_data_path)
    print("Structure des données:")
    import json
    print(json.dumps(data_structure, indent=2))

    # Test de lecture d'un fichier spécifique
    file_to_test = 'data/Manufacturing/Alimentaire/Generale/lait.xlsx'
    print(f"\nDonnées pour {file_to_test}:")
    df_lait_data = get_product_data(file_to_test)
    print(df_lait_data)

    # Test avec filtre
    print(f"\nDonnées pour {file_to_test} (filtré par Prix > 1.2):")
    df_lait_filtered = get_product_data(file_to_test, filters={'Prix': 1.2})
    print(df_lait_filtered)


