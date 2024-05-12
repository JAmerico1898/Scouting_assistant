import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
#from PIL import image
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import plotly.express as px
import io
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar
from sklearn.decomposition import PCA
import matplotlib.ticker as ticker
#import openai
from openai import OpenAI

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#CABEÇALHO DO FORM
st.markdown("<h1 style='text-align: center;'>Assistente de Scouting<br>Fase 2</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>app by @JAmerico1898</h6>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:

    #jogadores = df1["Atleta"]
    choose = option_menu("Galeria de Apps", ["Análise Individual", "Compare Jogadores"],
                         icons=['graph-up-arrow', "question-lg"],
                         menu_icon="universal-access", default_index=0, 
                         styles={
                         "container": {"padding": "5!important", "background-color": "#fafafa"},
                         "icon": {"color": "orange", "font-size": "25px"},
                         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                         "nav-link-selected": {"background-color": "#02ab21"},    
                         }
                         )


df13 = pd.read_csv("base_jogadores.csv")
df16 = pd.read_csv("Atributos.csv")
prospectos = df13["Atleta"]
clubes = df13["Equipe Janela Análise"]
posições = df13["Posição"]
atributos_lateral = pd.read_csv("atributos_lateral.csv")
atributos_lateral_2 = pd.read_csv("atributos_lateral_2.csv")
atributos_zagueiro = pd.read_csv("atributos_zagueiro.csv")
atributos_meio_campo = pd.read_csv("atributos_meio_campo.csv")
atributos_meio_campo_2 = pd.read_csv("atributos_meio_campo_2.csv")
atributos_extremo = pd.read_csv("atributos_extremo.csv")
atributos_extremo_2 = pd.read_csv("atributos_extremo_2.csv")
atributos_atacante = pd.read_csv("atributos_atacante.csv")
atributos_atacante_2 = pd.read_csv("atributos_atacante_2.csv")


if choose == "Análise Individual":

    jogadores = st.selectbox("Escolha o Jogador", options=prospectos, index = None)
    if jogadores:
        #Determinar Liga
        df14 = df13.loc[(df13['Atleta']==jogadores)]
        ligas = df14['Liga'].unique()
        liga = st.selectbox("Escolha a Liga", options=ligas)
        #Determinar Posição
        if liga:
            df15 = df14.loc[(df13['Liga']==liga)]
            posições = df14['Posição'].unique()
            posição = st.selectbox("Escolha a Posição", options=posições)
            if posição == ("LATERAL"):
            
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                Lateral_Charts = pd.read_csv('Lateral.csv')
                Lateral_Charts_1 = Lateral_Charts[(Lateral_Charts['Atleta']==jogadores)&(Lateral_Charts['Liga']==liga)]
                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Lateral_Charts_1.iloc[:, np.r_[10:16]].reset_index(drop=True)
                metrics_list = metrics.iloc[0].tolist()
                #Collecting clube
                clube = Lateral_Charts_1.iat[0, 1]
                
                ## parameter names
                params = metrics.columns.tolist()

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                ## parameter value
                values = metrics_list

                ## title values
                title = dict(
                    title_name=jogadores,
                    title_color = 'blue',
                    subtitle_name= (posição),
                    subtitle_color='#344D94',
                    title_name_2=clube,
                    title_color_2 = 'blue',
                    subtitle_name_2='2023',
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                ## instantiate object
                radar = Radar()

                ## instantiate object -- changing fontsize
                radar=Radar(fontfamily='Cursive', range_fontsize=13)
                radar=Radar(fontfamily='Cursive', label_fontsize=15)

                ## plot radar -- filename and dpi
                fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                        title=title, endnote=endnote, dpi=600)
                st.pyplot(fig)

                #################################################################################################################################
                #################################################################################################################################
                #################################################################################################################################
                
                #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição dos Atributos de todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                # Dynamically create the HTML string with the 'jogadores' variable
                title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                # Use the dynamically created HTML string in st.markdown
                st.markdown(title_html, unsafe_allow_html=True)

                #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                # Collecting data
                Lateral_Charts_2 = Lateral_Charts[(Lateral_Charts['Liga']==liga)]

                #Collecting data to plot
                metrics = Lateral_Charts_2.iloc[:, np.r_[4:10]].reset_index(drop=True)
                metrics_participação = metrics.iloc[:, 0].tolist()
                metrics_defesa = metrics.iloc[:, 1].tolist()
                metrics_apoio = metrics.iloc[:, 2].tolist()
                metrics_ataque = metrics.iloc[:, 3].tolist()
                metrics_último_passe = metrics.iloc[:, 4].tolist()
                metrics_drible = metrics.iloc[:, 5].tolist()
                metrics_y = [0] * len(metrics_participação)

                # The specific data point you want to highlight
                highlight = Lateral_Charts_2[(Lateral_Charts_2['Atleta']==jogadores)]
                highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                highlight_participação = highlight.iloc[:, 0].tolist()
                highlight_defesa = highlight.iloc[:, 1].tolist()
                highlight_apoio = highlight.iloc[:, 2].tolist()
                highlight_ataque = highlight.iloc[:, 3].tolist()
                highlight_último_passe = highlight.iloc[:, 4].tolist()
                highlight_drible = highlight.iloc[:, 5].tolist()
                highlight_y = 0

                # Computing the selected player specific values
                highlight_participação_value = pd.DataFrame(highlight_participação).reset_index(drop=True)
                highlight_defesa_value = pd.DataFrame(highlight_defesa).reset_index(drop=True)
                highlight_apoio_value = pd.DataFrame(highlight_apoio).reset_index(drop=True)
                highlight_ataque_value = pd.DataFrame(highlight_ataque).reset_index(drop=True)
                highlight_último_passe_value = pd.DataFrame(highlight_último_passe).reset_index(drop=True)
                highlight_drible_value = pd.DataFrame(highlight_drible).reset_index(drop=True)

                highlight_participação_value = highlight_participação_value.iat[0,0]
                highlight_defesa_value = highlight_defesa_value.iat[0,0]
                highlight_apoio_value = highlight_apoio_value.iat[0,0]
                highlight_ataque_value = highlight_ataque_value.iat[0,0]
                highlight_último_passe_value = highlight_último_passe_value.iat[0,0]
                highlight_drible_value = highlight_drible_value.iat[0,0]

                # Computing the min and max value across all lists using a generator expression
                min_value = min(min(lst) for lst in [metrics_participação, metrics_defesa, metrics_apoio, 
                                                    metrics_ataque, metrics_último_passe, metrics_drible])
                min_value = min_value - 0.1
                max_value = max(max(lst) for lst in [metrics_participação, metrics_defesa, metrics_apoio, 
                                                    metrics_ataque, metrics_último_passe, metrics_drible])
                max_value = max_value + 0.1

                # Create two subplots vertically aligned with separate x-axes
                fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1)
                ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                #Collecting Additional Information
                # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                lateral_ranking_df = pd.read_csv("Lateral_ranking.csv")

                # Building the Extended Title"
                rows_count = lateral_ranking_df[lateral_ranking_df['Liga'] == liga].shape[0]
                participacao_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Participação_Ranking'].values
                participacao_ranking_value = participacao_ranking_value[0].astype(int)
                output_str = f"({participacao_ranking_value}/{rows_count})"
                full_title_participação = f"Participação {output_str} {highlight_participação_value}"

                # Building the Extended Title"
                defesa_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Defesa_Ranking'].values
                defesa_ranking_value = defesa_ranking_value[0].astype(int)
                output_str = f"({defesa_ranking_value}/{rows_count})"
                full_title_defesa = f"Defesa {output_str} {highlight_defesa_value}"

                # Building the Extended Title"
                apoio_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Apoio_Ranking'].values
                apoio_ranking_value = apoio_ranking_value[0].astype(int)
                output_str = f"({apoio_ranking_value}/{rows_count})"
                full_title_apoio = f"Apoio {output_str} {highlight_apoio_value}"

                # Building the Extended Title"
                ataque_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Ataque_Ranking'].values
                ataque_ranking_value = ataque_ranking_value[0].astype(int)
                output_str = f"({ataque_ranking_value}/{rows_count})"
                full_title_ataque = f"Ataque {output_str} {highlight_ataque_value}"
                # Building the Extended Title"
                último_passe_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Último passe_Ranking'].values
                último_passe_ranking_value = último_passe_ranking_value[0].astype(int)
                output_str = f"({último_passe_ranking_value}/{rows_count})"
                full_title_último_passe = f"Último passe {output_str} {highlight_último_passe_value}"
                # Building the Extended Title"
                drible_ranking_value = lateral_ranking_df.loc[(lateral_ranking_df['Atleta'] == jogadores) & 
                                                                    (lateral_ranking_df['Liga'] == liga), 'Drible_Ranking'].values
                drible_ranking_value = drible_ranking_value[0].astype(int)
                output_str = f"({drible_ranking_value}/{rows_count})"
                full_title_drible = f"Drible {output_str} {highlight_drible_value}"

                # Plot the first scatter plot in the first subplot
                ax1.scatter(metrics_participação, metrics_y, color='deepskyblue')
                ax1.scatter(highlight_participação, highlight_y, color='blue', s=60)
                ax1.get_yaxis().set_visible(False)
                ax1.set_title(full_title_participação, fontsize=12, fontweight='bold')
                ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax2.scatter(metrics_defesa, metrics_y, color='deepskyblue')
                ax2.scatter(highlight_defesa, highlight_y, color='blue', s=60)
                ax2.get_yaxis().set_visible(False)
                ax2.set_title(full_title_defesa, fontsize=12, fontweight='bold')
                ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax3.scatter(metrics_apoio, metrics_y, color='deepskyblue')
                ax3.scatter(highlight_apoio, highlight_y, color='blue', s=60)
                ax3.get_yaxis().set_visible(False)
                ax3.set_title(full_title_apoio, fontsize=12, fontweight='bold')
                ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax4.scatter(metrics_ataque, metrics_y, color='deepskyblue')
                ax4.scatter(highlight_ataque, highlight_y, color='blue', s=60)            
                ax4.get_yaxis().set_visible(False)
                ax4.set_title(full_title_ataque, fontsize=12, fontweight='bold')
                ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax4.spines['top'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['left'].set_visible(False)
                ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax5.scatter(metrics_último_passe, metrics_y, color='deepskyblue')
                ax5.scatter(highlight_último_passe, highlight_y, color='blue', s=60)            
                ax5.get_yaxis().set_visible(False)
                ax5.set_title(full_title_último_passe, fontsize=12, fontweight='bold')
                ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax5.spines['top'].set_visible(False)
                ax5.spines['right'].set_visible(False)
                ax5.spines['bottom'].set_visible(False)
                ax5.spines['left'].set_visible(False)
                ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax6.scatter(metrics_drible, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                ax6.scatter(highlight_drible, highlight_y, color='blue', s=60, label=jogadores)            
                ax6.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                ax6.get_yaxis().set_visible(False)
                ax6.set_title(full_title_drible, fontsize=12, fontweight='bold')
                ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax6.spines['top'].set_visible(False)
                ax6.spines['right'].set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.spines['left'].set_visible(False)
                ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                plt.tight_layout()  # Adjust the layout to prevent overlap
                plt.show()

                ax6.legend(loc='right', bbox_to_anchor=(0.2, -5), fontsize="6", frameon=False)
                plt.show()

                st.pyplot(fig)


    ##########################################################################################################################
    ##########################################################################################################################
                if posição:
                    atributos = atributos_lateral['LATERAL']
                    atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
                    if atributo == ("Participação"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Participação_Lateral_Charts = pd.read_csv('Participação.csv')
                        Participação_Lateral_Charts_1 = Participação_Lateral_Charts[(Participação_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Participação_Lateral_Charts['Liga']==liga)&
                                                                                    (Participação_Lateral_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Participação_Lateral_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Participação_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Participação_Lateral_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Participação_Lateral_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)


                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Participação_Lateral_Charts_2 = Participação_Lateral_Charts[(Participação_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Participação_Lateral_Charts_2 = Participação_Lateral_Charts[(Participação_Lateral_Charts['Liga']==liga)&(Participação_Lateral_Charts['Posição']==posição)]
                        metrics = Participação_Lateral_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_participação_1 = metrics.iloc[:, 0].tolist()
                        metrics_participação_2 = metrics.iloc[:, 1].tolist()
                        metrics_participação_3 = metrics.iloc[:, 2].tolist()
                        metrics_participação_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Participação_Lateral_Charts_2[(Participação_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_participação_1 = highlight.iloc[:, 0].tolist()
                        highlight_participação_2 = highlight.iloc[:, 1].tolist()
                        highlight_participação_3 = highlight.iloc[:, 2].tolist()
                        highlight_participação_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
                        highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
                        highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
                        highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

                        highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
                        highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
                        highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
                        highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        participação_ranking_df = pd.read_csv("Participação_ranking.csv")
                        # Building the Extended Title
                        rows_count = participação_ranking_df[(participação_ranking_df['Liga'] == liga)  & 
                                                                            (participação_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_participação_1_value}"
                        
                        # Building the Extended Title"
                        Passes_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes /90_Ranking'].values
                        Passes_per_ranking_value = Passes_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_per_ranking_value}/{rows_count})"
                        full_title_Passes_per_ranking_value = f"Passes /90 {output_str} {highlight_participação_2_value}"
                        
                        # Building the Extended Title"
                        Passes_recebidos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_participação_3_value}"
                        
                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_participação_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_participação_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_participação_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_participação_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_participação_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_participação_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_participação_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_participação_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_participação_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -2.0), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Defesa"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Defesa_Lateral_Charts = pd.read_csv('defesa.csv')
                        Defesa_Lateral_Charts_1 = Defesa_Lateral_Charts[(Defesa_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Defesa_Lateral_Charts['Liga']==liga)&
                                                                                    (Defesa_Lateral_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Defesa_Lateral_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Defesa_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Defesa_Lateral_Charts_1.iloc[:, np.r_[10:16]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Defesa_Lateral_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Defesa_Lateral_Charts_2 = Defesa_Lateral_Charts[(Defesa_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Defesa_Lateral_Charts_2 = Defesa_Lateral_Charts[(Defesa_Lateral_Charts['Liga']==liga)&(Defesa_Lateral_Charts['Posição']==posição)]
                        metrics = Defesa_Lateral_Charts_2.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        metrics_defesa_1 = metrics.iloc[:, 0].tolist()
                        metrics_defesa_2 = metrics.iloc[:, 1].tolist()
                        metrics_defesa_3 = metrics.iloc[:, 2].tolist()
                        metrics_defesa_4 = metrics.iloc[:, 3].tolist()
                        metrics_defesa_5 = metrics.iloc[:, 4].tolist()
                        metrics_defesa_6 = metrics.iloc[:, 5].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Defesa_Lateral_Charts_2[(Defesa_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_defesa_1 = highlight.iloc[:, 0].tolist()
                        highlight_defesa_2 = highlight.iloc[:, 1].tolist()
                        highlight_defesa_3 = highlight.iloc[:, 2].tolist()
                        highlight_defesa_4 = highlight.iloc[:, 3].tolist()
                        highlight_defesa_5 = highlight.iloc[:, 4].tolist()
                        highlight_defesa_6 = highlight.iloc[:, 5].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_defesa_1_value = pd.DataFrame(highlight_defesa_1).reset_index(drop=True)
                        highlight_defesa_2_value = pd.DataFrame(highlight_defesa_2).reset_index(drop=True)
                        highlight_defesa_3_value = pd.DataFrame(highlight_defesa_3).reset_index(drop=True)
                        highlight_defesa_4_value = pd.DataFrame(highlight_defesa_4).reset_index(drop=True)
                        highlight_defesa_5_value = pd.DataFrame(highlight_defesa_5).reset_index(drop=True)
                        highlight_defesa_6_value = pd.DataFrame(highlight_defesa_6).reset_index(drop=True)

                        highlight_defesa_1_value = highlight_defesa_1_value.iat[0,0]
                        highlight_defesa_2_value = highlight_defesa_2_value.iat[0,0]
                        highlight_defesa_3_value = highlight_defesa_3_value.iat[0,0]
                        highlight_defesa_4_value = highlight_defesa_4_value.iat[0,0]
                        highlight_defesa_5_value = highlight_defesa_5_value.iat[0,0]
                        highlight_defesa_6_value = highlight_defesa_6_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        defesa_ranking_df = pd.read_csv("Defesa_ranking.csv")
                        # Building the Extended Title"
                        rows_count = defesa_ranking_df[(defesa_ranking_df['Liga'] == liga)  & 
                                                                            (defesa_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_defesa_1_value}"

                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_defesa_2_value}"

                        # Building the Extended Title"
                        Interceptações_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Interceptações /90_Ranking'].values
                        Interceptações_per_ranking_value = Interceptações_per_ranking_value[0].astype(int)
                        output_str = f"({Interceptações_per_ranking_value}/{rows_count})"
                        full_title_Interceptações_per_ranking_value = f"Interceptações /90 {output_str} {highlight_defesa_3_value}"

                        # Building the Extended Title"
                        Carrinhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Carrinhos /90_Ranking'].values
                        Carrinhos_per_ranking_value = Carrinhos_per_ranking_value[0].astype(int)
                        output_str = f"({Carrinhos_per_ranking_value}/{rows_count})"
                        full_title_Carrinhos_per_ranking_value = f"Carrinhos /90 {output_str} {highlight_defesa_4_value}"

                        # Building the Extended Title"
                        Ações_defensivas_bem_sucedidas_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Ações defensivas bem sucedidas /90_Ranking'].values
                        Ações_defensivas_bem_sucedidas_per_ranking_value = Ações_defensivas_bem_sucedidas_per_ranking_value[0].astype(int)
                        output_str = f"({Ações_defensivas_bem_sucedidas_per_ranking_value}/{rows_count})"
                        full_title_Ações_defensivas_bem_sucedidas_per_ranking_value = f"Ações defensivas bem sucedidas /90 {output_str} {highlight_defesa_5_value}"

                        # Building the Extended Title"
                        Duelos_defensivos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos ganhos /90_Ranking'].values
                        Duelos_defensivos_ganhos_per_ranking_value = Duelos_defensivos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_ganhos_per_ranking_value = f"Duelos defensivos ganhos /90 {output_str} {highlight_defesa_6_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_defesa_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_defesa_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_defesa_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_defesa_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_defesa_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_defesa_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Interceptações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_defesa_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_defesa_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Carrinhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax5.scatter(metrics_defesa_5, metrics_y, color='deepskyblue')
                        ax5.scatter(highlight_defesa_5, highlight_y, color='blue', s=60)
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Ações_defensivas_bem_sucedidas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax6.scatter(metrics_defesa_6, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax6.scatter(highlight_defesa_6, highlight_y, color='blue', s=60, label=jogadores)
                        ax6.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax6.get_yaxis().set_visible(False)
                        ax6.set_title(full_title_Duelos_defensivos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax6.spines['top'].set_visible(False)
                        ax6.spines['right'].set_visible(False)
                        ax6.spines['bottom'].set_visible(False)
                        ax6.spines['left'].set_visible(False)
                        ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax6.legend(loc='right', bbox_to_anchor=(0.2, -5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Apoio"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Apoio_Lateral_Charts = pd.read_csv('apoio.csv')
                        Apoio_Lateral_Charts_1 = Apoio_Lateral_Charts[(Apoio_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Apoio_Lateral_Charts['Liga']==liga)&
                                                                                    (Apoio_Lateral_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Apoio_Lateral_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Apoio_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Apoio_Lateral_Charts_1.iloc[:, np.r_[10:16]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Apoio_Lateral_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Apoio_Lateral_Charts_2 = Apoio_Lateral_Charts[(Apoio_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Apoio_Lateral_Charts_2 = Apoio_Lateral_Charts[(Apoio_Lateral_Charts['Liga']==liga)&(Apoio_Lateral_Charts['Posição']==posição)]
                        metrics = Apoio_Lateral_Charts_2.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        metrics_apoio_1 = metrics.iloc[:, 0].tolist()
                        metrics_apoio_2 = metrics.iloc[:, 1].tolist()
                        metrics_apoio_3 = metrics.iloc[:, 2].tolist()
                        metrics_apoio_4 = metrics.iloc[:, 3].tolist()
                        metrics_apoio_5 = metrics.iloc[:, 4].tolist()
                        metrics_apoio_6 = metrics.iloc[:, 5].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Apoio_Lateral_Charts_2[(Apoio_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_apoio_1 = highlight.iloc[:, 0].tolist()
                        highlight_apoio_2 = highlight.iloc[:, 1].tolist()
                        highlight_apoio_3 = highlight.iloc[:, 2].tolist()
                        highlight_apoio_4 = highlight.iloc[:, 3].tolist()
                        highlight_apoio_5 = highlight.iloc[:, 4].tolist()
                        highlight_apoio_6 = highlight.iloc[:, 5].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_apoio_1_value = pd.DataFrame(highlight_apoio_1).reset_index(drop=True)
                        highlight_apoio_2_value = pd.DataFrame(highlight_apoio_2).reset_index(drop=True)
                        highlight_apoio_3_value = pd.DataFrame(highlight_apoio_3).reset_index(drop=True)
                        highlight_apoio_4_value = pd.DataFrame(highlight_apoio_4).reset_index(drop=True)
                        highlight_apoio_5_value = pd.DataFrame(highlight_apoio_5).reset_index(drop=True)
                        highlight_apoio_6_value = pd.DataFrame(highlight_apoio_6).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_apoio_1_value = highlight_apoio_1_value.iat[0,0]
                        highlight_apoio_2_value = highlight_apoio_2_value.iat[0,0]
                        highlight_apoio_3_value = highlight_apoio_3_value.iat[0,0]
                        highlight_apoio_4_value = highlight_apoio_4_value.iat[0,0]
                        highlight_apoio_5_value = highlight_apoio_5_value.iat[0,0]
                        highlight_apoio_6_value = highlight_apoio_6_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_apoio_1, metrics_apoio_2, 
                                                            metrics_apoio_3, metrics_apoio_4,
                                                            metrics_apoio_5, metrics_apoio_6])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_apoio_1, metrics_apoio_2, 
                                                            metrics_apoio_3, metrics_apoio_4,
                                                            metrics_apoio_5, metrics_apoio_6])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        apoio_ranking_df = pd.read_csv("Apoio_ranking.csv")
                        # Building the Extended Title"
                        rows_count = apoio_ranking_df[(apoio_ranking_df['Liga'] == liga)  & 
                                                                            (apoio_ranking_df['Posição'] == posição)].shape[0]
                        Passes_longos_recebidos_per_ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Passes longos recebidos /90_Ranking'].values
                        Passes_longos_recebidos_per_ranking_value = Passes_longos_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_longos_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_longos_recebidos_per_ranking_value = f"Passes longos recebidos /90 {output_str} {highlight_apoio_1_value}"

                        # Building the Extended Title"
                        Acelerações_per_ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Acelerações /90_Ranking'].values
                        Acelerações_per_ranking_value = Acelerações_per_ranking_value[0].astype(int)
                        output_str = f"({Acelerações_per_ranking_value}/{rows_count})"
                        full_title_Acelerações_per_ranking_value = f"Acelerações /90 {output_str} {highlight_apoio_2_value}"

                        # Building the Extended Title"
                        Corridas_progressivas_per_Ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Corridas progressivas /90_Ranking'].values
                        Corridas_progressivas_per_Ranking_value = Corridas_progressivas_per_Ranking_value[0].astype(int)
                        output_str = f"({Corridas_progressivas_per_Ranking_value}/{rows_count})"
                        full_title_Corridas_progressivas_per_Ranking_value = f"Corridas progressivas /90 {output_str} {highlight_apoio_3_value}"

                        # Building the Extended Title"
                        Passes_entre_linhas_certos_per_Ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Passes entre linhas certos /90_Ranking'].values
                        Passes_entre_linhas_certos_per_Ranking_value = Passes_entre_linhas_certos_per_Ranking_value[0].astype(int)
                        output_str = f"({Passes_entre_linhas_certos_per_Ranking_value}/{rows_count})"
                        full_title_Passes_entre_linhas_certos_per_Ranking_value = f"Passes entre linhas certos /90 {output_str} {highlight_apoio_4_value}"

                        # Building the Extended Title"
                        Passes_progressivos_certos_per_Ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Passes progressivos certos /90_Ranking'].values
                        Passes_progressivos_certos_per_Ranking_value = Passes_progressivos_certos_per_Ranking_value[0].astype(int)
                        output_str = f"({Passes_progressivos_certos_per_Ranking_value}/{rows_count})"
                        full_title_Passes_progressivos_certos_per_Ranking_value = f"Passes progressivos certos /90 {output_str} {highlight_apoio_5_value}"

                        # Building the Extended Title"
                        Passes_frontais_certos_per_Ranking_value = apoio_ranking_df.loc[(apoio_ranking_df['Atleta'] == jogadores) & 
                                                                            (apoio_ranking_df['Liga'] == liga) & 
                                                                            (apoio_ranking_df['Posição'] == posição), 'Passes frontais certos /90_Ranking'].values
                        Passes_frontais_certos_per_Ranking_value = Passes_frontais_certos_per_Ranking_value[0].astype(int)
                        output_str = f"({Passes_frontais_certos_per_Ranking_value}/{rows_count})"
                        full_title_Passes_frontaiss_certos_per_Ranking_value = f"Passes frontais certos /90 {output_str} {highlight_apoio_6_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_apoio_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_apoio_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_longos_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_apoio_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_apoio_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Acelerações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_apoio_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_apoio_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Corridas_progressivas_per_Ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_apoio_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_apoio_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_entre_linhas_certos_per_Ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax5.scatter(metrics_apoio_5, metrics_y, color='deepskyblue')
                        ax5.scatter(highlight_apoio_5, highlight_y, color='blue', s=60)
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Passes_progressivos_certos_per_Ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax6.scatter(metrics_apoio_6, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax6.scatter(highlight_apoio_6, highlight_y, color='blue', s=60, label=jogadores)
                        ax6.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax6.get_yaxis().set_visible(False)
                        ax6.set_title(full_title_Passes_frontaiss_certos_per_Ranking_value, fontsize=12, fontweight='bold')
                        ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax6.spines['top'].set_visible(False)
                        ax6.spines['right'].set_visible(False)
                        ax6.spines['bottom'].set_visible(False)
                        ax6.spines['left'].set_visible(False)
                        ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax6.legend(loc='right', bbox_to_anchor=(0.2, -5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Ataque"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Ataque_Lateral_Charts = pd.read_csv('ataque.csv')
                        Ataque_Lateral_Charts_1 = Ataque_Lateral_Charts[(Ataque_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Ataque_Lateral_Charts['Liga']==liga)&
                                                                                    (Ataque_Lateral_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Ataque_Lateral_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Ataque_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Ataque_Lateral_Charts_1.iloc[:, np.r_[9:14]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Ataque_Lateral_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Ataque_Lateral_Charts_2 = Ataque_Lateral_Charts[(Ataque_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Ataque_Lateral_Charts_2 = Ataque_Lateral_Charts[(Ataque_Lateral_Charts['Liga']==liga)&(Ataque_Lateral_Charts['Posição']==posição)]
                        metrics = Ataque_Lateral_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_ataque_1 = metrics.iloc[:, 0].tolist()
                        metrics_ataque_2 = metrics.iloc[:, 1].tolist()
                        metrics_ataque_3 = metrics.iloc[:, 2].tolist()
                        metrics_ataque_4 = metrics.iloc[:, 3].tolist()
                        metrics_ataque_5 = metrics.iloc[:, 4].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Ataque_Lateral_Charts_2[(Ataque_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_ataque_1 = highlight.iloc[:, 0].tolist()
                        highlight_ataque_2 = highlight.iloc[:, 1].tolist()
                        highlight_ataque_3 = highlight.iloc[:, 2].tolist()
                        highlight_ataque_4 = highlight.iloc[:, 3].tolist()
                        highlight_ataque_5 = highlight.iloc[:, 4].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = pd.DataFrame(highlight_ataque_1).reset_index(drop=True)
                        highlight_ataque_2_value = pd.DataFrame(highlight_ataque_2).reset_index(drop=True)
                        highlight_ataque_3_value = pd.DataFrame(highlight_ataque_3).reset_index(drop=True)
                        highlight_ataque_4_value = pd.DataFrame(highlight_ataque_4).reset_index(drop=True)
                        highlight_ataque_5_value = pd.DataFrame(highlight_ataque_5).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = highlight_ataque_1_value.iat[0,0]
                        highlight_ataque_2_value = highlight_ataque_2_value.iat[0,0]
                        highlight_ataque_3_value = highlight_ataque_3_value.iat[0,0]
                        highlight_ataque_4_value = highlight_ataque_4_value.iat[0,0]
                        highlight_ataque_5_value = highlight_ataque_5_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"ataque
                        ataque_ranking_df = pd.read_csv("Ataque_ranking.csv")
                        # Building the Extended Title"
                        rows_count = ataque_ranking_df[(ataque_ranking_df['Liga'] == liga)  & 
                                                                            (ataque_ranking_df['Posição'] == posição)].shape[0]
                        Passes_terço_final_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes terço final certos /90_Ranking'].values
                        Passes_terço_final_certos_per_ranking_value = Passes_terço_final_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_terço_final_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_terço_final_certos_per_ranking_value = f"Passes terço final certos /90 {output_str} {highlight_ataque_1_value}"

                        # Building the Extended Title"
                        Cruzamentos_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Cruzamentos certos p/90_Ranking'].values
                        Cruzamentos_certos_per_ranking_value = Cruzamentos_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Cruzamentos_certos_per_ranking_value}/{rows_count})"
                        full_title_Cruzamentos_certos_per_ranking_value = f"Cruzamentos certos /90 {output_str} {highlight_ataque_2_value}"

                        # Building the Extended Title"
                        Passes_área_do_pênalti_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes área do pênalti certos /90_Ranking'].values
                        Passes_área_do_pênalti_certos_per_ranking_value = Passes_área_do_pênalti_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_área_do_pênalti_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_área_do_pênalti_certos_per_ranking_value = f"Passes área do pênalti certos /90 {output_str} {highlight_ataque_3_value}"

                        # Building the Extended Title"
                        Passes_inteligentes_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes inteligentes certos /90_Ranking'].values
                        Passes_inteligentes_certos_per_ranking_value = Passes_inteligentes_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_inteligentes_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_inteligentes_certos_per_ranking_value = f"Passes inteligentes certos /90 {output_str} {highlight_ataque_4_value}"

                        # Building the Extended Title"
                        Deep_completed_crosses_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Deep completed crosses /90_Ranking'].values
                        Deep_completed_crosses_per_ranking_value = Deep_completed_crosses_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completed_crosses_per_ranking_value}/{rows_count})"
                        full_title_Deep_completed_crosses_per_ranking_value = f"Deep completed crosses /90 {output_str} {highlight_ataque_5_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_ataque_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_ataque_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_terço_final_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_ataque_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_ataque_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Cruzamentos_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_ataque_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_ataque_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_área_do_pênalti_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_ataque_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_ataque_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_inteligentes_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax5.scatter(metrics_ataque_5, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax5.scatter(highlight_ataque_5, highlight_y, color='blue', s=60, label=jogadores)
                        ax5.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Deep_completed_crosses_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax5.legend(loc='right', bbox_to_anchor=(0.2, -2.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Último passe"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Último_passe_Lateral_Charts = pd.read_csv('último_passe.csv')
                        Último_passe_Lateral_Charts_1 = Último_passe_Lateral_Charts[(Último_passe_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Último_passe_Lateral_Charts['Liga']==liga)&
                                                                                    (Último_passe_Lateral_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Último_passe_Lateral_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Último_passe_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Último_passe_Lateral_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Último_passe_Lateral_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Último_passe_Lateral_Charts_2 = Último_passe_Lateral_Charts[(Último_passe_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Último_passe_Lateral_Charts_2 = Último_passe_Lateral_Charts[(Último_passe_Lateral_Charts['Liga']==liga)&(Último_passe_Lateral_Charts['Posição']==posição)]
                        metrics = Último_passe_Lateral_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_último_passe_1 = metrics.iloc[:, 0].tolist()
                        metrics_último_passe_2 = metrics.iloc[:, 1].tolist()
                        metrics_último_passe_3 = metrics.iloc[:, 2].tolist()
                        metrics_último_passe_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Último_passe_Lateral_Charts_2[(Último_passe_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_último_passe_1 = highlight.iloc[:, 0].tolist()
                        highlight_último_passe_2 = highlight.iloc[:, 1].tolist()
                        highlight_último_passe_3 = highlight.iloc[:, 2].tolist()
                        highlight_último_passe_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = pd.DataFrame(highlight_último_passe_1).reset_index(drop=True)
                        highlight_último_passe_2_value = pd.DataFrame(highlight_último_passe_2).reset_index(drop=True)
                        highlight_último_passe_3_value = pd.DataFrame(highlight_último_passe_3).reset_index(drop=True)
                        highlight_último_passe_4_value = pd.DataFrame(highlight_último_passe_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = highlight_último_passe_1_value.iat[0,0]
                        highlight_último_passe_2_value = highlight_último_passe_2_value.iat[0,0]
                        highlight_último_passe_3_value = highlight_último_passe_3_value.iat[0,0]
                        highlight_último_passe_4_value = highlight_último_passe_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        último_passe_ranking_df = pd.read_csv("Último_passe_ranking.csv")
                        # Building the Extended Title"
                        rows_count = último_passe_ranking_df[(último_passe_ranking_df['Liga'] == liga)  & 
                                                                            (último_passe_ranking_df['Posição'] == posição)].shape[0]
                        Assistências_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Assistências /90_Ranking'].values
                        Assistências_per_ranking_value = Assistências_per_ranking_value[0].astype(int)
                        output_str = f"({Assistências_per_ranking_value}/{rows_count})"
                        full_title_Assistências_per_ranking_value = f"Assistências /90 {output_str} {highlight_último_passe_1_value}"

                        # Building the Extended Title"
                        xA_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'xA /90_Ranking'].values
                        xA_per_ranking_value = xA_per_ranking_value[0].astype(int)
                        output_str = f"({xA_per_ranking_value}/{rows_count})"
                        full_title_xA_per_ranking_value = f"xA /90 {output_str} {highlight_último_passe_2_value}"

                        # Building the Extended Title"
                        Deep_completions_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Deep completions /90_Ranking'].values
                        Deep_completions_per_ranking_value = Deep_completions_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completions_per_ranking_value}/{rows_count})"
                        full_title_Deep_completions_per_ranking_value = f"Deep completions /90 {output_str} {highlight_último_passe_3_value}"

                        # Building the Extended Title"
                        Passes_chave_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Passes chave /90_Ranking'].values
                        Passes_chave_per_ranking_value = Passes_chave_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_chave_per_ranking_value}/{rows_count})"
                        full_title_Passes_chave_per_ranking_value = f"Passes chave /90 {output_str} {highlight_último_passe_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_último_passe_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_último_passe_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Assistências_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_último_passe_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_último_passe_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_xA_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_último_passe_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_último_passe_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Deep_completions_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_último_passe_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_último_passe_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_chave_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.7), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Drible"):
                
                        Drible_Lateral_Charts = pd.read_csv('drible.csv')
                        Drible_Lateral_Charts_1 = Drible_Lateral_Charts[(Drible_Lateral_Charts['Atleta']==jogadores)&
                                                                                    (Drible_Lateral_Charts['Liga']==liga)&
                                                                                    (Drible_Lateral_Charts['Posição']==posição)]

    ##########################################################################################################################
    ##########################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Drible_Lateral_Charts_2 = Drible_Lateral_Charts[(Drible_Lateral_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Drible_Lateral_Charts_2 = Drible_Lateral_Charts[(Drible_Lateral_Charts['Liga']==liga)&(Drible_Lateral_Charts['Posição']==posição)]
                        metrics = Drible_Lateral_Charts_2.iloc[:, np.r_[-2]].reset_index(drop=True)
                        metrics_drible_1 = metrics.iloc[:, 0].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Drible_Lateral_Charts_2[(Drible_Lateral_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[-2]].reset_index(drop=True)
                        highlight_drible_1 = highlight.iloc[:, 0].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = pd.DataFrame(highlight_drible_1).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = highlight_drible_1_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_drible_1])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_drible_1])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1) = plt.subplots(figsize=(7, 1.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        drible_ranking_df = pd.read_csv("Drible_ranking.csv")
                        # Building the Extended Title"
                        rows_count = drible_ranking_df[(drible_ranking_df['Liga'] == liga)  & 
                                                                            (drible_ranking_df['Posição'] == posição)].shape[0]
                        Dribles_bem_sucedidos_per_ranking_value = drible_ranking_df.loc[(drible_ranking_df['Atleta'] == jogadores) & 
                                                                            (drible_ranking_df['Liga'] == liga) & 
                                                                            (drible_ranking_df['Posição'] == posição), 'Dribles bem sucedidos /90_Ranking'].values
                        Dribles_bem_sucedidos_per_ranking_value = Dribles_bem_sucedidos_per_ranking_value[0].astype(int)
                        output_str = f"({Dribles_bem_sucedidos_per_ranking_value}/{rows_count})"
                        full_title_Dribles_bem_sucedidos_per_ranking_value = f"Dribles bem sucedidos /90 {output_str} {highlight_drible_1_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_drible_1, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax1.scatter(highlight_drible_1, highlight_y, color='blue', s=60, label=jogadores)
                        ax1.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Dribles_bem_sucedidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax1.legend(loc='right', bbox_to_anchor=(0.2, -1.3), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
                
            elif posição == ("ZAGUEIRO"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                Zagueiro_Charts = pd.read_csv('Zagueiro.csv')
                Zagueiro_Charts_1 = Zagueiro_Charts[(Zagueiro_Charts['Atleta']==jogadores)&(Zagueiro_Charts['Liga']==liga)]
                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Zagueiro_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Zagueiro_Charts_1.iloc[:, np.r_[7:10]].reset_index(drop=True)
                metrics_list = metrics.iloc[0].tolist()
                #Collecting clube
                clube =  Zagueiro_Charts_1.iat[0, 1]
                
                ## parameter names
                params = metrics.columns.tolist()

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100)]

                ## parameter value
                values = metrics_list

                ## title values
                title = dict(
                    title_name=jogadores,
                    title_color = 'blue',
                    subtitle_name=posição,
                    subtitle_color='#344D94',
                    title_name_2=clube,
                    title_color_2 = 'blue',
                    subtitle_name_2='2023',
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                ## instantiate object
                radar = Radar()

                ## instantiate object -- changing fontsize
                radar=Radar(fontfamily='Cursive', range_fontsize=13)
                radar=Radar(fontfamily='Cursive', label_fontsize=15)

                ## plot radar -- filename and dpi
                fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                        title=title, endnote=endnote, dpi=600)
                st.pyplot(fig)


                #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição dos Atributos de todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                # Dynamically create the HTML string with the 'jogadores' variable
                title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                # Use the dynamically created HTML string in st.markdown
                st.markdown(title_html, unsafe_allow_html=True)

                #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                # Collecting data
                Zagueiro_Charts_2 = Zagueiro_Charts[(Zagueiro_Charts['Liga']==liga)]

                #Collecting data to plot
                metrics = Zagueiro_Charts_2.iloc[:, np.r_[4:7]].reset_index(drop=True)
                metrics_participação = metrics.iloc[:, 0].tolist()
                metrics_defesa = metrics.iloc[:, 1].tolist()
                metrics_construção = metrics.iloc[:, 2].tolist()
                metrics_y = [0] * len(metrics_participação)

                # The specific data point you want to highlight
                highlight = Zagueiro_Charts_2[(Zagueiro_Charts_2['Atleta']==jogadores)]
                highlight = highlight.iloc[:, np.r_[4:7]].reset_index(drop=True)
                highlight_participação = highlight.iloc[:, 0].tolist()
                highlight_defesa = highlight.iloc[:, 1].tolist()
                highlight_construção = highlight.iloc[:, 2].tolist()
                highlight_y = 0

                # Computing the selected player specific values
                highlight_participação_value = pd.DataFrame(highlight_participação).reset_index(drop=True)
                highlight_defesa_value = pd.DataFrame(highlight_defesa).reset_index(drop=True)
                highlight_construção_value = pd.DataFrame(highlight_construção).reset_index(drop=True)

                highlight_participação_value = highlight_participação_value.iat[0,0]
                highlight_defesa_value = highlight_defesa_value.iat[0,0]
                highlight_construção_value = highlight_construção_value.iat[0,0]

                # Computing the min and max value across all lists using a generator expression
                min_value = min(min(lst) for lst in [metrics_participação, metrics_defesa, metrics_construção])
                min_value = min_value - 0.1
                max_value = max(max(lst) for lst in [metrics_participação, metrics_defesa, metrics_construção])
                max_value = max_value + 0.1

                # Create two subplots vertically aligned with separate x-axes
                fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 3.5))
                ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                #Collecting Additional Information
                # Load the saved DataFrame from "Zagueiro_ranking.csv"apoio
                zagueiro_ranking_df = pd.read_csv("Zagueiro_ranking.csv")
                # Building the Extended Title"
                rows_count = zagueiro_ranking_df[zagueiro_ranking_df['Liga'] == liga].shape[0]
                participacao_ranking_value = zagueiro_ranking_df.loc[(zagueiro_ranking_df['Atleta'] == jogadores) & 
                                                                    (zagueiro_ranking_df['Liga'] == liga), 'Participação_Ranking'].values
                participacao_ranking_value = participacao_ranking_value[0].astype(int)
                output_str = f"({participacao_ranking_value}/{rows_count})"
                full_title_participação = f"Participação {output_str} {highlight_participação_value}"
                
                # Building the Extended Title"
                defesa_ranking_value = zagueiro_ranking_df.loc[(zagueiro_ranking_df['Atleta'] == jogadores) & 
                                                                    (zagueiro_ranking_df['Liga'] == liga), 'Defesa_Ranking'].values
                defesa_ranking_value = defesa_ranking_value[0].astype(int)
                output_str = f"({defesa_ranking_value}/{rows_count})"
                full_title_defesa = f"Defesa {output_str} {highlight_defesa_value}"
                
                # Building the Extended Title"
                construção_ranking_value = zagueiro_ranking_df.loc[(zagueiro_ranking_df['Atleta'] == jogadores) & 
                                                                    (zagueiro_ranking_df['Liga'] == liga), 'Construção_Ranking'].values
                construção_ranking_value = construção_ranking_value[0].astype(int)
                output_str = f"({construção_ranking_value}/{rows_count})"
                full_title_construção = f"Construção {output_str} {highlight_construção_value}"

                # Plot the first scatter plot in the first subplot
                ax1.scatter(metrics_participação, metrics_y, color='deepskyblue')
                ax1.scatter(highlight_participação, highlight_y, color='blue', s=60)
                ax1.get_yaxis().set_visible(False)
                ax1.set_title(full_title_participação, fontsize=12, fontweight='bold')
                ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax2.scatter(metrics_defesa, metrics_y, color='deepskyblue')
                ax2.scatter(highlight_defesa, highlight_y, color='blue', s=60)
                ax2.get_yaxis().set_visible(False)
                ax2.set_title(full_title_defesa, fontsize=12, fontweight='bold')
                ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax3.scatter(metrics_construção, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                ax3.scatter(highlight_construção, highlight_y, color='blue', s=60, label=jogadores)
                ax3.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                ax3.get_yaxis().set_visible(False)
                ax3.set_title(full_title_construção, fontsize=12, fontweight='bold')
                ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                plt.tight_layout()  # Adjust the layout to prevent overlap
                plt.show()

                ax3.legend(loc='right', bbox_to_anchor=(0.2, -1.7), fontsize="6", frameon=False)
                plt.show()

                st.pyplot(fig)
    #############################################################################################################################
    #############################################################################################################################
    #############################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
                if posição:
                    atributos = atributos_zagueiro['ZAGUEIRO']
                    atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
                    if atributo == ("Participação"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Participação_Zagueiro_Charts = pd.read_csv('participação.csv')
                        Participação_Zagueiro_Charts_1 = Participação_Zagueiro_Charts[(Participação_Zagueiro_Charts['Atleta']==jogadores)&
                                                                                    (Participação_Zagueiro_Charts['Liga']==liga)&
                                                                                    (Participação_Zagueiro_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Participação_Zagueiro_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Participação_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Participação_Zagueiro_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Participação_Zagueiro_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)


                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Participação_Zagueiro_Charts_2 = Participação_Zagueiro_Charts[(Participação_Zagueiro_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Participação_Zagueiro_Charts_2 = Participação_Zagueiro_Charts[(Participação_Zagueiro_Charts['Liga']==liga)&(Participação_Zagueiro_Charts['Posição']==posição)]
                        metrics = Participação_Zagueiro_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_participação_1 = metrics.iloc[:, 0].tolist()
                        metrics_participação_2 = metrics.iloc[:, 1].tolist()
                        metrics_participação_3 = metrics.iloc[:, 2].tolist()
                        metrics_participação_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Participação_Zagueiro_Charts_2[(Participação_Zagueiro_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_participação_1 = highlight.iloc[:, 0].tolist()
                        highlight_participação_2 = highlight.iloc[:, 1].tolist()
                        highlight_participação_3 = highlight.iloc[:, 2].tolist()
                        highlight_participação_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
                        highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
                        highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
                        highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

                        highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
                        highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
                        highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
                        highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        participação_ranking_df = pd.read_csv("Participação_ranking.csv")
                        # Building the Extended Title
                        rows_count = participação_ranking_df[(participação_ranking_df['Liga'] == liga)  & 
                                                                            (participação_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_participação_1_value}"
                        
                        # Building the Extended Title"
                        Passes_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes /90_Ranking'].values
                        Passes_per_ranking_value = Passes_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_per_ranking_value}/{rows_count})"
                        full_title_Passes_per_ranking_value = f"Passes /90 {output_str} {highlight_participação_2_value}"
                        
                        # Building the Extended Title"
                        Passes_recebidos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_participação_3_value}"
                        
                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_participação_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_participação_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_participação_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_participação_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_participação_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_participação_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_participação_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_participação_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_participação_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -2.0), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Defesa"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Defesa_Zagueiro_Charts = pd.read_csv('defesa.csv')
                        Defesa_Zagueiro_Charts_1 = Defesa_Zagueiro_Charts[(Defesa_Zagueiro_Charts['Atleta']==jogadores)&
                                                                                    (Defesa_Zagueiro_Charts['Liga']==liga)&
                                                                                    (Defesa_Zagueiro_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Defesa_Zagueiro_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Defesa_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Defesa_Zagueiro_Charts_1.iloc[:, np.r_[10:16]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Defesa_Zagueiro_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #Collecting data to plot
                        Defesa_Zagueiro_Charts_2 = Defesa_Zagueiro_Charts[(Defesa_Zagueiro_Charts['Liga']==liga)&(Defesa_Zagueiro_Charts['Posição']==posição)]
                        metrics = Defesa_Zagueiro_Charts_2.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        metrics_defesa_1 = metrics.iloc[:, 0].tolist()
                        metrics_defesa_2 = metrics.iloc[:, 1].tolist()
                        metrics_defesa_3 = metrics.iloc[:, 2].tolist()
                        metrics_defesa_4 = metrics.iloc[:, 3].tolist()
                        metrics_defesa_5 = metrics.iloc[:, 4].tolist()
                        metrics_defesa_6 = metrics.iloc[:, 5].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Defesa_Zagueiro_Charts_2[(Defesa_Zagueiro_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_defesa_1 = highlight.iloc[:, 0].tolist()
                        highlight_defesa_2 = highlight.iloc[:, 1].tolist()
                        highlight_defesa_3 = highlight.iloc[:, 2].tolist()
                        highlight_defesa_4 = highlight.iloc[:, 3].tolist()
                        highlight_defesa_5 = highlight.iloc[:, 4].tolist()
                        highlight_defesa_6 = highlight.iloc[:, 5].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_defesa_1_value = pd.DataFrame(highlight_defesa_1).reset_index(drop=True)
                        highlight_defesa_2_value = pd.DataFrame(highlight_defesa_2).reset_index(drop=True)
                        highlight_defesa_3_value = pd.DataFrame(highlight_defesa_3).reset_index(drop=True)
                        highlight_defesa_4_value = pd.DataFrame(highlight_defesa_4).reset_index(drop=True)
                        highlight_defesa_5_value = pd.DataFrame(highlight_defesa_5).reset_index(drop=True)
                        highlight_defesa_6_value = pd.DataFrame(highlight_defesa_6).reset_index(drop=True)

                        highlight_defesa_1_value = highlight_defesa_1_value.iat[0,0]
                        highlight_defesa_2_value = highlight_defesa_2_value.iat[0,0]
                        highlight_defesa_3_value = highlight_defesa_3_value.iat[0,0]
                        highlight_defesa_4_value = highlight_defesa_4_value.iat[0,0]
                        highlight_defesa_5_value = highlight_defesa_5_value.iat[0,0]
                        highlight_defesa_6_value = highlight_defesa_6_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        defesa_ranking_df = pd.read_csv("Defesa_ranking.csv")
                        # Building the Extended Title"
                        rows_count = defesa_ranking_df[(defesa_ranking_df['Liga'] == liga)  & 
                                                                            (defesa_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_defesa_1_value}"

                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_defesa_2_value}"

                        # Building the Extended Title"
                        Interceptações_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Interceptações /90_Ranking'].values
                        Interceptações_per_ranking_value = Interceptações_per_ranking_value[0].astype(int)
                        output_str = f"({Interceptações_per_ranking_value}/{rows_count})"
                        full_title_Interceptações_per_ranking_value = f"Interceptações /90 {output_str} {highlight_defesa_3_value}"

                        # Building the Extended Title"
                        Carrinhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Carrinhos /90_Ranking'].values
                        Carrinhos_per_ranking_value = Carrinhos_per_ranking_value[0].astype(int)
                        output_str = f"({Carrinhos_per_ranking_value}/{rows_count})"
                        full_title_Carrinhos_per_ranking_value = f"Carrinhos /90 {output_str} {highlight_defesa_4_value}"

                        # Building the Extended Title"
                        Ações_defensivas_bem_sucedidas_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Ações defensivas bem sucedidas /90_Ranking'].values
                        Ações_defensivas_bem_sucedidas_per_ranking_value = Ações_defensivas_bem_sucedidas_per_ranking_value[0].astype(int)
                        output_str = f"({Ações_defensivas_bem_sucedidas_per_ranking_value}/{rows_count})"
                        full_title_Ações_defensivas_bem_sucedidas_per_ranking_value = f"Ações defensivas bem sucedidas /90 {output_str} {highlight_defesa_5_value}"

                        # Building the Extended Title"
                        Duelos_defensivos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos ganhos /90_Ranking'].values
                        Duelos_defensivos_ganhos_per_ranking_value = Duelos_defensivos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_ganhos_per_ranking_value = f"Duelos defensivos ganhos /90 {output_str} {highlight_defesa_6_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_defesa_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_defesa_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_defesa_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_defesa_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_defesa_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_defesa_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Interceptações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_defesa_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_defesa_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Carrinhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax5.scatter(metrics_defesa_5, metrics_y, color='deepskyblue')
                        ax5.scatter(highlight_defesa_5, highlight_y, color='blue', s=60)
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Ações_defensivas_bem_sucedidas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax6.scatter(metrics_defesa_6, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax6.scatter(highlight_defesa_6, highlight_y, color='blue', s=60, label=jogadores)
                        ax6.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax6.get_yaxis().set_visible(False)
                        ax6.set_title(full_title_Duelos_defensivos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax6.spines['top'].set_visible(False)
                        ax6.spines['right'].set_visible(False)
                        ax6.spines['bottom'].set_visible(False)
                        ax6.spines['left'].set_visible(False)
                        ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax6.legend(loc='right', bbox_to_anchor=(0.2, -5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Construção"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Construção_Zagueiro_Charts = pd.read_csv('construção.csv')
                        Construção_Zagueiro_Charts_1 = Construção_Zagueiro_Charts[(Construção_Zagueiro_Charts['Atleta']==jogadores)&
                                                                                    (Construção_Zagueiro_Charts['Liga']==liga)&
                                                                                    (Construção_Zagueiro_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Construção_Zagueiro_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Construção_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Construção_Zagueiro_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Construção_Zagueiro_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Construção_Zagueiro_Charts_2 = Construção_Zagueiro_Charts[(Construção_Zagueiro_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Construção_Zagueiro_Charts_2 = Construção_Zagueiro_Charts[(Construção_Zagueiro_Charts['Liga']==liga)&(Construção_Zagueiro_Charts['Posição']==posição)]
                        metrics = Construção_Zagueiro_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_construção_1 = metrics.iloc[:, 0].tolist()
                        metrics_construção_2 = metrics.iloc[:, 1].tolist()
                        metrics_construção_3 = metrics.iloc[:, 2].tolist()
                        metrics_construção_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Construção_Zagueiro_Charts_2[(Construção_Zagueiro_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_construção_1 = highlight.iloc[:, 0].tolist()
                        highlight_construção_2 = highlight.iloc[:, 1].tolist()
                        highlight_construção_3 = highlight.iloc[:, 2].tolist()
                        highlight_construção_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_construção_1_value = pd.DataFrame(highlight_construção_1).reset_index(drop=True)
                        highlight_construção_2_value = pd.DataFrame(highlight_construção_2).reset_index(drop=True)
                        highlight_construção_3_value = pd.DataFrame(highlight_construção_3).reset_index(drop=True)
                        highlight_construção_4_value = pd.DataFrame(highlight_construção_4).reset_index(drop=True)

                        highlight_construção_1_value = highlight_construção_1_value.iat[0,0]
                        highlight_construção_2_value = highlight_construção_2_value.iat[0,0]
                        highlight_construção_3_value = highlight_construção_3_value.iat[0,0]
                        highlight_construção_4_value = highlight_construção_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_construção_1, metrics_construção_2, 
                                                            metrics_construção_3, metrics_construção_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_construção_1, metrics_construção_2, 
                                                            metrics_construção_3, metrics_construção_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        construção_ranking_df = pd.read_csv("Construção_ranking.csv")

                        # Building the Extended Title"
                        rows_count = construção_ranking_df[(construção_ranking_df['Liga'] == liga)  & 
                                                                            (construção_ranking_df['Posição'] == posição)].shape[0]
                        Passes_entre_linhas_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes entre linhas certos /90_Ranking'].values
                        Passes_entre_linhas_certos_per_ranking_value = Passes_entre_linhas_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_entre_linhas_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_entre_linhas_certos_per_ranking_value = f"Passes entre linhas certos /90 {output_str} {highlight_construção_1_value}"

                        # Building the Extended Title"
                        Passes_progressivos_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes progressivos certos /90_Ranking'].values
                        Passes_progressivos_certos_per_ranking_value = Passes_progressivos_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_progressivos_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_progressivos_certos_per_ranking_value = f"Passes progressivos certos /90 /90 {output_str} {highlight_construção_2_value}"

                        # Building the Extended Title"
                        Passes_frontais_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes frontais certos /90_Ranking'].values
                        Passes_frontais_certos_per_ranking_value = Passes_frontais_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_frontais_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_frontais_certos_per_ranking_value = f"Passes frontais certos /90 {output_str} {highlight_construção_3_value}"

                        # Building the Extended Title"
                        Passes_terço_final_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes terço final certos /90_Ranking'].values
                        Passes_terço_final_certos_per_ranking_value = Passes_terço_final_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_terço_final_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_terço_final_certos_per_ranking_value = f"Passes terço final certos /90 {output_str} {highlight_construção_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_construção_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_construção_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_entre_linhas_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_construção_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_construção_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_progressivos_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_construção_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_construção_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_frontais_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_construção_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_construção_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_terço_final_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    #############################################################################################################################
    #############################################################################################################################
    #############################################################################################################################

            elif posição == ("MEIO-CAMPO"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                Meio_campo_Charts = pd.read_csv('Meio_Campo.csv')
                Meio_campo_Charts_1 = Meio_campo_Charts[(Meio_campo_Charts['Atleta']==jogadores)&(Meio_campo_Charts['Liga']==liga)]
                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Meio_campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Meio_campo_Charts_1.iloc[:, np.r_[11:18]].reset_index(drop=True)
                metrics_list = metrics.iloc[0].tolist()
                #Collecting clube
                clube = Meio_campo_Charts_1.iat[0, 1]
                
                ## parameter names
                params = metrics.columns.tolist()

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                ## parameter value
                values = metrics_list

                ## title values
                title = dict(
                    title_name=jogadores,
                    title_color = 'blue',
                    subtitle_name=posição,
                    subtitle_color='#344D94',
                    title_name_2=clube,
                    title_color_2 = 'blue',
                    subtitle_name_2='2023',
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                ## instantiate object
                radar = Radar()

                ## instantiate object -- changing fontsize
                radar=Radar(fontfamily='Cursive', range_fontsize=13)
                radar=Radar(fontfamily='Cursive', label_fontsize=15)

                ## plot radar -- filename and dpi
                fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                        title=title, endnote=endnote, dpi=600)
                st.pyplot(fig)

                ############################################################################################################################
                ############################################################################################################################
                ############################################################################################################################

                #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição dos Atributos de todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                # Dynamically create the HTML string with the 'jogadores' variable
                title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                # Use the dynamically created HTML string in st.markdown
                st.markdown(title_html, unsafe_allow_html=True)

                #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                # Collecting data
                Meio_campo_Charts_2 = Meio_campo_Charts[(Meio_campo_Charts['Liga']==liga)]

                #Collecting data to plot
                metrics = Meio_campo_Charts_2.iloc[:, np.r_[4:11]].reset_index(drop=True)
                metrics_participação = metrics.iloc[:, 0].tolist()
                metrics_defesa = metrics.iloc[:, 1].tolist()
                metrics_construção = metrics.iloc[:, 2].tolist()
                metrics_ataque = metrics.iloc[:, 3].tolist()
                metrics_último_passe = metrics.iloc[:, 4].tolist()
                metrics_ameaça_ofensiva = metrics.iloc[:, 5].tolist()
                metrics_drible = metrics.iloc[:, 6].tolist()
                metrics_y = [0] * len(metrics_participação)

                # The specific data point you want to highlight
                highlight = Meio_campo_Charts_2[(Meio_campo_Charts_2['Atleta']==jogadores)]
                highlight = highlight.iloc[:, np.r_[4:11]].reset_index(drop=True)
                highlight_participação = highlight.iloc[:, 0].tolist()
                highlight_defesa = highlight.iloc[:, 1].tolist()
                highlight_construção = highlight.iloc[:, 2].tolist()
                highlight_ataque = highlight.iloc[:, 3].tolist()
                highlight_último_passe = highlight.iloc[:, 4].tolist()
                highlight_ameaça_ofensiva = highlight.iloc[:, 5].tolist()
                highlight_drible = highlight.iloc[:, 6].tolist()
                highlight_y = 0

                # Computing the selected player specific values
                highlight_participação_value = pd.DataFrame(highlight_participação).reset_index(drop=True)
                highlight_defesa_value = pd.DataFrame(highlight_defesa).reset_index(drop=True)
                highlight_construção_value = pd.DataFrame(highlight_construção).reset_index(drop=True)
                highlight_ataque_value = pd.DataFrame(highlight_ataque).reset_index(drop=True)
                highlight_último_passe_value = pd.DataFrame(highlight_último_passe).reset_index(drop=True)
                highlight_ameaça_ofensiva_value = pd.DataFrame(highlight_ameaça_ofensiva).reset_index(drop=True)
                highlight_drible_value = pd.DataFrame(highlight_drible).reset_index(drop=True)

                highlight_participação_value = highlight_participação_value.iat[0,0]
                highlight_defesa_value = highlight_defesa_value.iat[0,0]
                highlight_construção_value = highlight_construção_value.iat[0,0]
                highlight_ataque_value = highlight_ataque_value.iat[0,0]
                highlight_último_passe_value = highlight_último_passe_value.iat[0,0]
                highlight_ameaça_ofensiva_value = highlight_ameaça_ofensiva_value.iat[0,0]
                highlight_drible_value = highlight_drible_value.iat[0,0]


                # Computing the min and max value across all lists using a generator expression
                min_value = min(min(lst) for lst in [metrics_participação, metrics_defesa, metrics_construção, 
                                                    metrics_ataque, metrics_último_passe, metrics_ameaça_ofensiva, 
                                                    metrics_drible])
                min_value = min_value - 0.1
                max_value = max(max(lst) for lst in [metrics_participação, metrics_defesa, metrics_construção, 
                                                    metrics_ataque, metrics_último_passe, metrics_ameaça_ofensiva, 
                                                    metrics_drible])
                max_value = max_value + 0.1

                # Create two subplots vertically aligned with separate x-axes
                fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(6.5, 6.5))
                ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                #Collecting Additional Information
                # Load the saved DataFrame from "Zagueiro_ranking.csv"apoio
                meio_campo_ranking_df = pd.read_csv("Meio_campo_ranking.csv")
                # Building the Extended Title"
                rows_count = meio_campo_ranking_df[meio_campo_ranking_df['Liga'] == liga].shape[0]
                participacao_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Participação_Ranking'].values
                participacao_ranking_value = participacao_ranking_value[0].astype(int)
                output_str = f"({participacao_ranking_value}/{rows_count})"
                full_title_participação = f"Participação {output_str} {highlight_participação_value}"
                
                # Building the Extended Title"
                defesa_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Defesa_Ranking'].values
                defesa_ranking_value = defesa_ranking_value[0].astype(int)
                output_str = f"({defesa_ranking_value}/{rows_count})"
                full_title_defesa = f"Defesa {output_str} {highlight_defesa_value}"

                # Building the Extended Title"
                construção_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Construção_Ranking'].values
                construção_ranking_value = construção_ranking_value[0].astype(int)
                output_str = f"({construção_ranking_value}/{rows_count})"
                full_title_construção = f"Construção {output_str} {highlight_construção_value}"

                # Building the Extended Title"
                ataque_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Ataque_Ranking'].values
                ataque_ranking_value = ataque_ranking_value[0].astype(int)
                output_str = f"({ataque_ranking_value}/{rows_count})"
                full_title_ataque = f"Ataque {output_str} {highlight_ataque_value}"

                # Building the Extended Title"
                último_passe_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Último passe_Ranking'].values
                último_passe_ranking_value = último_passe_ranking_value[0].astype(int)
                output_str = f"({último_passe_ranking_value}/{rows_count})"
                full_title_último_passe = f"Último passe {output_str} {highlight_último_passe_value}"

                # Building the Extended Title"
                ameaça_ofensiva_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Ameaça Ofensiva_Ranking'].values
                ameaça_ofensiva_ranking_value = ameaça_ofensiva_ranking_value[0].astype(int)
                output_str = f"({ameaça_ofensiva_ranking_value}/{rows_count})"
                full_title_ameaça_ofensiva = f"Ameaça ofensiva {output_str} {highlight_ameaça_ofensiva_value}"
                # Building the Extended Title"
                drible_ranking_value = meio_campo_ranking_df.loc[(meio_campo_ranking_df['Atleta'] == jogadores) & 
                                                                    (meio_campo_ranking_df['Liga'] == liga), 'Drible_Ranking'].values
                drible_ranking_value = drible_ranking_value[0].astype(int)
                output_str = f"({drible_ranking_value}/{rows_count})"
                full_title_drible = f"Drible {output_str} {highlight_drible_value}"

                # Plot the first scatter plot in the first subplot
                ax1.scatter(metrics_participação, metrics_y, color='deepskyblue')
                ax1.scatter(highlight_participação, highlight_y, color='blue', s=60)
                ax1.get_yaxis().set_visible(False)
                ax1.set_title(full_title_participação, fontsize=12, fontweight='bold')
                ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax2.scatter(metrics_defesa, metrics_y, color='deepskyblue')
                ax2.scatter(highlight_defesa, highlight_y, color='blue', s=60)
                ax2.get_yaxis().set_visible(False)
                ax2.set_title(full_title_defesa, fontsize=12, fontweight='bold')
                ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax3.scatter(metrics_construção, metrics_y, color='deepskyblue')
                ax3.scatter(highlight_construção, highlight_y, color='blue', s=60)
                ax3.get_yaxis().set_visible(False)
                ax3.set_title(full_title_construção, fontsize=12, fontweight='bold')
                ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax4.scatter(metrics_ataque, metrics_y, color='deepskyblue')
                ax4.scatter(highlight_ataque, highlight_y, color='blue', s=60)            
                ax4.get_yaxis().set_visible(False)
                ax4.set_title(full_title_ataque, fontsize=12, fontweight='bold')
                ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax4.spines['top'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['left'].set_visible(False)
                ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax5.scatter(metrics_último_passe, metrics_y, color='deepskyblue')
                ax5.scatter(highlight_último_passe, highlight_y, color='blue', s=60)            
                ax5.get_yaxis().set_visible(False)
                ax5.set_title(full_title_último_passe, fontsize=12, fontweight='bold')
                ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax5.spines['top'].set_visible(False)
                ax5.spines['right'].set_visible(False)
                ax5.spines['bottom'].set_visible(False)
                ax5.spines['left'].set_visible(False)
                ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax6.scatter(metrics_ameaça_ofensiva, metrics_y, color='deepskyblue')
                ax6.scatter(highlight_ameaça_ofensiva, highlight_y, color='blue', s=60)            
                ax6.get_yaxis().set_visible(False)
                ax6.set_title(full_title_ameaça_ofensiva, fontsize=12, fontweight='bold')
                ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax6.spines['top'].set_visible(False)
                ax6.spines['right'].set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.spines['left'].set_visible(False)
                ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax7.scatter(metrics_drible, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                ax7.scatter(highlight_drible, highlight_y, color='blue', s=60, label=jogadores)            
                ax7.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                ax7.get_yaxis().set_visible(False)
                ax7.set_title(full_title_drible, fontsize=12, fontweight='bold')
                ax7.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax7.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax7.spines['top'].set_visible(False)
                ax7.spines['right'].set_visible(False)
                ax7.spines['bottom'].set_visible(False)
                ax7.spines['left'].set_visible(False)
                ax7.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                plt.tight_layout()  # Adjust the layout to prevent overlap
                plt.show()

                ax7.legend(loc='right', bbox_to_anchor=(0.2, -3), fontsize="6", frameon=False)
                plt.show()

                st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
                if posição:
                    atributos = atributos_meio_campo['MEIO-CAMPO']
                    atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
                    if atributo == ("Participação"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Participação_Meio_campo_Charts = pd.read_csv('participação.csv')
                        Participação_Meio_campo_Charts_1 = Participação_Meio_campo_Charts[(Participação_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Participação_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Participação_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Participação_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Participação_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Participação_Meio_campo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Participação_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Participação_Meio_campo_Charts_2 = Participação_Meio_campo_Charts[(Participação_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Participação_Meio_campo_Charts_2 = Participação_Meio_campo_Charts[(Participação_Meio_campo_Charts['Liga']==liga)&(Participação_Meio_campo_Charts['Posição']==posição)]
                        metrics = Participação_Meio_campo_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_participação_1 = metrics.iloc[:, 0].tolist()
                        metrics_participação_2 = metrics.iloc[:, 1].tolist()
                        metrics_participação_3 = metrics.iloc[:, 2].tolist()
                        metrics_participação_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Participação_Meio_campo_Charts_2[(Participação_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_participação_1 = highlight.iloc[:, 0].tolist()
                        highlight_participação_2 = highlight.iloc[:, 1].tolist()
                        highlight_participação_3 = highlight.iloc[:, 2].tolist()
                        highlight_participação_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0


                        # Computing the selected player specific values
                        highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
                        highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
                        highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
                        highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

                        highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
                        highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
                        highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
                        highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        participação_ranking_df = pd.read_csv("Participação_ranking.csv")
                        # Building the Extended Title
                        rows_count = participação_ranking_df[(participação_ranking_df['Liga'] == liga)  & 
                                                                            (participação_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_participação_1_value}"
                        
                        # Building the Extended Title"
                        Passes_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes /90_Ranking'].values
                        Passes_per_ranking_value = Passes_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_per_ranking_value}/{rows_count})"
                        full_title_Passes_per_ranking_value = f"Passes /90 {output_str} {highlight_participação_2_value}"
                        
                        # Building the Extended Title"
                        Passes_recebidos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_participação_3_value}"
                        
                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_participação_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_participação_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_participação_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_participação_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_participação_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_participação_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_participação_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_participação_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_participação_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -2.0), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    if atributo == ("Defesa"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Defesa_Meio_campo_Charts = pd.read_csv('defesa.csv')
                        Defesa_Meio_campo_Charts_1 = Defesa_Meio_campo_Charts[(Defesa_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Defesa_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Defesa_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Defesa_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Defesa_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Defesa_Meio_campo_Charts_1.iloc[:, np.r_[10:16]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Defesa_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Defesa_Meio_campo_Charts_2 = Defesa_Meio_campo_Charts[(Defesa_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Defesa_Meio_campo_Charts_2 = Defesa_Meio_campo_Charts[(Defesa_Meio_campo_Charts['Liga']==liga)&(Defesa_Meio_campo_Charts['Posição']==posição)]
                        metrics = Defesa_Meio_campo_Charts_2.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        metrics_defesa_1 = metrics.iloc[:, 0].tolist()
                        metrics_defesa_2 = metrics.iloc[:, 1].tolist()
                        metrics_defesa_3 = metrics.iloc[:, 2].tolist()
                        metrics_defesa_4 = metrics.iloc[:, 3].tolist()
                        metrics_defesa_5 = metrics.iloc[:, 4].tolist()
                        metrics_defesa_6 = metrics.iloc[:, 5].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Defesa_Meio_campo_Charts_2[(Defesa_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_defesa_1 = highlight.iloc[:, 0].tolist()
                        highlight_defesa_2 = highlight.iloc[:, 1].tolist()
                        highlight_defesa_3 = highlight.iloc[:, 2].tolist()
                        highlight_defesa_4 = highlight.iloc[:, 3].tolist()
                        highlight_defesa_5 = highlight.iloc[:, 4].tolist()
                        highlight_defesa_6 = highlight.iloc[:, 5].tolist()
                        highlight_y = 0
                        # Computing the selected player specific values
                        highlight_defesa_1_value = pd.DataFrame(highlight_defesa_1).reset_index(drop=True)
                        highlight_defesa_2_value = pd.DataFrame(highlight_defesa_2).reset_index(drop=True)
                        highlight_defesa_3_value = pd.DataFrame(highlight_defesa_3).reset_index(drop=True)
                        highlight_defesa_4_value = pd.DataFrame(highlight_defesa_4).reset_index(drop=True)
                        highlight_defesa_5_value = pd.DataFrame(highlight_defesa_5).reset_index(drop=True)
                        highlight_defesa_6_value = pd.DataFrame(highlight_defesa_6).reset_index(drop=True)

                        highlight_defesa_1_value = highlight_defesa_1_value.iat[0,0]
                        highlight_defesa_2_value = highlight_defesa_2_value.iat[0,0]
                        highlight_defesa_3_value = highlight_defesa_3_value.iat[0,0]
                        highlight_defesa_4_value = highlight_defesa_4_value.iat[0,0]
                        highlight_defesa_5_value = highlight_defesa_5_value.iat[0,0]
                        highlight_defesa_6_value = highlight_defesa_6_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_defesa_1, metrics_defesa_2, 
                                                            metrics_defesa_3, metrics_defesa_4,
                                                            metrics_defesa_5, metrics_defesa_6])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        defesa_ranking_df = pd.read_csv("Defesa_ranking.csv")
                        # Building the Extended Title"
                        rows_count = defesa_ranking_df[(defesa_ranking_df['Liga'] == liga)  & 
                                                                            (defesa_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_defesa_1_value}"

                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_defesa_2_value}"

                        # Building the Extended Title"
                        Interceptações_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Interceptações /90_Ranking'].values
                        Interceptações_per_ranking_value = Interceptações_per_ranking_value[0].astype(int)
                        output_str = f"({Interceptações_per_ranking_value}/{rows_count})"
                        full_title_Interceptações_per_ranking_value = f"Interceptações /90 {output_str} {highlight_defesa_3_value}"

                        # Building the Extended Title"
                        Carrinhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Carrinhos /90_Ranking'].values
                        Carrinhos_per_ranking_value = Carrinhos_per_ranking_value[0].astype(int)
                        output_str = f"({Carrinhos_per_ranking_value}/{rows_count})"
                        full_title_Carrinhos_per_ranking_value = f"Carrinhos /90 {output_str} {highlight_defesa_4_value}"

                        # Building the Extended Title"
                        Ações_defensivas_bem_sucedidas_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Ações defensivas bem sucedidas /90_Ranking'].values
                        Ações_defensivas_bem_sucedidas_per_ranking_value = Ações_defensivas_bem_sucedidas_per_ranking_value[0].astype(int)
                        output_str = f"({Ações_defensivas_bem_sucedidas_per_ranking_value}/{rows_count})"
                        full_title_Ações_defensivas_bem_sucedidas_per_ranking_value = f"Ações defensivas bem sucedidas /90 {output_str} {highlight_defesa_5_value}"

                        # Building the Extended Title"
                        Duelos_defensivos_ganhos_per_ranking_value = defesa_ranking_df.loc[(defesa_ranking_df['Atleta'] == jogadores) & 
                                                                            (defesa_ranking_df['Liga'] == liga) & 
                                                                            (defesa_ranking_df['Posição'] == posição), 'Duelos defensivos ganhos /90_Ranking'].values
                        Duelos_defensivos_ganhos_per_ranking_value = Duelos_defensivos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_ganhos_per_ranking_value = f"Duelos defensivos ganhos /90 {output_str} {highlight_defesa_6_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_defesa_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_defesa_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_defesa_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_defesa_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_defesa_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_defesa_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Interceptações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_defesa_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_defesa_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Carrinhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax5.scatter(metrics_defesa_5, metrics_y, color='deepskyblue')
                        ax5.scatter(highlight_defesa_5, highlight_y, color='blue', s=60)
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Ações_defensivas_bem_sucedidas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax6.scatter(metrics_defesa_6, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax6.scatter(highlight_defesa_6, highlight_y, color='blue', s=60, label=jogadores)
                        ax6.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax6.get_yaxis().set_visible(False)
                        ax6.set_title(full_title_Duelos_defensivos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax6.spines['top'].set_visible(False)
                        ax6.spines['right'].set_visible(False)
                        ax6.spines['bottom'].set_visible(False)
                        ax6.spines['left'].set_visible(False)
                        ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax6.legend(loc='right', bbox_to_anchor=(0.2, -5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                    ##########################################################################################################################
                    ##########################################################################################################################
                    ##########################################################################################################################
                    ##########################################################################################################################
                    ##########################################################################################################################
                    ##########################################################################################################################

                    if atributo == ("Construção"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Construção_Meio_campo_Charts = pd.read_csv('construção.csv')
                        Construção_Meio_campo_Charts_1 = Construção_Meio_campo_Charts[(Construção_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Construção_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Construção_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Construção_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Construção_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Construção_Meio_campo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Construção_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Construção_Meio_campo_Charts_2 = Construção_Meio_campo_Charts[(Construção_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Construção_Meio_campo_Charts_2 = Construção_Meio_campo_Charts[(Construção_Meio_campo_Charts['Liga']==liga)&(Construção_Meio_campo_Charts['Posição']==posição)]
                        metrics = Construção_Meio_campo_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_construção_1 = metrics.iloc[:, 0].tolist()
                        metrics_construção_2 = metrics.iloc[:, 1].tolist()
                        metrics_construção_3 = metrics.iloc[:, 2].tolist()
                        metrics_construção_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Construção_Meio_campo_Charts_2[(Construção_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:10]].reset_index(drop=True)
                        highlight_construção_1 = highlight.iloc[:, 0].tolist()
                        highlight_construção_2 = highlight.iloc[:, 1].tolist()
                        highlight_construção_3 = highlight.iloc[:, 2].tolist()
                        highlight_construção_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_construção_1_value = pd.DataFrame(highlight_construção_1).reset_index(drop=True)
                        highlight_construção_2_value = pd.DataFrame(highlight_construção_2).reset_index(drop=True)
                        highlight_construção_3_value = pd.DataFrame(highlight_construção_3).reset_index(drop=True)
                        highlight_construção_4_value = pd.DataFrame(highlight_construção_4).reset_index(drop=True)

                        highlight_construção_1_value = highlight_construção_1_value.iat[0,0]
                        highlight_construção_2_value = highlight_construção_2_value.iat[0,0]
                        highlight_construção_3_value = highlight_construção_3_value.iat[0,0]
                        highlight_construção_4_value = highlight_construção_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_construção_1, metrics_construção_2, 
                                                            metrics_construção_3, metrics_construção_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_construção_1, metrics_construção_2, 
                                                            metrics_construção_3, metrics_construção_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        construção_ranking_df = pd.read_csv("Construção_ranking.csv")

                        # Building the Extended Title"
                        rows_count = construção_ranking_df[(construção_ranking_df['Liga'] == liga)  & 
                                                                            (construção_ranking_df['Posição'] == posição)].shape[0]
                        Passes_entre_linhas_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes entre linhas certos /90_Ranking'].values
                        Passes_entre_linhas_certos_per_ranking_value = Passes_entre_linhas_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_entre_linhas_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_entre_linhas_certos_per_ranking_value = f"Passes entre linhas certos /90 {output_str} {highlight_construção_1_value}"

                        # Building the Extended Title"
                        Passes_progressivos_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes progressivos certos /90_Ranking'].values
                        Passes_progressivos_certos_per_ranking_value = Passes_progressivos_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_progressivos_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_progressivos_certos_per_ranking_value = f"Passes progressivos certos /90 /90 {output_str} {highlight_construção_2_value}"

                        # Building the Extended Title"
                        Passes_frontais_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes frontais certos /90_Ranking'].values
                        Passes_frontais_certos_per_ranking_value = Passes_frontais_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_frontais_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_frontais_certos_per_ranking_value = f"Passes frontais certos /90 {output_str} {highlight_construção_3_value}"

                        # Building the Extended Title"
                        Passes_terço_final_certos_per_ranking_value = construção_ranking_df.loc[(construção_ranking_df['Atleta'] == jogadores) & 
                                                                            (construção_ranking_df['Liga'] == liga) & 
                                                                            (construção_ranking_df['Posição'] == posição), 'Passes terço final certos /90_Ranking'].values
                        Passes_terço_final_certos_per_ranking_value = Passes_terço_final_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_terço_final_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_terço_final_certos_per_ranking_value = f"Passes terço final certos /90 {output_str} {highlight_construção_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_construção_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_construção_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_entre_linhas_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_construção_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_construção_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_progressivos_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_construção_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_construção_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_frontais_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_construção_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_construção_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_terço_final_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Ataque"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Ataque_Meio_campo_Charts = pd.read_csv('ataque.csv')
                        Ataque_Meio_campo_Charts_1 = Ataque_Meio_campo_Charts[(Ataque_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Ataque_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Ataque_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Ataque_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Ataque_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Ataque_Meio_campo_Charts_1.iloc[:, np.r_[9:14]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Ataque_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Ataque_Meio_campo_Charts_2 = Ataque_Meio_campo_Charts[(Ataque_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Ataque_Meio_campo_Charts_2 = Ataque_Meio_campo_Charts[(Ataque_Meio_campo_Charts['Liga']==liga)&(Ataque_Meio_campo_Charts['Posição']==posição)]
                        metrics = Ataque_Meio_campo_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_ataque_1 = metrics.iloc[:, 0].tolist()
                        metrics_ataque_2 = metrics.iloc[:, 1].tolist()
                        metrics_ataque_3 = metrics.iloc[:, 2].tolist()
                        metrics_ataque_4 = metrics.iloc[:, 3].tolist()
                        metrics_ataque_5 = metrics.iloc[:, 4].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Ataque_Meio_campo_Charts_2[(Ataque_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_ataque_1 = highlight.iloc[:, 0].tolist()
                        highlight_ataque_2 = highlight.iloc[:, 1].tolist()
                        highlight_ataque_3 = highlight.iloc[:, 2].tolist()
                        highlight_ataque_4 = highlight.iloc[:, 3].tolist()
                        highlight_ataque_5 = highlight.iloc[:, 4].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = pd.DataFrame(highlight_ataque_1).reset_index(drop=True)
                        highlight_ataque_2_value = pd.DataFrame(highlight_ataque_2).reset_index(drop=True)
                        highlight_ataque_3_value = pd.DataFrame(highlight_ataque_3).reset_index(drop=True)
                        highlight_ataque_4_value = pd.DataFrame(highlight_ataque_4).reset_index(drop=True)
                        highlight_ataque_5_value = pd.DataFrame(highlight_ataque_5).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = highlight_ataque_1_value.iat[0,0]
                        highlight_ataque_2_value = highlight_ataque_2_value.iat[0,0]
                        highlight_ataque_3_value = highlight_ataque_3_value.iat[0,0]
                        highlight_ataque_4_value = highlight_ataque_4_value.iat[0,0]
                        highlight_ataque_5_value = highlight_ataque_5_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"ataque
                        ataque_ranking_df = pd.read_csv("Ataque_ranking.csv")
                        # Building the Extended Title"
                        rows_count = ataque_ranking_df[(ataque_ranking_df['Liga'] == liga)  & 
                                                                            (ataque_ranking_df['Posição'] == posição)].shape[0]
                        Passes_terço_final_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes terço final certos /90_Ranking'].values
                        Passes_terço_final_certos_per_ranking_value = Passes_terço_final_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_terço_final_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_terço_final_certos_per_ranking_value = f"Passes terço final certos /90 {output_str} {highlight_ataque_1_value}"

                        # Building the Extended Title"
                        Cruzamentos_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Cruzamentos certos p/90_Ranking'].values
                        Cruzamentos_certos_per_ranking_value = Cruzamentos_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Cruzamentos_certos_per_ranking_value}/{rows_count})"
                        full_title_Cruzamentos_certos_per_ranking_value = f"Cruzamentos certos /90 {output_str} {highlight_ataque_2_value}"

                        # Building the Extended Title"
                        Passes_área_do_pênalti_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes área do pênalti certos /90_Ranking'].values
                        Passes_área_do_pênalti_certos_per_ranking_value = Passes_área_do_pênalti_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_área_do_pênalti_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_área_do_pênalti_certos_per_ranking_value = f"Passes área do pênalti certos /90 {output_str} {highlight_ataque_3_value}"

                        # Building the Extended Title"
                        Passes_inteligentes_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes inteligentes certos /90_Ranking'].values
                        Passes_inteligentes_certos_per_ranking_value = Passes_inteligentes_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_inteligentes_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_inteligentes_certos_per_ranking_value = f"Passes inteligentes certos /90 {output_str} {highlight_ataque_4_value}"

                        # Building the Extended Title"
                        Deep_completed_crosses_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Deep completed crosses /90_Ranking'].values
                        Deep_completed_crosses_per_ranking_value = Deep_completed_crosses_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completed_crosses_per_ranking_value}/{rows_count})"
                        full_title_Deep_completed_crosses_per_ranking_value = f"Deep completed crosses /90 {output_str} {highlight_ataque_5_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_ataque_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_ataque_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_terço_final_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_ataque_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_ataque_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Cruzamentos_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_ataque_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_ataque_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_área_do_pênalti_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_ataque_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_ataque_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_inteligentes_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax5.scatter(metrics_ataque_5, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax5.scatter(highlight_ataque_5, highlight_y, color='blue', s=60, label=jogadores)
                        ax5.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Deep_completed_crosses_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax5.legend(loc='right', bbox_to_anchor=(0.2, -2.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Último passe"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Último_passe_Meio_campo_Charts = pd.read_csv('último_passe.csv')
                        Último_passe_Meio_campo_Charts_1 = Último_passe_Meio_campo_Charts[(Último_passe_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Último_passe_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Último_passe_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Último_passe_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Último_passe_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Último_passe_Meio_campo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Último_passe_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Último_passe_Meio_campo_Charts_2 = Último_passe_Meio_campo_Charts[(Último_passe_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Último_passe_Meio_campo_Charts_2 = Último_passe_Meio_campo_Charts[(Último_passe_Meio_campo_Charts['Liga']==liga)&(Último_passe_Meio_campo_Charts['Posição']==posição)]
                        metrics = Último_passe_Meio_campo_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_último_passe_1 = metrics.iloc[:, 0].tolist()
                        metrics_último_passe_2 = metrics.iloc[:, 1].tolist()
                        metrics_último_passe_3 = metrics.iloc[:, 2].tolist()
                        metrics_último_passe_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Último_passe_Meio_campo_Charts_2[(Último_passe_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_último_passe_1 = highlight.iloc[:, 0].tolist()
                        highlight_último_passe_2 = highlight.iloc[:, 1].tolist()
                        highlight_último_passe_3 = highlight.iloc[:, 2].tolist()
                        highlight_último_passe_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = pd.DataFrame(highlight_último_passe_1).reset_index(drop=True)
                        highlight_último_passe_2_value = pd.DataFrame(highlight_último_passe_2).reset_index(drop=True)
                        highlight_último_passe_3_value = pd.DataFrame(highlight_último_passe_3).reset_index(drop=True)
                        highlight_último_passe_4_value = pd.DataFrame(highlight_último_passe_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = highlight_último_passe_1_value.iat[0,0]
                        highlight_último_passe_2_value = highlight_último_passe_2_value.iat[0,0]
                        highlight_último_passe_3_value = highlight_último_passe_3_value.iat[0,0]
                        highlight_último_passe_4_value = highlight_último_passe_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        último_passe_ranking_df = pd.read_csv("Último_passe_ranking.csv")
                        # Building the Extended Title"
                        rows_count = último_passe_ranking_df[(último_passe_ranking_df['Liga'] == liga)  & 
                                                                            (último_passe_ranking_df['Posição'] == posição)].shape[0]
                        Assistências_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Assistências /90_Ranking'].values
                        Assistências_per_ranking_value = Assistências_per_ranking_value[0].astype(int)
                        output_str = f"({Assistências_per_ranking_value}/{rows_count})"
                        full_title_Assistências_per_ranking_value = f"Assistências /90 {output_str} {highlight_último_passe_1_value}"

                        # Building the Extended Title"
                        xA_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'xA /90_Ranking'].values
                        xA_per_ranking_value = xA_per_ranking_value[0].astype(int)
                        output_str = f"({xA_per_ranking_value}/{rows_count})"
                        full_title_xA_per_ranking_value = f"xA /90 {output_str} {highlight_último_passe_2_value}"

                        # Building the Extended Title"
                        Deep_completions_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Deep completions /90_Ranking'].values
                        Deep_completions_per_ranking_value = Deep_completions_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completions_per_ranking_value}/{rows_count})"
                        full_title_Deep_completions_per_ranking_value = f"Deep completions /90 {output_str} {highlight_último_passe_3_value}"

                        # Building the Extended Title"
                        Passes_chave_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Passes chave /90_Ranking'].values
                        Passes_chave_per_ranking_value = Passes_chave_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_chave_per_ranking_value}/{rows_count})"
                        full_title_Passes_chave_per_ranking_value = f"Passes chave /90 {output_str} {highlight_último_passe_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_último_passe_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_último_passe_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Assistências_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_último_passe_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_último_passe_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_xA_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_último_passe_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_último_passe_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Deep_completions_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_último_passe_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_último_passe_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_chave_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.7), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)


    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Ameaça ofensiva"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Ameaça_ofensiva_Meio_campo_Charts = pd.read_csv('ameaça_ofensiva.csv')
                        Ameaça_ofensiva_Meio_campo_Charts_1 = Ameaça_ofensiva_Meio_campo_Charts[(Ameaça_ofensiva_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Ameaça_ofensiva_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Ameaça_ofensiva_Meio_campo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Ameaça_ofensiva_Meio_campo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Ameaça_ofensiva_Meio_campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Ameaça_ofensiva_Meio_campo_Charts_1.iloc[:, np.r_[7:10]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Ameaça_ofensiva_Meio_campo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Ameaça_ofensiva_Meio_campo_Charts_2 = Ameaça_ofensiva_Meio_campo_Charts[(Ameaça_ofensiva_Meio_campo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Ameaça_ofensiva_Meio_campo_Charts_2 = Ameaça_ofensiva_Meio_campo_Charts[(Ameaça_ofensiva_Meio_campo_Charts['Liga']==liga)&(Ameaça_ofensiva_Meio_campo_Charts['Posição']==posição)]
                        metrics = Ameaça_ofensiva_Meio_campo_Charts_2.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        metrics_ameaça_ofensiva1 = metrics.iloc[:, 0].tolist()
                        metrics_ameaça_ofensiva2 = metrics.iloc[:, 1].tolist()
                        metrics_ameaça_ofensiva3 = metrics.iloc[:, 2].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Ameaça_ofensiva_Meio_campo_Charts_2[(Ameaça_ofensiva_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_ameaça_ofensiva1 = highlight.iloc[:, 0].tolist()
                        highlight_ameaça_ofensiva2 = highlight.iloc[:, 1].tolist()
                        highlight_ameaça_ofensiva3 = highlight.iloc[:, 2].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_ameaça_ofensiva1_value = pd.DataFrame(highlight_ameaça_ofensiva1).reset_index(drop=True)
                        highlight_ameaça_ofensiva2_value = pd.DataFrame(highlight_ameaça_ofensiva2).reset_index(drop=True)
                        highlight_ameaça_ofensiva3_value = pd.DataFrame(highlight_ameaça_ofensiva3).reset_index(drop=True)

                        highlight_ameaça_ofensiva1_value = highlight_ameaça_ofensiva1_value.iat[0,0]
                        highlight_ameaça_ofensiva2_value = highlight_ameaça_ofensiva2_value.iat[0,0]
                        highlight_ameaça_ofensiva3_value = highlight_ameaça_ofensiva3_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_ameaça_ofensiva1, metrics_ameaça_ofensiva2, 
                                                            metrics_ameaça_ofensiva3])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_ameaça_ofensiva1, metrics_ameaça_ofensiva2, 
                                                            metrics_ameaça_ofensiva3])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 3.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        ameaça_ofensiva_ranking_df = pd.read_csv("Ameaça_ofensiva_ranking.csv")

                        # Building the Extended Title"
                        rows_count = ameaça_ofensiva_ranking_df[(ameaça_ofensiva_ranking_df['Liga'] == liga)  & 
                                                                            (ameaça_ofensiva_ranking_df['Posição'] == posição)].shape[0]
                        Pisadas_na_área_per_ranking_value = ameaça_ofensiva_ranking_df.loc[(ameaça_ofensiva_ranking_df['Atleta'] == jogadores) & 
                                                                            (ameaça_ofensiva_ranking_df['Liga'] == liga) & 
                                                                            (ameaça_ofensiva_ranking_df['Posição'] == posição), 'Pisadas na área /90_Ranking'].values
                        Pisadas_na_área_per_ranking_value = Pisadas_na_área_per_ranking_value[0].astype(int)
                        output_str = f"({Pisadas_na_área_per_ranking_value}/{rows_count})"
                        full_title_Pisadas_na_área_per_ranking_value = f"Pisadas na área certos /90 {output_str} {highlight_ameaça_ofensiva1_value}"

                        # Building the Extended Title"
                        Gols_per_ranking_value = ameaça_ofensiva_ranking_df.loc[(ameaça_ofensiva_ranking_df['Atleta'] == jogadores) & 
                                                                            (ameaça_ofensiva_ranking_df['Liga'] == liga) & 
                                                                            (ameaça_ofensiva_ranking_df['Posição'] == posição), 'Gols /90_Ranking'].values
                        Gols_per_ranking_value = Gols_per_ranking_value[0].astype(int)
                        output_str = f"({Gols_per_ranking_value}/{rows_count})"
                        full_title_Gols_per_ranking_value = f"Gols /90 {output_str} {highlight_ameaça_ofensiva2_value}"

                        # Building the Extended Title"
                        xG_per_ranking_value = ameaça_ofensiva_ranking_df.loc[(ameaça_ofensiva_ranking_df['Atleta'] == jogadores) & 
                                                                            (ameaça_ofensiva_ranking_df['Liga'] == liga) & 
                                                                            (ameaça_ofensiva_ranking_df['Posição'] == posição), 'xG /90_Ranking'].values
                        xG_per_ranking_value = xG_per_ranking_value[0].astype(int)
                        output_str = f"({xG_per_ranking_value}/{rows_count})"
                        full_title_xG_per_ranking_value = f"xG /90 {output_str} {highlight_ameaça_ofensiva3_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_ameaça_ofensiva1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_ameaça_ofensiva1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Pisadas_na_área_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_ameaça_ofensiva2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_ameaça_ofensiva2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Gols_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_ameaça_ofensiva3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax3.scatter(highlight_ameaça_ofensiva3, highlight_y, color='blue', s=60, label=jogadores)
                        ax3.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_xG_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax3.legend(loc='right', bbox_to_anchor=(0.2, -1.75), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Drible"):
                
                        Drible_Meio_campo_Charts = pd.read_csv('drible.csv')
                        Drible_Meio_campo_Charts_1 = Drible_Meio_campo_Charts[(Drible_Meio_campo_Charts['Atleta']==jogadores)&
                                                                                    (Drible_Meio_campo_Charts['Liga']==liga)&
                                                                                    (Drible_Meio_campo_Charts['Posição']==posição)]

    ##########################################################################################################################
    ##########################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Drible_Meio_campo_Charts_2 = Drible_Meio_campo_Charts[(Drible_Meio_campo_Charts['Liga']==liga)&(Drible_Meio_campo_Charts['Posição']==posição)]
                        metrics = Drible_Meio_campo_Charts_2.iloc[:, np.r_[-2]].reset_index(drop=True)
                        metrics_drible_1 = metrics.iloc[:, 0].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Drible_Meio_campo_Charts_2[(Drible_Meio_campo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[-2]].reset_index(drop=True)
                        highlight_drible_1 = highlight.iloc[:, 0].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = pd.DataFrame(highlight_drible_1).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = highlight_drible_1_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_drible_1])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_drible_1])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1) = plt.subplots(figsize=(7, 1.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        drible_ranking_df = pd.read_csv("Drible_ranking.csv")
                        # Building the Extended Title"
                        rows_count = drible_ranking_df[(drible_ranking_df['Liga'] == liga)  & 
                                                                            (drible_ranking_df['Posição'] == posição)].shape[0]
                        Dribles_bem_sucedidos_per_ranking_value = drible_ranking_df.loc[(drible_ranking_df['Atleta'] == jogadores) & 
                                                                            (drible_ranking_df['Liga'] == liga) & 
                                                                            (drible_ranking_df['Posição'] == posição), 'Dribles bem sucedidos /90_Ranking'].values
                        Dribles_bem_sucedidos_per_ranking_value = Dribles_bem_sucedidos_per_ranking_value[0].astype(int)
                        output_str = f"({Dribles_bem_sucedidos_per_ranking_value}/{rows_count})"
                        full_title_Dribles_bem_sucedidos_per_ranking_value = f"Dribles bem sucedidos /90 {output_str} {highlight_drible_1_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_drible_1, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax1.scatter(highlight_drible_1, highlight_y, color='blue', s=60, label=jogadores)
                        ax1.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Dribles_bem_sucedidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax1.legend(loc='right', bbox_to_anchor=(0.2, -1.3), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

            elif posição == ("EXTREMO"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                Extremo_Charts = pd.read_csv('Extremo.csv')
                Extremo_Charts_1 = Extremo_Charts[(Extremo_Charts['Atleta']==jogadores)&(Extremo_Charts['Liga']==liga)]
                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Extremo_Charts_1.iloc[:, np.r_[11:18]].reset_index(drop=True)
                metrics_list = metrics.iloc[0].tolist()
                
                #Collecting clube
                clube = Extremo_Charts_1.iat[0, 1]

                ## parameter names
                params = metrics.columns.tolist()

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                ## parameter value
                values = metrics_list

                ## title values
                title = dict(
                    title_name=jogadores,
                    title_color = 'blue',
                    subtitle_name=posição,
                    subtitle_color='#344D94',
                    title_name_2=clube,
                    title_color_2 = 'blue',
                    subtitle_name_2='2023',
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                ## instantiate object
                radar = Radar()

                ## instantiate object -- changing fontsize
                radar=Radar(fontfamily='Cursive', range_fontsize=13)
                radar=Radar(fontfamily='Cursive', label_fontsize=15)

                ## plot radar -- filename and dpi
                fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                        title=title, endnote=endnote, dpi=600)
                st.pyplot(fig)

                ############################################################################################################################
                ############################################################################################################################
                ############################################################################################################################

                #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição dos Atributos de todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                # Dynamically create the HTML string with the 'jogadores' variable
                title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                # Use the dynamically created HTML string in st.markdownRetenção_Possefinalização
                st.markdown(title_html, unsafe_allow_html=True)

                #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                # Collecting data
                Extremo_Charts_2 = Extremo_Charts[(Extremo_Charts['Liga']==liga)]

                #Collecting data to plot
                metrics = Extremo_Charts_2.iloc[:, np.r_[4:11]].reset_index(drop=True)
                metrics_participação = metrics.iloc[:, 0].tolist()
                metrics_recomposição = metrics.iloc[:, 1].tolist()
                metrics_Retenção_Posse = metrics.iloc[:, 2].tolist()
                metrics_ataque = metrics.iloc[:, 3].tolist()
                metrics_último_passe = metrics.iloc[:, 4].tolist()
                metrics_finalização = metrics.iloc[:, 5].tolist()
                metrics_drible = metrics.iloc[:, 6].tolist()
                metrics_y = [0] * len(metrics_participação)

                # The specific data point you want to highlight
                highlight = Extremo_Charts_2[(Extremo_Charts_2['Atleta']==jogadores)]
                highlight = highlight.iloc[:, np.r_[4:11]].reset_index(drop=True)
                highlight_participação = highlight.iloc[:, 0].tolist()
                highlight_recomposição = highlight.iloc[:, 1].tolist()
                highlight_Retenção_Posse = highlight.iloc[:, 2].tolist()
                highlight_ataque = highlight.iloc[:, 3].tolist()
                highlight_último_passe = highlight.iloc[:, 4].tolist()
                highlight_finalização = highlight.iloc[:, 5].tolist()
                highlight_drible = highlight.iloc[:, 6].tolist()
                highlight_y = 0

                # Computing the selected player specific values
                highlight_participação_value = pd.DataFrame(highlight_participação).reset_index(drop=True)
                highlight_recomposição_value = pd.DataFrame(highlight_recomposição).reset_index(drop=True)
                highlight_Retenção_Posse_value = pd.DataFrame(highlight_Retenção_Posse).reset_index(drop=True)
                highlight_ataque_value = pd.DataFrame(highlight_ataque).reset_index(drop=True)
                highlight_último_passe_value = pd.DataFrame(highlight_último_passe).reset_index(drop=True)
                highlight_finalização_value = pd.DataFrame(highlight_finalização).reset_index(drop=True)
                highlight_drible_value = pd.DataFrame(highlight_drible).reset_index(drop=True)

                highlight_participação_value = highlight_participação_value.iat[0,0]
                highlight_recomposição_value = highlight_recomposição_value.iat[0,0]
                highlight_Retenção_Posse_value = highlight_Retenção_Posse_value.iat[0,0]
                highlight_ataque_value = highlight_ataque_value.iat[0,0]
                highlight_último_passe_value = highlight_último_passe_value.iat[0,0]
                highlight_finalização_value = highlight_finalização_value.iat[0,0]
                highlight_drible_value = highlight_drible_value.iat[0,0]

                # Computing the min and max value across all lists using a generator expression
                min_value = min(min(lst) for lst in [metrics_participação, metrics_recomposição, metrics_arranque, 
                                                    metrics_ataque, metrics_último_passe, metrics_finalização, 
                                                    metrics_drible])
                min_value = min_value - 0.1
                max_value = max(max(lst) for lst in [metrics_participação, metrics_recomposição, metrics_arranque, 
                                                    metrics_ataque, metrics_último_passe, metrics_finalização, 
                                                    metrics_drible])
                max_value = max_value + 0.1

                # Create two subplots vertically aligned with separate x-axes
                fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(7.0, 6.5))
                ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                #Collecting Additional Information
                # Load the saved DataFrame from "Zagueiro_ranking.csv"apoio
                extremo_ranking_df = pd.read_csv("Extremo_ranking.csv")
                # Building the Extended Title"
                rows_count = extremo_ranking_df[extremo_ranking_df['Liga'] == liga].shape[0]
                participacao_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Participação_Ranking'].values
                participacao_ranking_value = participacao_ranking_value[0].astype(int)
                output_str = f"({participacao_ranking_value}/{rows_count})"
                full_title_participação = f"Participação {output_str} {highlight_participação_value}"

                # Building the Extended Title"
                recomposição_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Recomposição_Ranking'].values
                recomposição_ranking_value = recomposição_ranking_value[0].astype(int)
                output_str = f"({recomposição_ranking_value}/{rows_count})"
                full_title_recomposição = f"Recomposição {output_str} {highlight_recomposição_value}"

                # Building the Extended Title"
                arranque_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Arranque_Ranking'].values
                arranque_ranking_value = arranque_ranking_value[0].astype(int)
                output_str = f"({arranque_ranking_value}/{rows_count})"
                full_title_arranque = f"Arranque {output_str} {highlight_arranque_value}"

                # Building the Extended Title"
                ataque_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Ataque_Ranking'].values
                ataque_ranking_value = ataque_ranking_value[0].astype(int)
                output_str = f"({ataque_ranking_value}/{rows_count})"
                full_title_ataque = f"Ataque {output_str} {highlight_ataque_value}"
                
                # Building the Extended Title"
                último_passe_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Último passe_Ranking'].values
                último_passe_ranking_value = último_passe_ranking_value[0].astype(int)
                output_str = f"({último_passe_ranking_value}/{rows_count})"
                full_title_último_passe = f"Último passe {output_str} {highlight_último_passe_value}"

                # Building the Extended Title"
                finalização_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Finalização_Ranking'].values
                finalização_ranking_value = finalização_ranking_value[0].astype(int)
                output_str = f"({finalização_ranking_value}/{rows_count})"
                full_title_finalização = f"Finalização {output_str} {highlight_finalização_value}"

                # Building the Extended Title"
                drible_ranking_value = extremo_ranking_df.loc[(extremo_ranking_df['Atleta'] == jogadores) & 
                                                                    (extremo_ranking_df['Liga'] == liga), 'Drible_Ranking'].values
                drible_ranking_value = drible_ranking_value[0].astype(int)
                output_str = f"({drible_ranking_value}/{rows_count})"
                full_title_drible = f"Drible {output_str} {highlight_drible_value}"

                # Plot the first scatter plot in the first subplot
                ax1.scatter(metrics_participação, metrics_y, color='deepskyblue')
                ax1.scatter(highlight_participação, highlight_y, color='blue', s=60)
                ax1.get_yaxis().set_visible(False)
                ax1.set_title(full_title_participação, fontsize=12, fontweight='bold')
                ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax2.scatter(metrics_recomposição, metrics_y, color='deepskyblue')
                ax2.scatter(highlight_recomposição, highlight_y, color='blue', s=60)
                ax2.get_yaxis().set_visible(False)
                ax2.set_title(full_title_recomposição, fontsize=12, fontweight='bold')
                ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax3.scatter(metrics_arranque, metrics_y, color='deepskyblue')
                ax3.scatter(highlight_arranque, highlight_y, color='blue', s=60)
                ax3.get_yaxis().set_visible(False)
                ax3.set_title(full_title_arranque, fontsize=12, fontweight='bold')
                ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax4.scatter(metrics_ataque, metrics_y, color='deepskyblue')
                ax4.scatter(highlight_ataque, highlight_y, color='blue', s=60)            
                ax4.get_yaxis().set_visible(False)
                ax4.set_title(full_title_ataque, fontsize=12, fontweight='bold')
                ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax4.spines['top'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['left'].set_visible(False)
                ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax5.scatter(metrics_último_passe, metrics_y, color='deepskyblue')
                ax5.scatter(highlight_último_passe, highlight_y, color='blue', s=60)            
                ax5.get_yaxis().set_visible(False)
                ax5.set_title(full_title_último_passe, fontsize=12, fontweight='bold')
                ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax5.spines['top'].set_visible(False)
                ax5.spines['right'].set_visible(False)
                ax5.spines['bottom'].set_visible(False)
                ax5.spines['left'].set_visible(False)
                ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax6.scatter(metrics_finalização, metrics_y, color='deepskyblue')
                ax6.scatter(highlight_finalização, highlight_y, color='blue', s=60)            
                ax6.get_yaxis().set_visible(False)
                ax6.set_title(full_title_finalização, fontsize=12, fontweight='bold')
                ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax6.spines['top'].set_visible(False)
                ax6.spines['right'].set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.spines['left'].set_visible(False)
                ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax7.scatter(metrics_drible, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                ax7.scatter(highlight_drible, highlight_y, color='blue', s=60, label=jogadores)            
                ax7.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                ax7.get_yaxis().set_visible(False)
                ax7.set_title(full_title_drible, fontsize=12, fontweight='bold')
                ax7.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax7.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax7.spines['top'].set_visible(False)
                ax7.spines['right'].set_visible(False)
                ax7.spines['bottom'].set_visible(False)
                ax7.spines['left'].set_visible(False)
                ax7.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                plt.tight_layout()  # Adjust the layout to prevent overlap
                plt.show()

                ax7.legend(loc='right', bbox_to_anchor=(0.2, -3.5), fontsize="6", frameon=False)
                plt.show()

                st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                if posição:
                    atributos = atributos_extremo['EXTREMO']
                    atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
                    if atributo == ("Participação"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Participação_Extremo_Charts = pd.read_csv('participação.csv')
                        Participação_Extremo_Charts_1 = Participação_Extremo_Charts[(Participação_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Participação_Extremo_Charts['Liga']==liga)&
                                                                                    (Participação_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Participação_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Participação_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Participação_Extremo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Participação_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Participação_Extremo_Charts_2 = Participação_Extremo_Charts[(Participação_Extremo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Participação_Extremo_Charts_2 = Participação_Extremo_Charts[(Participação_Extremo_Charts['Liga']==liga)&(Participação_Extremo_Charts['Posição']==posição)]
                        metrics = Participação_Extremo_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_participação_1 = metrics.iloc[:, 0].tolist()
                        metrics_participação_2 = metrics.iloc[:, 1].tolist()
                        metrics_participação_3 = metrics.iloc[:, 2].tolist()
                        metrics_participação_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Participação_Extremo_Charts_2[(Participação_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_participação_1 = highlight.iloc[:, 0].tolist()
                        highlight_participação_2 = highlight.iloc[:, 1].tolist()
                        highlight_participação_3 = highlight.iloc[:, 2].tolist()
                        highlight_participação_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
                        highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
                        highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
                        highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

                        highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
                        highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
                        highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
                        highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        participação_ranking_df = pd.read_csv("Participação_ranking.csv")
                        # Building the Extended Title
                        rows_count = participação_ranking_df[(participação_ranking_df['Liga'] == liga)  & 
                                                                            (participação_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_participação_1_value}"
                        
                        # Building the Extended Title"
                        Passes_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes /90_Ranking'].values
                        Passes_per_ranking_value = Passes_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_per_ranking_value}/{rows_count})"
                        full_title_Passes_per_ranking_value = f"Passes /90 {output_str} {highlight_participação_2_value}"
                        
                        # Building the Extended Title"
                        Passes_recebidos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_participação_3_value}"
                        
                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_participação_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_participação_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_participação_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_participação_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_participação_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_participação_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_participação_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_participação_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_participação_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -2.0), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    elif atributo == ("Recomposição"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Recomposição_Extremo_Charts = pd.read_csv('recomposição.csv')
                        Recomposição_Extremo_Charts_1 = Recomposição_Extremo_Charts[(Recomposição_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Recomposição_Extremo_Charts['Liga']==liga)&
                                                                                    (Recomposição_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Recomposição_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Recomposição_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Recomposição_Extremo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Recomposição_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Recomposição_Extremo_Charts_2 = Recomposição_Extremo_Charts[(Recomposição_Extremo_Charts['Liga']==liga)]

                        #Collecting data to plot
                        Recomposição_Extremo_Charts_2 = Recomposição_Extremo_Charts[(Recomposição_Extremo_Charts['Liga']==liga)&(Recomposição_Extremo_Charts['Posição']==posição)]
                        metrics = Recomposição_Extremo_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_recomposição_1 = metrics.iloc[:, 0].tolist()
                        metrics_recomposição_2 = metrics.iloc[:, 1].tolist()
                        metrics_recomposição_3 = metrics.iloc[:, 2].tolist()
                        metrics_recomposição_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Recomposição_Extremo_Charts_2[(Recomposição_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_recomposição_1 = highlight.iloc[:, 0].tolist()
                        highlight_recomposição_2 = highlight.iloc[:, 1].tolist()
                        highlight_recomposição_3 = highlight.iloc[:, 2].tolist()
                        highlight_recomposição_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_recomposição_1_value = pd.DataFrame(highlight_recomposição_1).reset_index(drop=True)
                        highlight_recomposição_2_value = pd.DataFrame(highlight_recomposição_2).reset_index(drop=True)
                        highlight_recomposição_3_value = pd.DataFrame(highlight_recomposição_3).reset_index(drop=True)
                        highlight_recomposição_4_value = pd.DataFrame(highlight_recomposição_4).reset_index(drop=True)

                        highlight_recomposição_1_value = highlight_recomposição_1_value.iat[0,0]
                        highlight_recomposição_2_value = highlight_recomposição_2_value.iat[0,0]
                        highlight_recomposição_3_value = highlight_recomposição_3_value.iat[0,0]
                        highlight_recomposição_4_value = highlight_recomposição_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_recomposição_1, metrics_recomposição_2, 
                                                            metrics_recomposição_3, metrics_recomposição_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_recomposição_1, metrics_recomposição_2, 
                                                            metrics_recomposição_3, metrics_recomposição_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        recomposição_ranking_df = pd.read_csv("Recomposição_ranking.csv")

                        # Building the Extended Title"
                        rows_count = recomposição_ranking_df[(recomposição_ranking_df['Liga'] == liga)  & 
                                                                            (recomposição_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_recomposição_1_value}"

                        # Building the Extended Title"
                        Interceptações_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Interceptações /90_Ranking'].values
                        Interceptações_per_ranking_value = Interceptações_per_ranking_value[0].astype(int)
                        output_str = f"({Interceptações_per_ranking_value}/{rows_count})"
                        full_title_Interceptações_per_ranking_value = f"Interceptações /90 {output_str} {highlight_recomposição_2_value}"

                        # Building the Extended Title"
                        Ações_defensivas_bem_sucedidas_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Ações defensivas bem sucedidas /90_Ranking'].values
                        Ações_defensivas_bem_sucedidas_per_ranking_value = Ações_defensivas_bem_sucedidas_per_ranking_value[0].astype(int)
                        output_str = f"({Ações_defensivas_bem_sucedidas_per_ranking_value}/{rows_count})"
                        full_title_Ações_defensivas_bem_sucedidas_per_ranking_value = f"Ações defensivas bem sucedidas /90 {output_str} {highlight_recomposição_3_value}"

                        # Building the Extended Title"
                        Duelos_defensivos_ganhos_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Duelos defensivos ganhos /90_Ranking'].values
                        Duelos_defensivos_ganhos_per_ranking_value = Duelos_defensivos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_ganhos_per_ranking_value = f"Duelos defensivos ganhos /90 {output_str} {highlight_recomposição_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_recomposição_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_recomposição_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_recomposição_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_recomposição_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Interceptações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_recomposição_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_recomposição_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Ações_defensivas_bem_sucedidas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_recomposição_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_recomposição_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_defensivos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    elif atributo == ("Arranque"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Arranque_Extremo_Charts = pd.read_csv('arranque.csv')
                        Arranque_Extremo_Charts_1 = Arranque_Extremo_Charts[(Arranque_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Arranque_Extremo_Charts['Liga']==liga)&
                                                                                    (Arranque_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Arranque_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Arranque_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Arranque_Extremo_Charts_1.iloc[:, np.r_[7:10]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Arranque_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #Collecting data to plot
                        Arranque_Extremo_Charts_2 = Arranque_Extremo_Charts[(Arranque_Extremo_Charts['Liga']==liga)&(Arranque_Extremo_Charts['Posição']==posição)]
                        metrics = Arranque_Extremo_Charts_2.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        metrics_arranque_1 = metrics.iloc[:, 0].tolist()
                        metrics_arranque_2 = metrics.iloc[:, 1].tolist()
                        metrics_arranque_3 = metrics.iloc[:, 2].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Arranque_Extremo_Charts_2[(Arranque_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        highlight_arranque_1 = highlight.iloc[:, 0].tolist()
                        highlight_arranque_2 = highlight.iloc[:, 1].tolist()
                        highlight_arranque_3 = highlight.iloc[:, 2].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_arranque_1_value = pd.DataFrame(highlight_arranque_1).reset_index(drop=True)
                        highlight_arranque_2_value = pd.DataFrame(highlight_arranque_2).reset_index(drop=True)
                        highlight_arranque_3_value = pd.DataFrame(highlight_arranque_3).reset_index(drop=True)

                        highlight_arranque_1_value = highlight_arranque_1_value.iat[0,0]
                        highlight_arranque_2_value = highlight_arranque_2_value.iat[0,0]
                        highlight_arranque_3_value = highlight_arranque_3_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_arranque_1, metrics_arranque_2, 
                                                            metrics_arranque_3])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_arranque_1, metrics_arranque_2, 
                                                            metrics_arranque_3])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 4.0))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        arranque_ranking_df = pd.read_csv("Arranque_ranking.csv")

                        # Building the Extended Title"
                        rows_count = arranque_ranking_df[(arranque_ranking_df['Liga'] == liga)  & 
                                                                            (arranque_ranking_df['Posição'] == posição)].shape[0]
                        Passes_longos_recebidos_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Passes longos recebidos /90_Ranking'].values
                        Passes_longos_recebidos_per_ranking_value = Passes_longos_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_longos_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_longos_recebidos_per_ranking_value = f"Passes longos recebidos /90 {output_str} {highlight_arranque_1_value}"

                        # Building the Extended Title"
                        Acelerações_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Acelerações /90_Ranking'].values
                        Acelerações_per_ranking_value = Acelerações_per_ranking_value[0].astype(int)
                        output_str = f"({Acelerações_per_ranking_value}/{rows_count})"
                        full_title_Acelerações_per_ranking_value = f"Acelerações /90 {output_str} {highlight_arranque_2_value}"

                        # Building the Extended Title"
                        Corridas_progressivas_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Corridas progressivas /90_Ranking'].values
                        Corridas_progressivas_per_ranking_value = Corridas_progressivas_per_ranking_value[0].astype(int)
                        output_str = f"({Corridas_progressivas_per_ranking_value}/{rows_count})"
                        full_title_Corridas_progressivas_per_ranking_value = f"Corridas progressivas /90 {output_str} {highlight_arranque_3_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_arranque_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_arranque_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_longos_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_arranque_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_arranque_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Acelerações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_arranque_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax3.scatter(highlight_arranque_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax3.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Corridas_progressivas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax3.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Ataque"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Ataque_Extremo_Charts = pd.read_csv('ataque.csv')
                        Ataque_Extremo_Charts_1 = Ataque_Extremo_Charts[(Ataque_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Ataque_Extremo_Charts['Liga']==liga)&
                                                                                    (Ataque_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Ataque_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Ataque_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Ataque_Extremo_Charts_1.iloc[:, np.r_[9:14]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Ataque_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Ataque_Extremo_Charts_2 = Ataque_Extremo_Charts[(Ataque_Extremo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Ataque_Extremo_Charts_2 = Ataque_Extremo_Charts[(Ataque_Extremo_Charts['Liga']==liga)&(Ataque_Extremo_Charts['Posição']==posição)]
                        metrics = Ataque_Extremo_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_ataque_1 = metrics.iloc[:, 0].tolist()
                        metrics_ataque_2 = metrics.iloc[:, 1].tolist()
                        metrics_ataque_3 = metrics.iloc[:, 2].tolist()
                        metrics_ataque_4 = metrics.iloc[:, 3].tolist()
                        metrics_ataque_5 = metrics.iloc[:, 4].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Ataque_Extremo_Charts_2[(Ataque_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_ataque_1 = highlight.iloc[:, 0].tolist()
                        highlight_ataque_2 = highlight.iloc[:, 1].tolist()
                        highlight_ataque_3 = highlight.iloc[:, 2].tolist()
                        highlight_ataque_4 = highlight.iloc[:, 3].tolist()
                        highlight_ataque_5 = highlight.iloc[:, 4].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = pd.DataFrame(highlight_ataque_1).reset_index(drop=True)
                        highlight_ataque_2_value = pd.DataFrame(highlight_ataque_2).reset_index(drop=True)
                        highlight_ataque_3_value = pd.DataFrame(highlight_ataque_3).reset_index(drop=True)
                        highlight_ataque_4_value = pd.DataFrame(highlight_ataque_4).reset_index(drop=True)
                        highlight_ataque_5_value = pd.DataFrame(highlight_ataque_5).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_ataque_1_value = highlight_ataque_1_value.iat[0,0]
                        highlight_ataque_2_value = highlight_ataque_2_value.iat[0,0]
                        highlight_ataque_3_value = highlight_ataque_3_value.iat[0,0]
                        highlight_ataque_4_value = highlight_ataque_4_value.iat[0,0]
                        highlight_ataque_5_value = highlight_ataque_5_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_ataque_1, metrics_ataque_2, 
                                                            metrics_ataque_3, metrics_ataque_4,
                                                            metrics_ataque_5])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"ataque
                        ataque_ranking_df = pd.read_csv("Ataque_ranking.csv")
                        # Building the Extended Title"
                        rows_count = ataque_ranking_df[(ataque_ranking_df['Liga'] == liga)  & 
                                                                            (ataque_ranking_df['Posição'] == posição)].shape[0]
                        Passes_terço_final_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes terço final certos /90_Ranking'].values
                        Passes_terço_final_certos_per_ranking_value = Passes_terço_final_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_terço_final_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_terço_final_certos_per_ranking_value = f"Passes terço final certos /90 {output_str} {highlight_ataque_1_value}"

                        # Building the Extended Title"
                        Cruzamentos_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Cruzamentos certos p/90_Ranking'].values
                        Cruzamentos_certos_per_ranking_value = Cruzamentos_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Cruzamentos_certos_per_ranking_value}/{rows_count})"
                        full_title_Cruzamentos_certos_per_ranking_value = f"Cruzamentos certos /90 {output_str} {highlight_ataque_2_value}"

                        # Building the Extended Title"
                        Passes_área_do_pênalti_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes área do pênalti certos /90_Ranking'].values
                        Passes_área_do_pênalti_certos_per_ranking_value = Passes_área_do_pênalti_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_área_do_pênalti_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_área_do_pênalti_certos_per_ranking_value = f"Passes área do pênalti certos /90 {output_str} {highlight_ataque_3_value}"

                        # Building the Extended Title"
                        Passes_inteligentes_certos_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Passes inteligentes certos /90_Ranking'].values
                        Passes_inteligentes_certos_per_ranking_value = Passes_inteligentes_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_inteligentes_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_inteligentes_certos_per_ranking_value = f"Passes inteligentes certos /90 {output_str} {highlight_ataque_4_value}"

                        # Building the Extended Title"
                        Deep_completed_crosses_per_ranking_value = ataque_ranking_df.loc[(ataque_ranking_df['Atleta'] == jogadores) & 
                                                                            (ataque_ranking_df['Liga'] == liga) & 
                                                                            (ataque_ranking_df['Posição'] == posição), 'Deep completed crosses /90_Ranking'].values
                        Deep_completed_crosses_per_ranking_value = Deep_completed_crosses_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completed_crosses_per_ranking_value}/{rows_count})"
                        full_title_Deep_completed_crosses_per_ranking_value = f"Deep completed crosses /90 {output_str} {highlight_ataque_5_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_ataque_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_ataque_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_terço_final_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_ataque_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_ataque_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Cruzamentos_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_ataque_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_ataque_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_área_do_pênalti_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_ataque_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_ataque_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_inteligentes_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax5.scatter(metrics_ataque_5, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax5.scatter(highlight_ataque_5, highlight_y, color='blue', s=60, label=jogadores)
                        ax5.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Deep_completed_crosses_per_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax5.legend(loc='right', bbox_to_anchor=(0.2, -2.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    if atributo == ("Último passe"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Último_passe_Extremo_Charts = pd.read_csv('último_passe.csv')
                        Último_passe_Extremo_Charts_1 = Último_passe_Extremo_Charts[(Último_passe_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Último_passe_Extremo_Charts['Liga']==liga)&
                                                                                    (Último_passe_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Último_passe_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Último_passe_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Último_passe_Extremo_Charts_1.iloc[:, np.r_[9:14]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Último_passe_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Último_passe_Extremo_Charts_2 = Último_passe_Extremo_Charts[(Último_passe_Extremo_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Último_passe_Extremo_Charts_2 = Último_passe_Extremo_Charts[(Último_passe_Extremo_Charts['Liga']==liga)&(Último_passe_Extremo_Charts['Posição']==posição)]
                        metrics = Último_passe_Extremo_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_último_passe_1 = metrics.iloc[:, 0].tolist()
                        metrics_último_passe_2 = metrics.iloc[:, 1].tolist()
                        metrics_último_passe_3 = metrics.iloc[:, 2].tolist()
                        metrics_último_passe_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Último_passe_Extremo_Charts_2[(Último_passe_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_último_passe_1 = highlight.iloc[:, 0].tolist()
                        highlight_último_passe_2 = highlight.iloc[:, 1].tolist()
                        highlight_último_passe_3 = highlight.iloc[:, 2].tolist()
                        highlight_último_passe_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = pd.DataFrame(highlight_último_passe_1).reset_index(drop=True)
                        highlight_último_passe_2_value = pd.DataFrame(highlight_último_passe_2).reset_index(drop=True)
                        highlight_último_passe_3_value = pd.DataFrame(highlight_último_passe_3).reset_index(drop=True)
                        highlight_último_passe_4_value = pd.DataFrame(highlight_último_passe_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = highlight_último_passe_1_value.iat[0,0]
                        highlight_último_passe_2_value = highlight_último_passe_2_value.iat[0,0]
                        highlight_último_passe_3_value = highlight_último_passe_3_value.iat[0,0]
                        highlight_último_passe_4_value = highlight_último_passe_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        último_passe_ranking_df = pd.read_csv("Último_passe_ranking.csv")
                        # Building the Extended Title"
                        rows_count = último_passe_ranking_df[(último_passe_ranking_df['Liga'] == liga)  & 
                                                                            (último_passe_ranking_df['Posição'] == posição)].shape[0]
                        Assistências_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Assistências /90_Ranking'].values
                        Assistências_per_ranking_value = Assistências_per_ranking_value[0].astype(int)
                        output_str = f"({Assistências_per_ranking_value}/{rows_count})"
                        full_title_Assistências_per_ranking_value = f"Assistências /90 {output_str} {highlight_último_passe_1_value}"

                        # Building the Extended Title"
                        xA_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'xA /90_Ranking'].values
                        xA_per_ranking_value = xA_per_ranking_value[0].astype(int)
                        output_str = f"({xA_per_ranking_value}/{rows_count})"
                        full_title_xA_per_ranking_value = f"xA /90 {output_str} {highlight_último_passe_2_value}"

                        # Building the Extended Title"
                        Deep_completions_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Deep completions /90_Ranking'].values
                        Deep_completions_per_ranking_value = Deep_completions_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completions_per_ranking_value}/{rows_count})"
                        full_title_Deep_completions_per_ranking_value = f"Deep completions /90 {output_str} {highlight_último_passe_3_value}"

                        # Building the Extended Title"
                        Passes_chave_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Passes chave /90_Ranking'].values
                        Passes_chave_per_ranking_value = Passes_chave_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_chave_per_ranking_value}/{rows_count})"
                        full_title_Passes_chave_per_ranking_value = f"Passes chave /90 {output_str} {highlight_último_passe_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_último_passe_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_último_passe_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Assistências_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_último_passe_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_último_passe_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_xA_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_último_passe_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_último_passe_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Deep_completions_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_último_passe_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_último_passe_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_chave_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.7), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)


    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Finalização"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Finalização_Extremo_Charts = pd.read_csv('finalização.csv')
                        Finalização_Extremo_Charts_1 = Finalização_Extremo_Charts[(Finalização_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Finalização_Extremo_Charts['Liga']==liga)&
                                                                                    (Finalização_Extremo_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Finalização_Extremo_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Finalização_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Finalização_Extremo_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Finalização_Extremo_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Finalização_Extremo_Charts_2 = Finalização_Extremo_Charts[(Finalização_Extremo_Charts['Liga']==liga)&(Finalização_Extremo_Charts['Posição']==posição)]
                        metrics = Finalização_Extremo_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_finalização_1 = metrics.iloc[:, 0].tolist()
                        metrics_finalização_2 = metrics.iloc[:, 1].tolist()
                        metrics_finalização_3 = metrics.iloc[:, 2].tolist()
                        metrics_finalização_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Finalização_Extremo_Charts_2[(Finalização_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_finalização_1 = highlight.iloc[:, 0].tolist()
                        highlight_finalização_2 = highlight.iloc[:, 1].tolist()
                        highlight_finalização_3 = highlight.iloc[:, 2].tolist()
                        highlight_finalização_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_finalização_1_value = pd.DataFrame(highlight_finalização_1).reset_index(drop=True)
                        highlight_finalização_2_value = pd.DataFrame(highlight_finalização_2).reset_index(drop=True)
                        highlight_finalização_3_value = pd.DataFrame(highlight_finalização_3).reset_index(drop=True)
                        highlight_finalização_4_value = pd.DataFrame(highlight_finalização_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_finalização_1_value = highlight_finalização_1_value.iat[0,0]
                        highlight_finalização_2_value = highlight_finalização_2_value.iat[0,0]
                        highlight_finalização_3_value = highlight_finalização_3_value.iat[0,0]
                        highlight_finalização_4_value = highlight_finalização_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                                            metrics_finalização_3, metrics_finalização_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                                            metrics_finalização_3, metrics_finalização_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        finalização_ranking_df = pd.read_csv("Finalização_ranking.csv")
                        # Building the Extended Title"
                        rows_count = finalização_ranking_df[(finalização_ranking_df['Liga'] == liga)  & 
                                                                            (finalização_ranking_df['Posição'] == posição)].shape[0]
                        Conversão_de_gols_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Conversão de gols_Ranking'].values
                        Conversão_de_gols_ranking_value = Conversão_de_gols_ranking_value[0].astype(int)
                        output_str = f"({Conversão_de_gols_ranking_value}/{rows_count})"
                        full_title_Conversão_de_gols_ranking_value = f"Conversão de gols {output_str} {highlight_finalização_1_value}"

                        # Building the Extended Title"
                        Conversão_de_xG_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Conversão de xG_Ranking'].values
                        Conversão_de_xG_ranking_value = Conversão_de_xG_ranking_value[0].astype(int)
                        output_str = f"({Conversão_de_xG_ranking_value}/{rows_count})"
                        full_title_Conversão_de_xG_ranking_value = f"Conversão de xG {output_str} {highlight_finalização_2_value}"

                        # Building the Extended Title"
                        Ameaça_ofensiva_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Ameaça_Ofensiva_Ranking'].values
                        Ameaça_ofensiva_ranking_value = Ameaça_ofensiva_ranking_value[0].astype(int)
                        output_str = f"({Ameaça_ofensiva_ranking_value}/{rows_count})"
                        full_title_Ameaça_ofensiva_ranking_value = f"Ameaça ofensiva {output_str} {highlight_finalização_3_value}"

                        # Building the Extended Title"
                        Finalizações_no_alvo_per_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Finalizações no alvo /90_Ranking'].values
                        Finalizações_no_alvo_per_ranking_value = Finalizações_no_alvo_per_ranking_value[0].astype(int)
                        output_str = f"({Finalizações_no_alvo_per_ranking_value}/{rows_count})"
                        full_title_Finalizações_no_alvo_per_ranking_value = f"Finalizaçõe no alvo /90 {output_str} {highlight_finalização_4_value}"


                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_finalização_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_finalização_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Conversão_de_gols_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_finalização_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_finalização_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Conversão_de_xG_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_finalização_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_finalização_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Ameaça_ofensiva_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_finalização_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_finalização_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Finalizações_no_alvo_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    elif atributo == ("Drible"):
                
                        Drible_Extremo_Charts = pd.read_csv('drible.csv')
                        Drible_Extremo_Charts_1 = Drible_Extremo_Charts[(Drible_Extremo_Charts['Atleta']==jogadores)&
                                                                                    (Drible_Extremo_Charts['Liga']==liga)&
                                                                                    (Drible_Extremo_Charts['Posição']==posição)]

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Drible_Extremo_Charts_2 = Drible_Extremo_Charts[(Drible_Extremo_Charts['Liga']==liga)&(Drible_Extremo_Charts['Posição']==posição)]
                        metrics = Drible_Extremo_Charts_2.iloc[:, np.r_[-2]].reset_index(drop=True)
                        metrics_drible_1 = metrics.iloc[:, 0].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Drible_Extremo_Charts_2[(Drible_Extremo_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[-2]].reset_index(drop=True)
                        highlight_drible_1 = highlight.iloc[:, 0].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = pd.DataFrame(highlight_drible_1).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = highlight_drible_1_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_drible_1])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_drible_1])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1) = plt.subplots(figsize=(7, 1.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        drible_ranking_df = pd.read_csv("Drible_ranking.csv")
                        # Building the Extended Title"
                        rows_count = drible_ranking_df[(drible_ranking_df['Liga'] == liga)  & 
                                                                            (drible_ranking_df['Posição'] == posição)].shape[0]
                        Dribles_bem_sucedidos_per_ranking_value = drible_ranking_df.loc[(drible_ranking_df['Atleta'] == jogadores) & 
                                                                            (drible_ranking_df['Liga'] == liga) & 
                                                                            (drible_ranking_df['Posição'] == posição), 'Dribles bem sucedidos /90_Ranking'].values
                        Dribles_bem_sucedidos_per_ranking_value = Dribles_bem_sucedidos_per_ranking_value[0].astype(int)
                        output_str = f"({Dribles_bem_sucedidos_per_ranking_value}/{rows_count})"
                        full_title_Dribles_bem_sucedidos_per_ranking_value = f"Dribles bem sucedidos /90 {output_str} {highlight_drible_1_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_drible_1, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax1.scatter(highlight_drible_1, highlight_y, color='blue', s=60, label=jogadores)
                        ax1.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Dribles_bem_sucedidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax1.legend(loc='right', bbox_to_anchor=(0.2, -1.3), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

            elif posição == ("ATACANTE"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                Atacante_Charts = pd.read_csv('Atacante.csv')
                Atacante_Charts_1 = Atacante_Charts[(Atacante_Charts['Atleta']==jogadores)&(Atacante_Charts['Liga']==liga)]
                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Atacante_Charts_1.iloc[:, np.r_[13:22]].reset_index(drop=True)
                metrics_list = metrics.iloc[0].tolist()

                #Collecting clube
                clube = Atacante_Charts_1.iat[0, 1]

                ## parameter names
                params = metrics.columns.tolist()

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                ## parameter value
                values = metrics_list

                ## title values
                title = dict(
                    title_name=jogadores,
                    title_color = 'blue',
                    subtitle_name=posição,
                    subtitle_color='#344D94',
                    title_name_2=clube,
                    title_color_2 = 'blue',
                    subtitle_name_2='2023',
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                ## instantiate object
                radar = Radar()

                ## instantiate object -- changing fontsize
                radar=Radar(fontfamily='Cursive', range_fontsize=13)
                radar=Radar(fontfamily='Cursive', label_fontsize=15)

                ## plot radar -- filename and dpi
                fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                        title=title, endnote=endnote, dpi=600)
                st.pyplot(fig)

                ############################################################################################################################
                ############################################################################################################################
                ############################################################################################################################

                #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição dos Atributos de todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                # Dynamically create the HTML string with the 'jogadores' variable
                title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                # Use the dynamically created HTML string in st.markdownarranquefinalização
                st.markdown(title_html, unsafe_allow_html=True)

                #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                # Collecting data
                Atacante_Charts_2 = Atacante_Charts[(Atacante_Charts['Liga']==liga)]

                #Collecting data to plot
                metrics = Atacante_Charts_2.iloc[:, np.r_[4:13]].reset_index(drop=True)
                metrics_participação = metrics.iloc[:, 0].tolist()
                metrics_recomposição = metrics.iloc[:, 1].tolist()
                metrics_retenção_posse = metrics.iloc[:, 2].tolist()
                metrics_arranque = metrics.iloc[:, 3].tolist()
                metrics_bola_aérea = metrics.iloc[:, 4].tolist()
                metrics_último_passe = metrics.iloc[:, 5].tolist()
                metrics_finalização = metrics.iloc[:, 6].tolist()
                metrics_drible = metrics.iloc[:, 7].tolist()
                metrics_oportunismo = metrics.iloc[:, 8].tolist()
                metrics_y = [0] * len(metrics_participação)

                # The specific data point you want to highlight
                highlight = Atacante_Charts_2[(Atacante_Charts_2['Atleta']==jogadores)]
                highlight = highlight.iloc[:, np.r_[4:13]].reset_index(drop=True)
                highlight_participação = highlight.iloc[:, 0].tolist()
                highlight_recomposição = highlight.iloc[:, 1].tolist()
                highlight_retenção_posse = highlight.iloc[:, 2].tolist()
                highlight_arranque = highlight.iloc[:, 3].tolist()
                highlight_bola_aérea = highlight.iloc[:, 4].tolist()
                highlight_último_passe = highlight.iloc[:, 5].tolist()
                highlight_finalização = highlight.iloc[:, 6].tolist()
                highlight_drible = highlight.iloc[:, 7].tolist()
                highlight_oportunismo = highlight.iloc[:, 8].tolist()
                highlight_y = 0

                # Computing the selected player specific values
                highlight_participação_value = pd.DataFrame(highlight_participação).reset_index(drop=True)
                highlight_recomposição_value = pd.DataFrame(highlight_recomposição).reset_index(drop=True)
                highlight_retenção_posse_value = pd.DataFrame(highlight_retenção_posse).reset_index(drop=True)
                highlight_arranque_value = pd.DataFrame(highlight_arranque).reset_index(drop=True)
                highlight_bola_aérea_value = pd.DataFrame(highlight_bola_aérea).reset_index(drop=True)
                highlight_último_passe_value = pd.DataFrame(highlight_último_passe).reset_index(drop=True)
                highlight_finalização_value = pd.DataFrame(highlight_finalização).reset_index(drop=True)
                highlight_drible_value = pd.DataFrame(highlight_drible).reset_index(drop=True)
                highlight_oportunismo_value = pd.DataFrame(highlight_oportunismo).reset_index(drop=True)

                highlight_participação_value = highlight_participação_value.iat[0,0]
                highlight_recomposição_value = highlight_recomposição_value.iat[0,0]
                highlight_retenção_posse_value = highlight_retenção_posse_value.iat[0,0]
                highlight_arranque_value = highlight_arranque_value.iat[0,0]
                highlight_bola_aérea_value = highlight_bola_aérea_value.iat[0,0]
                highlight_último_passe_value = highlight_último_passe_value.iat[0,0]
                highlight_finalização_value = highlight_finalização_value.iat[0,0]
                highlight_drible_value = highlight_drible_value.iat[0,0]
                highlight_oportunismo_value = highlight_oportunismo_value.iat[0,0]

                # Computing the min and max value across all lists using a generator expression
                min_value = min(min(lst) for lst in [metrics_participação, metrics_recomposição, metrics_retenção_posse, 
                                                    metrics_arranque, metrics_bola_aérea, metrics_último_passe, 
                                                    metrics_finalização, metrics_drible, metrics_oportunismo])
                min_value = min_value - 0.1
                max_value = max(max(lst) for lst in [metrics_participação, metrics_recomposição, metrics_retenção_posse, 
                                                    metrics_arranque, metrics_bola_aérea, metrics_último_passe, 
                                                    metrics_finalização, metrics_drible, metrics_oportunismo])
                max_value = max_value + 0.1

                # Create two subplots vertically aligned with separate x-axes
                fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = plt.subplots(9, 1, figsize=(7.0, 8.0))
                ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Create two subplots vertically aligned with separate x-axes
    #            fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(6.0, 7.0))
    #            ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                #Collecting Additional Information
                # Load the saved DataFrame from "Zagueiro_ranking.csv"apoio
                atacante_ranking_df = pd.read_csv("Atacante_ranking.csv")
                # Building the Extended Title"
                rows_count = atacante_ranking_df[atacante_ranking_df['Liga'] == liga].shape[0]
                participacao_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Participação_Ranking'].values
                participacao_ranking_value = participacao_ranking_value[0].astype(int)
                output_str = f"({participacao_ranking_value}/{rows_count})"
                full_title_participação = f"Participação {output_str} {highlight_participação_value}"

                # Building the Extended Title
                recomposição_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Recomposição_Ranking'].values
                recomposição_ranking_value = recomposição_ranking_value[0].astype(int)
                output_str = f"({recomposição_ranking_value}/{rows_count})"
                full_title_recomposição = f"Recomposição {output_str} {highlight_recomposição_value}"

                # Building the Extended Title"
                retenção_posse_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Retenção Posse_Ranking'].values
                retenção_posse_ranking_value = retenção_posse_ranking_value[0].astype(int)
                output_str = f"({retenção_posse_ranking_value}/{rows_count})"
                full_title_retenção_posse = f"Retenção Posse {output_str} {highlight_retenção_posse_value}"

                # Building the Extended Title"
                arranque_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Arranque_Ranking'].values
                arranque_ranking_value = arranque_ranking_value[0].astype(int)
                output_str = f"({arranque_ranking_value}/{rows_count})"
                full_title_arranque = f"Arranque {output_str} {highlight_arranque_value}"

                # Building the Extended Title"
                bola_aérea_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Bola aérea_Ranking'].values
                bola_aérea_ranking_value = bola_aérea_ranking_value[0].astype(int)
                output_str = f"({bola_aérea_ranking_value}/{rows_count})"
                full_title_bola_aérea = f"Bola Aérea {output_str} {highlight_bola_aérea_value}"

                # Building the Extended Title"
                último_passe_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Último passe_Ranking'].values
                último_passe_ranking_value = último_passe_ranking_value[0].astype(int)
                output_str = f"({último_passe_ranking_value}/{rows_count})"
                full_title_último_passe = f"Último passe {output_str} {highlight_último_passe_value}"

                # Building the Extended Title"
                finalização_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Finalização_Ranking'].values
                finalização_ranking_value = finalização_ranking_value[0].astype(int)
                output_str = f"({finalização_ranking_value}/{rows_count})"
                full_title_finalização = f"Finalização {output_str} {highlight_finalização_value}"

                # Building the Extended Title"
                drible_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Drible_Ranking'].values
                drible_ranking_value = drible_ranking_value[0].astype(int)
                output_str = f"({drible_ranking_value}/{rows_count})"
                full_title_drible = f"Drible {output_str} {highlight_drible_value}"

                # Building the Extended Title"
                oportunismo_ranking_value = atacante_ranking_df.loc[(atacante_ranking_df['Atleta'] == jogadores) & 
                                                                    (atacante_ranking_df['Liga'] == liga), 'Oportunismo_Ranking'].values
                oportunismo_ranking_value = oportunismo_ranking_value[0].astype(int)
                output_str = f"({oportunismo_ranking_value}/{rows_count})"
                full_title_oportunismo = f"Oportunismo {output_str} {highlight_oportunismo_value}"

                # Plot the first scatter plot in the first subplot
                ax1.scatter(metrics_participação, metrics_y, color='deepskyblue')
                ax1.scatter(highlight_participação, highlight_y, color='blue', s=60)
                ax1.get_yaxis().set_visible(False)
                ax1.set_title(full_title_participação, fontsize=12, fontweight='bold')
                ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['bottom'].set_visible(False)
                ax1.spines['left'].set_visible(False)
                ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax2.scatter(metrics_recomposição, metrics_y, color='deepskyblue')
                ax2.scatter(highlight_recomposição, highlight_y, color='blue', s=60)
                ax2.get_yaxis().set_visible(False)
                ax2.set_title(full_title_recomposição, fontsize=12, fontweight='bold')
                ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)
                ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax3.scatter(metrics_retenção_posse, metrics_y, color='deepskyblue')
                ax3.scatter(highlight_retenção_posse, highlight_y, color='blue', s=60)
                ax3.get_yaxis().set_visible(False)
                ax3.set_title(full_title_retenção_posse, fontsize=12, fontweight='bold')
                ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax3.spines['bottom'].set_visible(False)
                ax3.spines['left'].set_visible(False)
                ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax4.scatter(metrics_arranque, metrics_y, color='deepskyblue')
                ax4.scatter(highlight_arranque, highlight_y, color='blue', s=60)
                ax4.get_yaxis().set_visible(False)
                ax4.set_title(full_title_arranque, fontsize=12, fontweight='bold')
                ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax4.spines['top'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['left'].set_visible(False)
                ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax5.scatter(metrics_bola_aérea, metrics_y, color='deepskyblue')
                ax5.scatter(highlight_bola_aérea, highlight_y, color='blue', s=60)            
                ax5.get_yaxis().set_visible(False)
                ax5.set_title(full_title_bola_aérea, fontsize=12, fontweight='bold')
                ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax5.spines['top'].set_visible(False)
                ax5.spines['right'].set_visible(False)
                ax5.spines['bottom'].set_visible(False)
                ax5.spines['left'].set_visible(False)
                ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax6.scatter(metrics_último_passe, metrics_y, color='deepskyblue')
                ax6.scatter(highlight_último_passe, highlight_y, color='blue', s=60)            
                ax6.get_yaxis().set_visible(False)
                ax6.set_title(full_title_último_passe, fontsize=12, fontweight='bold')
                ax6.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax6.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax6.spines['top'].set_visible(False)
                ax6.spines['right'].set_visible(False)
                ax6.spines['bottom'].set_visible(False)
                ax6.spines['left'].set_visible(False)
                ax6.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax7.scatter(metrics_finalização, metrics_y, color='deepskyblue')
                ax7.scatter(highlight_finalização, highlight_y, color='blue', s=60)            
                ax7.get_yaxis().set_visible(False)
                ax7.set_title(full_title_finalização, fontsize=12, fontweight='bold')
                ax7.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax7.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax7.spines['top'].set_visible(False)
                ax7.spines['right'].set_visible(False)
                ax7.spines['bottom'].set_visible(False)
                ax7.spines['left'].set_visible(False)
                ax7.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax8.scatter(metrics_drible, metrics_y, color='deepskyblue')
                ax8.scatter(highlight_drible, highlight_y, color='blue', s=60)            
                ax8.get_yaxis().set_visible(False)
                ax8.set_title(full_title_drible, fontsize=12, fontweight='bold')
                ax8.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax8.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax8.spines['top'].set_visible(False)
                ax8.spines['right'].set_visible(False)
                ax8.spines['bottom'].set_visible(False)
                ax8.spines['left'].set_visible(False)
                ax8.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                # Plot the second scatter plot in the second subplot
                ax9.scatter(metrics_oportunismo, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                ax9.scatter(highlight_oportunismo, highlight_y, color='blue', s=60, label=jogadores)            
                ax9.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                ax9.get_yaxis().set_visible(False)
                ax9.set_title(full_title_oportunismo, fontsize=12, fontweight='bold')
                ax9.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                ax9.xaxis.set_major_locator(ticker.MultipleLocator(2))
                ax9.spines['top'].set_visible(False)
                ax9.spines['right'].set_visible(False)
                ax9.spines['bottom'].set_visible(False)
                ax9.spines['left'].set_visible(False)
                ax9.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                plt.tight_layout()  # Adjust the layout to prevent overlap
                plt.show()

                ax9.legend(loc='right', bbox_to_anchor=(0.2, -3.5), fontsize="6", frameon=False)
                plt.show()

                st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                if posição:
                    atributos = atributos_atacante['ATACANTE']
                    atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
                    if atributo == ("Participação"):
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Participação_Atacante_Charts = pd.read_csv('participação.csv')
                        Participação_Atacante_Charts_1 = Participação_Atacante_Charts[(Participação_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Participação_Atacante_Charts['Liga']==liga)&
                                                                                    (Participação_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Participação_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Participação_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Participação_Atacante_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Participação_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #Collecting data to plot
                        Participação_Atacante_Charts_2 = Participação_Atacante_Charts[(Participação_Atacante_Charts['Liga']==liga)&(Participação_Atacante_Charts['Posição']==posição)]
                        metrics = Participação_Atacante_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_participação_1 = metrics.iloc[:, 0].tolist()
                        metrics_participação_2 = metrics.iloc[:, 1].tolist()
                        metrics_participação_3 = metrics.iloc[:, 2].tolist()
                        metrics_participação_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Participação_Atacante_Charts_2[(Participação_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_participação_1 = highlight.iloc[:, 0].tolist()
                        highlight_participação_2 = highlight.iloc[:, 1].tolist()
                        highlight_participação_3 = highlight.iloc[:, 2].tolist()
                        highlight_participação_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_participação_1_value = pd.DataFrame(highlight_participação_1).reset_index(drop=True)
                        highlight_participação_2_value = pd.DataFrame(highlight_participação_2).reset_index(drop=True)
                        highlight_participação_3_value = pd.DataFrame(highlight_participação_3).reset_index(drop=True)
                        highlight_participação_4_value = pd.DataFrame(highlight_participação_4).reset_index(drop=True)

                        highlight_participação_1_value = highlight_participação_1_value.iat[0,0]
                        highlight_participação_2_value = highlight_participação_2_value.iat[0,0]
                        highlight_participação_3_value = highlight_participação_3_value.iat[0,0]
                        highlight_participação_4_value = highlight_participação_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_participação_1, metrics_participação_2, 
                                                            metrics_participação_3, metrics_participação_4])

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        participação_ranking_df = pd.read_csv("Participação_ranking.csv")
                        # Building the Extended Title
                        rows_count = participação_ranking_df[(participação_ranking_df['Liga'] == liga)  & 
                                                                            (participação_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_participação_1_value}"
                        
                        # Building the Extended Title"
                        Passes_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes /90_Ranking'].values
                        Passes_per_ranking_value = Passes_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_per_ranking_value}/{rows_count})"
                        full_title_Passes_per_ranking_value = f"Passes /90 {output_str} {highlight_participação_2_value}"
                        
                        # Building the Extended Title"
                        Passes_recebidos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_participação_3_value}"
                        
                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = participação_ranking_df.loc[(participação_ranking_df['Atleta'] == jogadores) & 
                                                                            (participação_ranking_df['Liga'] == liga) & 
                                                                            (participação_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_participação_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_participação_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_participação_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_participação_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_participação_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Passes_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_participação_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_participação_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_participação_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_participação_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -2.0), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    elif atributo == ("Recomposição"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Recomposição_Atacante_Charts = pd.read_csv('recomposição.csv')
                        Recomposição_Atacante_Charts_1 = Recomposição_Atacante_Charts[(Recomposição_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Recomposição_Atacante_Charts['Liga']==liga)&
                                                                                    (Recomposição_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Recomposição_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Recomposição_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Recomposição_Atacante_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Recomposição_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Recomposição_Atacante_Charts_2 = Recomposição_Atacante_Charts[(Recomposição_Atacante_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Recomposição_Atacante_Charts_2 = Recomposição_Atacante_Charts[(Recomposição_Atacante_Charts['Liga']==liga)&(Recomposição_Atacante_Charts['Posição']==posição)]
                        metrics = Recomposição_Atacante_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_recomposição_1 = metrics.iloc[:, 0].tolist()
                        metrics_recomposição_2 = metrics.iloc[:, 1].tolist()
                        metrics_recomposição_3 = metrics.iloc[:, 2].tolist()
                        metrics_recomposição_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Recomposição_Atacante_Charts_2[(Recomposição_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_recomposição_1 = highlight.iloc[:, 0].tolist()
                        highlight_recomposição_2 = highlight.iloc[:, 1].tolist()
                        highlight_recomposição_3 = highlight.iloc[:, 2].tolist()
                        highlight_recomposição_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_recomposição_1_value = pd.DataFrame(highlight_recomposição_1).reset_index(drop=True)
                        highlight_recomposição_2_value = pd.DataFrame(highlight_recomposição_2).reset_index(drop=True)
                        highlight_recomposição_3_value = pd.DataFrame(highlight_recomposição_3).reset_index(drop=True)
                        highlight_recomposição_4_value = pd.DataFrame(highlight_recomposição_4).reset_index(drop=True)

                        highlight_recomposição_1_value = highlight_recomposição_1_value.iat[0,0]
                        highlight_recomposição_2_value = highlight_recomposição_2_value.iat[0,0]
                        highlight_recomposição_3_value = highlight_recomposição_3_value.iat[0,0]
                        highlight_recomposição_4_value = highlight_recomposição_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_recomposição_1, metrics_recomposição_2, 
                                                            metrics_recomposição_3, metrics_recomposição_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_recomposição_1, metrics_recomposição_2, 
                                                            metrics_recomposição_3, metrics_recomposição_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        recomposição_ranking_df = pd.read_csv("Recomposição_ranking.csv")

                        # Building the Extended Title"
                        rows_count = recomposição_ranking_df[(recomposição_ranking_df['Liga'] == liga)  & 
                                                                            (recomposição_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_defensivos_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Duelos defensivos /90_Ranking'].values
                        Duelos_defensivos_per_ranking_value = Duelos_defensivos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_per_ranking_value = f"Duelos defensivos /90 {output_str} {highlight_recomposição_1_value}"

                        # Building the Extended Title"
                        Interceptações_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Interceptações /90_Ranking'].values
                        Interceptações_per_ranking_value = Interceptações_per_ranking_value[0].astype(int)
                        output_str = f"({Interceptações_per_ranking_value}/{rows_count})"
                        full_title_Interceptações_per_ranking_value = f"Interceptações /90 {output_str} {highlight_recomposição_2_value}"

                        # Building the Extended Title"
                        Ações_defensivas_bem_sucedidas_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Ações defensivas bem sucedidas /90_Ranking'].values
                        Ações_defensivas_bem_sucedidas_per_ranking_value = Ações_defensivas_bem_sucedidas_per_ranking_value[0].astype(int)
                        output_str = f"({Ações_defensivas_bem_sucedidas_per_ranking_value}/{rows_count})"
                        full_title_Ações_defensivas_bem_sucedidas_per_ranking_value = f"Ações defensivas bem sucedidas /90 {output_str} {highlight_recomposição_3_value}"

                        # Building the Extended Title"
                        Duelos_defensivos_ganhos_per_ranking_value = recomposição_ranking_df.loc[(recomposição_ranking_df['Atleta'] == jogadores) & 
                                                                            (recomposição_ranking_df['Liga'] == liga) & 
                                                                            (recomposição_ranking_df['Posição'] == posição), 'Duelos defensivos ganhos /90_Ranking'].values
                        Duelos_defensivos_ganhos_per_ranking_value = Duelos_defensivos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_defensivos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_defensivos_ganhos_per_ranking_value = f"Duelos defensivos ganhos /90 {output_str} {highlight_recomposição_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_recomposição_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_recomposição_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_defensivos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_recomposição_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_recomposição_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Interceptações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_recomposição_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_recomposição_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Ações_defensivas_bem_sucedidas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_recomposição_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_recomposição_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Duelos_defensivos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    if atributo == ("Retenção de posse"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Retenção_posse_atacante_Charts = pd.read_csv('retenção_posse.csv')
                        Retenção_posse_atacante_Charts_1 = Retenção_posse_atacante_Charts[(Retenção_posse_atacante_Charts['Atleta']==jogadores)&
                                                                                    (Retenção_posse_atacante_Charts['Liga']==liga)&
                                                                                    (Retenção_posse_atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Retenção_posse_atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Retenção_posse_atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Retenção_posse_atacante_Charts_1.iloc[:, np.r_[9:14]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Retenção_posse_atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Retenção_posse_atacante_Charts_2 = Retenção_posse_atacante_Charts[(Retenção_posse_atacante_Charts['Liga']==liga)&(Retenção_posse_atacante_Charts['Posição']==posição)]
                        metrics = Retenção_posse_atacante_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_retenção_posse_1 = metrics.iloc[:, 0].tolist()
                        metrics_retenção_posse_2 = metrics.iloc[:, 1].tolist()
                        metrics_retenção_posse_3 = metrics.iloc[:, 2].tolist()
                        metrics_retenção_posse_4 = metrics.iloc[:, 3].tolist()
                        metrics_retenção_posse_5 = metrics.iloc[:, 4].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Retenção_posse_atacante_Charts_2[(Retenção_posse_atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_retenção_posse_1 = highlight.iloc[:, 0].tolist()
                        highlight_retenção_posse_2 = highlight.iloc[:, 1].tolist()
                        highlight_retenção_posse_3 = highlight.iloc[:, 2].tolist()
                        highlight_retenção_posse_4 = highlight.iloc[:, 3].tolist()
                        highlight_retenção_posse_5 = highlight.iloc[:, 4].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_retenção_posse_1_value = pd.DataFrame(highlight_retenção_posse_1).reset_index(drop=True)
                        highlight_retenção_posse_2_value = pd.DataFrame(highlight_retenção_posse_2).reset_index(drop=True)
                        highlight_retenção_posse_3_value = pd.DataFrame(highlight_retenção_posse_3).reset_index(drop=True)
                        highlight_retenção_posse_4_value = pd.DataFrame(highlight_retenção_posse_4).reset_index(drop=True)
                        highlight_retenção_posse_5_value = pd.DataFrame(highlight_retenção_posse_5).reset_index(drop=True)

                        highlight_retenção_posse_1_value = highlight_retenção_posse_1_value.iat[0,0]
                        highlight_retenção_posse_2_value = highlight_retenção_posse_2_value.iat[0,0]
                        highlight_retenção_posse_3_value = highlight_retenção_posse_3_value.iat[0,0]
                        highlight_retenção_posse_4_value = highlight_retenção_posse_4_value.iat[0,0]
                        highlight_retenção_posse_5_value = highlight_retenção_posse_5_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_retenção_posse_1, metrics_retenção_posse_2, 
                                                            metrics_retenção_posse_3, metrics_retenção_posse_4,
                                                            metrics_retenção_posse_5])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_retenção_posse_1, metrics_retenção_posse_2, 
                                                            metrics_retenção_posse_3, metrics_retenção_posse_4,
                                                            metrics_retenção_posse_5])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        retenção_posse_ranking_df = pd.read_csv("Retenção_posse_ranking.csv")

                        # Building the Extended Title"
                        rows_count = retenção_posse_ranking_df[(retenção_posse_ranking_df['Liga'] == liga)  & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição)].shape[0]
                        Passes_recebidos_per_ranking_value = retenção_posse_ranking_df.loc[(retenção_posse_ranking_df['Atleta'] == jogadores) & 
                                                                            (retenção_posse_ranking_df['Liga'] == liga) & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição), 'Passes recebidos /90_Ranking'].values
                        Passes_recebidos_per_ranking_value = Passes_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_recebidos_per_ranking_value = f"Passes recebidos /90 {output_str} {highlight_retenção_posse_1_value}"

                        # Building the Extended Title"
                        Duelos_ganhos_per_ranking_value = retenção_posse_ranking_df.loc[(retenção_posse_ranking_df['Atleta'] == jogadores) & 
                                                                            (retenção_posse_ranking_df['Liga'] == liga) & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição), 'Duelos ganhos /90_Ranking'].values
                        Duelos_ganhos_per_ranking_value = Duelos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_ganhos_per_ranking_value = f"Duelos ganhos /90 {output_str} {highlight_retenção_posse_2_value}"

                        # Building the Extended Title"
                        Passes_longos_recebidos_per_ranking_value = retenção_posse_ranking_df.loc[(retenção_posse_ranking_df['Atleta'] == jogadores) & 
                                                                            (retenção_posse_ranking_df['Liga'] == liga) & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição), 'Passes longos recebidos /90_Ranking'].values
                        Passes_longos_recebidos_per_ranking_value = Passes_longos_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_longos_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_longos_recebidos_per_ranking_value = f"Passes longos recebidos /90 {output_str} {highlight_retenção_posse_3_value}"

                        # Building the Extended Title"
                        Passes_curtos_médios_certos_per_ranking_value = retenção_posse_ranking_df.loc[(retenção_posse_ranking_df['Atleta'] == jogadores) & 
                                                                            (retenção_posse_ranking_df['Liga'] == liga) & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição), 'Passes curtos/médios certos p/90_Ranking'].values
                        Passes_curtos_médios_certos_per_ranking_value = Passes_curtos_médios_certos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_curtos_médios_certos_per_ranking_value}/{rows_count})"
                        full_title_Passes_curtos_médios_certos_per_ranking_value = f"Passes curtos/médios certos /90 {output_str} {highlight_retenção_posse_4_value}"

                        # Building the Extended Title"
                        Duelos_aéreos_ganhos_ranking_value = retenção_posse_ranking_df.loc[(retenção_posse_ranking_df['Atleta'] == jogadores) & 
                                                                            (retenção_posse_ranking_df['Liga'] == liga) & 
                                                                            (retenção_posse_ranking_df['Posição'] == posição), 'Duelos aéreos ganhos %_Ranking'].values
                        Duelos_aéreos_ganhos_ranking_value = Duelos_aéreos_ganhos_ranking_value[0].astype(int)
                        output_str = f"({Duelos_aéreos_ganhos_ranking_value}/{rows_count})"
                        full_title_Duelos_aéreos_ganhos_ranking_value = f"Duelos aéreos ganhos % {output_str} {highlight_retenção_posse_5_value}"


                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_retenção_posse_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_retenção_posse_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_retenção_posse_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_retenção_posse_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Duelos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_retenção_posse_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_retenção_posse_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Passes_longos_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax4.scatter(metrics_retenção_posse_4, metrics_y, color='deepskyblue')
                        ax4.scatter(highlight_retenção_posse_4, highlight_y, color='blue', s=60)
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_curtos_médios_certos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax5.scatter(metrics_retenção_posse_5, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax5.scatter(highlight_retenção_posse_5, highlight_y, color='blue', s=60, label=jogadores)
                        ax5.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax5.get_yaxis().set_visible(False)
                        ax5.set_title(full_title_Duelos_aéreos_ganhos_ranking_value, fontsize=12, fontweight='bold')
                        ax5.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax5.spines['top'].set_visible(False)
                        ax5.spines['right'].set_visible(False)
                        ax5.spines['bottom'].set_visible(False)
                        ax5.spines['left'].set_visible(False)
                        ax5.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax5.legend(loc='right', bbox_to_anchor=(0.2, -2.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Arranque"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Arranque_Atacante_Charts = pd.read_csv('arranque.csv')
                        Arranque_Atacante_Charts_1 = Arranque_Atacante_Charts[(Arranque_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Arranque_Atacante_Charts['Liga']==liga)&
                                                                                    (Arranque_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Arranque_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Arranque_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Arranque_Atacante_Charts_1.iloc[:, np.r_[7:10]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Arranque_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #Collecting data to plot
                        Arranque_Atacante_Charts_2 = Arranque_Atacante_Charts[(Arranque_Atacante_Charts['Liga']==liga)&(Arranque_Atacante_Charts['Posição']==posição)]
                        metrics = Arranque_Atacante_Charts_2.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        metrics_arranque_1 = metrics.iloc[:, 0].tolist()
                        metrics_arranque_2 = metrics.iloc[:, 1].tolist()
                        metrics_arranque_3 = metrics.iloc[:, 2].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Arranque_Atacante_Charts_2[(Arranque_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        highlight_arranque_1 = highlight.iloc[:, 0].tolist()
                        highlight_arranque_2 = highlight.iloc[:, 1].tolist()
                        highlight_arranque_3 = highlight.iloc[:, 2].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_arranque_1_value = pd.DataFrame(highlight_arranque_1).reset_index(drop=True)
                        highlight_arranque_2_value = pd.DataFrame(highlight_arranque_2).reset_index(drop=True)
                        highlight_arranque_3_value = pd.DataFrame(highlight_arranque_3).reset_index(drop=True)

                        highlight_arranque_1_value = highlight_arranque_1_value.iat[0,0]
                        highlight_arranque_2_value = highlight_arranque_2_value.iat[0,0]
                        highlight_arranque_3_value = highlight_arranque_3_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_arranque_1, metrics_arranque_2, 
                                                            metrics_arranque_3])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_arranque_1, metrics_arranque_2, 
                                                            metrics_arranque_3])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 4.0))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        arranque_ranking_df = pd.read_csv("Arranque_ranking.csv")

                        # Building the Extended Title"
                        rows_count = arranque_ranking_df[(arranque_ranking_df['Liga'] == liga)  & 
                                                                            (arranque_ranking_df['Posição'] == posição)].shape[0]
                        Passes_longos_recebidos_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Passes longos recebidos /90_Ranking'].values
                        Passes_longos_recebidos_per_ranking_value = Passes_longos_recebidos_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_longos_recebidos_per_ranking_value}/{rows_count})"
                        full_title_Passes_longos_recebidos_per_ranking_value = f"Passes longos recebidos /90 {output_str} {highlight_arranque_1_value}"

                        # Building the Extended Title"
                        Acelerações_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Acelerações /90_Ranking'].values
                        Acelerações_per_ranking_value = Acelerações_per_ranking_value[0].astype(int)
                        output_str = f"({Acelerações_per_ranking_value}/{rows_count})"
                        full_title_Acelerações_per_ranking_value = f"Acelerações /90 {output_str} {highlight_arranque_2_value}"

                        # Building the Extended Title"
                        Corridas_progressivas_per_ranking_value = arranque_ranking_df.loc[(arranque_ranking_df['Atleta'] == jogadores) & 
                                                                            (arranque_ranking_df['Liga'] == liga) & 
                                                                            (arranque_ranking_df['Posição'] == posição), 'Corridas progressivas /90_Ranking'].values
                        Corridas_progressivas_per_ranking_value = Corridas_progressivas_per_ranking_value[0].astype(int)
                        output_str = f"({Corridas_progressivas_per_ranking_value}/{rows_count})"
                        full_title_Corridas_progressivas_per_ranking_value = f"Corridas progressivas /90 {output_str} {highlight_arranque_3_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_arranque_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_arranque_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Passes_longos_recebidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_arranque_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_arranque_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Acelerações_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_arranque_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax3.scatter(highlight_arranque_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax3.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Corridas_progressivas_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax3.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Bola aérea"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Bola_Aérea_Atacante_Charts = pd.read_csv('bola_aérea.csv')
                        Bola_Aérea_Atacante_Charts_1 = Bola_Aérea_Atacante_Charts[(Bola_Aérea_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Bola_Aérea_Atacante_Charts['Liga']==liga)&
                                                                                    (Bola_Aérea_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Bola_Aérea_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Bola_Aérea_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Bola_Aérea_Atacante_Charts_1.iloc[:, np.r_[7:10]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Bola_Aérea_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #Collecting data to plot
                        Bola_Aérea_Atacante_Charts_2 = Bola_Aérea_Atacante_Charts[(Bola_Aérea_Atacante_Charts['Liga']==liga)&(Bola_Aérea_Atacante_Charts['Posição']==posição)]
                        metrics = Bola_Aérea_Atacante_Charts_2.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        metrics_bola_aérea_1 = metrics.iloc[:, 0].tolist()
                        metrics_bola_aérea_2 = metrics.iloc[:, 1].tolist()
                        metrics_bola_aérea_3 = metrics.iloc[:, 2].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Bola_Aérea_Atacante_Charts_2[(Bola_Aérea_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:7]].reset_index(drop=True)
                        highlight_bola_aérea_1 = highlight.iloc[:, 0].tolist()
                        highlight_bola_aérea_2 = highlight.iloc[:, 1].tolist()
                        highlight_bola_aérea_3 = highlight.iloc[:, 2].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_bola_aérea_1_value = pd.DataFrame(highlight_bola_aérea_1).reset_index(drop=True)
                        highlight_bola_aérea_2_value = pd.DataFrame(highlight_bola_aérea_2).reset_index(drop=True)
                        highlight_bola_aérea_3_value = pd.DataFrame(highlight_bola_aérea_3).reset_index(drop=True)

                        highlight_bola_aérea_1_value = highlight_bola_aérea_1_value.iat[0,0]
                        highlight_bola_aérea_2_value = highlight_bola_aérea_2_value.iat[0,0]
                        highlight_bola_aérea_3_value = highlight_bola_aérea_3_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_bola_aérea_1, metrics_bola_aérea_2, 
                                                            metrics_bola_aérea_3])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_bola_aérea_1, metrics_bola_aérea_2, 
                                                            metrics_bola_aérea_3])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 4.0))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"apoio
                        bola_aérea_ranking_df = pd.read_csv("Bola_aérea_ranking.csv")

                        # Building the Extended Title"
                        rows_count = bola_aérea_ranking_df[(bola_aérea_ranking_df['Liga'] == liga)  & 
                                                                            (bola_aérea_ranking_df['Posição'] == posição)].shape[0]
                        Duelos_aéreos_ganhos_ranking_value = bola_aérea_ranking_df.loc[(bola_aérea_ranking_df['Atleta'] == jogadores) & 
                                                                            (bola_aérea_ranking_df['Liga'] == liga) & 
                                                                            (bola_aérea_ranking_df['Posição'] == posição), 'Duelos aéreos ganhos %_Ranking'].values
                        Duelos_aéreos_ganhos_ranking_value = Duelos_aéreos_ganhos_ranking_value[0].astype(int)
                        output_str = f"({Duelos_aéreos_ganhos_ranking_value}/{rows_count})"
                        full_title_Duelos_aéreos_ganhos_ranking_value = f"Duelos aéreos ganhos % {output_str} {highlight_bola_aérea_1_value}"

                        # Building the Extended Title"
                        Duelos_aéreos_ganhos_per_ranking_value = bola_aérea_ranking_df.loc[(bola_aérea_ranking_df['Atleta'] == jogadores) & 
                                                                            (bola_aérea_ranking_df['Liga'] == liga) & 
                                                                            (bola_aérea_ranking_df['Posição'] == posição), 'Duelos aéreos ganhos /90_Ranking'].values
                        Duelos_aéreos_ganhos_per_ranking_value = Duelos_aéreos_ganhos_per_ranking_value[0].astype(int)
                        output_str = f"({Duelos_aéreos_ganhos_per_ranking_value}/{rows_count})"
                        full_title_Duelos_aéreos_ganhos_per_ranking_value = f"Duelos aéreos ganhos /90 {output_str} {highlight_bola_aérea_2_value}"

                        # Building the Extended Title"
                        Gols_de_cabeça_ranking_value = bola_aérea_ranking_df.loc[(bola_aérea_ranking_df['Atleta'] == jogadores) & 
                                                                            (bola_aérea_ranking_df['Liga'] == liga) & 
                                                                            (bola_aérea_ranking_df['Posição'] == posição), 'Gols de cabeça %_Ranking'].values
                        Gols_de_cabeça_ranking_value = Gols_de_cabeça_ranking_value[0].astype(int)
                        output_str = f"({Gols_de_cabeça_ranking_value}/{rows_count})"
                        full_title_Gols_de_cabeça_ranking_value = f"Gols de cabeça % {output_str} {highlight_bola_aérea_3_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_bola_aérea_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_bola_aérea_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Duelos_aéreos_ganhos_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_bola_aérea_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_bola_aérea_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Duelos_aéreos_ganhos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_bola_aérea_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax3.scatter(highlight_bola_aérea_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax3.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Gols_de_cabeça_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax3.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                    elif atributo == ("Último passe"):
                
                    #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Último_passe_Atacante_Charts = pd.read_csv('último_passe.csv')
                        Último_passe_Atacante_Charts_1 = Último_passe_Atacante_Charts[(Último_passe_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Último_passe_Atacante_Charts['Liga']==liga)&
                                                                                    (Último_passe_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Último_passe_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Último_passe_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Último_passe_Atacante_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Último_passe_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        ###############################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        # Collecting data
                        #Último_passe_Atacante_Charts_2 = Último_passe_Atacante_Charts[(Último_passe_Atacante_Charts['Liga']==liga)]


                        #Collecting data to plot
                        Último_passe_Atacante_Charts_2 = Último_passe_Atacante_Charts[(Último_passe_Atacante_Charts['Liga']==liga)&(Último_passe_Atacante_Charts['Posição']==posição)]
                        metrics = Último_passe_Atacante_Charts_2.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        metrics_último_passe_1 = metrics.iloc[:, 0].tolist()
                        metrics_último_passe_2 = metrics.iloc[:, 1].tolist()
                        metrics_último_passe_3 = metrics.iloc[:, 2].tolist()
                        metrics_último_passe_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Último_passe_Atacante_Charts_2[(Último_passe_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:9]].reset_index(drop=True)
                        highlight_último_passe_1 = highlight.iloc[:, 0].tolist()
                        highlight_último_passe_2 = highlight.iloc[:, 1].tolist()
                        highlight_último_passe_3 = highlight.iloc[:, 2].tolist()
                        highlight_último_passe_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0


                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = pd.DataFrame(highlight_último_passe_1).reset_index(drop=True)
                        highlight_último_passe_2_value = pd.DataFrame(highlight_último_passe_2).reset_index(drop=True)
                        highlight_último_passe_3_value = pd.DataFrame(highlight_último_passe_3).reset_index(drop=True)
                        highlight_último_passe_4_value = pd.DataFrame(highlight_último_passe_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_último_passe_1_value = highlight_último_passe_1_value.iat[0,0]
                        highlight_último_passe_2_value = highlight_último_passe_2_value.iat[0,0]
                        highlight_último_passe_3_value = highlight_último_passe_3_value.iat[0,0]
                        highlight_último_passe_4_value = highlight_último_passe_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_último_passe_1, metrics_último_passe_2, 
                                                            metrics_último_passe_3, metrics_último_passe_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 4.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        último_passe_ranking_df = pd.read_csv("Último_passe_ranking.csv")
                        # Building the Extended Title"
                        rows_count = último_passe_ranking_df[(último_passe_ranking_df['Liga'] == liga)  & 
                                                                            (último_passe_ranking_df['Posição'] == posição)].shape[0]
                        Assistências_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Assistências /90_Ranking'].values
                        Assistências_per_ranking_value = Assistências_per_ranking_value[0].astype(int)
                        output_str = f"({Assistências_per_ranking_value}/{rows_count})"
                        full_title_Assistências_per_ranking_value = f"Assistências /90 {output_str} {highlight_último_passe_1_value}"

                        # Building the Extended Title"
                        xA_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'xA /90_Ranking'].values
                        xA_per_ranking_value = xA_per_ranking_value[0].astype(int)
                        output_str = f"({xA_per_ranking_value}/{rows_count})"
                        full_title_xA_per_ranking_value = f"xA /90 {output_str} {highlight_último_passe_2_value}"

                        # Building the Extended Title"
                        Deep_completions_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Deep completions /90_Ranking'].values
                        Deep_completions_per_ranking_value = Deep_completions_per_ranking_value[0].astype(int)
                        output_str = f"({Deep_completions_per_ranking_value}/{rows_count})"
                        full_title_Deep_completions_per_ranking_value = f"Deep completions /90 {output_str} {highlight_último_passe_3_value}"

                        # Building the Extended Title"
                        Passes_chave_per_ranking_value = último_passe_ranking_df.loc[(último_passe_ranking_df['Atleta'] == jogadores) & 
                                                                            (último_passe_ranking_df['Liga'] == liga) & 
                                                                            (último_passe_ranking_df['Posição'] == posição), 'Passes chave /90_Ranking'].values
                        Passes_chave_per_ranking_value = Passes_chave_per_ranking_value[0].astype(int)
                        output_str = f"({Passes_chave_per_ranking_value}/{rows_count})"
                        full_title_Passes_chave_per_ranking_value = f"Passes chave /90 {output_str} {highlight_último_passe_4_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_último_passe_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_último_passe_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Assistências_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_último_passe_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_último_passe_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_xA_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the third scatter plot in the second subplot
                        ax3.scatter(metrics_último_passe_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_último_passe_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Deep_completions_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_último_passe_4, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_último_passe_4, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Passes_chave_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.7), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Finalização"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Finalização_Atacante_Charts = pd.read_csv('finalização.csv')
                        Finalização_Atacante_Charts_1 = Finalização_Atacante_Charts[(Finalização_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Finalização_Atacante_Charts['Liga']==liga)&
                                                                                    (Finalização_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Finalização_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Finalização_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Finalização_Atacante_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Finalização_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Finalização_Atacante_Charts_2 = Finalização_Atacante_Charts[(Finalização_Atacante_Charts['Liga']==liga)&(Finalização_Atacante_Charts['Posição']==posição)]
                        metrics = Finalização_Atacante_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_finalização_1 = metrics.iloc[:, 0].tolist()
                        metrics_finalização_2 = metrics.iloc[:, 1].tolist()
                        metrics_finalização_3 = metrics.iloc[:, 2].tolist()
                        metrics_finalização_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Finalização_Atacante_Charts_2[(Finalização_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_finalização_1 = highlight.iloc[:, 0].tolist()
                        highlight_finalização_2 = highlight.iloc[:, 1].tolist()
                        highlight_finalização_3 = highlight.iloc[:, 2].tolist()
                        highlight_finalização_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_finalização_1_value = pd.DataFrame(highlight_finalização_1).reset_index(drop=True)
                        highlight_finalização_2_value = pd.DataFrame(highlight_finalização_2).reset_index(drop=True)
                        highlight_finalização_3_value = pd.DataFrame(highlight_finalização_3).reset_index(drop=True)
                        highlight_finalização_4_value = pd.DataFrame(highlight_finalização_4).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_finalização_1_value = highlight_finalização_1_value.iat[0,0]
                        highlight_finalização_2_value = highlight_finalização_2_value.iat[0,0]
                        highlight_finalização_3_value = highlight_finalização_3_value.iat[0,0]
                        highlight_finalização_4_value = highlight_finalização_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                                            metrics_finalização_3, metrics_finalização_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_finalização_1, metrics_finalização_2, 
                                                            metrics_finalização_3, metrics_finalização_4])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        finalização_ranking_df = pd.read_csv("Finalização_ranking.csv")
                        # Building the Extended Title"
                        rows_count = finalização_ranking_df[(finalização_ranking_df['Liga'] == liga)  & 
                                                                            (finalização_ranking_df['Posição'] == posição)].shape[0]
                        Conversão_de_gols_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Conversão de gols_Ranking'].values
                        Conversão_de_gols_ranking_value = Conversão_de_gols_ranking_value[0].astype(int)
                        output_str = f"({Conversão_de_gols_ranking_value}/{rows_count})"
                        full_title_Conversão_de_gols_ranking_value = f"Conversão de gols {output_str} {highlight_finalização_1_value}"

                        # Building the Extended Title"
                        Conversão_de_xG_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Conversão de xG_Ranking'].values
                        Conversão_de_xG_ranking_value = Conversão_de_xG_ranking_value[0].astype(int)
                        output_str = f"({Conversão_de_xG_ranking_value}/{rows_count})"
                        full_title_Conversão_de_xG_ranking_value = f"Conversão de xG {output_str} {highlight_finalização_2_value}"

                        # Building the Extended Title"
                        Ameaça_ofensiva_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Ameaça_Ofensiva_Ranking'].values
                        Ameaça_ofensiva_ranking_value = Ameaça_ofensiva_ranking_value[0].astype(int)
                        output_str = f"({Ameaça_ofensiva_ranking_value}/{rows_count})"
                        full_title_Ameaça_ofensiva_ranking_value = f"Ameaça ofensiva {output_str} {highlight_finalização_3_value}"

                        # Building the Extended Title"
                        Finalizações_no_alvo_per_ranking_value = finalização_ranking_df.loc[(finalização_ranking_df['Atleta'] == jogadores) & 
                                                                            (finalização_ranking_df['Liga'] == liga) & 
                                                                            (finalização_ranking_df['Posição'] == posição), 'Finalizações no alvo /90_Ranking'].values
                        Finalizações_no_alvo_per_ranking_value = Finalizações_no_alvo_per_ranking_value[0].astype(int)
                        output_str = f"({Finalizações_no_alvo_per_ranking_value}/{rows_count})"
                        full_title_Finalizações_no_alvo_per_ranking_value = f"Finalizaçõe no alvo /90 {output_str} {highlight_finalização_4_value}"


                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_finalização_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_finalização_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Conversão_de_gols_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_finalização_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_finalização_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_Conversão_de_xG_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_finalização_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_finalização_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Ameaça_ofensiva_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_finalização_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_finalização_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_Finalizações_no_alvo_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################

                    elif atributo == ("Drible"):
                
                        Drible_Atacante_Charts = pd.read_csv('drible.csv')
                        Drible_Atacante_Charts_1 = Drible_Atacante_Charts[(Drible_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Drible_Atacante_Charts['Liga']==liga)&
                                                                                    (Drible_Atacante_Charts['Posição']==posição)]

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
                        
                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Drible_Atacante_Charts_2 = Drible_Atacante_Charts[(Drible_Atacante_Charts['Liga']==liga)&(Drible_Atacante_Charts['Posição']==posição)]
                        metrics = Drible_Atacante_Charts_2.iloc[:, np.r_[-2]].reset_index(drop=True)
                        metrics_drible_1 = metrics.iloc[:, 0].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Drible_Atacante_Charts_2[(Drible_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[-2]].reset_index(drop=True)
                        highlight_drible_1 = highlight.iloc[:, 0].tolist()
                        highlight_y = 0

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = pd.DataFrame(highlight_drible_1).reset_index(drop=True)

                        # Computing the selected attribute specific values
                        highlight_drible_1_value = highlight_drible_1_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_drible_1])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_drible_1])
                        max_value = max_value + 0.1

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1) = plt.subplots(figsize=(7, 1.5))
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        drible_ranking_df = pd.read_csv("Drible_ranking.csv")
                        # Building the Extended Title"
                        rows_count = drible_ranking_df[(drible_ranking_df['Liga'] == liga)  & 
                                                                            (drible_ranking_df['Posição'] == posição)].shape[0]
                        Dribles_bem_sucedidos_per_ranking_value = drible_ranking_df.loc[(drible_ranking_df['Atleta'] == jogadores) & 
                                                                            (drible_ranking_df['Liga'] == liga) & 
                                                                            (drible_ranking_df['Posição'] == posição), 'Dribles bem sucedidos /90_Ranking'].values
                        Dribles_bem_sucedidos_per_ranking_value = Dribles_bem_sucedidos_per_ranking_value[0].astype(int)
                        output_str = f"({Dribles_bem_sucedidos_per_ranking_value}/{rows_count})"
                        full_title_Dribles_bem_sucedidos_per_ranking_value = f"Dribles bem sucedidos /90 {output_str} {highlight_drible_1_value}"

                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_drible_1, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax1.scatter(highlight_drible_1, highlight_y, color='blue', s=60, label=jogadores)
                        ax1.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_Dribles_bem_sucedidos_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax1.legend(loc='right', bbox_to_anchor=(0.2, -1.3), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################

                    elif atributo == ("Oportunismo"):
                
                        #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                        st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido para o Jogador na Liga em 2023</h3>", unsafe_allow_html=True)
                        Oportunismo_Atacante_Charts = pd.read_csv('oportunismo.csv')
                        Oportunismo_Atacante_Charts_1 = Oportunismo_Atacante_Charts[(Oportunismo_Atacante_Charts['Atleta']==jogadores)&
                                                                                    (Oportunismo_Atacante_Charts['Liga']==liga)&
                                                                                    (Oportunismo_Atacante_Charts['Posição']==posição)]
                        columns_to_rename = {
                            col: col.replace('_percentil', '') for col in Oportunismo_Atacante_Charts.columns if '_percentil' in col
                        }
                        # Renaming the columns in the DataFrame
                        Oportunismo_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                        #Collecting data to plot
                        metrics = Oportunismo_Atacante_Charts_1.iloc[:, np.r_[8:12]].reset_index(drop=True)
                        metrics_list = metrics.iloc[0].tolist()
                        #Collecting clube
                        clube = Oportunismo_Atacante_Charts_1.iat[0, 1]

                        ## parameter names
                        params = metrics.columns.tolist()

                        ## range values
                        ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]

                        ## parameter value
                        values = metrics_list

                        ## title values
                        title = dict(
                            title_name=jogadores,
                            title_color = 'blue',
                            subtitle_name= (posição),
                            subtitle_color='#344D94',
                            title_name_2=clube,
                            title_color_2 = 'blue',
                            subtitle_name_2='2023',
                            subtitle_color_2='#344D94',
                            title_fontsize=20,
                            subtitle_fontsize=18,
                        )            

                        ## endnote 
                        endnote = "Visualization made by: @JAmerico1898\nAll units are in per90 or %"

                        ## instantiate object
                        radar = Radar()

                        ## instantiate object -- changing fontsize
                        radar=Radar(fontfamily='Cursive', range_fontsize=13)
                        radar=Radar(fontfamily='Cursive', label_fontsize=15)

                        ## plot radar -- filename and dpi
                        fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=[('#B6282F', 0.65), ('#344D94', 0.65)], 
                                                title=title, endnote=endnote, dpi=600)
                        st.pyplot(fig)

                        ################################################################################################################################
                        ################################################################################################################################

                        #Plotar Segundo Gráfico - Dispersão dos jogadores da mesma posição na liga em eixo único:

                        st.markdown("<h3 style='text-align: center; color: blue; '>Distribuição das Métricas Associadas ao Atributo Escolhido para todos os jogadores da Liga em 2023</h3>", unsafe_allow_html=True)


                        # Dynamically create the HTML string with the 'jogadores' variable
                        title_html = f"<h3 style='text-align: center; font-weight: bold; color: blue;'>{jogadores}</h3>"

                        # Use the dynamically created HTML string in st.markdown
                        st.markdown(title_html, unsafe_allow_html=True)

                        #st.markdown("<h3 style='text-align: center;'>Percentis dos Atributos do Jogador na Liga em 2023</h3>", unsafe_allow_html=True)

                        #Collecting data to plot
                        Oportunismo_Atacante_Charts_2 = Oportunismo_Atacante_Charts[(Oportunismo_Atacante_Charts['Liga']==liga)&(Oportunismo_Atacante_Charts['Posição']==posição)]
                        metrics = Oportunismo_Atacante_Charts_2.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        metrics_oportunismo_1 = metrics.iloc[:, 0].tolist()
                        metrics_oportunismo_2 = metrics.iloc[:, 1].tolist()
                        metrics_oportunismo_3 = metrics.iloc[:, 2].tolist()
                        metrics_oportunismo_4 = metrics.iloc[:, 3].tolist()
                        metrics_y = [0] * len(metrics)

                        # The specific data point you want to highlight
                        highlight = Oportunismo_Atacante_Charts_2[(Oportunismo_Atacante_Charts_2['Atleta']==jogadores)]
                        highlight = highlight.iloc[:, np.r_[4:8]].reset_index(drop=True)
                        highlight_oportunismo_1 = highlight.iloc[:, 0].tolist()
                        highlight_oportunismo_2 = highlight.iloc[:, 1].tolist()
                        highlight_oportunismo_3 = highlight.iloc[:, 2].tolist()
                        highlight_oportunismo_4 = highlight.iloc[:, 3].tolist()
                        highlight_y = 0

                        # Computing the selected player specific values
                        highlight_oportunismo_1_value = pd.DataFrame(highlight_oportunismo_1).reset_index(drop=True)
                        highlight_oportunismo_2_value = pd.DataFrame(highlight_oportunismo_2).reset_index(drop=True)
                        highlight_oportunismo_3_value = pd.DataFrame(highlight_oportunismo_3).reset_index(drop=True)
                        highlight_oportunismo_4_value = pd.DataFrame(highlight_oportunismo_4).reset_index(drop=True)

                        highlight_oportunismo_1_value = highlight_oportunismo_1_value.iat[0,0]
                        highlight_oportunismo_2_value = highlight_oportunismo_2_value.iat[0,0]
                        highlight_oportunismo_3_value = highlight_oportunismo_3_value.iat[0,0]
                        highlight_oportunismo_4_value = highlight_oportunismo_4_value.iat[0,0]

                        # Computing the min and max value across all lists using a generator expression
                        min_value = min(min(lst) for lst in [metrics_oportunismo_1, metrics_oportunismo_2, 
                                                            metrics_oportunismo_3, metrics_oportunismo_4])
                        min_value = min_value - 0.1
                        max_value = max(max(lst) for lst in [metrics_oportunismo_1, metrics_oportunismo_2, 
                                                            metrics_oportunismo_3, metrics_oportunismo_4])
                        max_value = max_value + 0.1

                        #Collecting Additional Information
                        # Load the saved DataFrame from "Lateral_ranking.csv"
                        oportunismo_ranking_df = pd.read_csv("Oportunismo_ranking.csv")
                        # Building the Extended Title"
                        rows_count = oportunismo_ranking_df[(oportunismo_ranking_df['Liga'] == liga)  & 
                                                                            (oportunismo_ranking_df['Posição'] == posição)].shape[0]
                        xG_per_ranking_value = oportunismo_ranking_df.loc[(oportunismo_ranking_df['Atleta'] == jogadores) & 
                                                                            (oportunismo_ranking_df['Liga'] == liga) & 
                                                                            (oportunismo_ranking_df['Posição'] == posição), 'xG /90_Ranking'].values
                        xG_per_ranking_value = xG_per_ranking_value[0].astype(int)
                        output_str = f"({xG_per_ranking_value}/{rows_count})"
                        full_title_xG_per_ranking_value = f"xG /90 {output_str} {highlight_oportunismo_1_value}"

                        # Building the Extended Title"
                        xG_por_finalização_per_ranking_value = oportunismo_ranking_df.loc[(oportunismo_ranking_df['Atleta'] == jogadores) & 
                                                                            (oportunismo_ranking_df['Liga'] == liga) & 
                                                                            (oportunismo_ranking_df['Posição'] == posição), 'xG por finalização /90_Ranking'].values
                        xG_por_finalização_per_ranking_value = xG_por_finalização_per_ranking_value[0].astype(int)
                        output_str = f"({xG_por_finalização_per_ranking_value}/{rows_count})"
                        full_title_xG_por_finalização_per_ranking_value = f"xG por finalização /90 {output_str} {highlight_oportunismo_2_value}"

                        # Building the Extended Title"
                        Gols_por_pisadas_na_área_per_ranking_value = oportunismo_ranking_df.loc[(oportunismo_ranking_df['Atleta'] == jogadores) & 
                                                                            (oportunismo_ranking_df['Liga'] == liga) & 
                                                                            (oportunismo_ranking_df['Posição'] == posição), 'Gols por pisadas na área /90_Ranking'].values
                        Gols_por_pisadas_na_área_per_ranking_value = Gols_por_pisadas_na_área_per_ranking_value[0].astype(int)
                        output_str = f"({Gols_por_pisadas_na_área_per_ranking_value}/{rows_count})"
                        full_title_Gols_por_pisadas_na_área_per_ranking_value = f"Gols por pisadas na área /90 {output_str} {highlight_oportunismo_3_value}"

                        # Building the Extended Title"
                        xG_por_pisadas_na_área_per_ranking_value = oportunismo_ranking_df.loc[(oportunismo_ranking_df['Atleta'] == jogadores) & 
                                                                            (oportunismo_ranking_df['Liga'] == liga) & 
                                                                            (oportunismo_ranking_df['Posição'] == posição), 'xG por pisadas na área /90_Ranking'].values
                        xG_por_pisadas_na_área_per_ranking_value = xG_por_pisadas_na_área_per_ranking_value[0].astype(int)
                        output_str = f"({xG_por_pisadas_na_área_per_ranking_value}/{rows_count})"
                        full_title_xG_por_pisadas_na_área_per_ranking_value = f"xG por pisadas na área /90 {output_str} {highlight_oportunismo_4_value}"

                        # Create two subplots vertically aligned with separate x-axes
                        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
                        ax.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot


                        # Plot the first scatter plot in the first subplot
                        ax1.scatter(metrics_oportunismo_1, metrics_y, color='deepskyblue')
                        ax1.scatter(highlight_oportunismo_1, highlight_y, color='blue', s=60)
                        ax1.get_yaxis().set_visible(False)
                        ax1.set_title(full_title_xG_per_ranking_value, fontsize=12, fontweight='bold')
                        ax1.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))            
                        ax1.spines['top'].set_visible(False)
                        ax1.spines['right'].set_visible(False)
                        ax1.spines['bottom'].set_visible(False)
                        ax1.spines['left'].set_visible(False)
                        ax1.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the second scatter plot in the second subplot
                        ax2.scatter(metrics_oportunismo_2, metrics_y, color='deepskyblue')
                        ax2.scatter(highlight_oportunismo_2, highlight_y, color='blue', s=60)
                        ax2.get_yaxis().set_visible(False)
                        ax2.set_title(full_title_xG_por_finalização_per_ranking_value, fontsize=12, fontweight='bold')
                        ax2.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax3.scatter(metrics_oportunismo_3, metrics_y, color='deepskyblue')
                        ax3.scatter(highlight_oportunismo_3, highlight_y, color='blue', s=60)
                        ax3.get_yaxis().set_visible(False)
                        ax3.set_title(full_title_Gols_por_pisadas_na_área_per_ranking_value, fontsize=12, fontweight='bold')
                        ax3.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax3.spines['top'].set_visible(False)
                        ax3.spines['right'].set_visible(False)
                        ax3.spines['bottom'].set_visible(False)
                        ax3.spines['left'].set_visible(False)
                        ax3.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        # Plot the fourth scatter plot in the second subplot
                        ax4.scatter(metrics_oportunismo_3, metrics_y, color='deepskyblue', label='Outros jogadores da Liga')
                        ax4.scatter(highlight_oportunismo_3, highlight_y, color='blue', s=60, label=jogadores)
                        ax4.set_xlabel('Desvio-padrão', fontsize=12, fontweight='bold', color='blue')
                        ax4.get_yaxis().set_visible(False)
                        ax4.set_title(full_title_xG_por_pisadas_na_área_per_ranking_value, fontsize=12, fontweight='bold')
                        ax4.axhline(y=0, color='grey', linewidth=1, alpha=0.4)
                        ax4.xaxis.set_major_locator(ticker.MultipleLocator(2))
                        ax4.spines['top'].set_visible(False)
                        ax4.spines['right'].set_visible(False)
                        ax4.spines['bottom'].set_visible(False)
                        ax4.spines['left'].set_visible(False)
                        ax4.set_xlim(min_value, max_value)  # Set the same x-axis scale for each plot

                        plt.tight_layout()  # Adjust the layout to prevent overlap
                        plt.show()

                        ax4.legend(loc='right', bbox_to_anchor=(0.2, -1.5), fontsize="6", frameon=False)
                        plt.show()

                        st.pyplot(fig)

                        ##########################################################################################################################
                        ##########################################################################################################################
                        ##########################################################################################################################
if choose == "Compare Jogadores":

    jogador_1 = st.selectbox("Escolha o primeiro Jogador!", options=prospectos, index=None, placeholder="Escolha o primeiro Jogador!")

    if jogador_1:
        #Determinar Equipe
        df20 = df13.loc[(df13['Atleta']==jogador_1)]
        equipes = df20['Equipe Janela Análise'].unique()
        equipe_1 = st.selectbox("Escolha o Clube do primeiro Jogador!", options=equipes)
        if equipe_1:
            #Determinar a Posição
            df21 = df20.loc[(df20['Equipe Janela Análise']==equipe_1)]
            posições = df21['Posição'].unique()
            posição_1 = st.selectbox("Escolha a Posição do primeiro Jogador!", options=posições)

    jogador_2 = st.selectbox("Escolha o segundo Jogador!", options=prospectos, index=None, placeholder="Escolha o segundo Jogador!")

    if jogador_2:
        #Determinar Equipe
        df20 = df13.loc[(df13['Atleta']==jogador_2)]
        equipes = df20['Equipe Janela Análise'].unique()
        equipe_2 = st.selectbox("Escolha o Clube do segundo Jogador!", options=equipes)
        if (equipe_2):
            #Determinar a Posição
            df21 = df20.loc[(df20['Equipe Janela Análise']==equipe_2)]
            posições = df21['Posição'].unique()
            posição_2 = st.selectbox("Escolha a Posição do segundo Jogador!", options=posições)

        if (posição_1 == posição_2 == ("LATERAL")):
            
            #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
            st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos dos Jogadores em 2023</h3>", unsafe_allow_html=True)
            Lateral_Charts = pd.read_csv('Lateral.csv')

            Lateral_Charts_1 = Lateral_Charts[(Lateral_Charts['Atleta']==jogador_1)&(Lateral_Charts['Equipe Janela Análise']==equipe_1)|(Lateral_Charts['Atleta']==jogador_2)&(Lateral_Charts['Equipe Janela Análise']==equipe_2)].reset_index()

            columns_to_rename = {
                        col: col.replace('_percentil', '') for col in Lateral_Charts.columns if '_percentil' in col
                    }
            # Renaming the columns in the DataFrame
            Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
            #Collecting data to plot
            metrics = Lateral_Charts_1.iloc[:, np.r_[1, 11:17]].reset_index(drop=True)

            ## parameter names
            params = list(metrics.columns[1:])

            ## range values
            ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
            a_values = []
            b_values = []

            # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
            for i, atleta in enumerate(metrics['Atleta']):
                if atleta == jogador_1:
                    a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                elif atleta == jogador_2:
                    b_values = metrics.iloc[i, 1:].tolist()

            values = [a_values, b_values]

            ## title values
            title = dict(
                title_name=jogador_1,
                title_color = '#B6282F',
                subtitle_name= equipe_1,
                subtitle_color='#B6282F',
                title_name_2=jogador_2,
                title_color_2 = '#344D94',
                subtitle_name_2=equipe_2,
                subtitle_color_2='#344D94',
                title_fontsize=20,
                subtitle_fontsize=18,
            )            

            ## endnote 
            endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

            ## instantiate object
            #radar = Radar()

            radar=Radar(fontfamily='Cursive', range_fontsize=8)
            fig, ax = radar.plot_radar(
                ranges=ranges,
                params=params,
                values=values,
                radar_color=['#B6282F', '#344D94'],
                dpi=600,
                alphas=[.8, .6],
                title=title,
                endnote=endnote,
                compare=True
            )
            st.pyplot(fig)

####################################################################################################
            
            atributos = atributos_lateral_2['LATERAL']
            atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
            if atributo == ("Participação"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Participação_Lateral_Charts = pd.read_csv('Participação.csv')
                Participação_Lateral_Charts_1 = Participação_Lateral_Charts[((Participação_Lateral_Charts['Atleta']==jogador_1)&
                                                                                    (Participação_Lateral_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Participação_Lateral_Charts['Posição']==posição_1))|
                                                                                    ((Participação_Lateral_Charts['Atleta']==jogador_2)&
                                                                                    (Participação_Lateral_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Participação_Lateral_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Participação_Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Participação_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Participação_Lateral_Charts_1.iloc[:, np.r_[0, 8:12]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Defesa"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Defesa_Lateral_Charts = pd.read_csv('defesa.csv')
                Defesa_Lateral_Charts_1 = Defesa_Lateral_Charts[((Defesa_Lateral_Charts['Atleta']==jogador_1)&
                                                                                    (Defesa_Lateral_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Defesa_Lateral_Charts['Posição']==posição_1))|
                                                                                    ((Defesa_Lateral_Charts['Atleta']==jogador_2)&
                                                                                    (Defesa_Lateral_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Defesa_Lateral_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Defesa_Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Defesa_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Defesa_Lateral_Charts_1.iloc[:, np.r_[0, 10:16]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Apoio"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Apoio_Lateral_Charts = pd.read_csv('apoio.csv')
                Apoio_Lateral_Charts_1 = Apoio_Lateral_Charts[((Apoio_Lateral_Charts['Atleta']==jogador_1)&
                                                                                    (Apoio_Lateral_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Apoio_Lateral_Charts['Posição']==posição_1))|
                                                                                    ((Apoio_Lateral_Charts['Atleta']==jogador_2)&
                                                                                    (Apoio_Lateral_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Apoio_Lateral_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Apoio_Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Apoio_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Apoio_Lateral_Charts_1.iloc[:, np.r_[0, 11:17]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Ataque"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Ataque_Lateral_Charts = pd.read_csv('ataque.csv')
                Ataque_Lateral_Charts_1 = Ataque_Lateral_Charts[((Ataque_Lateral_Charts['Atleta']==jogador_1)&
                                                                                    (Ataque_Lateral_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Ataque_Lateral_Charts['Posição']==posição_1))|
                                                                                    ((Ataque_Lateral_Charts['Atleta']==jogador_2)&
                                                                                    (Ataque_Lateral_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Ataque_Lateral_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Ataque_Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Ataque_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Ataque_Lateral_Charts_1.iloc[:, np.r_[0, 9:14]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Último passe"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Último_passe_Lateral_Charts = pd.read_csv('último_passe.csv')
                Último_passe_Lateral_Charts_1 = Último_passe_Lateral_Charts[((Último_passe_Lateral_Charts['Atleta']==jogador_1)&
                                                                                    (Último_passe_Lateral_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Último_passe_Lateral_Charts['Posição']==posição_1))|
                                                                                    ((Último_passe_Lateral_Charts['Atleta']==jogador_2)&
                                                                                    (Último_passe_Lateral_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Último_passe_Lateral_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Último_passe_Lateral_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Último_passe_Lateral_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Último_passe_Lateral_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
####################################################################################################

        elif (posição_1 == posição_2 == ("ZAGUEIRO")):
            
            #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
            st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos dos Jogadores em 2023</h3>", unsafe_allow_html=True)
            Zagueiro_Charts = pd.read_csv('Zagueiro.csv')

            Zagueiro_Charts_1 = Zagueiro_Charts[(Zagueiro_Charts['Atleta']==jogador_1)&(Zagueiro_Charts['Equipe Janela Análise']==equipe_1)|(Zagueiro_Charts['Atleta']==jogador_2)&(Zagueiro_Charts['Equipe Janela Análise']==equipe_2)].reset_index()

            columns_to_rename = {
                        col: col.replace('_percentil', '') for col in Zagueiro_Charts.columns if '_percentil' in col
                    }
            # Renaming the columns in the DataFrame
            Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
            #Collecting data to plot
            metrics = Zagueiro_Charts_1.iloc[:, np.r_[1, 8:11]].reset_index(drop=True)

            ## parameter names
            params = list(metrics.columns[1:])

            ## range values
            ranges = [(0, 100), (0, 100), (0, 100)]
            a_values = []
            b_values = []

            # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
            for i, atleta in enumerate(metrics['Atleta']):
                if atleta == jogador_1:
                    a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                elif atleta == jogador_2:
                    b_values = metrics.iloc[i, 1:].tolist()

            values = [a_values, b_values]

            ## title values
            title = dict(
                title_name=jogador_1,
                title_color = '#B6282F',
                subtitle_name= equipe_1,
                subtitle_color='#B6282F',
                title_name_2=jogador_2,
                title_color_2 = '#344D94',
                subtitle_name_2=equipe_2,
                subtitle_color_2='#344D94',
                title_fontsize=20,
                subtitle_fontsize=18,
            )            

            ## endnote 
            endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

            ## instantiate object
            #radar = Radar()

            radar=Radar(fontfamily='Cursive', range_fontsize=8)
            fig, ax = radar.plot_radar(
                ranges=ranges,
                params=params,
                values=values,
                radar_color=['#B6282F', '#344D94'],
                dpi=600,
                alphas=[.8, .6],
                title=title,
                endnote=endnote,
                compare=True
            )
            st.pyplot(fig)

####################################################################################################
            
            atributos = atributos_zagueiro['ZAGUEIRO']
            atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
            if atributo == ("Participação"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Participação_Zagueiro_Charts = pd.read_csv('Participação.csv')
                Participação_Zagueiro_Charts_1 = Participação_Zagueiro_Charts[((Participação_Zagueiro_Charts['Atleta']==jogador_1)&
                                                                                    (Participação_Zagueiro_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Participação_Zagueiro_Charts['Posição']==posição_1))|
                                                                                    ((Participação_Zagueiro_Charts['Atleta']==jogador_2)&
                                                                                    (Participação_Zagueiro_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Participação_Zagueiro_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Participação_Zagueiro_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Participação_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Participação_Zagueiro_Charts_1.iloc[:, np.r_[0, 8:12]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Defesa"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Defesa_Zagueiro_Charts = pd.read_csv('defesa.csv')
                Defesa_Zagueiro_Charts_1 = Defesa_Zagueiro_Charts[((Defesa_Zagueiro_Charts['Atleta']==jogador_1)&
                                                                                    (Defesa_Zagueiro_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Defesa_Zagueiro_Charts['Posição']==posição_1))|
                                                                                    ((Defesa_Zagueiro_Charts['Atleta']==jogador_2)&
                                                                                    (Defesa_Zagueiro_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Defesa_Zagueiro_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Defesa_Zagueiro_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Defesa_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Defesa_Zagueiro_Charts_1.iloc[:, np.r_[0, 10:16]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Construção"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Construção_Zagueiro_Charts = pd.read_csv('construção.csv')
                Construção_Zagueiro_Charts_1 = Construção_Zagueiro_Charts[((Construção_Zagueiro_Charts['Atleta']==jogador_1)&
                                                                                    (Construção_Zagueiro_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Construção_Zagueiro_Charts['Posição']==posição_1))|
                                                                                    ((Construção_Zagueiro_Charts['Atleta']==jogador_2)&
                                                                                    (Construção_Zagueiro_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Construção_Zagueiro_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Construção_Zagueiro_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Construção_Zagueiro_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Construção_Zagueiro_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
####################################################################################################

        elif (posição_1 == posição_2 == ("MEIO-CAMPO")):
            
            #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
            st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos dos Jogadores em 2023</h3>", unsafe_allow_html=True)
            Meio_Campo_Charts = pd.read_csv('Meio_Campo.csv')

            Meio_Campo_Charts_1 = Meio_Campo_Charts[(Meio_Campo_Charts['Atleta']==jogador_1)&(Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)|(Meio_Campo_Charts['Atleta']==jogador_2)&(Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)].reset_index()

            columns_to_rename = {
                        col: col.replace('_percentil', '') for col in Meio_Campo_Charts.columns if '_percentil' in col
                    }
            # Renaming the columns in the DataFrame
            Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
            #Collecting data to plot
            metrics = Meio_Campo_Charts_1.iloc[:, np.r_[1, 12:19]].reset_index(drop=True)

            ## parameter names
            params = list(metrics.columns[1:])

            ## range values
            ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
            a_values = []
            b_values = []

            # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
            for i, atleta in enumerate(metrics['Atleta']):
                if atleta == jogador_1:
                    a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                elif atleta == jogador_2:
                    b_values = metrics.iloc[i, 1:].tolist()

            values = [a_values, b_values]

            ## title values
            title = dict(
                title_name=jogador_1,
                title_color = '#B6282F',
                subtitle_name= equipe_1,
                subtitle_color='#B6282F',
                title_name_2=jogador_2,
                title_color_2 = '#344D94',
                subtitle_name_2=equipe_2,
                subtitle_color_2='#344D94',
                title_fontsize=20,
                subtitle_fontsize=18,
            )            

            ## endnote 
            endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

            ## instantiate object
            #radar = Radar()

            radar=Radar(fontfamily='Cursive', range_fontsize=8)
            fig, ax = radar.plot_radar(
                ranges=ranges,
                params=params,
                values=values,
                radar_color=['#B6282F', '#344D94'],
                dpi=600,
                alphas=[.8, .6],
                title=title,
                endnote=endnote,
                compare=True
            )
            st.pyplot(fig)

####################################################################################################
            
            atributos = atributos_meio_campo_2['MEIO-CAMPO']
            atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
            if atributo == ("Participação"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Participação_Meio_Campo_Charts = pd.read_csv('Participação.csv')
                Participação_Meio_Campo_Charts_1 = Participação_Meio_Campo_Charts[((Participação_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Participação_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Participação_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Participação_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Participação_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Participação_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Participação_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Participação_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Participação_Meio_Campo_Charts_1.iloc[:, np.r_[0, 8:12]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Defesa"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Defesa_Meio_Campo_Charts = pd.read_csv('defesa.csv')
                Defesa_Meio_Campo_Charts_1 = Defesa_Meio_Campo_Charts[((Defesa_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Defesa_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Defesa_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Defesa_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Defesa_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Defesa_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Defesa_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Defesa_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Defesa_Meio_Campo_Charts_1.iloc[:, np.r_[0, 10:16]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Construção"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Construção_Meio_Campo_Charts = pd.read_csv('construção.csv')
                Construção_Meio_Campo_Charts_1 = Construção_Meio_Campo_Charts[((Construção_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Construção_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Construção_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Construção_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Construção_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Construção_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Construção_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Construção_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Construção_Meio_Campo_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)


####################################################################################################
            
            elif atributo == ("Apoio"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Apoio_Meio_Campo_Charts = pd.read_csv('apoio.csv')
                Apoio_Meio_Campo_Charts_1 = Apoio_Meio_Campo_Charts[((Apoio_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Apoio_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Apoio_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Apoio_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Apoio_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Apoio_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Apoio_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Apoio_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Apoio_Meio_Campo_Charts_1.iloc[:, np.r_[0, 11:17]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Ataque"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Ataque_Meio_Campo_Charts = pd.read_csv('ataque.csv')
                Ataque_Meio_Campo_Charts_1 = Ataque_Meio_Campo_Charts[((Ataque_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Ataque_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Ataque_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Ataque_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Ataque_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Ataque_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Ataque_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Ataque_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Ataque_Meio_Campo_Charts_1.iloc[:, np.r_[0, 9:14]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Último passe"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Último_passe_Meio_Campo_Charts = pd.read_csv('último_passe.csv')
                Último_passe_Meio_Campo_Charts_1 = Último_passe_Meio_Campo_Charts[((Último_passe_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Último_passe_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Último_passe_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Último_passe_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Último_passe_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Último_passe_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Último_passe_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Último_passe_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Último_passe_Meio_Campo_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Ameaça ofensiva"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Ameaça_ofensiva_Meio_Campo_Charts = pd.read_csv('Ameaça_ofensiva.csv')
                Ameaça_ofensiva_Meio_Campo_Charts_1 = Ameaça_ofensiva_Meio_Campo_Charts[((Ameaça_ofensiva_Meio_Campo_Charts['Atleta']==jogador_1)&
                                                                                    (Ameaça_ofensiva_Meio_Campo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Ameaça_ofensiva_Meio_Campo_Charts['Posição']==posição_1))|
                                                                                    ((Ameaça_ofensiva_Meio_Campo_Charts['Atleta']==jogador_2)&
                                                                                    (Ameaça_ofensiva_Meio_Campo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Ameaça_ofensiva_Meio_Campo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Ameaça_ofensiva_Meio_Campo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Ameaça_ofensiva_Meio_Campo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Ameaça_ofensiva_Meio_Campo_Charts_1.iloc[:, np.r_[0, 8:11]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
####################################################################################################

        elif (posição_1 == posição_2 == ("EXTREMO")):
            
            #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
            st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos dos Jogadores em 2023</h3>", unsafe_allow_html=True)
            Extremo_Charts = pd.read_csv('Extremo.csv')

            Extremo_Charts_1 = Extremo_Charts[(Extremo_Charts['Atleta']==jogador_1)&(Extremo_Charts['Equipe Janela Análise']==equipe_1)|(Extremo_Charts['Atleta']==jogador_2)&(Extremo_Charts['Equipe Janela Análise']==equipe_2)].reset_index()

            columns_to_rename = {
                        col: col.replace('_percentil', '') for col in Extremo_Charts.columns if '_percentil' in col
                    }
            # Renaming the columns in the DataFrame
            Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
            #Collecting data to plot
            metrics = Extremo_Charts_1.iloc[:, np.r_[1, 12:19]].reset_index(drop=True)

            ## parameter names
            params = list(metrics.columns[1:])

            ## range values
            ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
            a_values = []
            b_values = []

            # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
            for i, atleta in enumerate(metrics['Atleta']):
                if atleta == jogador_1:
                    a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                elif atleta == jogador_2:
                    b_values = metrics.iloc[i, 1:].tolist()

            values = [a_values, b_values]

            ## title values
            title = dict(
                title_name=jogador_1,
                title_color = '#B6282F',
                subtitle_name= equipe_1,
                subtitle_color='#B6282F',
                title_name_2=jogador_2,
                title_color_2 = '#344D94',
                subtitle_name_2=equipe_2,
                subtitle_color_2='#344D94',
                title_fontsize=20,
                subtitle_fontsize=18,
            )            

            ## endnote 
            endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

            ## instantiate object
            #radar = Radar()

            radar=Radar(fontfamily='Cursive', range_fontsize=8)
            fig, ax = radar.plot_radar(
                ranges=ranges,
                params=params,
                values=values,
                radar_color=['#B6282F', '#344D94'],
                dpi=600,
                alphas=[.8, .6],
                title=title,
                endnote=endnote,
                compare=True
            )
            st.pyplot(fig)

####################################################################################################
            
            atributos = atributos_extremo_2['EXTREMO']
            atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
            if atributo == ("Participação"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Participação_Extremo_Charts = pd.read_csv('Participação.csv')
                Participação_Extremo_Charts_1 = Participação_Extremo_Charts[((Participação_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Participação_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Participação_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Participação_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Participação_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Participação_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Participação_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Participação_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Participação_Extremo_Charts_1.iloc[:, np.r_[0, 8:12]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Recomposição"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Recomposição_Extremo_Charts = pd.read_csv('recomposição.csv')
                Recomposição_Extremo_Charts_1 = Recomposição_Extremo_Charts[((Recomposição_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Recomposição_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Recomposição_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Recomposição_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Recomposição_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Recomposição_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Recomposição_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Recomposição_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Recomposição_Extremo_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Arranque"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Arranque_Extremo_Charts = pd.read_csv('arranque.csv')
                Arranque_Extremo_Charts_1 = Arranque_Extremo_Charts[((Arranque_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Arranque_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Arranque_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Arranque_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Arranque_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Arranque_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Arranque_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Arranque_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Arranque_Extremo_Charts_1.iloc[:, np.r_[0, 8:11]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Ataque"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Ataque_Extremo_Charts = pd.read_csv('ataque.csv')
                Ataque_Extremo_Charts_1 = Ataque_Extremo_Charts[((Ataque_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Ataque_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Ataque_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Ataque_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Ataque_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Ataque_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Ataque_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Ataque_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Ataque_Extremo_Charts_1.iloc[:, np.r_[0, 9:14]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Último passe"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Último_passe_Extremo_Charts = pd.read_csv('último_passe.csv')
                Último_passe_Extremo_Charts_1 = Último_passe_Extremo_Charts[((Último_passe_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Último_passe_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Último_passe_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Último_passe_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Último_passe_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Último_passe_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Último_passe_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Último_passe_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Último_passe_Extremo_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Finalização"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Finalização_Extremo_Charts = pd.read_csv('finalização.csv')
                Finalização_Extremo_Charts_1 = Finalização_Extremo_Charts[((Finalização_Extremo_Charts['Atleta']==jogador_1)&
                                                                                    (Finalização_Extremo_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Finalização_Extremo_Charts['Posição']==posição_1))|
                                                                                    ((Finalização_Extremo_Charts['Atleta']==jogador_2)&
                                                                                    (Finalização_Extremo_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Finalização_Extremo_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Finalização_Extremo_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Finalização_Extremo_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Finalização_Extremo_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
####################################################################################################

        elif (posição_1 == posição_2 == ("ATACANTE")):
            
            #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
            st.markdown("<h3 style='text-align: center; color: blue; '>Percentis dos Atributos dos Jogadores em 2023</h3>", unsafe_allow_html=True)
            Atacante_Charts = pd.read_csv('Atacante.csv')

            Atacante_Charts_1 = Atacante_Charts[(Atacante_Charts['Atleta']==jogador_1)&(Atacante_Charts['Equipe Janela Análise']==equipe_1)|(Atacante_Charts['Atleta']==jogador_2)&(Atacante_Charts['Equipe Janela Análise']==equipe_2)].reset_index()

            columns_to_rename = {
                        col: col.replace('_percentil', '') for col in Atacante_Charts.columns if '_percentil' in col
                    }
            # Renaming the columns in the DataFrame
            Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
            #Collecting data to plot
            metrics = Atacante_Charts_1.iloc[:, np.r_[1, 14:23]].reset_index(drop=True)

            ## parameter names
            params = list(metrics.columns[1:])

            ## range values
            ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
            a_values = []
            b_values = []

            # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
            for i, atleta in enumerate(metrics['Atleta']):
                if atleta == jogador_1:
                    a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                elif atleta == jogador_2:
                    b_values = metrics.iloc[i, 1:].tolist()

            values = [a_values, b_values]

            ## title values
            title = dict(
                title_name=jogador_1,
                title_color = '#B6282F',
                subtitle_name= equipe_1,
                subtitle_color='#B6282F',
                title_name_2=jogador_2,
                title_color_2 = '#344D94',
                subtitle_name_2=equipe_2,
                subtitle_color_2='#344D94',
                title_fontsize=20,
                subtitle_fontsize=18,
            )            

            ## endnote 
            endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

            ## instantiate object
            #radar = Radar()

            radar=Radar(fontfamily='Cursive', range_fontsize=8)
            fig, ax = radar.plot_radar(
                ranges=ranges,
                params=params,
                values=values,
                radar_color=['#B6282F', '#344D94'],
                dpi=600,
                alphas=[.8, .6],
                title=title,
                endnote=endnote,
                compare=True
            )
            st.pyplot(fig)

####################################################################################################
            
            atributos = atributos_atacante_2['ATACANTE']
            atributo = st.selectbox("Se quiser aprofundar, escolha o Atributo", options=atributos, index = None)
            if atributo == ("Participação"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Participação_Atacante_Charts = pd.read_csv('Participação.csv')
                Participação_Atacante_Charts_1 = Participação_Atacante_Charts[((Participação_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Participação_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Participação_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Participação_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Participação_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Participação_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Participação_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Participação_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Participação_Atacante_Charts_1.iloc[:, np.r_[0, 8:12]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Recomposição"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Recomposição_Atacante_Charts = pd.read_csv('recomposição.csv')
                Recomposição_Atacante_Charts_1 = Recomposição_Atacante_Charts[((Recomposição_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Recomposição_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Recomposição_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Recomposição_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Recomposição_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Recomposição_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Recomposição_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Recomposição_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Recomposição_Atacante_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################

            elif atributo == ("Retenção de posse"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Retenção_Posse_Atacante_Charts = pd.read_csv('retenção_posse.csv')
                Retenção_Posse_Atacante_Charts_1 = Retenção_Posse_Atacante_Charts[((Retenção_Posse_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Retenção_Posse_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Retenção_Posse_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Retenção_Posse_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Retenção_Posse_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Retenção_Posse_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Retenção_Posse_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Retenção_Posse_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Retenção_Posse_Atacante_Charts_1.iloc[:, np.r_[0, 10:15]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################

            elif atributo == ("Arranque"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Arranque_Atacante_Charts = pd.read_csv('arranque.csv')
                Arranque_Atacante_Charts_1 = Arranque_Atacante_Charts[((Arranque_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Arranque_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Arranque_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Arranque_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Arranque_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Arranque_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Arranque_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Arranque_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Arranque_Atacante_Charts_1.iloc[:, np.r_[0, 8:11]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Bola aérea"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Bola_Aérea_Atacante_Charts = pd.read_csv('bola_aérea.csv')
                Bola_Aérea_Atacante_Charts_1 = Bola_Aérea_Atacante_Charts[((Bola_Aérea_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Bola_Aérea_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Bola_Aérea_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Bola_Aérea_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Bola_Aérea_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Bola_Aérea_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Bola_Aérea_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Bola_Aérea_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Bola_Aérea_Atacante_Charts_1.iloc[:, np.r_[0, 8:11]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Último passe"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Último_passe_Atacante_Charts = pd.read_csv('último_passe.csv')
                Último_passe_Atacante_Charts_1 = Último_passe_Atacante_Charts[((Último_passe_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Último_passe_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Último_passe_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Último_passe_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Último_passe_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Último_passe_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Último_passe_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Último_passe_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Último_passe_Atacante_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Finalização"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Finalização_Atacante_Charts = pd.read_csv('finalização.csv')
                Finalização_Atacante_Charts_1 = Finalização_Atacante_Charts[((Finalização_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Finalização_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Finalização_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Finalização_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Finalização_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Finalização_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Finalização_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Finalização_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Finalização_Atacante_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)

####################################################################################################
            
            elif atributo == ("Oportunismo"):
                
                #Plotar Primeiro Gráfico - Radar de Percentis do Jogador na liga:
                st.markdown("<h3 style='text-align: center; color: blue; '>Percentis das Métricas Associadas ao Atributo Escolhido em 2023</h3>", unsafe_allow_html=True)
                Oportunismo_Atacante_Charts = pd.read_csv('oportunismo.csv')
                Oportunismo_Atacante_Charts_1 = Oportunismo_Atacante_Charts[((Oportunismo_Atacante_Charts['Atleta']==jogador_1)&
                                                                                    (Oportunismo_Atacante_Charts['Equipe Janela Análise']==equipe_1)&
                                                                                    (Oportunismo_Atacante_Charts['Posição']==posição_1))|
                                                                                    ((Oportunismo_Atacante_Charts['Atleta']==jogador_2)&
                                                                                    (Oportunismo_Atacante_Charts['Equipe Janela Análise']==equipe_2)&
                                                                                    (Oportunismo_Atacante_Charts['Posição']==posição_2))]

                columns_to_rename = {
                    col: col.replace('_percentil', '') for col in Oportunismo_Atacante_Charts.columns if '_percentil' in col
                }
                # Renaming the columns in the DataFrame
                Oportunismo_Atacante_Charts_1.rename(columns=columns_to_rename, inplace=True)
                #Collecting data to plot
                metrics = Oportunismo_Atacante_Charts_1.iloc[:, np.r_[0, 9:13]].reset_index(drop=True)
                ## parameter names
                params = list(metrics.columns[1:])

                ## range values
                ranges = [(0, 100), (0, 100), (0, 100), (0, 100)]
                a_values = []
                b_values = []

                # Check each entry in 'Atleta' column to find match for jogador_1 and jogador_2
                for i, atleta in enumerate(metrics['Atleta']):
                    if atleta == jogador_1:
                        a_values = metrics.iloc[i, 1:].tolist()  # Skip 'Atleta' column
                    elif atleta == jogador_2:
                        b_values = metrics.iloc[i, 1:].tolist()

                values = [a_values, b_values]

                ## title values
                title = dict(
                    title_name=jogador_1,
                    title_color = '#B6282F',
                    subtitle_name= equipe_1,
                    subtitle_color='#B6282F',
                    title_name_2=jogador_2,
                    title_color_2 = '#344D94',
                    subtitle_name_2=equipe_2,
                    subtitle_color_2='#344D94',
                    title_fontsize=20,
                    subtitle_fontsize=18,
                )            

                ## endnote 
                endnote = "Gráfico: @JAmerico1898\nTodos os dados em percentil"

                ## instantiate object
                #radar = Radar()

                radar=Radar(fontfamily='Cursive', range_fontsize=8)
                fig, ax = radar.plot_radar(
                    ranges=ranges,
                    params=params,
                    values=values,
                    radar_color=['#B6282F', '#344D94'],
                    dpi=600,
                    alphas=[.8, .6],
                    title=title,
                    endnote=endnote,
                    compare=True
                )
                st.pyplot(fig)
