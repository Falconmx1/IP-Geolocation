# 📍 IP Geolocation

> Herramienta CLI para geolocalizar direcciones IP públicas usando APIs gratuitas.

## 🚀 Características
- Geolocalización de IPs (país, ciudad, región, lat/lon)
- Información de ISP y organización
- Zona horaria y código postal (según API)
- Soporte para IPs individuales o lotes (archivo CSV/TXT)
- Modo silencioso para scripts
- Exportación a JSON/CSV

## 📊 Exportar resultados

```bash
# Exportar a CSV
python ip_geolocation.py 8.8.8.8 --output resultados.csv

# Exportar a JSON
python ip_geolocation.py --file ips.txt --output datos.json

# Formato automático según extensión
python ip_geolocation.py --myip --output mi_ubicacion.csv


## 📦 Instalación

```bash
git clone https://github.com/Falconmx1/IP-Geolocation.git
cd IP-Geolocation
pip install -r requirements.txt
