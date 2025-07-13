import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from data_processing import get_product_data, list_data_structure

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord - Suivi des Prix",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des variables de session
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

# Titre principal
st.title("📊 Tableau de Bord - Suivi des Prix")
st.markdown("Suivez l'évolution des prix par catégorie et sous-catégorie")

# Fonction pour afficher la structure des dossiers de manière récursive
def display_folder_structure(structure, level=0):
    """
    Affiche la structure des dossiers et fichiers de manière hiérarchique.
    Retourne le fichier sélectionné s'il y en a un.
    """
    selected_file = None
    
    for item in structure:
        if item["type"] == "folder":
            # Afficher le dossier avec un expander
            with st.expander(f"📁 {item['name']}", expanded=(level == 0)):
                child_selected = display_folder_structure(item["children"], level + 1)
                if child_selected:
                    selected_file = child_selected
        elif item["type"] == "file":
            # Afficher le fichier avec un bouton de sélection
            file_name = item["name"].replace(".xlsx", "")
            if st.button(f"📄 {file_name}", key=f"file_{item['path']}"):
                selected_file = item["path"]
    
    return selected_file

# Sidebar pour la navigation
with st.sidebar:
    st.header("🗂️ Navigation")
    
    # Charger la structure des données
    @st.cache_data
    def load_data_structure():
        try:
            base_path = os.path.join(os.path.dirname(__file__), "data")
            return list_data_structure(base_path)
        except Exception as e:
            st.error(f"Erreur lors du chargement de la structure: {e}")
            return []
    
    data_structure = load_data_structure()
    
    if data_structure:
        st.markdown("### Sélectionnez un fichier de données:")
        selected_file = display_folder_structure(data_structure)
        
        if selected_file:
            st.session_state.selected_file = selected_file
            st.success(f"Fichier sélectionné: {os.path.basename(selected_file)}")
    else:
        st.warning("Aucune donnée trouvée dans le dossier 'data'")

# Section principale
if st.session_state.selected_file:
    # Chargement des données du fichier sélectionné
    @st.cache_data
    def load_product_data(file_path):
        try:
            return get_product_data(file_path)
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None
    
    data = load_product_data(st.session_state.selected_file)
    
    if data is not None and not data.empty:
        st.success(f"✅ Données chargées: {len(data)} entrées trouvées")
        
        # Section des filtres
        st.markdown("---")
        st.subheader("🔍 Filtres")
        
        # Créer les colonnes pour les filtres
        col1, col2, col3, col4 = st.columns(4)
        
        # Initialiser les filtres
        filters = {}
        
        with col1:
            if 'marque' in data.columns:
                marques = ['Toutes'] + sorted(data['marque'].dropna().unique().tolist())
                selected_marque = st.selectbox("Marque:", marques)
                if selected_marque != 'Toutes':
                    filters['marque'] = selected_marque
        
        with col2:
            if 'type' in data.columns:
                types = ['Tous'] + sorted(data['type'].dropna().unique().tolist())
                selected_type = st.selectbox("Type:", types)
                if selected_type != 'Tous':
                    filters['type'] = selected_type
        
        with col3:
            if 'gramage' in data.columns:
                gramages = ['Tous'] + sorted(data['gramage'].dropna().unique().tolist())
                selected_gramage = st.selectbox("Gramage:", gramages)
                if selected_gramage != 'Tous':
                    filters['gramage'] = selected_gramage
        
        with col4:
            if 'origine' in data.columns:
                origines = ['Toutes'] + sorted(data['origine'].dropna().unique().tolist())
                selected_origine = st.selectbox("Origine:", origines)
                if selected_origine != 'Toutes':
                    filters['origine'] = selected_origine
        
        # Filtres de prix
        col5, col6 = st.columns(2)
        with col5:
            if 'prix' in data.columns:
                min_prix = st.number_input("Prix minimum (€):", 
                                         min_value=0.0, 
                                         value=float(data['prix'].min()),
                                         step=0.01)
        with col6:
            if 'prix' in data.columns:
                max_prix = st.number_input("Prix maximum (€):", 
                                         min_value=0.0, 
                                         value=float(data['prix'].max()),
                                         step=0.01)
        
        # Appliquer les filtres
        filtered_data = data.copy()
        
        # Filtres par colonnes
        for column, value in filters.items():
            if column in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[column].astype(str).str.contains(str(value), case=False, na=False)]
        
        # Filtre par prix
        if 'prix' in filtered_data.columns:
            filtered_data = filtered_data[
                (filtered_data['prix'] >= min_prix) & 
                (filtered_data['prix'] <= max_prix)
            ]
        
        # Affichage des statistiques
        st.markdown("---")
        st.subheader("📈 Statistiques")
        
        if not filtered_data.empty and 'prix' in filtered_data.columns:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Nombre d'entrées", len(filtered_data))
            with col2:
                st.metric("Prix moyen", f"{filtered_data['prix'].mean():.2f} €")
            with col3:
                st.metric("Prix minimum", f"{filtered_data['prix'].min():.2f} €")
            with col4:
                st.metric("Prix maximum", f"{filtered_data['prix'].max():.2f} €")
        
        # Graphique de l'évolution des prix
        st.markdown("---")
        st.subheader("📊 Évolution des Prix")
        
        if not filtered_data.empty and 'date' in filtered_data.columns and 'prix' in filtered_data.columns:
            # Convertir la colonne date si nécessaire
            try:
                filtered_data['date'] = pd.to_datetime(filtered_data['date'])
                
                # Créer le graphique
                fig = px.line(filtered_data.sort_values('date'), 
                             x='date', 
                             y='prix',
                             title="Évolution des prix dans le temps",
                             labels={'date': 'Date', 'prix': 'Prix (€)'},
                             hover_data=['marque', 'type', 'gramage'] if all(col in filtered_data.columns for col in ['marque', 'type', 'gramage']) else None)
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Prix (€)",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erreur lors de la création du graphique: {e}")
        else:
            st.info("Aucune donnée disponible pour le graphique ou colonnes 'date'/'prix' manquantes")
        
        # Tableau des données
        st.markdown("---")
        st.subheader("📋 Données")
        
        if not filtered_data.empty:
            st.dataframe(filtered_data, use_container_width=True)
            
            # Bouton de téléchargement
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les données filtrées (CSV)",
                data=csv,
                file_name=f"donnees_filtrees_{os.path.basename(st.session_state.selected_file).replace('.xlsx', '')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés")
    
    else:
        st.error("Impossible de charger les données du fichier sélectionné.")

else:
    # Page d'accueil
    st.markdown("---")
    st.subheader("🏠 Bienvenue")
    st.info("Sélectionnez un fichier de données dans la barre latérale pour commencer l'analyse des prix.")
    
    # Affichage de la structure des données disponibles
    if 'data_structure' in locals() and data_structure:
        st.subheader("📁 Structure des Données Disponibles")
        
        def display_structure_info(structure, level=0):
            for item in structure:
                indent = "  " * level
                if item["type"] == "folder":
                    st.markdown(f"{indent}📂 **{item['name']}**")
                    if "children" in item:
                        display_structure_info(item["children"], level + 1)
                elif item["type"] == "file":
                    st.markdown(f"{indent}📄 {item['name']}")
        
        display_structure_info(data_structure)

# Footer
st.markdown("---")
st.markdown("*Application de suivi des prix développée avec Streamlit*")

