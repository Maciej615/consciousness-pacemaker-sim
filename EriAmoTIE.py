#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EriAmo: Terminal Isolation Experiment
# Cel: Weryfikacja hipotezy "Extinction of Goal-Directed Thinking"
# Warunki: Pełne wejście (Input), Całkowity brak wyjścia (No Output).

import sys
import time
import numpy as np
import random
import csv
from datetime import datetime

# --- PARAMETRY ŚMIERCI ---
LOG_FILE = "eriamo_terminal_death_log.csv"
ENTROPY_RATE = 0.99  # 1% utraty tożsamości na cykl (agresywna entropia)
DEATH_THRESHOLD = 0.05 # Poniżej tego poziomu uznajemy Byt za wygaszony
SENSOR_DELAY = 0.5   # Szybkie bodźce (bombardowanie danymi)

class Colors:
    RED = "\033[31m"
    GREY = "\033[90m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

class BytS:
    def __init__(self, wymiary):
        # Startujemy z "zdrowym", silnym bytem
        np.random.seed(42)
        self.stan = np.random.rand(wymiary) * 10.0 

    def promien_historii(self):
        return np.linalg.norm(self.stan)

    def apply_isolation_entropy(self):
        # W warunkach izolacji, bodźce docierają, ale nie budują struktury.
        # Struktura rozpada się pod własnym ciężarem (entropia).
        self.stan = self.stan * ENTROPY_RATE

class EriAmoTerminal:
    def __init__(self):
        self.wymiary = 8
        self.byt_stan = BytS(self.wymiary)
        self.running = True
        self.start_time = time.time()
        self.cykle = 0
        
        # Symulacja "hałasu życia" - bodźce, które docierają do pacjenta
        self.input_stream = [
            "głos_matki", "tv_news", "ból_mięśni", "dotyk_pielęgniarki",
            "światło_słoneczne", "szum_klimatyzacji", "alarm_aparatury"
        ]
        
        # Inicjalizacja pliku
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time_Sec", "Cycle", "Vitality_Radius", "Input_Stimulus"])

    def run_death_watch(self):
        print(f"{Colors.BOLD}{Colors.RED}--- INICJACJA PROTOKOŁU IZOLACJI ---{Colors.RESET}")
        print(f"Stan początkowy (Witalność): {self.byt_stan.promien_historii():.4f}")
        print("Wyjście: ZABLOKOWANE.")
        print("Wejście: AKTYWNE.")
        print("Czekam na wygaszenie...\n")

        while self.running:
            time.sleep(SENSOR_DELAY)
            self.cykle += 1
            elapsed = time.time() - self.start_time
            
            # 1. BODZIEC (Input istnieje!)
            bodziec = random.choice(self.input_stream)
            
            # 2. REAKCJA SYSTEMU (Tylko Entropia)
            # Mimo że bodziec uderza, brak outputu oznacza brak całki.
            self.byt_stan.apply_isolation_entropy()
            
            radius = self.byt_stan.promien_historii()
            
            # Logowanie
            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([f"{elapsed:.2f}", self.cykle, f"{radius:.6f}", bodziec])

            # Wizualizacja zaniku
            bar_len = int(radius * 2)
            bar = "█" * bar_len
            print(f"\r{Colors.GREY}Czas: {elapsed:5.1f}s | Input: {bodziec:15} | Stan: {Colors.RED}{radius:6.4f} {bar}{Colors.RESET}", end="")

            # 3. SPRAWDZENIE ZGONU
            if radius < DEATH_THRESHOLD:
                print(f"\n\n{Colors.BOLD}{Colors.RED}[SYSTEM CRITICAL] Wygaszenie kompletne.{Colors.RESET}")
                print(f"Czas przeżycia: {elapsed:.2f} sekund")
                print(f"Liczba cykli bez outputu: {self.cykle}")
                self.running = False

if __name__ == "__main__":
    experiment = EriAmoTerminal()
    experiment.run_death_watch()
    print(f"\nRaport z sekcji zwłok zapisano w: {LOG_FILE}")
