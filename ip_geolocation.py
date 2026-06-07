#!/usr/bin/env python3
"""
📍 IP Geolocation - Herramienta CLI para geolocalizar IPs públicas
Autor: Falconmx1
Licencia: MIT
"""

import argparse
import json
import sys
import requests
from colorama import init, Fore, Style

init(autoreset=True)

def geolocate_ip(ip_address):
    """Obtiene geolocalización de una IP usando ip-api.com (gratis, sin key)"""
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon,isp,org,timezone"
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
