#!/usr/bin/env python3
"""
📍 IP Geolocation - Herramienta CLI para geolocalizar IPs públicas
Autor: Falconmx1
Licencia: MIT
Soporta: JSON y CSV
"""

import argparse
import json
import csv
import sys
import requests
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def geolocate_ip(ip_address):
    """Obtiene geolocalización de una IP usando ip-api.com (gratis, sin key)"""
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon,isp,org,timezone,zip"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'success':
            return data
        else:
            return {'error': data.get('message', 'Error desconocido')}
    except Exception as e:
        return {'error': str(e)}

def get_my_ip():
    """Obtiene tu IP pública actual"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def print_colorized(data, ip):
    """Imprime resultado con colores"""
    if 'error' in data:
        print(f"{Fore.RED}❌ Error con IP {ip}: {data['error']}{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}📍 IP Geolocalizada: {Fore.YELLOW}{ip}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🌍 País: {Fore.WHITE}{data.get('country', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🏙️ Ciudad: {Fore.WHITE}{data.get('city', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🗺️ Región: {Fore.WHITE}{data.get('regionName', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📡 ISP: {Fore.WHITE}{data.get('isp', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🏢 Org: {Fore.WHITE}{data.get('org', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📍 Coordenadas: {Fore.WHITE}{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}⏰ Zona Horaria: {Fore.WHITE}{data.get('timezone', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📮 Código Postal: {Fore.WHITE}{data.get('zip', 'N/A')}{Style.RESET_ALL}")
    print()

def export_to_csv(resultados, filename):
    """Exporta resultados a archivo CSV"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Definir las columnas del CSV
            fieldnames = ['IP', 'País', 'Ciudad', 'Región', 'ISP', 'Organización', 
                         'Latitud', 'Longitud', 'Zona Horaria', 'Código Postal', 'Error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for ip, data in resultados.items():
                if 'error' in data:
                    row = {
                        'IP': ip,
                        'País': 'N/A',
                        'Ciudad': 'N/A',
                        'Región': 'N/A',
                        'ISP': 'N/A',
                        'Organización': 'N/A',
                        'Latitud': 'N/A',
                        'Longitud': 'N/A',
                        'Zona Horaria': 'N/A',
                        'Código Postal': 'N/A',
                        'Error': data['error']
                    }
                else:
                    row = {
                        'IP': ip,
                        'País': data.get('country', 'N/A'),
                        'Ciudad': data.get('city', 'N/A'),
                        'Región': data.get('regionName', 'N/A'),
                        'ISP': data.get('isp', 'N/A'),
                        'Organización': data.get('org', 'N/A'),
                        'Latitud': data.get('lat', 'N/A'),
                        'Longitud': data.get('lon', 'N/A'),
                        'Zona Horaria': data.get('timezone', 'N/A'),
                        'Código Postal': data.get('zip', 'N/A'),
                        'Error': ''
                    }
                writer.writerow(row)
        
        print(f"{Fore.GREEN}✅ CSV exportado exitosamente: {filename}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error exportando a CSV: {str(e)}{Style.RESET_ALL}")
        return False

def export_to_json(resultados, filename):
    """Exporta resultados a archivo JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print(f"{Fore.GREEN}✅ JSON exportado exitosamente: {filename}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error exportando a JSON: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='📍 Geolocaliza direcciones IP públicas',
        epilog='Ejemplos:\n  python ip_geolocation.py 8.8.8.8\n  python ip_geolocation.py --myip --output resultados.csv\n  python ip_geolocation.py --file ips.txt --format csv'
    )
    parser.add_argument('ip', nargs='?', help='Dirección IP a geolocalizar')
    parser.add_argument('--myip', action='store_true', help='Geolocalizar tu propia IP pública')
    parser.add_argument('--file', '-f', help='Archivo con lista de IPs (una por línea)')
    parser.add_argument('--output', '-o', help='Guardar resultados (ej: resultados.json o resultados.csv)')
    parser.add_argument('--format', choices=['json', 'csv', 'auto'], default='auto', 
                       help='Formato de exportación (auto detecta por extensión, json o csv)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo detallado')
    
    args = parser.parse_args()
    
    # Determinar formato de exportación
    output_format = None
    if args.output:
        if args.format == 'auto':
            if args.output.lower().endswith('.csv'):
                output_format = 'csv'
            elif args.output.lower().endswith('.json'):
                output_format = 'json'
            else:
                output_format = 'json'  # Por defecto JSON
                print(f"{Fore.YELLOW}⚠️ Extensión no reconocida, usando JSON por defecto{Style.RESET_ALL}")
        else:
            output_format = args.format
    
    # Caso 1: Usar mi propia IP
    if args.myip:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{Fore.YELLOW}🔍 Tu IP pública es: {my_ip}{Style.RESET_ALL}")
            data = geolocate_ip(my_ip)
            print_colorized(data, my_ip)
            if args.output:
                resultados = {my_ip: data}
                if output_format == 'csv':
                    export_to_csv(resultados, args.output)
                else:
                    export_to_json(resultados, args.output)
        else:
            print(f"{Fore.RED}❌ No se pudo obtener tu IP pública")
        return
    
    # Caso 2: Archivo con múltiples IPs
    if args.file:
        try:
            with open(args.file, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            
            print(f"{Fore.CYAN}📊 Procesando {len(ips)} IPs...{Style.RESET_ALL}")
            resultados = {}
            exitos = 0
            errores = 0
            
            for idx, ip in enumerate(ips, 1):
                if args.verbose:
                    print(f"{Fore.CYAN}[{idx}/{len(ips)}] Procesando {ip}...{Style.RESET_ALL}")
                resultados[ip] = geolocate_ip(ip)
                if 'error' in resultados[ip]:
                    errores += 1
                else:
                    exitos += 1
                if not args.verbose:
                    print_colorized(resultados[ip], ip)
            
            # Resumen
            print(f"\n{Fore.CYAN}📈 Resumen:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Exitosas: {exitos}{Style.RESET_ALL}")
            print(f"{Fore.RED}❌ Errores: {errores}{Style.RESET_ALL}")
            
            if args.output:
                if output_format == 'csv':
                    export_to_csv(resultados, args.output)
                else:
                    export_to_json(resultados, args.output)
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Archivo no encontrado: {args.file}")
        return
    
    # Caso 3: Una sola IP
    if args.ip:
        data = geolocate_ip(args.ip)
        print_colorized(data, args.ip)
        if args.output:
            resultados = {args.ip: data}
            if output_format == 'csv':
                export_to_csv(resultados, args.output)
            else:
                export_to_json(resultados, args.output)
        return
    
    # Si no hay argumentos, mostrar ayuda
    parser.print_help()

if __name__ == "__main__":
    print(f"{Fore.CYAN}📍 IP Geolocation Tool v1.0 - Falconmx1{Style.RESET_ALL}")
    main()
def print_colorized(data, ip):
    """Imprime resultado con colores"""
    if 'error' in data:
        print(f"{Fore.RED}❌ Error con IP {ip}: {data['error']}{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}📍 IP Geolocalizada: {Fore.YELLOW}{ip}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🌍 País: {Fore.WHITE}{data.get('country', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🏙️ Ciudad: {Fore.WHITE}{data.get('city', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🗺️ Región: {Fore.WHITE}{data.get('regionName', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📡 ISP: {Fore.WHITE}{data.get('isp', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🏢 Org: {Fore.WHITE}{data.get('org', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📍 Coordenadas: {Fore.WHITE}{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}⏰ Zona Horaria: {Fore.WHITE}{data.get('timezone', 'N/A')}{Style.RESET_ALL}")
    print()

def main():
    parser = argparse.ArgumentParser(description='📍 Geolocaliza direcciones IP públicas')
    parser.add_argument('ip', nargs='?', help='Dirección IP a geolocalizar')
    parser.add_argument('--myip', action='store_true', help='Geolocalizar tu propia IP pública')
    parser.add_argument('--file', '-f', help='Archivo con lista de IPs (una por línea)')
    parser.add_argument('--output', '-o', help='Guardar resultados en archivo JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo detallado')
    
    args = parser.parse_args()
    
    # Caso 1: Usar mi propia IP
    if args.myip:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{Fore.YELLOW}🔍 Tu IP pública es: {my_ip}{Style.RESET_ALL}")
            data = geolocate_ip(my_ip)
            print_colorized(data, my_ip)
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump({my_ip: data}, f, indent=2)
                print(f"{Fore.GREEN}✅ Resultados guardados en {args.output}")
        else:
            print(f"{Fore.RED}❌ No se pudo obtener tu IP pública")
        return
    
    # Caso 2: Archivo con múltiples IPs
    if args.file:
        try:
            with open(args.file, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            
            resultados = {}
            for ip in ips:
                if args.verbose:
                    print(f"{Fore.CYAN}Procesando {ip}...")
                resultados[ip] = geolocate_ip(ip)
                print_colorized(resultados[ip], ip)
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(resultados, f, indent=2)
                print(f"{Fore.GREEN}✅ Resultados guardados en {args.output}")
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Archivo no encontrado: {args.file}")
        return
    
    # Caso 3: Una sola IP
    if args.ip:
        data = geolocate_ip(args.ip)
        print_colorized(data, args.ip)
        if args.output:
            with open(args.output, 'w') as f:
                json.dump({args.ip: data}, f, indent=2)
            print(f"{Fore.GREEN}✅ Resultados guardados en {args.output}")
        return
    
    # Si no hay argumentos, mostrar ayuda
    parser.print_help()

if __name__ == "__main__":
    main()
