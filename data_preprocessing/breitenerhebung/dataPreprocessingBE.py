"""
Module serves for data generation from original and imputated BE-Data to a modified input dataset used as input in annualSimulation.py


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2021, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2021, Institut Wohnen und Umwelt"
__license__ = "MIT"


# Import packages
import numpy as np
import pandas as pd
import warnings
from pandas.core.common import SettingWithCopyWarning



# Ignore CopyWarnings caused by map() [See: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy]
warnings.simplefilter(action = "ignore", category = SettingWithCopyWarning)

##############################################################################
##############################################################################
# Import Input Data
##############################################################################
##############################################################################
# Import Data Breitenerhebung with relevant buildings
be_data_original = pd.read_excel(r'BE_data/BE_BuildingData.xlsx')
# Import Data from DIN V 18599-10:2018-09, DIN V 18599-4:2018-09
profile_zuweisung_18599_10 = pd.read_excel(r'BE_data/normData.xlsx', sheet_name = 'profile_zuweisung_18599_10', decimal = ",")
data_18599_10_4 = pd.read_excel(r'BE_data/normData.xlsx', sheet_name = 'data_18599_10_4', decimal = ",")


##############################################################################
##############################################################################
# Data Pre-Processing
##############################################################################
##############################################################################

# Gebäude-ID (scr_gebaeude_id)
##############################################################################
# Create DataFrame building_data with column 'scr_gebaeude_id' including all buildings from be_data_original
building_data = be_data_original[['scr_gebaeude_id']]


# PLZ (plz)
##############################################################################
# Map 'scr_plz' from be_data_original to building_data and name column 'plz'
building_data['plz'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['plz'])


# Gebäudefunktion Hauptkategorie/Unterkategorie (hk_geb, uk_geb)
##############################################################################
# Map 'HK_Geb' and 'UK_Geb' to be_data_original
building_data['hk_geb'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['hk_geb']).astype(str)
building_data['uk_geb'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['uk_geb']).astype(str)


# Encode Labelling 
cleanup_hk_geb = {"hk_geb": {'1': 'Büro-, Verwaltungs- oder Amtsgebäude',                                           
                             '2': 'Gebäude für Forschung und Hochschullehre',                                        
                             '3': 'Gebäude für Gesundheit und Pflege',                                               
                             '4': 'Schule, Kindertagesstätte und sonstiges Betreuungsgebäude',                       
                             '5': 'Gebäude für Kultur und Freizeit',                                                 
                             '6': 'Sportgebäude',                                                                    
                             '7': 'Beherbergungs- oder Unterbringungsgebäude, Gastronomie- oder Verpflegungsgebäude', 
                             '8': 'Produktions-, Werkstatt-, Lager- oder Betriebsgebäude',                           
                             '9': 'Handelsgebäude',                                                                 
                             '10': 'Technikgebäude (Ver- und Entsorgung)',                                            
                             '11': 'Verkehrsgebäude',                                                                 
                             '12': 'Sonstiges Nichtwohngebäude'}}
building_data.replace(cleanup_hk_geb, inplace = True)

cleanup_uk_geb = {"uk_geb": {'1,01': 'Parlaments- oder Gerichtsgebäude',                                                                                                                                 
                             '1,02': 'Öffentliches Verwaltungs- oder Ämtergebäude, Rathaus',                      
                             '1,03': 'Bürogebäude',                                                               
                             '1,04': 'Rundfunk- oder Fernsehanstalt',                                             
                             '1,05': 'Polizeipräsidium oder -station, Bürogebäude sonstiger Bereitschaftsdienste',
                             '1,06': 'Sonstige Gebäudefunktion',
                             '2,01': 'Hörsaalgebäude',                                                                                                                                                                                        
                             '2,02': 'Verwaltungs- oder Seminargebäude',                                                                                                                                                                
                             '2,03': 'Institutsgebäude für Forschung und Lehre (Labor mit geringen Anforderungen an die Raumlufttechnik, z.B. Medizin, Informatik)',
                             '2,04': 'Institutsgebäude für Forschung und Lehre (Labor mit hohen Anforderungen an die Raumlufttechnik, z.B. Chemie, Tierforschung)', 
                             '2,05': 'Bürogebäude von Forschungsanstalten ohne Lehre',                                                                              
                             '2,06': 'Laborgebäude von Forschungsanstalten und Unternehmen (Labor mit geringen Anforderungen an die Raumlufttechnik)',              
                             '2,07': 'Laborgebäude von Forschungsanstalten und Unternehmen (Labor mit hohen Anforderungen an die Raumlufttechnik)',                 
                             '2,08': 'Sonstiges Gebäudefunktion',
                             '3,01': 'Hochschulklinik',                                                                                                                                          
                             '3,02': 'Krankenhaus',                                                                  
                             '3,03': 'Gebäude für teilstationäre Versorgung (z.B. Tagesklinik, Geburtshaus)',        
                             '3,04': 'Rehabilitation',                                                               
                             '3,05': 'Kur und Genesung',                                                             
                             '3,06': 'Medizinisches Versorgungszentrum, Ärztehaus',                            
                             '3,07': 'Arztpraxis',                                                                   
                             '3,08': 'Notfallpraxis',                                                                
                             '3,09': 'Altenheim/Altenpflegeheim (ohne eigene Haushaltsführung der Bewohner/innen)',
                             '3,10': 'Pflegeheim für Behinderte (ohne eigene Haushaltsführung der Bewohner/innen)',
                             '3,11': 'Psychiatrische Pflegeheim (ohne eigene Haushaltsführung der Bewohner/innen)',
                             '3,12': 'Tagespflegeeinrichtung',                                                     
                             '3,13': 'Hospiz',                                                                     
                             '3,14': 'Sonstige Gebäudefunktion',
                             '4,01': 'Schule, allgemein',
                             '4,02': 'Ganztagesschule',                                                              
                             '4,03': 'Internatsschule',                                                              
                             '4,04': 'Förder-, Sonderschule',                                                        
                             '4,05': 'Berufsbildende Schule (gewerblich, wirtschaftlich)',                          
                             '4,06': 'Berufsbildende Schule (mit höherer technischer Ausstattung, z.B. Werkstätten)',
                             '4,07': 'Berufsakademie, Berufskolleg',                                                 
                             '4,08': 'Bildungszentrum',                                                              
                             '4,09': 'Ausbildungsstätte',                                                            
                             '4,10': 'Volkshochschule',                                                              
                             '4,11': 'KiTa',                                                                         
                             '4,12': 'KiTa mit Küche',                                                               
                             '4,13': 'Studentenhaus',                                                                
                             '4,14': 'Altentagesstätte',                                                             
                             '4,15': 'Jugendzentrum',                                                                
                             '4,16': 'Sonstige Gebäudefunktion',
                             '5,01': 'Bibliothek/Archiv (einfach, z.B. Stadtbücherei)',                                                            
                             '5,02': 'Bibliothek/Archiv (höher technisiert, z.B. Unibibliothek)',       
                             '5,03': 'Ausstellungsgebäude (Museen, Galerien)',                          
                             '5,04': 'Oper, Theater und Veranstaltungshalle, Kino, Konferenzzentrum',
                             '5,05': 'Freizeit-, Gemeinschafts-, Bürgerhaus',                           
                             '5,06': 'Spielkasino, -bank, -halle',                                      
                             '5,07': 'Sonstige Gebäudefunktion',
                             '6,01': 'Einfeldhalle',                                                                   
                             '6,02': 'Mehrfeldhalle',                                                   
                             '6,03': 'Gymnastikhalle',                                                  
                             '6,04': 'Sporthalle mit Mehrzwecknutzung',                                 
                             '6,05': 'Hallenbad',                                                       
                             '6,06': 'Spaß- und Freizeitbad',                                           
                             '6,07': 'Thermalbad',                                                      
                             '6,08': 'Hallenbad mit Freibadanlage',                                     
                             '6,09': 'Kegelbahn/Bowling',                                               
                             '6,10': 'Schießstand',                                                     
                             '6,11': 'Raumschießanlage',                                                
                             '6,12': 'Reithalle',                                                       
                             '6,13': 'Eissporthalle',                                                   
                             '6,14': 'Tennishalle',                                                     
                             '6,15': 'Fitnessstudio',                                                   
                             '6,16': 'Gebäude für Sportaußenanlage (Tribünen-, Umkleidegebäude)',       
                             '6,17': 'Sonstige Gebäudefunktion',
                             '7,01': 'Herberge, Ferienheim, Ferienhaus, Hotel/Pension einfach',                                       
                             '7,02': 'Sterne-Hotel',                                                    
                             '7,03': 'Ausschankwirtschaft',                                             
                             '7,04': 'Speisegaststätte (einfach)',                                      
                             '7,05': 'Restaurant (gehoben)',                                            
                             '7,06': 'Mensa/Kantine',                                                   
                             '7,07': 'Gemeinschaftsunterkunft (z.B. Flüchtlingsheim, Kaserne, Kloster)',
                             '7,08': 'Sonstige Gebäudefunktion',
                             '8,01': 'Gebäude für gewerbliche Produktion und Verarbeitung (z.B. Brauerei, Molkerei, Schlachthof)',              
                             '8,02': 'Gebäude für industrielle Produktion und Verarbeitung (z.B. Chemie, Metall, Textilien, Lebensmittel, Holz)',
                             '8,03': 'Werkstattgebäude allgemein (z.B. von Handwerksbetrieben wie Klempner, Schlosser, Schreiner)',             
                             '8,04': 'Werkstattgebäude zur Wartung, Instandsetzung, Reparatur (von z.B. Kfz)',                                  
                             '8,05': 'Logistikimmobilie mit Toren bzw. Rampen',                                                                 
                             '8,06': 'Sonstiges Gebäude für Lagerung',                                                                           
                             '8,07': 'Feuerwehr, Rettungswache',                                                                                
                             '8,08': 'Straßenmeisterei, Bauhof u.ä.',                                                                           
                             '8,09': 'Fuhrpark',                                                                                                
                             '8,10': 'zentrales Wirtschaftsgebäude (z.B. Zentralküche oder -wäscherei in Krankenhaus)',                       
                             '8,11': 'Rechenzentrum',                                                                                         
                             '8,12': 'Sonstige Gebäudefunktion',
                             '9,01': 'Handelsgebäude des Lebensmitteleinzel- und -großhandels',        
                             '9,02': 'Handelsgebäude des Non-Food-Einzel- und -Großhandels',            
                             '9,03': 'Einkaufszentrum, Shopping-Mall',                                  
                             '9,04': 'Markthalle',                                                      
                             '9,05': 'Messehalle',                                                     
                             '9,06': 'von Dienstleistern (z.B. Frisör, Kosmetik) genutztes Ladengebäude',                                          
                             '9,07': 'Sonstige Gebäudefunktion',
                             '10,01': 'Kraftwerk (Gesamtanlage für Energieversorgung)',                                                                      
                             '10,02': 'Gebäude für Lenkung, Steuerung, Überwachung und Nachrichtenübermittlung (z.B. Stellwerk, Leuchtturm)',
                             '10,03': 'Gebäude für Energieversorgung (z.B. Fernheizwerk, Tankstelle)',                                       
                             '10,04': 'Gebäude für Wasserversorgung',                                                                        
                             '10,05': 'Gebäude für Abwasserbehandlung',                                                                      
                             '10,06': 'Gebäude für Abfallbehandlung',                                                                        
                             '10,07': 'Sonstige Gebäudefunktion',
                             '11,01': 'Park-/Garagengebäude, Fahrradparkhaus',                                                                                         
                             '11,02': 'Halle für sonstige Verkehrsmittel (z.B. für Flugzeuge, Schienenfahrzeuge)',
                             '11,03': 'Gebäude zur Pflege von Fahrzeugen (z.B. Waschstraße)',                    
                             '11,04': 'Empfangsgebäude (Bahnhof, Busbahnhof, Flughafen, Schiffsterminal)',        
                             '11,05': 'Sonstige Gebäudefunktion'}}
building_data.replace(cleanup_uk_geb, inplace = True)

# Map Profile from DIN V 18599-10:2018-09 according to profile_zuweisung_18599_10 (See: normData.xlsx)
# Used for further calculations
building_data['typ_18599'] = building_data['uk_geb'].map(profile_zuweisung_18599_10.set_index('uk_geb')['typ_18599'])

# Maximale Personenbelegung (max_occupancy)
##############################################################################
# Map 'q25'(max. Personenbelegung) from be_data_original to building_data as column 'max_occupancy'
building_data['max_occupancy'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['q25'])


# Oberirdische Außenwandfläche (wall_area_og)
##############################################################################
# Map 'AW_fl' from be_data_original to building_data as column 'wall_area_og'
building_data['wall_area_og'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['AW_fl'])


# Unterirdische Außenwandfläche (wall_area_ug)
##############################################################################
# Map 'unterAW_fl' from be_data_original to building_data as column 'wall_area_ug'
building_data['wall_area_ug'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['unterAW_fl'])


# Fensterflächen (window_area_north, window_area_east, window_area_south, window_area_west)
##############################################################################
# Map windows share and building area for each direction to building_data
building_data['Fen_ant'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qD1'])
building_data['geb_f_flaeche_n_iwu'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['geb_f_flaeche_n_iwu'])
building_data['geb_f_flaeche_o_iwu'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['geb_f_flaeche_o_iwu'])
building_data['geb_f_flaeche_s_iwu'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['geb_f_flaeche_s_iwu'])
building_data['geb_f_flaeche_w_iwu'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['geb_f_flaeche_w_iwu'])

# Calculate window area for each directions                                                         
building_data['window_area_north'] = (building_data['Fen_ant']/100) * building_data['geb_f_flaeche_n_iwu'] 
building_data['window_area_east'] = (building_data['Fen_ant']/100) * building_data['geb_f_flaeche_o_iwu'] 
building_data['window_area_south'] = (building_data['Fen_ant']/100) * building_data['geb_f_flaeche_s_iwu'] 
building_data['window_area_west'] = (building_data['Fen_ant']/100) * building_data['geb_f_flaeche_w_iwu'] 


# Dachfläche (roof_area)
##############################################################################
# Map 'D_fl_be' from be_data_original to building_data as column 'roof_area'
building_data['roof_area'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['D_fl_beheizt_be']) 


# Netto-Raumfläche (net_room_area)
##############################################################################
# Map 'NRF_2' from be_data_original to building_data as column 'net_room_area'
building_data['net_room_area'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['NRF_2']) 


# Energiebezugsfläche (energy_ref_area)
##############################################################################
# Map 'EBF' from be_data_original to building_data as column 'energy_ref_area'
building_data['energy_ref_area'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['EBF']) 

    
# Fläche des unteren Gebäudeabschlusses (base_area)
##############################################################################
# Map 'Mittlere Anzahl oberidrische Geschosse' from be_data_original to building_data as column 'Mittlere Anzahl oberidrische Geschosse'
building_data['n_OG'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['n_OG']) 
# Calculate base_area
building_data['base_area'] = building_data['energy_ref_area'] / (building_data['n_OG'] * 0.87)


# Mittlere Gebäudehöhe (building_height)
##############################################################################
# Map 'geb_f_hoehe_mittel_iwu' from be_data_original to building_data as column 'building_height'
building_data['building_height'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['geb_f_hoehe_mittel_iwu'])


# spezifische Beleuchtungsleistung (lighting_load)
##############################################################################
# Create Subset for calculation of lighting_load 
subset_lighting_load = building_data[['scr_gebaeude_id', 'typ_18599']]

# Map 'qF1' (überw. Beleuchtungsart) from be_data_original to subset_lighting_load as column 'qF1'
subset_lighting_load['qF1'] = subset_lighting_load['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qF1'])
# Encode Labelling
cleanup_beleuchtungsart = {'qF1':{
                                  1: 'Direkt (Licht fällt direkt auf den Arbeitsbereich)',                                           
                                  2: 'Direkt / indirekt', 
                                  3: 'Indirekt (Licht, das von Decken und Wänden reflektiert wird)'}}
subset_lighting_load.replace(cleanup_beleuchtungsart, inplace = True)

# Map 'qF1' (überw. Lampenart) from be_data_original to subset_lighting_load as column 'lampenart_be'
subset_lighting_load['lampenart_be'] = subset_lighting_load['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['lampenart_be'])
# Encode Labelling
cleanup_lampenart = {'lampenart_be':{
                                    1: 'Glüh- oder Halogenlampe',                                           
                                    2: 'Leuchtstofflampe', 
                                    3: 'LED (allgemein)',
                                    3.1: 'LED-Ersatzlampe',
                                    3.2: 'LED-Speziallampe'}}
subset_lighting_load.replace(cleanup_lampenart, inplace = True)

## Start with calculation: Tabellenverfahren nach 18599-4:2018-09, S. 25

# Add column 'k_L' to subset_lighting_load based on column 'lampenart_be' [See DIN V 18599-4:2018-09, S. 27] using mean values
subset_lighting_load.loc[:, 'k_L'] = subset_lighting_load['lampenart_be']
# Encode Labelling
cleanup_k_L = {'k_L':{
                    'Glüh- oder Halogenlampe': 5.5,                                           
                    'Leuchtstofflampe': 1.235, 
                    'LED (allgemein)': 1.09,
                    'LED-Ersatzlampe': 0.605,
                    'LED-Speziallampe': 0.465}}
subset_lighting_load.replace(cleanup_k_L, inplace = True)

# Map 'E_m', 'k_A', 'k_VB', 'k_WF', 'k' from data_18599_10_4 as new columns to subset_lighting_load
subset_lighting_load['E_m'] = subset_lighting_load['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['E_m'])
subset_lighting_load['k_A'] = subset_lighting_load['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['k_A'])
subset_lighting_load['k_VB'] = subset_lighting_load['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['k_VB'])
subset_lighting_load['k_WF'] = subset_lighting_load['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['k_WF'])
subset_lighting_load['k'] = subset_lighting_load['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['k'])

# Create DataFrame of Table 5 DIN V 18599-4:2018-09, S. 24
p_j_lx = pd.DataFrame({'beleuchtungsart': ['Direkt (Licht fällt direkt auf den Arbeitsbereich)',
                                           'Direkt / indirekt',
                                           'Indirekt (Licht, das von Decken und Wänden reflektiert wird)'], 
                        0.6: [0.045, 0.067, 0.122],
                        0.7: [0.041, 0.059, 0.105],
                        0.8: [0.037, 0.053, 0.09],
                        0.91: [0.035, 0.049, 0.08],
                        1: [0.033, 0.045, 0.071],
                        1.2: [0.0298, 0.0402, 0.0606],
                        1.25: [0.029, 0.039, 0.058],
                        1.5: [0.027, 0.036, 0.05],
                        2: [0.025, 0.032, 0.044],
                        2.4: [0.0242, 0.0296, 0.04],
                        2.5: [0.024, 0.029, 0.039],
                        3: [0.023, 0.028, 0.037],
                        4: [0.022, 0.026, 0.035],
                        5: [0.021, 0.025, 0.033]})
p_j_lx = p_j_lx.set_index('beleuchtungsart')
p_j_lx = p_j_lx.unstack().reset_index().rename(columns = {'level_0':'k', 0:'p_j_lx'})
p_j_lx['k'] = p_j_lx['k'].astype('float')
p_j_lx = p_j_lx.rename(columns={'beleuchtungsart': 'qF1'})

# Merge value for p_j_lx based on 'qF1' respectively 'beleuchtungsart' and 'k' to subset_lighting_load
subset_lighting_load = pd.merge(subset_lighting_load, p_j_lx, left_on = ['qF1', 'k'], right_on = ['qF1', 'k'], how = 'left')

# Calculate 'p_j'
# p_j = p_j_lx * E_m * k_WF * k_A * k_L * k_VB [See: DIN V 18599-4:2018-09, S. 25]
subset_lighting_load['p_j'] = subset_lighting_load['p_j_lx'] * subset_lighting_load['E_m'] * \
                                subset_lighting_load['k_WF'] * subset_lighting_load['k_L'] * subset_lighting_load['k_VB']

# Map 'p_j' from subset_lighting_load as column 'lighting_load' to building_data
building_data['lighting_load'] = building_data['scr_gebaeude_id'].map(subset_lighting_load.set_index('scr_gebaeude_id')['p_j'])


# Lichtausnutzungsgrad der Verglasung (lighting_control)
##############################################################################
# Map 'E_m' from data_18599_10_4 to building_data
building_data['lighting_control'] = building_data['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['E_m'])


# Wartungsfaktor der Verglasung (lighting_utilisation_factor) 
##############################################################################
# Assumption [See Szokolay (1980): Environmental Science Handbook for Architects and Builders, p. 104ff.]
building_data['lighting_utilisation_factor'] = 0.45


# Wartungsfaktor der Fensterflächen (lighting_maintenance_factor) 
##############################################################################
# See Szokolay (1980): Environmental Science Handbook for Architects and Builders, p. 109
def set_lighting_maintenance_factor(row):
    if row['hk_geb'] == 'Produktions-, Werkstatt-, Lager- oder Betriebsgebäude':
        lighting_maintenance_factor = 0.8
    else:
        lighting_maintenance_factor = 0.9
    return lighting_maintenance_factor
building_data['lighting_maintenance_factor'] = building_data.apply(set_lighting_maintenance_factor, axis = 1)    


# Energiedurchlassgrad der Verglasung (glass_solar_transmittance)
##############################################################################
# Map 'Fen_glasart_1' from be_data_original as column 'glass_solar_transmittance' to building_data
building_data['glass_solar_transmittance'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['Fen_glasart_1'])

# 1: 1-S-Glas                                           
# 2: 2-S-Glas
# 3: 3-S-Glas
# 4: PH-Fenster'
cleanup_glass_solar_transmittance = {'glass_solar_transmittance':{
                                                                1: 0.87,                                           
                                                                2: 0.78, 
                                                                3: 0.7,
                                                                4: 0.53}}
building_data.replace(cleanup_glass_solar_transmittance, inplace = True)


# Energiedurchlassgrad der Verglasung bei aktiviertem Sonnenschutz (glass_solar_shading_transmittance)
##############################################################################
# Map 'qD8' from be_data_original as column 'qD8' to building_data
building_data['qD8'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qD8'])

# 1: 'Sonnenschutzverglasung',                                           
# 2: 'Außenliegende variable Sonnenschutzvorrichtung (z.B. Lamellen-Raffstoren)', 
# 3: 'Außenliegende feststehende Sonnenschutzvorrichtung',
# 4: 'In der Verglasung liegende Sonnenschutzvorrichtung',
# 5: 'Innenliegende Sonnenschutzvorrichtung',
# 6: 'Keine Sonnenschutzvorrichtung'

# Shading factor (Abschattungsfaktor) Fc [See DIN 4108-2:2013-02, p. 25]
cleanup_glass_solar_shading_transmittance = {'qD8':{
                                                    1: 1,                                           
                                                    2: 0.22, 
                                                    3: 0.32,
                                                    4: 0.78,
                                                    5: 0.78,
                                                    6: 1}}
building_data.replace(cleanup_glass_solar_shading_transmittance, inplace = True)

building_data['glass_solar_shading_transmittance'] = building_data['glass_solar_transmittance'] * building_data['qD8']   


# Lichttransmissionsgrad der Verglasung (glass_light_transmittance)
##############################################################################
# Map 'Fen_glasart_1' from be_data_original as column 'qD8' to building_data
building_data['Fen_glasart_1'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['Fen_glasart_1'])

# k_1 = 0.7 if no further information is available [See DIN V 18599-4:2018-09, p.39]
building_data['k_1'] =  0.7

# k_3 = 0.85 [See DIN V 18599-4:2018-09, p.39]
building_data['k_3'] =  0.85

# tau_D65SNA [See DIN V 18599-4:2018-09, p.40]
def assign_tau_D65SNA(row):
    if row['Fen_glasart_1'] == '1-S-Glas':
        tau_D65SNA = 0.9
    elif row['Fen_glasart_1'] == '2-S-Glas':
        tau_D65SNA = 0.82  
    elif row['Fen_glasart_1'] == '3-S-Glas':
        tau_D65SNA = 0.75
    else: # PH-Glas --> Mean WDG 3-fach
        tau_D65SNA = 0.705
    return tau_D65SNA
        
building_data['tau_D65SNA'] = building_data.apply(assign_tau_D65SNA, axis = 1)   
    
building_data['glass_light_transmittance'] = building_data['k_1'] * building_data['lighting_maintenance_factor'] * building_data['k_3'] * building_data['tau_D65SNA']


# U-Wert Fenster (u_windows)
##############################################################################
building_data['u_windows'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['U_fen'])


# U-Wert Außenwände (u_walls)
##############################################################################
building_data['u_walls'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['U_AW'])


# U-Wert Dach (u_roof)
##############################################################################
building_data['u_roof'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['U_D'])


# U-Wert Bodenplatte/Kellerdecke (u_base)
##############################################################################
building_data['u_base'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['U_K'])


# Temperaturanpassungsfaktor unterer Gebäudeabschluss (temp_adj_base)
##############################################################################
building_data['n_UG'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['n_UG'])

# Find corresponding case according to DIN V 4108-6:2003-06
def fall_temp_adj_base(row):
    if row['n_UG'] == 0:                                                           # If there's no basement, Case 12
        return_value = 12                                                                       
    else:
        return_value = 16                                                          # Case 16, not heated
    return return_value

building_data['case_temp_adj_base'] = building_data.apply(fall_temp_adj_base, axis = 1)   

arrays_fx = [['<5', '<5', '5 bis 10', '5 bis 10',  '>10', '>10'], ['<=1', '>1', '<=1', '>1', '<=1', '>1']]
tuples_fx = list(zip(*arrays_fx))

index_fx = pd.MultiIndex.from_tuples(tuples_fx, names = ['B', 'R'])
fx = pd.DataFrame(([0.3, 0.45, 0.25, 0.4, 0.2, 0.35],
                    [0.4, 0.6, 0.4, 0.6, 0.4, 0.6],
                    [0.45, 0.6, 0.4, 0.5, 0.25, 0.35],
                    [0.55, 0.55, 0.5, 0.5, 0.45, 0.45],
                    [0.7, 0.7, 0.65, 0.65, 0.55, 0.55]), index=['10', '11', '12', '15', '16'], columns=index_fx)
fx = fx.unstack().reset_index()
fx = fx.rename(columns = {'level_2': 'case_temp_adj', 0: 'temp_adj_factors'})
fx['case_temp_adj'] = fx['case_temp_adj'].astype(int)

building_data['building_length_n'] = building_data['geb_f_flaeche_n_iwu'] / building_data['building_height']
building_data['building_length_s'] = building_data['geb_f_flaeche_s_iwu'] / building_data['building_height']
building_data['building_length_o'] = building_data['geb_f_flaeche_o_iwu'] / building_data['building_height']
building_data['building_length_w'] = building_data['geb_f_flaeche_w_iwu'] / building_data['building_height']

building_data['B_raw'] = (2 * building_data[['building_length_n', 'building_length_s']].values.max(1)) + (2 * building_data[['building_length_o', 'building_length_w']].values.max(1))

def clean_B(row):
    if row['B_raw'] < 5:
        value = '<5'
    elif 5 <= row['B_raw'] <= 10:
        value = '5 bis 10'   
    else:
        value = '>10'
    return value    
building_data['B'] = building_data.apply(clean_B, axis = 1) 

building_data['R_raw'] = 1 / building_data['u_base']
def clean_R(row):
    if row['R_raw'] <= 1:
        value = '<=1'
    else:
        value = '>1'
    return value  
building_data['R'] = building_data.apply(clean_R, axis = 1)

building_data = pd.merge(building_data, fx, left_on = ['B', 'R', 'case_temp_adj_base'], right_on = ['B', 'R', 'case_temp_adj'], how = 'left' )


# Temperaturanpassungsfaktor unterirdische Außenwandflächen (temp_adj_walls_ug)
##############################################################################
def case_temp_adj_walls_ug(row):
    if row['n_UG'] > 0:
        return_value = 11
    else: 
        return_value = 0
    return return_value
 
building_data['case_temp_adj_walls_ug'] = building_data.apply(case_temp_adj_walls_ug, axis = 1)  
   
building_data = pd.merge(building_data, fx, left_on = ['B', 'R', 'case_temp_adj_walls_ug'], right_on = ['B', 'R', 'case_temp_adj'], how = 'left' )
building_data = building_data.drop(['case_temp_adj_x', 'case_temp_adj_y', 'n_UG'], axis = 1)     
building_data = building_data.rename(columns = {'temp_adj_factors_x': 'temp_adj_base', 
                                          'temp_adj_factors_y': 'temp_adj_walls_ug'})

# Fill NaNs with 0 
building_data['temp_adj_walls_ug'] = building_data['temp_adj_walls_ug'].replace(np.nan, 0)


# Luftwechselrate Infiltration (ach_inf)
##############################################################################
# Map minimum flow rate from data_18599_10_4 to building_data
building_data['V_min_18599'] = building_data['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['Außenluftvolumenstrom'])

# Map bak_grob
# 1: Altbau bis einschl. 1978
# 2: 1979 - 2009 (1. Wärmeschutzverordnung vor 2010)
# 3: Neubau ab 2010
building_data['bak_grob'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['bak_grob'])

# Min flow from DIN V 18599-10 in m³/hm², multiply by m²/m³ for air change rate
building_data['ach_min'] = (building_data['V_min_18599'] * building_data['net_room_area']) / (building_data['net_room_area'] * (building_data['building_height']/building_data['n_OG']))

building_data['qH1'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qH1'])
cleanup_rlt_encode = {"qH1": {
                            1: 'Nein, Fensterlüftung',
                            2: 'Nein, nur dezentrale Anlage(n) vorhanden',
                            3: 'Ja, zentrale Anlage(n) vorhanden',
                            4: 'Weiß nicht'}}
building_data.replace(cleanup_rlt_encode, inplace = True)

# n_50_standard_av: 
# 'Passivhausanforderung erfüllt': 0.6,
# 'Neubau mit Dichtheitstest und raumlufttechnische Anlage': 1,
# 'Neubau mit Dichtheitstest ohne raumlufttechnische Anlage': 2,
# 'Neubau ohne Dichtheitstest': 4,
# 'Bestehendes Gebäude ohne Dichtheitstest': 6,
# 'Bestehndes Gebäude mit offensichtlichen Undichtheiten': 10
def assign_n_50_standard_av(row):
    if row['bak_grob'] == 3:
        if row['qH1'] == 'Ja, zentrale Anlage(n) vorhanden':
            n_50_standard_av = 1
        else:
            n_50_standard_av = 2
    elif row['bak_grob'] == 2:
        n_50_standard_av = 4
    else:
        n_50_standard_av = 6
    return n_50_standard_av  
   
building_data['n_50_standard_av'] = building_data.apply(assign_n_50_standard_av, axis = 1)  
      
building_data['standard av-verhältnis'] = 0.9

# AV-Verhältnis Gebäude = Thermische Hüllfläche des Gebäudes / beheiztes Bruttogebäudevolumen
building_data['facade_area'] = building_data['geb_f_flaeche_n_iwu'] + building_data['geb_f_flaeche_o_iwu'] + building_data['geb_f_flaeche_s_iwu'] + building_data['geb_f_flaeche_w_iwu']
building_data['av-verhältnis'] = (building_data['facade_area'] + building_data['roof_area'] + (building_data['base_area'])) / (building_data['base_area'] * building_data['building_height'])

# Luftdichtheit n50
building_data['n_50'] = building_data['n_50_standard_av'] * building_data['av-verhältnis'] / building_data['standard av-verhältnis']

# Abschätzung der Infiltrationsluftwechselrate nach ISO 13789 bzw. der früheren EN 832
# ach_inf = n_50 * e * fATD
# mit e = 0.07 (DIN V 18599-2, S. 58)
# mit fATD = 1 (keine Außenluftdurchlässe: Annahme, da keine Informationen vorhanden)
building_data['ach_inf'] = building_data['n_50'] * 0.07


# Luftwechselrate Fenster (ach_win)
##############################################################################
def calc_ach_win(row):
    if row['qH1'] in ('Nein, Fensterlüftung', 'Nein, nur dezentrale Anlage(n) vorhanden', 'Weiß nicht'):
        ach_win = max(0.1, (row['ach_min'] - row['ach_inf']))
    else:
        ach_win = 0.1
    return ach_win  
building_data['ach_win'] = building_data.apply(calc_ach_win, axis = 1) 


# Luftwechselrate RLT (ach_vent)
##############################################################################
def calc_ach_vent(row):
    if row['qH1'] == 'Ja, zentrale Anlage(n) vorhanden':
        ach_vent = max(0.1, (row['ach_min'] - row['ach_inf']))
    else:
        ach_vent = 0.1
    return ach_vent  
building_data['ach_vent'] = building_data.apply(calc_ach_vent, axis = 1) 


# Wirkungsgrad der Wärmerückgewinnungseinheit RLT (heat_recovery_efficiency)
##############################################################################
building_data['qH3'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qH3'])

cleanup_rlt_funkt_encode = {"qH3": {
                            1: 'Wärmerückgewinnung',
                            2: 'Heizen (zusätzlich zur Wärmerückgewinnung)',
                            3: 'Kühlen',
                            4: 'Befeuchten',
                            5: 'Entfeuchten',
                            6: 'Abluft',
                            7: 'Zuluft',
                            8: 'Umluft'}}
building_data.replace(cleanup_rlt_funkt_encode, inplace = True)

def find_heat_recovery_efficiency(row):
    if row['qH3'] in ('Wärmerückgewinnung', 'Heizen (zusätzlich zur Wärmerückgewinnung)'):
            heat_recovery_efficiency = 0.7
    else:
        heat_recovery_efficiency = 0
    return heat_recovery_efficiency  
building_data['heat_recovery_efficiency'] = building_data.apply(find_heat_recovery_efficiency, axis = 1) 


# Wärmespeicherfähigkeit (thermal_capacitance)
##############################################################################
building_data['thermal_capacitance'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['AW_konstr_1']).astype(str)

# 1,0: Massive Bauweise (z.B. Mauerwerk, Beton) / keine Angabe (weiß nicht)
# 1,10: Massive Bauweise (z.B. Mauerwerk, Beton) / Einschalige, massive Bauweise mit leichten Baustoffen (z.B. Leicht- oder Porenbeton, Wärmedämmziegel)
# 1,11: Massive Bauweise (z.B. Mauerwerk, Beton) / Einschalige, massive Bauweise mit leichten Baustoffen (z.B. Leicht- oder Porenbeton, Wärmedämmziegel) mit Zusatzdämmung
# 1,20: Massive Bauweise (z.B. Mauerwerk, Beton) / Einschalige, massive Bauweise mit schweren Baustoffen (z.B. Stahlbeton, Ziegel, Naturstein)
# 1,30: Massive Bauweise (z.B. Mauerwerk, Beton) / Zweischalige, massive Bauweise (z.B. mit gemauerter Vorsatzschale vor einem mit Luft oder Dämmstoff gefüllten Zwischenraum)
# 1,40: Massive Bauweise (z.B. Mauerwerk, Beton) / Bauweise mit vorgehängter, hinterlüfteter Verkleidung (z.B. mit Metallpaneelen verkleidet oder mit vorgehängten Betonteilen bzw. Natursteinplatten)
# 1,50: Massive Bauweise (z.B. Mauerwerk, Beton) / Fertigteilbau (z.B. Betonfertigteile, Großtafelbauweise, Systembau)
# 2,0: Leichtbauweise (z.B. Holz, Metall, Fachwerk) / keine Angabe (weiß nicht)
# 2,10: Leichtbauweise (z.B. Holz, Metall, Fachwerk) / Sandwichpaneele
# 2,20: Leichtbauweise (z.B. Holz, Metall, Fachwerk) / Holztafel- oder Holzrahmenbauweise
# 2,30: Leichtbauweise (z.B. Holz, Metall, Fachwerk) / Fachwerkbauweise
# 3,0: Fassadensystem (z.B. Glasfassade) / keine Angabe (weiß nicht)
# 3,10: Fassadensystem (z.B. Glasfassade) / Pfosten-Riegel-Fassade (Glasfassade mit Pfosten)
# 3,20: Fassadensystem (z.B. Glasfassade) / Structural-Glazing-Fassade (halterlose Ganzglasfassade) 
# 3,30: Fassadensystem (z.B. Glasfassade) / Vorhangfassade
# 3,40: Fassadensystem (z.B. Glasfassade) / Doppelfassade

# Seperated cleanup for better readability
cleanup_thermal_capacitance_encode = {"thermal_capacitance": {
                                                            '1,0': 'schwer',
                                                            '1,10': 'mittel',
                                                            '1,11': 'mittel',
                                                            '1,20': 'schwer',
                                                            '1,30': 'schwer',
                                                            '1,40': 'schwer',
                                                            '1,50': 'schwer',
                                                            '2,0': 'leicht',
                                                            '2,10': 'leicht',
                                                            '2,20': 'leicht',
                                                            '2,30': 'leicht',
                                                            '3,0': 'mittel',
                                                            '3,10': 'mittel',
                                                            '3,20': 'mittel',
                                                            '3,30': 'mittel',
                                                            '3,40': 'mittel'}}
building_data.replace(cleanup_thermal_capacitance_encode, inplace = True)

# See EN ISO 13790:2008-09, p. 81 
cleanup_thermal_capacitance_assignment = {"thermal_capacitance": {
                                                              'schwer': 260000,
                                                              'mittel': 165000,
                                                              'leicht': 110000}}
building_data.replace(cleanup_thermal_capacitance_assignment, inplace = True)

# Sollwert Heizung (t_set_heating)
##############################################################################
building_data['t_set_heating'] = building_data['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['Raum-Solltemperatur Heizung'])


# Anfangstemperatur im Gebäude (t_start)
##############################################################################
building_data['t_start'] = building_data['t_set_heating']


# Sollwert Kühlung (t_set_cooling)
##############################################################################
building_data['t_set_cooling'] = building_data['typ_18599'].map(data_18599_10_4.set_index('typ_18599')['Raum-Solltemperatur Kühlung'])


# Nachtlüftung (night_flushing_flow)
##############################################################################
building_data['night_flushing_flow'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qI1Av6'])

# Gebäude, ggf. zusätzlich, durch sommerliche Nachtlüftung passiv oder durch freie Kühlung gekühlt? 
# 1: Ja, ausschließlich passive Kühlung durch sommerliche Nachtlüftung
# 2: Ja, ausschließlich freie Kühlung z.B. durch Rückkühlwerke, Grundwasser o.ä.
# 3: Ja, beides
# 4: Nein

def night_flushing_flow(row):
    if row['night_flushing_flow'] == 4:
        flow_rate = 0
    else: 
        flow_rate = 2
    return flow_rate

building_data['night_flushing_flow'] = building_data.apply(night_flushing_flow, axis = 1)     


# Max. Heizlast (max_heating_energy_per_floor_area)
##############################################################################
# Set to inf (no further information available)
building_data['max_heating_energy_per_floor_area'] = np.inf


# Max. Kühllast (max_cooling_energy_per_floor_area)
##############################################################################
# Set to -inf (no further information available)
building_data['max_cooling_energy_per_floor_area'] = -np.inf


# Art der Heizanlage (heating_supply_system)
##############################################################################
building_data['heating_supply_system'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['w_erz_art_et']).astype(str)
    
# 108	 zentral elektrisch	Sonstige zentral elektrische Wärmeerzeuger oder keine Angabe	elektr. Strom
# 118	 zentral elektrisch	Wärmepumpe	elektr. Strom
# 128	 zentral elektrisch	zentraler, elektrisch beheizter Wärmeerzeuger	elektr. Strom
# 208	 dezentral elektrisch	Sonstige dezentral elektrische Wärmeerzeuger oder keine Angabe	elektr. Strom
# 218	 dezentral elektrisch	Elektrische Direktheizung 	elektr. Strom
# 228	 dezentral elektrisch	Elektrische Nachtspeicherheizung	elektr. Strom
# 301	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Erdgas
# 302	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Flüssiggas
# 303	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Heizöl
# 304	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Bioöl/-gas
# 305	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Holz
# 306	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	feste Biomasse
# 307	 zentral Brennstoff	 Sonstige zentral Brennstoff Wärmeerzeuger oder keine Angabe	Kohle
# 311	 zentral Brennstoff	 Heizkessel	Erdgas
# 312	 zentral Brennstoff	 Heizkessel	Flüssiggas
# 313	 zentral Brennstoff	 Heizkessel	Heizöl
# 314	 zentral Brennstoff	 Heizkessel	Bioöl/-gas
# 315	 zentral Brennstoff	 Heizkessel	Holz
# 316	 zentral Brennstoff	 Heizkessel	feste Biomasse
# 317	 zentral Brennstoff	 Heizkessel	Kohle
# 321	 zentral Brennstoff	 KraftWärme-Kopplungsanlage (z.B. BHKW)	Erdgas
# 322	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	Flüssiggas
# 323	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	Heizöl
# 324	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	Bioöl/-gas
# 325	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	Holz
# 326	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	feste Biomasse
# 327	 zentral Brennstoff	 Kraft-Wärme-Kopplungsanlage (z.B. BHKW)	Kohle
# 331	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	Erdgas
# 332	 zentral Brennstoff Wärmepumpe (mit Brennstoff betrieben)	Flüssiggas
# 333	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	Heizöl
# 334	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	Bioöl/-gas
# 335	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	Holz
# 336	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	feste Biomasse
# 337	 zentral Brennstoff	 Wärmepumpe (mit Brennstoff betrieben)	Kohle
# 401	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Erdgas
# 402	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Flüssiggas
# 403	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Heizöl
# 404	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Bioöl/gas
# 405	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Holz
# 406	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	feste Biomasse
# 407	 dezentral Brennstoff	Sonstige dezentral Brennstoff Wärmeerzeuger oder keine Angabe	Kohle
# 411	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Erdgas
# 412	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Flüssiggas
# 413	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Heizöl
# 414	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Bioöl/gas
# 415	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Holz
# 416	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	feste Biomasse
# 417	 dezentral Brennstoff	Öfen, dezentral, mit Brennstoff betrieben	Kohle
# 421	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Erdgas
# 422	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Flüssiggas
# 423	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Heizöl
# 424	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Bioöl/gas
# 425	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Holz
# 426	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	feste Biomasse
# 427	 dezentral Brennstoff	Gas-betriebene Hell- oder Dunkelstrahler	Kohle
# 431	 dezentral Brennstoff	Dezentrale Etagenheizung	Erdgas
# 432	 dezentral Brennstoff	Dezentrale Etagenheizung	Flüssiggas
# 433	 dezentral Brennstoff	Dezentrale Etagenheizung	Heizöl
# 434	 dezentral Brennstoff	Dezentrale Etagenheizung	Bioöl/gas
# 435	 dezentral Brennstoff	Dezentrale Etagenheizung	Holz
# 436	 dezentral Brennstoff	Dezentrale Etagenheizung	feste Biomasse
# 437	 dezentral Brennstoff	Dezentrale Etagenheizung	Kohle
# 509	 Nah- oder Fernwärme	Sonstige Nah- oder Fernwärme oder keine Angabe	FW / NW
# 519	 Nah- oder Fernwärme	Heizwerken mit fossilem Brennstoff	FW / NW
# 529	 Nah- oder Fernwärme	Heizwerken mit erneuerbarem Brennstoff	FW / NW
# 539	 Nah- oder Fernwärme	Kraft-Wärme-Kopplung mit fossilem Brennstoff	FW / NW
# 549	 Nah- oder Fernwärme	Kraft-Wärme-Kopplung mit erneuerbarem Brennstoff	FW / NW
# 559	 Nah- oder Fernwärme	Abwärme (z.B. aus industriellen Prozessen)	FW / NW
# -8   trifft nicht zu
    
cleanup_heating_supply_system = {"heating_supply_system": {
                                                        '108': 'ElectricHeating',
                                                        '118': 'HeatPumpGroundSource',
                                                        '128': 'ElectricHeating',
                                                        '208': 'ElectricHeating',
                                                        '218': 'ElectricHeating',
                                                        '228': 'ElectricHeating',
                                                        '301': 'GasBoilerCondensingFrom95',
                                                        '302': 'LGasBoilerCondensingFrom95',
                                                        '303': 'OilBoilerCondensingFrom95',
                                                        '304': 'BiogasOilBoilerCondensingFrom95',
                                                        '305': 'WoodPelletSolidFuelBoiler',
                                                        '306': 'WoodPelletSolidFuelBoiler',
                                                        '307': 'CoalSolidFuelBoiler',
                                                        '311': 'GasBoilerCondensingFrom95',
                                                        '312': 'LGasBoilerCondensingFrom95',
                                                        '313': 'OilBoilerCondensingFrom95',
                                                        '314': 'BiogasOilBoilerCondensingFrom95',
                                                        '315': 'WoodPelletSolidFuelBoiler',
                                                        '316': 'WoodPelletSolidFuelBoiler',
                                                        '317': 'CoalSolidFuelBoiler',
                                                        '321': 'GasCHP',
                                                        '322': 'GasCHP',
                                                        '323': 'GasCHP',
                                                        '324': 'GasCHP',
                                                        '325': 'GasCHP',
                                                        '326': 'GasCHP',
                                                        '327': 'GasCHP',
                                                        '331': 'HeatPumpGroundSource',
                                                        '332': 'HeatPumpGroundSource',
                                                        '333': 'HeatPumpGroundSource',
                                                        '334': 'HeatPumpGroundSource',
                                                        '335': 'HeatPumpGroundSource',
                                                        '336': 'HeatPumpGroundSource',
                                                        '337': 'HeatPumpGroundSource',
                                                        '401': 'GasBoilerCondensingFrom95',
                                                        '402': 'LGasBoilerCondensingFrom95',
                                                        '403': 'OilBoilerCondensingFrom95',
                                                        '404': 'BiogasOilBoilerCondensingFrom95',
                                                        '405': 'WoodPelletSolidFuelBoiler',
                                                        '406': 'WoodPelletSolidFuelBoiler',
                                                        '407': 'CoalSolidFuelBoiler',
                                                        '411': 'SolidFuelLiquidFuelFurnace',
                                                        '412': 'SolidFuelLiquidFuelFurnace',	
                                                        '413': 'SolidFuelLiquidFuelFurnace',	
                                                        '414': 'SolidFuelLiquidFuelFurnace',	
                                                        '415': 'SolidFuelLiquidFuelFurnace',	
                                                        '416': 'SolidFuelLiquidFuelFurnace',	
                                                        '417': 'SolidFuelLiquidFuelFurnace',	
                                                        '421': 'GasBoilerLowTempBefore95',
                                                        '422': 'LGasBoilerLowTempBefore95',
                                                        '423': 'OilBoilerLowTempBefore95',
                                                        '424': 'BiogasOilBoilerLowTempBefore95',
                                                        '425': 'WoodSolidFuelBoilerCentral',
                                                        '426': 'WoodSolidFuelBoilerCentral',
                                                        '427': 'CoalSolidFuelBoiler',
                                                        '431': 'GasBoilerCondensingImproved',
                                                        '432': 'LGasBoilerCondensingImproved',
                                                        '433': 'OilBoilerCondensingImproved',
                                                        '434': 'BiogasOilBoilerCondensingImproved',
                                                        '435': 'WoodPelletSolidFuelBoiler',
                                                        '436': 'WoodPelletSolidFuelBoiler',
                                                        '437': 'CoalSolidFuelBoiler',
                                                        '509': 'DistrictHeating',
                                                        '519': 'DistrictHeating',
                                                        '529': 'DistrictHeating',
                                                        '539': 'DistrictHeating',
                                                        '549': 'DistrictHeating',
                                                        '559': 'DistrictHeating',
                                                        '-8': 'NoHeating'}}
building_data.replace(cleanup_heating_supply_system, inplace = True)


# Art der Kühlanlage (cooling_supply_system)
##############################################################################
building_data['cooling_supply_system'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['k_erz_art_rk']).astype(str)

cleanup_cooling_supply_system_encode = {"cooling_supply_system": {
                                                            '1': 'Kompressionskältemaschine (elektrisch betrieben), weiß nicht',
                                                            '11': 'Kompressionskältemaschine (elektrisch betrieben), Wasserkühlung (trocken)',
                                                            '12': 'Kompressionskältemaschine (elektrisch betrieben), Wasserkühlung (trocken)',
                                                            '13': 'Kompressionskältemaschine (elektrisch betrieben), Luftkühlung',
                                                            '2': 'Absorptionskälte-maschine (mit Wärme betrieben), weiß nicht',
                                                            '21': 'Absorptionskälte-maschine (mit Wärme betrieben), Wasser-kühlung (trocken)',
                                                            '22': 'Absorptionskälte-maschine (mit Wärme betrieben), Wasser-kühlung (nass)',
                                                            '3': 'Nah- oder Fernkälte',
                                                            '-8': 'trifft nicht zu',
                                                            '-7': 'weiß nicht'}}
building_data.replace(cleanup_cooling_supply_system_encode, inplace = True)

# Seperated cleanup for better readability
cleanup_cooling_supply_system_assignment = {"cooling_supply_system": {
                                                            'Kompressionskältemaschine (elektrisch betrieben), weiß nicht': 'WaterCooledPistonScroll',
                                                            'Kompressionskältemaschine (elektrisch betrieben), Wasserkühlung (trocken)': 'WaterCooledPistonScroll',
                                                            'Kompressionskältemaschine (elektrisch betrieben), Wasserkühlung (trocken)': 'WaterCooledPistonScroll',
                                                            'Kompressionskältemaschine (elektrisch betrieben), Luftkühlung': 'AirCooledPistonScroll',
                                                            'Absorptionskälte-maschine (mit Wärme betrieben), weiß nicht': 'AbsorptionRefrigerationSystem',
                                                            'Absorptionskälte-maschine (mit Wärme betrieben), Wasser-kühlung (trocken)': 'AbsorptionRefrigerationSystem',
                                                            'Absorptionskälte-maschine (mit Wärme betrieben), Wasser-kühlung (nass)': 'AbsorptionRefrigerationSystem',
                                                            'Nah- oder Fernkälte': 'DistrictCooling',
                                                            'trifft nicht zu': 'NoCooling',
                                                            'weiß nicht': 'NoCooling'}}
building_data.replace(cleanup_cooling_supply_system_assignment, inplace = True)


# Art der Wärmeübergabe (heating_emission_system)
##############################################################################
building_data['heating_emission_system'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qG13'])

# 1: Heizkörper
# 2: Konvektoren
# 3: Fußbodenheizung
# 4: Deckenheizung (bzw. Heiz-Kühl-Decke)
# 5: Thermisch aktivierte Bauteile (Systeme, welche Gebäudemassen zur Temperaturregulierung nutzen, z.B. thermoaktive Decke)
# 6: Deckenstrahlplatten
# 7: Luftheizung (erzeugte Wärme wird über ein Gebläse oder eine raumlufttechnische Anlage eingebracht)

cleanup_heating_emission_system = {"heating_emission_system": {
                                                              1: 'AirConditioning',
                                                              2: 'AirConditioning',
                                                              3: 'SurfaceHeatingCooling',
                                                              4: 'AirConditioning',
                                                              5: 'ThermallyActivated',
                                                              6: 'AirConditioning',
                                                              7: 'AirConditioning'}}
building_data.replace(cleanup_heating_emission_system, inplace = True)

# If there's no heating_supply_system, there can't be any heating
building_data['heating_emission_system'] = np.where(building_data['heating_supply_system'] == 'NoHeating', 'NoHeating', building_data['heating_emission_system'])


# Art der Kälteübergabe (cooling_emission_system)
##############################################################################
building_data['cooling_emission_system'] = building_data['scr_gebaeude_id'].map(be_data_original.set_index('scr_gebaeude_id')['qI11'])

# 1: Klimaanlage (raumlufttechnische Anlage)
# 2: Ventilatorkonvektoren (z.B. in der Fensterbrüstung)
# 3: Kühldecke (bzw. Heiz-Kühl-Decke)
# 4: Thermisch aktivierte Bauteile

cleanup_cooling_emission_system = {"cooling_emission_system": {
                                      1: 'AirConditioning',
                                      2: 'AirConditioning',
                                      3: 'AirConditioning',
                                      4: 'ThermallyActivated'}}
building_data.replace(cleanup_cooling_emission_system, inplace = True)

# If there's no cooling_supply_system, there can't be any cooling
building_data['cooling_emission_system'] = np.where(building_data['cooling_supply_system'] == 'NoCooling', 'NoCooling', building_data['cooling_emission_system'])


##############################################################################
# Delete unnecessary columns
building_data.drop(['typ_18599', 'Fen_ant', 'geb_f_flaeche_n_iwu', 'geb_f_flaeche_o_iwu', 'geb_f_flaeche_s_iwu', 'geb_f_flaeche_w_iwu', 'building_length_n', 'building_length_s', 'building_length_o', 'building_length_w', 'n_OG', 'qD8', 'Fen_glasart_1', 'k_1', 'k_3', 'tau_D65SNA', 'case_temp_adj_base', 'B_raw', 'B', 'R_raw', 'R', 'case_temp_adj_walls_ug', 'V_min_18599', 'bak_grob', 'ach_min', 'qH1', 'n_50_standard_av', 'standard av-verhältnis', 'facade_area', 'av-verhältnis', 'n_50', 'qH3'], axis = 1, inplace = True)  

# Save data to \iso_simulator\examples\SimulationData_Breitenerhebung.csv
building_data.to_csv(r'..\..\iso_simulator\examples\SimulationData_Breitenerhebung.csv', index = False, sep = ';') 