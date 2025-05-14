import streamlit as st
import ee
import geemap
from google.oauth2 import service_account
import geemap.foliumap as geemap

# 從 Streamlit Secrets 讀取 GEE 服務帳戶金鑰 JSON
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]

# 使用 google-auth 進行 GEE 授權
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 GEE
ee.Initialize(credentials)
###############################################
st.set_page_config(layout="wide")
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")


# 地理區域
point = ee.Geometry.Point([120.5583462887228, 24.081653403304525])

# 擷取 Harmonized Sentinel-2 MSI
image = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(point) \
    .filterDate("2021-01-01", "2022-01-01") \
    .sort('CLOUDY_PIXEL_PERCENTAGE') \
    .first() \
    .select('B.*') \

vis_params = { 'min':100, 'max':3500, 'bands':['B11', 'B8', 'B3']}

Map = geemap.Map()
Map.centerObject(image, 12)
Map.addLayer(image, vis_params, "Sentinel-2")
Map

training001 = image.sample(
    **{
        'region': image.geometry(),
        'scale': 10,
        'numPixels': 10000,
        'seed': 0,
        'geometries': True,
    }
)

Map.addLayer(training001, {}, 'Training samples')
Map

n_clusters = 10
clusterer_KMeans = ee.Clusterer.wekaKMeans(nClusters=n_clusters).train(training001)
result001 = my_image.cluster(clusterer_KMeans)

legend_dict = {
    'zero': '#ab0000',
    'one': '#1c5f2c',
    'two': '#d99282',
    'three': '#466b9f',
    'four': '#ab6c28',
    'five': '#e6b800',
    'six': '#5e3c99',
    'seven': '#7b3294',
    'eight': '#a6cee3',
    'nine': '#b15928'
    }

palette = list(legend_dict.values())
vis_params_001 = {'min': 0, 'max': 9, 'palette': palette}

Map = geemap.Map()
Map.centerObject(result001, 8)
Map.addLayer(result001, vis_params_001, 'Labelled clusters')
Map.add_legend(title='Land Cover Type', legend_dict = legend_dict1, position = 'bottomright')
Map

Map = geemap.Map()

left_layer = geemap.ee_tile_layer(image, vis_params, 'visible light')
right_layer = geemap.ee_tile_layer(result001,vis_params_001 , 'KMeans classified land cover')

Map.centerObject(my_image.geometry(), 9)
Map.split_map(left_layer, right_layer)
Map
