import streamlit as st
import cv2
import numpy as np
import pages.util.imgfilters as ig
from PIL import Image

st.set_page_config(
    page_title="Pré-Processamento",
    page_icon="🔍",
)


def filter_parameter_builder(filter_type, index):
    if filter_type == 'Tornar Cinza':
        return 0
    elif filter_type == 'Equalizar':
        return 0
    elif filter_type == 'Filtro da Média' or filter_type == 'Filtro da Mediana' or filter_type == 'Filtro Gaussiano':
        return st.number_input('Selecione o tamanho da Mascara', max_value=15, value=3, min_value=3, key=index)
    elif filter_type == 'Filtro Sobel':
        return st.selectbox('Selecione o tipo', ['Horizontal', 'Vertical', 'Horizontal e Vertical'])
    elif filter_type == 'Filtro Laplaciano':
        return 0
    elif filter_type == 'Filtro Butterworth (passa-baixa)':
        n = st.number_input('Selecione n', max_value=15,
                            value=3, min_value=3, key=index)
        cutoff = st.number_input(
            'Selecione o tamanho da Mascara', max_value=15, value=3, min_value=3, key=index+55)
        return [n, cutoff]
    elif filter_type == 'Filtro Butterworth (passa-alta)':
        n = st.number_input('Selecione n', max_value=15,
                            value=3, min_value=3, key=index)
        cutoff = st.number_input(
            'Selecione o tamanho da Mascara', max_value=15, value=3, min_value=3, key=index+55)
        return [n, cutoff]


def apply_filters(filters_list,parameters_list):
    pass

filter_options_list = ['Tornar Cinza', 'Equalizar', 'Filtro da Média', 'Filtro da Mediana', 'Filtro Gaussiano',
                       'Filtro Sobel', 'Filtro Laplaciano', 'Filtro Butterworth (passa-baixa)', 'Filtro Butterworth (passa-alta)']
filters = []
filters_parameters = []

img_file = st.file_uploader('Selecione uma imagem', type=['png', 'jpg'])
if img_file != None:
    img = np.array(Image.open(img_file))
    st.write('Imagem original')
    st.image(img)

filter_counter = st.number_input(
    'Selecione a quantidade de filtros', max_value=6, min_value=1, value=3, key=55)

for i in range(filter_counter):
    filter_counter += 1
    with st.expander('Filtro ' + str(i+1), expanded=True):
        filter = st.selectbox('Selecione um filtro',
                              filter_options_list, key=i)
        filter_parameter = filter_parameter_builder(filter, i)
    filters_parameters.append(filter_parameter)
    filters.append(filter)

if img_file != None:
    st.button('Aplicar filtros',on_click=apply_filters(filters,filters_parameters))