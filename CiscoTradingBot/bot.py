from tradingview_ta import TA_Handler, Interval
import pandas as pd
import matplotlib.pyplot as plt
from colorama import init, Fore, Back, Style
import time
import sys
import os

# Inicializar colorama
init(autoreset=True)

# Configuración de monedas
MONEDAS = {
    '1': {'nombre': 'Ethereum', 'symbol': 'ETHUSDT'},
    '2': {'nombre': 'Pepe', 'symbol': 'PEPEUSDT'},
    '3': {'nombre': 'Solana', 'symbol': 'SOLUSDT'},
    '4': {'nombre': 'Bitcoin', 'symbol': 'BTCUSDT'}
}

# Banner mejorado
banner = f"""
{Fore.LIGHTMAGENTA_EX}╔{'═'*60}╗
║{Back.LIGHTMAGENTA_EX}{Fore.WHITE}{Style.BRIGHT}{' CiscoTradingBot '.center(58)}{Style.RESET_ALL}{Fore.LIGHTMAGENTA_EX}║
║{Back.LIGHTMAGENTA_EX}{Fore.WHITE}{Style.BRIGHT}{' Creado por Erick Cedeno '.center(58)}{Style.RESET_ALL}{Fore.LIGHTMAGENTA_EX}║
╚{'═'*60}╝
{Style.RESET_ALL}"""

# Función para selección de moneda
def seleccionar_moneda():
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            print(f"\n{Fore.LIGHTMAGENTA_EX}╔{'═'*60}╗")
            print(f"║{Fore.WHITE}{Back.LIGHTMAGENTA_EX}{' SELECCIÓN DE CRIPTOMONEDA '.center(58)}{Style.RESET_ALL}{Fore.LIGHTMAGENTA_EX}║")
            print(f"║{Fore.WHITE} 1. Ethereum (ETH) {'':<40}║")
            print(f"║{Fore.WHITE} 2. Pepe (PEPE) {'':<43}║")
            print(f"║{Fore.WHITE} 3. Solana (SOL) {'':<43}║")
            print(f"║{Fore.WHITE} 4. Bitcoin (BTC) {'':<42}║")
            print(f"╚{'═'*60}╝")
            
            opcion = input(f"\n{Fore.LIGHTMAGENTA_EX}👉 Seleccione una moneda (1-4) o Q para salir: ").strip().lower()
            
            if opcion == 'q':
                return None
            if opcion in MONEDAS:
                return MONEDAS[opcion]
            
            raise ValueError
            
        except ValueError:
            print(f"\n{Fore.RED}❌ Error: Selección inválida! Por favor ingrese 1-4 o Q{Style.RESET_ALL}")
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}🚨 Operación cancelada{Style.RESET_ALL}")
            return None

# Función para loader animado con manejo de interrupciones
def mostrar_loader(duracion=3):
    try:
        print(f"\n{Fore.LIGHTMAGENTA_EX}🔃 Cargando análisis...{Style.RESET_ALL}")
        start_time = time.time()
        frames = ["🌑 ", "🌒 ", "🌓 ", "🌔 ", "🌕 ", "🌖 ", "🌗 ", "🌘 "]
        while (time.time() - start_time) < duracion:
            for frame in frames:
                if (time.time() - start_time) >= duracion:
                    break
                sys.stdout.write(f"\r{Fore.LIGHTMAGENTA_EX}{frame} Procesando datos...")
                sys.stdout.flush()
                time.sleep(0.2)
        print("\n")
        return True
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🚨 Carga interrumpida{Style.RESET_ALL}")
        return False

# Función principal de análisis con manejo de errores
def realizar_analisis(moneda):
    try:
        handler = TA_Handler(
            symbol=moneda['symbol'],
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_15_MINUTES
        )

        analysis = handler.get_analysis()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        decimales = 8 if 'PEPE' in moneda['symbol'] else 2
        formato_precio = f"{{:.{decimales}f}}"
        
        indicadores = {
            '📈 Precio Actual': f"{Fore.WHITE}{formato_precio.format(analysis.indicators.get('close'))} {moneda['symbol'][:3]}{Style.RESET_ALL}",
            '📊 RSI': f"{analysis.indicators.get('RSI', 0):.2f}",
            '🌀 RSI Estocástico (K)': f"{analysis.indicators.get('Stoch.RSI.K', 0):.2f}",
            '💹 Volumen': f"{analysis.indicators.get('volume', 0):.2f}",
            '📉 Bandas Bollinger': f"{Fore.WHITE}Superior: {analysis.indicators.get('BB.upper', 0):.2f} | Media: {analysis.indicators.get('SMA20', 0):.2f} | Inferior: {analysis.indicators.get('BB.lower', 0):.2f}",
            '📈 MACD': f"{Fore.WHITE}Valor: {analysis.indicators.get('MACD.macd', 0):.2f} | Señal: {analysis.indicators.get('MACD.signal', 0):.2f}",
            '📊 ADX': f"{analysis.indicators.get('ADX', 0):.2f}",
            '📌 Estocástico': f"{Fore.WHITE}K: {analysis.indicators.get('Stoch.K', 0):.2f} | D: {analysis.indicators.get('Stoch.D', 0):.2f}",
            '📌 CCI (20)': f"{analysis.indicators.get('CCI20', 0):.2f}",
            '📅 EMAs': f"{Fore.WHITE}50: {analysis.indicators.get('EMA50', 0):.2f} | 200: {analysis.indicators.get('EMA200', 0):.2f}",
            '🛑 Soporte': f"{Fore.WHITE}S1: {analysis.indicators.get('Pivot.M.Classic.S1', 0):.2f} | S2: {analysis.indicators.get('Pivot.M.Classic.S2', 0):.2f}",
            '🎯 Resistencia': f"{Fore.WHITE}R1: {analysis.indicators.get('Pivot.M.Classic.R1', 0):.2f} | R2: {analysis.indicators.get('Pivot.M.Classic.R2', 0):.2f}"
        }

        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(f"\n{Fore.LIGHTMAGENTA_EX}▬▬▬▬▬▬▬▬▬▬▬ 💰 {moneda['nombre']} ({moneda['symbol']}) ▬▬▬▬▬▬▬▬▬▬▬{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⏰ Última actualización: {current_time}{Style.RESET_ALL}\n")
        
        for titulo, valor in indicadores.items():
            print(f"{Fore.LIGHTMAGENTA_EX}│ {titulo.ljust(22)} ➜ {valor}")
        
        summary = analysis.summary
        print(f"\n{Back.LIGHTMAGENTA_EX}{Fore.WHITE}{Style.BRIGHT} 📊 RECOMENDACIÓN: {summary['RECOMMENDATION'].upper().ljust(15)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTMAGENTA_EX}🔔 Señales: [{Fore.GREEN}▲ {summary['BUY']} Compra{Fore.LIGHTMAGENTA_EX}] - [{Fore.RED}▼ {summary['SELL']} Venta{Fore.LIGHTMAGENTA_EX}] - [{Fore.WHITE}🔄 {summary['NEUTRAL']} Neutral{Fore.LIGHTMAGENTA_EX}]")
        
        generar_graficos_profesionales(analysis, moneda)
        return True

    except Exception as e:
        print(f"\n{Fore.RED}⚠️ Error en el análisis: {e}{Style.RESET_ALL}")
        return False

# Función para gráficos profesionales
def generar_graficos_profesionales(analysis, moneda):
    try:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial']
        
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(16, 10), facecolor='#1a1a1a')
        fig.suptitle(f"Análisis {moneda['nombre']} ({moneda['symbol']})", 
                    color='white', fontsize=14, y=0.98)
        
        gs = fig.add_gridspec(3, 3)
        
        # Gráfico de tendencias
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot([analysis.indicators.get('EMA50', 0), 
                analysis.indicators.get('EMA200', 0), 
                analysis.indicators.get('close', 0)], 
                marker='o', linestyle='--', linewidth=2)
        ax1.set_title('Tendencias (EMA50 vs EMA200 vs Precio)', color='white', fontsize=12)
        ax1.legend(['EMA50', 'EMA200', 'Precio Actual'], loc='upper left')
        ax1.grid(color='#333333', linestyle='--')
        
        # Gráfico de osciladores
        ax2 = fig.add_subplot(gs[0, 2])
        osciladores = {
            'RSI': analysis.indicators.get('RSI', 0),
            'Stoch RSI': analysis.indicators.get('Stoch.RSI.K', 0),
            'CCI20': analysis.indicators.get('CCI20', 0),
            'ADX': analysis.indicators.get('ADX', 0)
        }
        ax2.bar(osciladores.keys(), osciladores.values(), 
               color=['#ff79c6', '#bd93f9', '#50fa7b', '#8be9fd'])
        ax2.set_ylim(0, 100)
        ax2.set_title('Osciladores Técnicos', color='white', fontsize=12)
        
        # Gráfico MACD
        ax3 = fig.add_subplot(gs[1, :])
        ax3.plot(analysis.indicators.get('MACD.macd', 0), 
                color='#ffb86c', linewidth=2, label='MACD')
        ax3.plot(analysis.indicators.get('MACD.signal', 0), 
                color='#ff5555', linewidth=2, label='Señal')
        ax3.set_title('Análisis MACD', color='white', fontsize=12)
        ax3.legend()
        ax3.grid(color='#333333', linestyle='--')
        
        # Niveles clave
        ax4 = fig.add_subplot(gs[2, :])
        niveles = ['S2', 'S1', 'Precio', 'R1', 'R2']
        valores = [
            analysis.indicators.get('Pivot.M.Classic.S2', 0),
            analysis.indicators.get('Pivot.M.Classic.S1', 0),
            analysis.indicators.get('close', 0),
            analysis.indicators.get('Pivot.M.Classic.R1', 0),
            analysis.indicators.get('Pivot.M.Classic.R2', 0)
        ]
        ax4.plot(niveles, valores, marker='D', markersize=8, 
                color='#bd93f9', linestyle='--', linewidth=2)
        ax4.set_title('Niveles Clave', color='white', fontsize=12)
        ax4.grid(color='#333333', linestyle='--')

        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"\n{Fore.RED}⚠️ Error al generar gráficos: {e}{Style.RESET_ALL}")

# Menú principal mejorado con manejo de errores
def menu_principal():
    moneda_actual = None
    while True:
        try:
            if not moneda_actual:
                moneda_actual = seleccionar_moneda()
                if not moneda_actual:
                    print(f"\n{Fore.YELLOW}👋 Operación cancelada por el usuario{Style.RESET_ALL}")
                    break
                
                if not mostrar_loader():
                    break

            if not realizar_analisis(moneda_actual):
                break

            print(f"\n{Fore.LIGHTMAGENTA_EX}╔{'═'*60}╗")
            print(f"║ {Fore.WHITE}1. 🔄 Actualizar Análisis".ljust(59) + f"{Fore.LIGHTMAGENTA_EX}║")
            print(f"║ {Fore.WHITE}2. 🔄 Cambiar Moneda".ljust(59) + f"{Fore.LIGHTMAGENTA_EX}║")
            print(f"║ {Fore.WHITE}3. 🚪 Salir del Sistema".ljust(59) + f"{Fore.LIGHTMAGENTA_EX}║")
            print(f"╚{'═'*60}╝")
            
            opcion = input(f"\n{Fore.LIGHTMAGENTA_EX}👉 Seleccione una opción (1-3): ").strip()
            
            if opcion == '1':
                print(f"\n{Fore.LIGHTMAGENTA_EX}🔄 Actualizando datos...{Style.RESET_ALL}")
                plt.close('all')
                time.sleep(1)
            elif opcion == '2':
                moneda_actual = None
                plt.close('all')
            elif opcion == '3':
                print(f"\n{Fore.LIGHTMAGENTA_EX}👋 Cerrando CiscoTradingBot... ¡Hasta pronto!{Style.RESET_ALL}")
                break
            else:
                print(f"\n{Fore.RED}❌ Error: Opción no válida!{Style.RESET_ALL}")
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}🚨 Operación cancelada por el usuario{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}⚠️ Error crítico: {e}{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    menu_principal()