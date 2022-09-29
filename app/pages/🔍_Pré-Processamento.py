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
    elif filter_type == 'Remover canal de cor':
        return st.selectbox('Selecione um canal de cor para remover', ['Green', 'Blue', 'Red'], key=index)
    elif filter_type == 'Saturar canal de cor':
        color = st.selectbox('Selecione um canal de cor para saturar', [
                             'Green', 'Blue', 'Red'], key=index)
        itsity = st.slider('Itensidade', min_value=-4.0,
                           max_value=4.0, value=2.0, key=index+55)
        return [color, itsity]
    elif filter_type == 'Negativa':
        return 0
    elif filter_type == 'Equalizar':
        return 0
    elif filter_type == 'Limiarizar':
        return 0
    elif filter_type == 'Filtro da Média' or filter_type == 'Filtro da Mediana' or filter_type == 'Filtro Gaussiano':
        return st.number_input('Selecione o tamanho da Mascara', max_value=15, value=3, min_value=3, key=index)
    elif filter_type == 'Filtro Sobel':
        return st.selectbox('Selecione o tipo', ['Horizontal', 'Vertical'])
    elif filter_type == 'Filtro Laplaciano':
        return 0
    elif filter_type == 'Filtro Butterworth (passa-baixa)':
        n = st.number_input('Selecione n', max_value=3,
                            value=1, min_value=1, key=index)
        cutoff = st.number_input(
            'Selecione o tamanho da Mascara', max_value=0.5, value=0.05, min_value=0.05, key=index+55)
        return [n, cutoff]
    elif filter_type == 'Filtro Butterworth (passa-alta)':
        n = st.number_input('Selecione n', max_value=15,
                            value=3, min_value=3, key=index)
        cutoff = st.number_input(
            'Selecione o tamanho da Mascara', max_value=15, value=3, min_value=3, key=index+55)
        return [n, cutoff]


def apply_filters(filters_list, parameters_list, img_input):
    img_proc = img_input.copy()
    for i in range(len(filters_list)):
        filter = filters_list[i]
        st.write(filter)
        if filter == 'Tornar Cinza':
            img_proc = ig.to_gray(img_proc)
        if filter == 'Remover canal de cor':
            img_proc = ig.remove_channel(img_proc, parameters_list[i])
        if filter == 'Saturar canal de cor':
            parameters = parameters_list[i]
            img_proc = ig.soak_channel(img_proc, parameters[0], parameters[1])
        if filter == 'Negativa':
            img_proc = ig.to_negative(img_proc)
        if filter == 'Limiarizar':
            img_proc = ig.filter_by_thresholding(img_proc)
        if filter == 'Equalizar':
            img_proc = ig.hist_equalize(img_proc)
        if filter == 'Filtro da Média':
            img_proc = ig.filter_by_mean_blur(img_proc, parameters_list[i])
        if filter == 'Filtro Sobel':
            img_proc = ig.filter_by_sobel(img_proc, parameters_list[i])
        if filter == 'Filtro Laplaciano':
            img_proc = ig.filter_by_laplacian(img_proc)
        if filter == 'Filtro Butterworth (passa-baixa)':
            parameters = parameters_list[i]
            img_proc = ig.filter_by_butterworth_low(
                img_proc, parameters[0], parameters[1])
        if filter == 'Filtro Butterworth (passa-alta)':
            parameters = parameters_list[i]
            img_proc = ig.filter_by_butterworth_high(
                img_proc, parameters[0], parameters[1])
        st.image(img_proc, clamp=True)


filter_options_list = ['Tornar Cinza', 'Remover canal de cor', 'Negativa', 'Limiarizar', 'Saturar canal de cor', 'Equalizar', 'Filtro da Média', 'Filtro da Mediana', 'Filtro Gaussiano',
                       'Filtro Sobel', 'Filtro Laplaciano', 'Filtro Butterworth (passa-baixa)', 'Filtro Butterworth (passa-alta)']
filters = []
filters_parameters = []

img_file = st.file_uploader('Selecione uma imagem', type=['png', 'jpg'])
if img_file != None:
    img = np.array(Image.open(img_file))
    st.write('Imagem original')
    st.image(img)

filter_counter = st.number_input(
    'Selecione a quantidade de filtros', max_value=10, min_value=1, value=1, key=55)

for i in range(filter_counter):
    filter_counter += 1
    with st.expander('Filtro ' + str(i+1), expanded=True):
        filter = st.selectbox('Selecione um filtro',
                              filter_options_list, key=i)
        filter_parameter = filter_parameter_builder(filter, i)
    filters_parameters.append(filter_parameter)
    filters.append(filter)

if img_file != None:
    if st.button('Aplicar filtros'):
        apply_filters(
            filters, filters_parameters, np.array(Image.open(img_file)))
