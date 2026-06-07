import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IDS Dashboard - Telecommunications", layout="wide")

# --- 1. SYSTÈME DE LOGIN ---
def login_page():
    st.title("🔐 Connexion au Système IDS")
    
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        
        if submitted:
            # Remplacer par vos propres identifiants
            if username == "admin" and password == "telecom2026":
                st.session_state['logged_in'] = True
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Identifiants incorrects")

# --- CHARGEMENT ET PREPROCESSING (SIMULÉ POUR LA DÉMO) ---
@st.cache_data
def load_and_train():
    # Note : Dans une application réelle, vous chargeriez votre fichier 'clean_network_dataset.csv'
    # Pour cet exemple, nous simulons l'entraînement du modèle Random Forest du code fourni
    # X_train, y_train, etc. devraient être chargés ici.
    
    # Simulation de métriques (basées sur vos résultats de labo)
    metrics = {
        "Accuracy": 0.982,
        "Precision": 0.975,
        "Recall": 0.988,
        "F1-Score": 0.981,
        "AUC": 0.992
    }
    return metrics

# --- 2. DASHBOARD ---
def dashboard_page():
    st.title("📊 Dashboard de Sécurité Réseau")
    
    metrics = load_and_train()
    
    # --- Statistiques du Dataset ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Flux", "257,673")
    col2.metric("Trafic Normal", "56,000", delta="-2%")
    col3.metric("Attaques Détectées", "201,673", delta="5%", delta_color="inverse")
    col4.metric("Fiabilité Modèle", f"{metrics['Accuracy']*100:.1f}%")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Distribution des Classes")
        # Simulation du countplot
        fig, ax = plt.subplots()
        sns.barplot(x=['Normal', 'Attaque'], y=[56000, 201673], palette='coolwarm', ax=ax)
        st.pyplot(fig)

    with col_right:
        st.subheader("Performances du Modèle (Random Forest)")
        perf_df = pd.DataFrame({
            'Métrique': list(metrics.keys()),
            'Valeur': list(metrics.values())
        })
        st.table(perf_df)

# --- 3. TEST DE PRÉDICTION ---
def prediction_page():
    st.title("🔍 Test de Prédiction en Temps Réel")
    st.write("Saisissez les paramètres réseau pour analyser la menace.")

    with st.form("pred_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dur = st.number_input("Durée (dur)", value=0.11)
            spkts = st.number_input("Paquets Source (spkts)", value=10)
        with col2:
            sbytes = st.number_input("Octets Source (sbytes)", value=500)
            sttl = st.number_input("TTL Source (sttl)", value=254)
        with col3:
            sloss = st.number_input("Pertes Source (sloss)", value=0)
            rate = st.number_input("Débit (rate)", value=100.0)

        submit = st.form_submit_button("Analyser le trafic")

    if submit:
        # Simulation du processus : Scaler -> Predict
        # Dans votre code : model.predict(scaler.transform([[dur, spkts, ...]]))
        
        with st.spinner('Analyse du payload en cours...'):
            import time
            time.sleep(1) # Simulation de calcul
            
            # Logique de décision simplifiée pour la démo
            if sttl > 64 and rate > 50:
                st.error("⚠️ ALERTE : Trafic identifié comme une ATTAQUE (DDoS)")
                st.warning("Recommandation : Isoler l'IP source et vérifier les règles Snort.")
            else:
                st.success("✅ Trafic NORMAL : Aucune menace détectée.")

# --- NAVIGATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller vers", ["Tableau de Bord", "Prédicteur en direct"])
    
    if st.sidebar.button("Déconnexion"):
        st.session_state['logged_in'] = False
        st.rerun()

    if page == "Tableau de Bord":
        dashboard_page()
    else:
        prediction_page()