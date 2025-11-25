import streamlit as st

class TapinomaKey:
    def __init__(self):
        self.logs = []

    def log(self, msg):
        self.logs.append(msg)

    def solve(self, inputs_um):
        """
        inputs_um: Dizionario con misure in MICROMETRI (numeri interi o float)
        Le formule discriminanti (LDA) dell'articolo richiedono MILLIMETRI.
        Le soglie semplici (es. SL < 475) usano i MICROMETRI.
        """
        
        # Creiamo una versione in mm per le formule matematiche
        m = {k: v / 1000.0 for k, v in inputs_um.items()}
        # Usiamo u per i valori originali in micrometri
        u = inputs_um

        # --- STEP 1 ---
        # Soglia: 475 micrometri
        if u['SL'] < 475:
            self.log("Step 1: Scapo corto (< 475 µm)")
            return "Tapinoma pygmaeum"
        
        # --- STEP 2: Geografia ---
        # Questo va gestito tramite input utente, qui assumiamo un parametro extra
        region = u.get('region', 'west') # west = Ovest (fino a 60°E), east = Est

        if region == 'east':
            self.log("Step 2: Regione Paleartico Orientale (60°E - 120°E)")
            # --- STEP 3 ---
            # D3 usa mm
            D3 = 64.89*m['CL'] - 49.21*m['CW'] - 63.57*m['PoOc'] + 20.81*m['SL'] - 8.45
            if D3 < 0:
                return "Tapinoma sinense"
            
            # --- STEP 4 -> 5 ---
            # IFu2 è un indice (adimensionale), ExClyLW è un rapporto (adimensionale)
            # D5 usa indici puri
            D5 = 6.469*u['IFu2'] - 1.946*u['ExClyLW'] - 11.268
            
            if D5 < 0:
                self.log("Step 5: Specie piccole del Sichuan")
                # ML/CS è un rapporto, non serve conversione mm
                if (u['ML'] / u['CS']) < 1.335:
                    return "Tapinoma dabashanica n.sp."
                else:
                    return "Tapinoma sichuense n.sp."
            else:
                return "Specie asiatica non determinata (D5 > 0)"

        else:
            self.log("Step 2: Regione Paleartico Occidentale (Europa/Nord Africa/Medio Oriente)")
            # --- STEP 7 ---
            # Formula complessa, richiede mm
            D7 = (19.06*m['CW'] - 19.92*m['CL'] + 70.87*m['dAN'] - 78.57*m['EL'] 
                  - 0.085*u['nExCly'] + 50.25*m['ExCly'] - 110.38*m['ExOcc'] 
                  + 113.82*m['Fu2L'] - 110.03*m['Fu2W'] - 16.97*m['MW'] + 3.184)
            
            if D7 < 0:
                return "Tapinoma glabrella"
            
            # Step 7b -> 8
            # Kinburni check
            DKin = 134.18*m['Fu2L'] - 14.42*m['CW'] - 1.184
            if (u['Fu2L'] / u['CS']) < 0.109 and DKin < 0:
                 return "Tapinoma kinburni"

            # Festae check (Step 8a)
            D8 = 20.29*m['CL'] - 101.78*m['dAN'] + 23.03*m['ExCly'] + 81.31*m['Fu2L'] - 0.728
            if D8 < 0:
                return "Tapinoma festae"

            # --- STEP 9: GRANDE BIVIO ---
            # Gruppo Nigerrimum vs Erraticum/Simrothi
            D9 = (0.119*u['nExCly'] - 11.4*m['CL'] + 11.11*m['CW'] + 35.02*m['dAN'] 
                  + 8.62*m['EL'] - 28.01*m['ExCly'] + 3.85*m['SL'] + 32.35*m['ExClyW'] 
                  + 19.79*m['ExOcc'] + 135.45*m['Fu2L'] - 253.50*m['Fu2W'] 
                  - 12.60*m['MGr'] - 10.54*m['ML'] - 12.98*m['MW'] + 6.15)

            if D9 > 0:
                self.log("Step 9: Gruppo Nigerrimum")
                # --- STEP 10 ---
                D10 = (-29.5*m['CW'] + 51.53*m['dAN'] + 26.6*m['EL'] - 51.05*m['ExCly'] 
                       + 25.1*m['ExClyW'] - 29.98*m['ExOcc'] + 56.41*m['Fu2L'] 
                       + 141.54*m['Fu2W'] + 63.37*m['MGr'] - 10.1)
                
                if D10 > 0:
                    return "Tapinoma magnum"
                
                # --- STEP 11 ---
                D11 = (19.04*m['CL'] + 57.56*m['dAN'] - 108.18*m['EL'] + 22.02*m['ExCly'] 
                       + 35.61*m['ExClyW'] + 26.49*m['ExOcc'] - 55.39*m['Fu2L'] 
                       + 158.80*m['Fu2W'] + 22.53*m['MGr'] - 18.71*m['ML'] 
                       - 12.96*m['MW'] + 10.40)
                
                if D11 > 0: # Step 12
                    D12 = (47.25*m['SL'] - 27.067*m['CW'] - 28.67*m['ExCly'] 
                           - 0.067*u['nExCly'] + 87.18*m['MGr'] - 14.728)
                    return "Tapinoma nigerrimum" if D12 > 0 else "Tapinoma hispanicum n.sp."
                else: # Step 13
                    D13 = (19.44*m['CL'] - 113.55*m['dAN'] + 45.86*m['ExCly'] 
                           + 21.53*m['SL'] - 39.59*m['ExOcc'] - 150.05*m['Fu2L'] 
                           + 379.6*m['Fu2W'] + 21.17*m['MGr'] - 16.89)
                    return "Tapinoma darioi" if D13 < 0 else "Tapinoma ibericum"

            else:
                self.log("Step 9: Gruppi Erraticum / Simrothi")
                # --- STEP 14 ---
                D14 = (54.85*m['ExCly'] - 28.27*m['dAN'] - 0.04*u['nExCly'] 
                       - 16.46*m['SL'] - 41.23*m['ExClyW'] + 38.87*m['ExOcc'] 
                       + 173.50*m['Fu2L'] - 44.53*m['Fu2W'] - 4.94*m['MW'] + 5.14)
                
                if D14 < 0: # Step 15
                    return "Complesso Tapinoma madeirense / subboreale (Richiede analisi genitali maschi o DNA)"
                
                # --- STEP 16 ---
                D16 = (17.96*m['CL'] + 74.89*m['dAN'] - 58.54*m['EL'] + 72.71*m['ExCly'] 
                       - 15.85*m['SL'] - 30.07*m['ExClyW'] - 48.23*m['ExOcc'] 
                       + 43.34*m['Fu2L'] - 6.606*m['ML'] - 19.41*m['MW'] - 0.265)
                
                if D16 < 0: # Step 17 (Gruppo Erraticum)
                    self.log("Step 16: Gruppo Erraticum")
                    D17 = (18.61*m['CL'] - 37.88*m['CW'] + 72.70*m['dAN'] 
                           + 43.16*m['EL'] - 84.94*m['ExCly'] + 0.111*u['nExCly'] 
                           + 58.18*m['MGr'] - 10.30)
                    if D17 > 0: # Nota: il testo dice > 0 per Israel
                        return "Tapinoma israelis"
                    
                    # Step 18
                    D18 = (47.8*m['CL'] + 121.79*m['EL'] - 21.92*m['SL'] 
                           - 39.55*m['ExClyW'] - 187.68*m['Fu2L'] - 11.68*m['ML'] 
                           - 13.5*m['MW'] + 0.16*u['nExCly'] - 6.69)
                    return "Tapinoma erraticum" if D18 < 0 else "Tapinoma glabrella"

                else: # Step 19 (Gruppo Simrothi)
                    self.log("Step 16: Gruppo Simrothi")
                    # Discriminante Ovest vs Est
                    D19 = (0.045*u['nExCly'] + 63.44*m['PoOc'] - 35.80*m['dAN'] 
                           + 64.72*m['EL'] + 68.58*m['ExCly'] - 30.02*m['SL'] 
                           - 23.56*m['ExClyW'] + 94.64*m['ExOcc'] - 33.70*m['Fu2L'] 
                           - 96.79*m['Fu2W'] - 28.09*m['MGr'] + 2.305)
                    
                    # CORREZIONE LOGICA 20/21
                    # Se D19 > 0 -> Gruppo OVEST (Simrothi/Insularis) - Step 20
                    # Se D19 < 0 -> Gruppo EST (Phoenicaeum/Karavaievi) - Step 21
                    
                    if D19 > 0: # Step 20
                        self.log("Step 19: Ramo Occidentale")
                        D20 = (17.82*m['CW'] - 30.01*m['CL'] - 82.78*m['dAN'] 
                               + 86.78*m['ExCly'] + 35.53*m['SL'] + 64.0*m['ExClyW'] 
                               - 125.50*m['Fu2W'] + 1.36)
                        return "Tapinoma insularis n.sp." if D20 < 0 else "Tapinoma simrothi"
                    
                    else: # Step 21
                        self.log("Step 19: Ramo Orientale")
                        D21 = (0.111*u['nExCly'] - 77.37*m['CL'] + 75.45*m['PoOc'] 
                               + 56.02*m['dAN'] + 117.44*m['EL'] + 30.22*m['SL'] 
                               + 83.70*m['ExClyW'] - 70.58*m['ExOcc'] - 140.86*m['Fu2L'] 
                               - 214.17*m['Fu2W'] + 79.04*m['MGr'] + 13.60*m['MW'] - 3.077)
                        return "Tapinoma phoenicaeum" if D21 < 0 else "Tapinoma karavaievi"

# --- INTERFACCIA WEB (STREAMLIT) ---
st.set_page_config(page_title="Tapinoma ID Key", layout="wide")

st.title("🔑 Chiave Identificativa Tapinoma (Paleartico)")
st.markdown("""
Questa applicazione implementa la logica **NUMOBAT** descritta in *Seifert et al. (2024)*.
**Istruzioni:** Inserisci tutte le misure in **micrometri (µm)**. Il software calcolerà automaticamente le discriminanti.
""")

# Sidebar per input
st.sidebar.header("Inserimento Dati (µm)")

region = st.sidebar.radio("Regione Geografica", 
                          ('Ovest (Europa, Nord Africa, < 60°E)', 'Est (Asia Centrale/Cina, > 60°E)'))
reg_code = 'east' if 'Est' in region else 'west'

# Input numerici
col1, col2 = st.sidebar.columns(2)
with col1:
    cl = st.number_input("CL (Lunghezza Testa)", value=800)
    cw = st.number_input("CW (Larghezza Testa)", value=750)
    sl = st.number_input("SL (Lunghezza Scapo)", value=800)
    el = st.number_input("EL (Lunghezza Occhio)", value=200)
    mw = st.number_input("MW (Largh. Pronoto)", value=500)
    ml = st.number_input("ML (Lungh. Mesosoma)", value=1000)
    pooc = st.number_input("PoOc (Postoculare)", value=300)

with col2:
    dan = st.number_input("dAN (Dist. Antenne)", value=250)
    excly = st.number_input("ExCly (Prof. Clipeo)", value=50)
    excly_w = st.number_input("ExClyW (Largh. Clipeo)", value=80)
    exocc = st.number_input("ExOcc (Excav. Occipite)", value=20)
    fu2l = st.number_input("Fu2L (Lungh. 2° Fun.)", value=100)
    fu2w = st.number_input("Fu2W (Largh. 2° Fun.)", value=60)
    mgr = st.number_input("MGr (Prof. Metanoto)", value=30)
    nexcly = st.number_input("nExCly (N. Sete Clipeo)", value=4.0, step=1.0)

# Calcoli automatici per indici
cs = (cl + cw) / 2
ifu2 = fu2l / fu2w if fu2w > 0 else 0
excly_lw = excly / excly_w if excly_w > 0 else 0

inputs = {
    'CL': cl, 'CW': cw, 'SL': sl, 'EL': el, 'MW': mw, 'ML': ml, 'PoOc': pooc,
    'dAN': dan, 'ExCly': excly, 'ExClyW': excly_w, 'ExOcc': exocc,
    'Fu2L': fu2l, 'Fu2W': fu2w, 'MGr': mgr, 'nExCly': nexcly,
    'CS': cs, 'IFu2': ifu2, 'ExClyLW': excly_lw, 'region': reg_code
}

st.sidebar.markdown("---")
if st.sidebar.button("IDENTIFICA SPECIE", type="primary"):
    solver = TapinomaKey()
    result = solver.solve(inputs)
    
    st.success(f"### Risultato: {result}")
    
    with st.expander("Vedi dettagli percorso decisionale"):
        for log in solver.logs:
            st.write(f"- {log}")
        st.write("---")
        st.write("#### Dati calcolati:")
        st.write(f"CS (Taglia cefalica): {cs:.1f} µm")
        st.write(f"IFu2 (Indice funicolo): {ifu2:.2f}")
