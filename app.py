import streamlit as st
import pandas as pd
import xlsxwriter


st.title("Traitement de fichiers ddPCR\n (CSV → Excel)")

uploaded_files = st.file_uploader("Sélectionnez un ou plusieurs fichiers CSV", accept_multiple_files=True, type="csv")

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file,index_col=False, na_values=[""," ","NA","NaN"])
        st.subheader(f"📄 Aperçu de : {uploaded_file.name}")
        st.dataframe(df.head())
        # Sélection des colonnes à garder
        colonnes_disponibles = list(df.columns)
        colonnes_par_defaut=["Well","Sample","Target","Concentration","AcceptedDroplets","Threshold","MeanAmplitudeofPositives","MeanAmplitudeofNegatives"]
        colonnes_choisies = st.multiselect(
            f"📌 Colonnes à conserver pour {uploaded_file.name} :",
            options=colonnes_disponibles,
            default=[col for col in colonnes_par_defaut if col in colonnes_disponibles] 
        )
        # On garde seulement les colonnes sélectionnées
        df = df[colonnes_choisies]
        df['Fichier'] = uploaded_file.name  # Ajout de l'origine
        all_data.append(df)

    # Concaténation
    result_df = pd.concat(all_data)

    # Téléchargement Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, index=False, sheet_name='ddPCR filtré')
    output.seek(0)


    st.success("Données prêtes ! Cliquez ci-dessous pour télécharger.")
    st.download_button("Télécharger le fichier Excel", data=output, file_name="resultats_ddpcr.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")