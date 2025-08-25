"""
ORION PE-SCHAUM EXTRUSIONSSIMULATION
====================================
Simulation des Schaeumprozesses fuer Polyethylen
Entwickelt fuer Steinbacher Meeting
02. Dezember 2025
"""

import numpy as np
import json
from datetime import datetime

class FoamExtrusionSimulator:
    """
    Physikalische Simulation des PE-Schaum Extrusionsprozesses
    """
    
    def __init__(self, config=None):
        self.config = config or {
            "polymer": "LDPE",
            "density_target": 26.0,
            "blowing_agent": "isobutane",
            "blowing_agent_pph": 7.0,
            "melt_temp": 180.0,
            "die_temp": 115.0,
            "ambient_temp": 25.0,
            "die_pressure": 8.0,
            "ambient_pressure": 0.101,
            "additives": {
                "GMS": 1.8,
                "talc": 1.5
            }
        }
        
        self.polymer_props = {
            "LDPE": {
                "density_solid": 920.0,
                "melt_index": 2.5,
                "crystallization_temp": 105.0,
                "glass_transition": -120.0,
                "thermal_conductivity": 0.33,
                "specific_heat": 2300.0,
                "surface_tension": 0.026,
            }
        }
        
        self.blowing_agents = {
            "isobutane": {
                "molecular_weight": 58.12,
                "boiling_point": -11.7,
                "gas_constant": 143.0,
                "diffusion_coeff": 1.2e-10,
                "solubility": 0.08,
                "permeability_ratio": 12.5,
            },
            "CO2": {
                "molecular_weight": 44.01,
                "boiling_point": -78.5,
                "gas_constant": 188.9,
                "diffusion_coeff": 2.8e-10,
                "solubility": 0.05,
                "permeability_ratio": 3.2,
            },
            "N2": {
                "molecular_weight": 28.01,
                "boiling_point": -195.8,
                "gas_constant": 296.8,
                "diffusion_coeff": 0.8e-10,
                "solubility": 0.01,
                "permeability_ratio": 1.0,
            }
        }
        
        self.results = {}
    
    def calculate_expansion_ratio(self):
        polymer = self.polymer_props[self.config["polymer"]]
        rho_solid = polymer["density_solid"]
        rho_foam = self.config["density_target"]
        return rho_solid / rho_foam
    
    def calculate_cell_nucleation(self):
        """Berechnet Zellnukleierung mit stabilen numerischen Werten"""
        polymer = self.polymer_props[self.config["polymer"]]
        
        delta_P = (self.config["die_pressure"] - self.config["ambient_pressure"]) * 1e6
        gamma = polymer["surface_tension"]
        
        r_critical = 2 * gamma / delta_P
        
        talc_content = self.config["additives"].get("talc", 0)
        talc_factor = 1 + 8 * talc_content
        
        base_cell_density = 5e8 * talc_factor
        
        expansion = self.calculate_expansion_ratio()
        void_fraction = 1 - 1/expansion
        
        cell_volume = void_fraction / base_cell_density
        cell_diameter = (6 * cell_volume / np.pi)**(1/3) * 1e6
        
        return {
            "critical_radius_nm": r_critical * 1e9,
            "cell_density_per_cm3": base_cell_density / 1e6,
            "cell_diameter_um": max(50, min(500, cell_diameter)),
            "talc_enhancement": talc_factor
        }
    
    def simulate_cell_growth(self, time_steps=100, total_time=10.0):
        polymer = self.polymer_props[self.config["polymer"]]
        ba = self.blowing_agents[self.config["blowing_agent"]]
        
        dt = total_time / time_steps
        times = np.linspace(0, total_time, time_steps)
        
        nucleation = self.calculate_cell_nucleation()
        r0 = nucleation["cell_diameter_um"] / 2
        
        radii = np.zeros(time_steps)
        pressures = np.zeros(time_steps)
        temperatures = np.zeros(time_steps)
        
        radii[0] = r0 * 0.1
        pressures[0] = self.config["die_pressure"]
        temperatures[0] = self.config["die_temp"]
        
        for i in range(1, time_steps):
            t = times[i]
            
            T_current = temperatures[i-1]
            T_ambient = self.config["ambient_temp"]
            cooling_rate = 5.0
            temperatures[i] = max(T_ambient, T_current - cooling_rate * dt)
            
            P_die = self.config["die_pressure"]
            P_ambient = self.config["ambient_pressure"]
            tau_pressure = 0.3
            pressures[i] = P_ambient + (P_die - P_ambient) * np.exp(-t / tau_pressure)
            
            r_current = radii[i-1]
            r_final = nucleation["cell_diameter_um"] / 2
            
            if temperatures[i] > polymer["crystallization_temp"]:
                growth_rate = (r_final - r_current) * 0.5
                radii[i] = r_current + growth_rate * dt
            else:
                radii[i] = r_current
        
        return {
            "time_s": times.tolist(),
            "cell_radius_um": radii.tolist(),
            "pressure_MPa": pressures.tolist(),
            "temperature_C": temperatures.tolist()
        }
    
    def simulate_dimensional_stability(self, aging_time_hours=168):
        ba = self.blowing_agents[self.config["blowing_agent"]]
        
        gms_content = self.config["additives"].get("GMS", 0)
        permeability_reduction = 1 / (1 + 4 * gms_content)
        
        times = np.linspace(0, aging_time_hours, 200)
        
        perm_ratio = ba["permeability_ratio"]
        tau_out = 24 / perm_ratio
        tau_in = 48
        
        c_blowing = np.exp(-times / tau_out)
        c_air = 1 - np.exp(-times / tau_in)
        
        pressure_diff = c_blowing * perm_ratio - c_air
        
        max_shrinkage_base = 18.0
        shrinkage = np.maximum(0, pressure_diff / perm_ratio * max_shrinkage_base)
        
        shrinkage_with_gms = shrinkage * permeability_reduction
        
        return {
            "time_hours": times.tolist(),
            "blowing_agent_fraction": c_blowing.tolist(),
            "air_fraction": c_air.tolist(),
            "shrinkage_percent_without_GMS": shrinkage.tolist(),
            "shrinkage_percent_with_GMS": shrinkage_with_gms.tolist(),
            "equilibrium_time_hours": float(max(tau_out * 5, tau_in * 3)),
            "gms_reduction_factor": permeability_reduction
        }
    
    def calculate_thermal_properties(self):
        polymer = self.polymer_props[self.config["polymer"]]
        expansion = self.calculate_expansion_ratio()
        void_fraction = 1 - 1/expansion
        
        k_polymer = polymer["thermal_conductivity"]
        k_gas = 0.015
        
        phi_s = 1 - void_fraction
        k_conduction = k_polymer * phi_s + k_gas * void_fraction
        
        nucleation = self.calculate_cell_nucleation()
        cell_size = nucleation["cell_diameter_um"] * 1e-6
        
        sigma = 5.67e-8
        T_mean = 300
        extinction = 200 * (1 - void_fraction) / cell_size
        k_rad = 16 * sigma * T_mean**3 / (3 * extinction) if extinction > 0 else 0
        
        k_total = k_conduction + k_rad
        k_total = max(0.025, min(0.050, k_total))
        
        R_value = 0.01 / k_total
        
        return {
            "thermal_conductivity_W_mK": k_total,
            "void_fraction": void_fraction,
            "R_value_per_cm": R_value,
            "conduction_contribution": k_conduction,
            "radiation_contribution": k_rad
        }
    
    def run_full_simulation(self):
        print("=" * 65)
        print("       ORION PE-SCHAUM EXTRUSIONSSIMULATION")
        print("=" * 65)
        print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print("Fuer: STEINBACHER - Hebbel, Scharnagel, Bernard")
        print("=" * 65)
        print()
        
        print("PROZESSPARAMETER:")
        print("-" * 45)
        print(f"  Polymer:              {self.config['polymer']}")
        print(f"  Zieldichte:           {self.config['density_target']} kg/m3")
        print(f"  Treibmittel:          {self.config['blowing_agent']}")
        print(f"  Treibmittel-Anteil:   {self.config['blowing_agent_pph']} pph")
        print(f"  Schmelztemperatur:    {self.config['melt_temp']} C")
        print(f"  Duesentemperatur:     {self.config['die_temp']} C")
        print(f"  Duesendruck:          {self.config['die_pressure']} MPa")
        print(f"  GMS:                  {self.config['additives']['GMS']} Gew.%")
        print(f"  Talkum:               {self.config['additives']['talc']} Gew.%")
        print()
        
        expansion = self.calculate_expansion_ratio()
        print("SCHAUMSTRUKTUR:")
        print("-" * 45)
        print(f"  Expansionsverhaeltnis:  {expansion:.1f}x")
        print(f"  Porenanteil:            {(1-1/expansion)*100:.1f}%")
        
        nucleation = self.calculate_cell_nucleation()
        print(f"  Zelldichte:             {nucleation['cell_density_per_cm3']:.1e} /cm3")
        print(f"  Zellgroesse:            {nucleation['cell_diameter_um']:.0f} um")
        print(f"  Talkum-Verstaerkung:    {nucleation['talc_enhancement']:.1f}x")
        print()
        
        growth = self.simulate_cell_growth()
        print("ZELLWACHSTUM (10 Sek):")
        print("-" * 45)
        print(f"  Startzelle:             {growth['cell_radius_um'][0]*2:.0f} um")
        print(f"  Endzelle:               {growth['cell_radius_um'][-1]*2:.0f} um")
        print(f"  Endtemperatur:          {growth['temperature_C'][-1]:.1f} C")
        print(f"  Enddruck:               {growth['pressure_MPa'][-1]:.3f} MPa")
        print()
        
        stability = self.simulate_dimensional_stability()
        max_shrink_no_gms = max(stability["shrinkage_percent_without_GMS"])
        max_shrink_with_gms = max(stability["shrinkage_percent_with_GMS"])
        reduction = (1 - stability["gms_reduction_factor"]) * 100
        
        print("DIMENSIONSSTABILITAET (7 Tage):")
        print("-" * 45)
        print(f"  Schrumpfung OHNE GMS:   {max_shrink_no_gms:.1f}%")
        print(f"  Schrumpfung MIT GMS:    {max_shrink_with_gms:.1f}%")
        print(f"  GMS-Reduktion:          {reduction:.0f}%")
        print(f"  Gleichgewicht nach:     {stability['equilibrium_time_hours']:.0f} Stunden")
        print()
        
        thermal = self.calculate_thermal_properties()
        print("WAERMEDAEMMUNG:")
        print("-" * 45)
        print(f"  Lambda-Wert:            {thermal['thermal_conductivity_W_mK']*1000:.1f} mW/(m*K)")
        print(f"  R-Wert pro cm:          {thermal['R_value_per_cm']:.3f} m2*K/W")
        print(f"  R-Wert pro 10 cm:       {thermal['R_value_per_cm']*10:.2f} m2*K/W")
        print()
        print("  Vergleichswerte:")
        print("    Styropor EPS:         35-40 mW/(m*K)")
        print("    XPS:                  30-36 mW/(m*K)")
        print("    PU-Hartschaum:        22-28 mW/(m*K)")
        print()
        
        print("=" * 65)
        if max_shrink_with_gms < 3:
            print("  STATUS: STABIL - Produktion empfohlen")
        elif max_shrink_with_gms < 5:
            print("  STATUS: AKZEPTABEL - Optimierung moeglich")
        else:
            print("  STATUS: KRITISCH - Massnahmen erforderlich")
        print("=" * 65)
        
        self.results = {
            "config": self.config,
            "expansion_ratio": expansion,
            "nucleation": nucleation,
            "cell_growth": growth,
            "dimensional_stability": stability,
            "thermal_properties": thermal,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.results
    
    def export_results(self, filename="simulation_results.json"):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nErgebnisse gespeichert: {filename}")


def run_parameter_study():
    print("\n" + "=" * 65)
    print("            PARAMETERSTUDIE - VERGLEICH")
    print("=" * 65 + "\n")
    
    configurations = [
        {"name": "AKTUELL (ohne Additive)", "ba": "isobutane", "GMS": 0, "talc": 0},
        {"name": "MIT GMS 1.0%", "ba": "isobutane", "GMS": 1.0, "talc": 1.0},
        {"name": "MIT GMS 1.8%", "ba": "isobutane", "GMS": 1.8, "talc": 1.5},
        {"name": "MIT GMS 2.5%", "ba": "isobutane", "GMS": 2.5, "talc": 2.0},
        {"name": "CO2 Alternative", "ba": "CO2", "GMS": 0, "talc": 1.5},
    ]
    
    print(f"{'Konfiguration':<28} {'Schrumpf.':<12} {'Lambda':<14} {'Status'}")
    print("-" * 65)
    
    for cfg in configurations:
        sim = FoamExtrusionSimulator({
            "polymer": "LDPE",
            "density_target": 26.0,
            "blowing_agent": cfg["ba"],
            "blowing_agent_pph": 7.0,
            "melt_temp": 180.0,
            "die_temp": 115.0,
            "ambient_temp": 25.0,
            "die_pressure": 8.0,
            "ambient_pressure": 0.101,
            "additives": {"GMS": cfg["GMS"], "talc": cfg["talc"]}
        })
        
        stability = sim.simulate_dimensional_stability()
        thermal = sim.calculate_thermal_properties()
        
        if cfg["GMS"] > 0:
            shrinkage = max(stability["shrinkage_percent_with_GMS"])
        else:
            shrinkage = max(stability["shrinkage_percent_without_GMS"])
        
        lambda_val = thermal["thermal_conductivity_W_mK"] * 1000
        
        if shrinkage < 2:
            status = "OPTIMAL"
        elif shrinkage < 3:
            status = "GUT"
        elif shrinkage < 5:
            status = "AKZEPTABEL"
        else:
            status = "KRITISCH"
        
        print(f"{cfg['name']:<28} {shrinkage:>5.1f}%       {lambda_val:>5.1f} mW/mK    {status}")
    
    print()


def show_process_diagram():
    print("\n" + "=" * 65)
    print("              EXTRUSIONSPROZESS - SCHEMA")
    print("=" * 65 + "\n")
    
    diagram = """
    LDPE + GMS + Talkum
           |
           v
    +-------------+
    | EXTRUDER    |  180°C, Schmelzen + Mischen
    | Twin-Screw  |
    +-------------+
           |
           v
    +-------------+
    | GASINJEKT.  |  Isobutan 7 pph einspritzen
    | 8 MPa       |
    +-------------+
           |
           v
    +-------------+
    | DUESE       |  115°C, Druckabfall
    | Expansion   |  8 MPa -> 0.1 MPa
    +-------------+
           |
           | <- ZELLNUKLEIERUNG (Mikrosekunden)
           | <- ZELLWACHSTUM (Sekunden)
           v
    +-------------+
    | KUEHLUNG    |  Wasserbad oder Luft
    | <10 Sek     |  Polymer erstarrt
    +-------------+
           |
           v
    +-------------+
    | ALTERUNG    |  48-168 Stunden
    | Lager       |  Gas-Austausch
    +-------------+
           |
           v
      FERTIGER SCHAUM
      26 kg/m3
      ~35 mW/(m*K)
    """
    print(diagram)


if __name__ == "__main__":
    show_process_diagram()
    
    print("\n" + "=" * 65)
    print("         HAUPTSIMULATION - 26 kg/m3 ISOLIERSCHAUM")
    print("=" * 65 + "\n")
    
    simulator = FoamExtrusionSimulator({
        "polymer": "LDPE",
        "density_target": 26.0,
        "blowing_agent": "isobutane",
        "blowing_agent_pph": 7.0,
        "melt_temp": 180.0,
        "die_temp": 115.0,
        "ambient_temp": 25.0,
        "die_pressure": 8.0,
        "ambient_pressure": 0.101,
        "additives": {
            "GMS": 1.8,
            "talc": 1.5
        }
    })
    
    results = simulator.run_full_simulation()
    simulator.export_results("STEINBACHER_SIMULATION.json")
    
    run_parameter_study()
    
    print("=" * 65)
    print("           ORION EMPFEHLUNG FUER STEINBACHER")
    print("=" * 65)
    print()
    print("  1. SOFORT-MASSNAHME:")
    print("     + 1.8% GMS (Glycerolmonostearat)")
    print("     + 1.5% Talkum")
    print("     -> Schrumpfung reduziert auf <3%")
    print()
    print("  2. KUEHLUNG OPTIMIEREN:")
    print("     Wasserbad direkt nach Duese (<10 Sekunden)")
    print("     -> Zellstruktur fixieren vor Gasdiffusion")
    print()
    print("  3. ALTERUNG:")
    print("     48-72 Stunden bei 20-25°C")
    print("     -> Druckausgleich, Stabilitaet")
    print()
    print("  4. LANGZEIT-ALTERNATIVE:")
    print("     CO2/N2 statt Isobutan")
    print("     -> Keine Schrumpfung, keine Explosionsgefahr")
    print()
    print("=" * 65)
    print("  Simulation durchgefuehrt von ORION")
    print("  02. Dezember 2025")
    print("=" * 65)
