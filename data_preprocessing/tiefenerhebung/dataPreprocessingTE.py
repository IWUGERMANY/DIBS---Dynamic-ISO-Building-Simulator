"""
Module serves for data generation from original TE-Data to a modified input dataset used as input in annualSimulation.py


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2021, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2021, Institut Wohnen und Umwelt"
__license__ = "MIT"

import pandas as pd
import numpy as np
import warnings
from pandas.core.common import SettingWithCopyWarning


# Ignore CopyWarnings caused by map() [See: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy]
warnings.simplefilter(action = "ignore", category = SettingWithCopyWarning)


##############################################################################
# Inputdatensätze
##############################################################################
# Datensatz Tiefenerhebung
data_te = pd.read_excel(r'TE_data/#Alle_Daten_DB_TE_inkl_TEK_GEO_Auszug.xlsx', dtype={'TEK_res_energy_relevant_area': float})
# data_te = pd.read_excel(r'TE_data/#Alle_Daten_DB_TE_inkl_TEK_GEOneu.xlsx', dtype={'TEK_res_energy_relevant_area': float}) #1


# # (Imputierter) Datensatz mit Angaben zur maximalen Personenbelegung aus Breitenerhebung
# # Verwendet, da in im originalen BE Datensatz (data_be_original) für einige Gebäude die Angabe zur maximalen Personenbelegung fehlt
max_occupancy_be_imputiert = pd.read_excel(r'TE_data/DB_BE_q25_1_imputiert_Auszug.xlsx')
# max_occupancy_be_imputiert = pd.read_excel(r'TE_data/DB_BE_q25_1_imputiert.xlsx')

# Auswahl des Heating Supply Systems via Excel # SIEHE UNTEN
heating_supply_system_more_than_one_adj = pd.read_excel(r'TE_data/heating_supply_system_more_than_one_adj_Auszug.xlsx')
# heating_supply_system_more_than_one_adj = pd.read_excel(r'TE_data/heating_supply_system_more_than_one_adj.xlsx')
  
##############################################################################
# Verschneidungen
##############################################################################
## Daten aus Breitenerhebung für Gebäude in Tiefenerhebung
data_te_ids = data_te[['pr_var_name']]

# Überprüfe ob Gebäude aus TE auch in der BE sind
data_be_te = max_occupancy_be_imputiert[max_occupancy_be_imputiert['scr_gebaeude_id'].isin(data_te_ids['pr_var_name'])]
# --> 4 Gebäude aus Tiefenerhebung sind nicht im Datensatz der Breitenerhebung
data_te_subset = data_te[['pr_var_name']]
data_te_subset = data_te_subset.rename(columns = {'pr_var_name': 'scr_gebaeude_id'})
data_be_te_subset = data_be_te[['scr_gebaeude_id']]
# te_not_in_be = data_be_te_subset.append(data_te_subset).drop_duplicates(keep = False)

del data_te_ids, data_te_subset, data_be_te_subset

# Anzureichernder Datensatz der im Folgenden verwendet wird
data_final = pd.DataFrame(data_be_te['scr_gebaeude_id'].reset_index(drop = True))
    

# plz aus TE #################################################################
##############################################################################
# PLZ aus data_te für jedes Gebäude in data_final überführen
data_final['plz'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['PLZ_location_correct'])
data_final['plz'] = data_final['plz'].astype(int)

# Baujahr ####################################################################
##############################################################################
data_final['baujahr'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_year'])


# hk_geb und uk_geb aus BE ###################################################
##############################################################################
data_final['hk_geb'] = data_final['scr_gebaeude_id'].map(data_be_te.set_index('scr_gebaeude_id')['hk_geb'])
data_final['uk_geb'] = data_final['scr_gebaeude_id'].map(data_be_te.set_index('scr_gebaeude_id')['uk_geb'])

cleanup_hk_geb = {"hk_geb": {1: 'Büro-, Verwaltungs- oder Amtsgebäude',                                           
                             2: 'Gebäude für Forschung und Hochschullehre',                                        
                             3: 'Gebäude für Gesundheit und Pflege',                                               
                             4: 'Schule, Kindertagesstätte und sonstiges Betreuungsgebäude',                       
                             5: 'Gebäude für Kultur und Freizeit',                                                 
                             6: 'Sportgebäude',                                                                    
                             7: 'Beherbergungs- oder Unterbringungsgebäude, Gastronomie- oder Verpflegungsgebäude', 
                             8: 'Produktions-, Werkstatt-, Lager- oder Betriebsgebäude',                           
                             9: 'Handelsgebäude',                                                                 
                             10: 'Technikgebäude (Ver- und Entsorgung)',                                            
                             11: 'Verkehrsgebäude',                                                                 
                             12: 'Sonstiges Nichtwohngebäude'}}

cleanup_uk_geb = {"uk_geb": {1.01: 'Parlaments- oder Gerichtsgebäude',                                                                                                                                 
                             1.02: 'Öffentliches Verwaltungs- oder Ämtergebäude, Rathaus',                      
                             1.03: 'Bürogebäude',                                                               
                             1.04: 'Rundfunk- oder Fernsehanstalt',                                             
                             1.05: 'Polizeipräsidium oder -station, Bürogebäude sonstiger Bereitschaftsdienste',
                             1.06: 'Sonstige Gebäudefunktion',
                             2.01: 'Hörsaalgebäude',                                                                                                                                                                                        
                             2.02: 'Verwaltungs- oder Seminargebäude',                                                                                                                                                                
                             2.03: 'Institutsgebäude für Forschung und Lehre (Labor mit geringen Anforderungen an die Raumlufttechnik, z.B. Medizin, Informatik)',
                             2.04: 'Institutsgebäude für Forschung und Lehre (Labor mit hohen Anforderungen an die Raumlufttechnik, z.B. Chemie, Tierforschung)', 
                             2.05: 'Bürogebäude von Forschungsanstalten ohne Lehre',                                                                              
                             2.06: 'Laborgebäude von Forschungsanstalten und Unternehmen (Labor mit geringen Anforderungen an die Raumlufttechnik)',              
                             2.07: 'Laborgebäude von Forschungsanstalten und Unternehmen (Labor mit hohen Anforderungen an die Raumlufttechnik)',                 
                             2.08: 'Sonstiges Gebäudefunktion',
                             3.01: 'Hochschulklinik',                                                                                                                                          
                             3.02: 'Krankenhaus',                                                                  
                             3.03: 'Gebäude für teilstationäre Versorgung (z.B. Tagesklinik, Geburtshaus)',        
                             3.04: 'Rehabilitation',                                                               
                             3.05: 'Kur und Genesung',                                                             
                             3.06: 'Medizinisches Versorgungszentrum, Ärztehaus',                            
                             3.07: 'Arztpraxis',                                                                   
                             3.08: 'Notfallpraxis',                                                                
                             3.09: 'Altenheim/Altenpflegeheim (ohne eigene Haushaltsführung der Bewohner/innen)',
                             3.10: 'Pflegeheim für Behinderte (ohne eigene Haushaltsführung der Bewohner/innen)',
                             3.11: 'Psychiatrische Pflegeheim (ohne eigene Haushaltsführung der Bewohner/innen)',
                             3.12: 'Tagespflegeeinrichtung',                                                     
                             3.13: 'Hospiz',                                                                     
                             3.14: 'Sonstige Gebäudefunktion',
                             4.01: 'Schule, allgemein',                                                                                       
                             4.02: 'Ganztagesschule',                                                              
                             4.03: 'Internatsschule',                                                              
                             4.04: 'Förder-, Sonderschule',                                                        
                             4.05: 'Berufsbildende Schule (gewerblich, wirtschaftlich)',                          
                             4.06: 'Berufsbildende Schule (mit höherer technischer Ausstattung, z.B. Werkstätten)',
                             4.07: 'Berufsakademie, Berufskolleg',                                                 
                             4.08: 'Bildungszentrum',                                                              
                             4.09: 'Ausbildungsstätte',                                                            
                             4.10: 'Volkshochschule',                                                              
                             4.11: 'KiTa',                                                                         
                             4.12: 'KiTa mit Küche',                                                               
                             4.13: 'Studentenhaus',                                                                
                             4.14: 'Altentagesstätte',                                                             
                             4.15: 'Jugendzentrum',                                                                
                             4.16: 'Sonstige Gebäudefunktion',
                             5.0: 'Freizeit-, Gemeinschafts-, Bürgerhaus', #! Sonstige uk_geb: Annahme Zuweisung anders Profils, da diese nicht in Norm existiert.
                             5.01: 'Bibliothek/Archiv (einfach, z.B. Stadtbücherei)',                                                            
                             5.02: 'Bibliothek/Archiv (höher technisiert, z.B. Unibibliothek)',       
                             5.03: 'Ausstellungsgebäude (Museen, Galerien)',                          
                             5.04: 'Oper, Theater und Veranstaltungshalle, Kino, Konferenzzentrum',
                             5.05: 'Freizeit-, Gemeinschafts-, Bürgerhaus',                           
                             5.06: 'Spielkasino, -bank, -halle',                                      
                             5.07: 'Sonstige Gebäudefunktion',
                             6.01: 'Einfeldhalle',                                                                   
                             6.02: 'Mehrfeldhalle',                                                   
                             6.03: 'Gymnastikhalle',                                                  
                             6.04: 'Sporthalle mit Mehrzwecknutzung',                                 
                             6.05: 'Hallenbad',                                                       
                             6.06: 'Spaß- und Freizeitbad',                                           
                             6.07: 'Thermalbad',                                                      
                             6.08: 'Hallenbad mit Freibadanlage',                                     
                             6.09: 'Kegelbahn/Bowling',                                               
                             6.10: 'Schießstand',                                                     
                             6.11: 'Raumschießanlage',                                                
                             6.12: 'Reithalle',                                                       
                             6.13: 'Eissporthalle',                                                   
                             6.14: 'Tennishalle',                                                     
                             6.15: 'Fitnessstudio',                                                   
                             6.16: 'Gebäude für Sportaußenanlage (Tribünen-, Umkleidegebäude)',       
                             6.17: 'Sonstige Gebäudefunktion',
                             7.01: 'Herberge, Ferienheim, Ferienhaus, Hotel/Pension einfach',                                       
                             7.02: 'Sterne-Hotel',                                                    
                             7.03: 'Ausschankwirtschaft',                                             
                             7.04: 'Speisegaststätte (einfach)',                                      
                             7.05: 'Restaurant (gehoben)',                                            
                             7.06: 'Mensa/Kantine',                                                   
                             7.07: 'Gemeinschaftsunterkunft (z.B. Flüchtlingsheim, Kaserne, Kloster)',
                             7.08: 'Sonstige Gebäudefunktion',
                             8.0: 'Gebäude für gewerbliche Produktion und Verarbeitung (z.B. Brauerei, Molkerei, Schlachthof)', #! Sonstige uk_geb: Annahme Zuweisung anders Profils, da diese nicht in Norm existiert.
                             8.01: 'Gebäude für gewerbliche Produktion und Verarbeitung (z.B. Brauerei, Molkerei, Schlachthof)',              
                             8.02: 'Gebäude für industrielle Produktion und Verarbeitung (z.B. Chemie, Metall, Textilien, Lebensmittel, Holz)',
                             8.03: 'Werkstattgebäude allgemein (z.B. von Handwerksbetrieben wie Klempner, Schlosser, Schreiner)',             
                             8.04: 'Werkstattgebäude zur Wartung, Instandsetzung, Reparatur (von z.B. Kfz)',                                  
                             8.05: 'Logistikimmobilie mit Toren bzw. Rampen',                                                                 
                             8.06: 'Sonstiges Gebäude für Lagerung',                                                                           
                             8.07: 'Feuerwehr, Rettungswache',                                                                                
                             8.08: 'Straßenmeisterei, Bauhof u.ä.',                                                                           
                             8.09: 'Fuhrpark',                                                                                                
                             8.10: 'zentrales Wirtschaftsgebäude (z.B. Zentralküche oder -wäscherei in Krankenhaus)',                       
                             8.11: 'Rechenzentrum',                                                                                         
                             8.12: 'Sonstige Gebäudefunktion',
                             9.0: 'Einkaufszentrum, Shopping-Mall', #! Sonstige uk_geb: Annahme Zuweisung anders Profils, da diese nicht in Norm existiert.
                             9.01: 'Handelsgebäude des Lebensmitteleinzel- und -großhandels',        
                             9.02: 'Handelsgebäude des Non-Food-Einzel- und -Großhandels',            
                             9.03: 'Einkaufszentrum, Shopping-Mall',                                  
                             9.04: 'Markthalle',                                                      
                             9.05: 'Messehalle',                                                     
                             9.06: 'von Dienstleistern (z.B. Frisör, Kosmetik) genutztes Ladengebäude',                                          
                             9.07: 'Sonstige Gebäudefunktion',
                             10.0: 'Gebäude für Lenkung, Steuerung, Überwachung und Nachrichtenübermittlung (z.B. Stellwerk, Leuchtturm)', #! Sonstige uk_geb: Annahme Zuweisung anders Profils, da diese nicht in Norm existiert.
                             10.01: 'Kraftwerk (Gesamtanlage für Energieversorgung)',                                                                      
                             10.02: 'Gebäude für Lenkung, Steuerung, Überwachung und Nachrichtenübermittlung (z.B. Stellwerk, Leuchtturm)',
                             10.03: 'Gebäude für Energieversorgung (z.B. Fernheizwerk, Tankstelle)',                                       
                             10.04: 'Gebäude für Wasserversorgung',                                                                        
                             10.05: 'Gebäude für Abwasserbehandlung',                                                                      
                             10.06: 'Gebäude für Abfallbehandlung',                                                                        
                             10.07: 'Sonstige Gebäudefunktion',
                             11.01: 'Park-/Garagengebäude, Fahrradparkhaus',                                                                                         
                             11.02: 'Halle für sonstige Verkehrsmittel (z.B. für Flugzeuge, Schienenfahrzeuge)',
                             11.03: 'Gebäude zur Pflege von Fahrzeugen (z.B. Waschstraße)',                    
                             11.04: 'Empfangsgebäude (Bahnhof, Busbahnhof, Flughafen, Schiffsterminal)',        
                             11.05: 'Sonstige Gebäudefunktion'}}

data_final.replace(cleanup_hk_geb, inplace = True)
data_final.replace(cleanup_uk_geb, inplace = True)

  
      
profile_zuweisung = pd.read_csv(r'TE_data/excel_export/profile_18599_10_zuweisung.csv', sep = ';', encoding= 'unicode_escape')
profile_data = pd.read_csv(r'TE_data/excel_export/profile_18599_10_data.csv', sep = ';', encoding= 'unicode_escape', decimal=",")

data_final['typ_18599'] = data_final['uk_geb'].map(profile_zuweisung.set_index('uk_geb')['typ_18599'])


# Setpoints ##################################################################
############################################################################## 
data_final['t_set_heating'] = data_final['typ_18599'].map(profile_data.set_index('typ_18599')['Raum-Solltemperatur Heizung'])

# Ersetze Raum-Solltemperatur für alle Arten von Schwimmbäder mit Temperaturen aus SIA2024
data_final['t_set_heating'] = np.where(((data_final['uk_geb'] == 'Hallenbad') |
                                       (data_final['uk_geb'] == 'Spaß- und Freizeitbad') |
                                       (data_final['uk_geb'] == 'Thermalbad') |
                                       (data_final['uk_geb'] == 'Hallenbad mit Freibadanlage')),
                                       24, data_final['t_set_heating'])

data_final['t_set_cooling'] = data_final['typ_18599'].map(profile_data.set_index('typ_18599')['Raum-Solltemperatur Kühlung'])

# Ersetze Raum-Solltemperatur für alle Arten von Schwimmbäder mit Temperaturen aus SIA2024
data_final['t_set_cooling'] = np.where(((data_final['uk_geb'] == 'Hallenbad') |
                                       (data_final['uk_geb'] == 'Spaß- und Freizeitbad') |
                                       (data_final['uk_geb'] == 'Thermalbad') |
                                       (data_final['uk_geb'] == 'Hallenbad mit Freibadanlage')),
                                       30, data_final['t_set_cooling'])


# mittlere Solltemp je Zone ##################################################
##############################################################################
soll_temp = data_final[['scr_gebaeude_id']]

for x in range(26):
    x += 1
    soll_temp['z_heat_temp_' + str(x)] = soll_temp['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_heat_temp_' + str(x)])
    soll_temp['z_cool_temp_' + str(x)] = soll_temp['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_cool_temp_' + str(x)])
    soll_temp['z_area_' + str(x)] = soll_temp['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_area_' + str(x)])
    soll_temp['z_heat_temp_' + str(x)] = soll_temp['z_heat_temp_' + str(x)].replace('?', 0)
    soll_temp['z_heat_temp_' + str(x)] = soll_temp['z_heat_temp_' + str(x)].replace('-', 0)
    soll_temp['z_cool_temp_' + str(x)] = soll_temp['z_cool_temp_' + str(x)].replace('?', 0)
    
    soll_temp.fillna(0, inplace = True)
    
# Nur die Flächen von Zonen im flächengewichteten Mittel berücksichtigen, von denen es Informationen über die Temperatur gibt     
soll_temp['sumproduct_zähler_heating'] = 0
soll_temp['sumproduct_nenner_heating'] = 0
soll_temp['sumproduct_zähler_cooling'] = 0
soll_temp['sumproduct_nenner_cooling'] = 0
for i in range(1,27):
    # sumproduct_zähler = z_heat_temp_1 * z_area_1 + z_heat_temp_2 * z_area_2 + ...
    soll_temp['sumproduct_zähler_heating'] += soll_temp['z_area_{}'.format(i)] * soll_temp['z_heat_temp_{}'.format(i)] 
    # sumproduct_nenner_heating: Summe der Fläche, aber nur wenn es Angabe zur Temperatur gibt
    soll_temp['sumproduct_nenner_heating'] += soll_temp['z_area_{}'.format(i)] * [1 if x > 0 else 0 for x in soll_temp['z_heat_temp_{}'.format(i)]]
    
    soll_temp['sumproduct_zähler_cooling'] += soll_temp['z_area_{}'.format(i)] * soll_temp['z_cool_temp_{}'.format(i)]
    soll_temp['sumproduct_nenner_cooling'] += soll_temp['z_area_{}'.format(i)] * [1 if x > 0 else 0 for x in soll_temp['z_cool_temp_{}'.format(i)]]
    
# Ergebnis     
soll_temp['t_heating'] = soll_temp['sumproduct_zähler_heating'] / soll_temp['sumproduct_nenner_heating']
soll_temp['t_cooling'] = soll_temp['sumproduct_zähler_cooling'] / soll_temp['sumproduct_nenner_cooling']

data_final['t_start'] = data_final['scr_gebaeude_id'].map(soll_temp.set_index('scr_gebaeude_id')['t_heating']) 

                                                                                                           
# energy_ref_area aus TE #####################################################
##############################################################################
# Errechnete Energiebezugsfläche aus TEK-Tool
data_final['energy_ref_area'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['TEK_res_energy_relevant_area'])


# net_room_area aus BE und TE ################################################
##############################################################################
# Aus TE
# Anteil thermisch konditionierter Fläche
data_final['building_area_value_heated_cooled_share'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['building_area_value_heated_cooled'])
# Nettoraumfläche = Energiebezugsfläche / Anteil therm. kond. Fläche
data_final['net_room_area'] = data_final['energy_ref_area'] / data_final['building_area_value_heated_cooled_share']
 

# thermal_capacitance ########################################################
##############################################################################
data_final['b_th_mass'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_th_mass'])
data_final['thermal_capacitance'] = data_final['b_th_mass'].copy()

# Aus DIN EN ISO 13790, Tab. 12, S.81
cleanup_thermal_capacitance = {"thermal_capacitance": {
                                'leicht': 110000,                                             
                                'mittelschwer': 165000,        
                                'schwer': 260000}}         
data_final.replace(cleanup_thermal_capacitance, inplace = True)


# building_height aus TE #####################################################
##############################################################################
data_final['b_storey_nr_1'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_storey_nr_1'])

# Wenn mittlere Anzahl der Vollgeschosse oberirdisch ohne Dachgeschoss Null ist, dann setze sie 1, 
# um eine Höhe bestimmen zu können. Hierbei handelt es sich bspw. um Lagerhallen
# Dies betrifft: NI4112617_0_00, NW4896249_1_00, NW7258792_0_00, NW977117_1_00
data_final['b_storey_nr_1'] = data_final['b_storey_nr_1'].replace(0, 1)

mittlere_geschosshöhe = data_final[['scr_gebaeude_id']]

#### Einschub 03.07.
# Berechne mittlere Geschosshöhe
for x in range(50):
    x += 1
    mittlere_geschosshöhe['z_height_' + str(x)] = mittlere_geschosshöhe['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_height_' + str(x)])
    mittlere_geschosshöhe['z_area_' + str(x)] = mittlere_geschosshöhe['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_area_' + str(x)])
    mittlere_geschosshöhe['z_th_cover_' + str(x)] = mittlere_geschosshöhe['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_th_cover_' + str(x)])

mittlere_geschosshöhe = mittlere_geschosshöhe.replace('ja', 1)
mittlere_geschosshöhe = mittlere_geschosshöhe.replace('nein', 0)
mittlere_geschosshöhe = mittlere_geschosshöhe.replace('2,,44', 2.44)
mittlere_geschosshöhe = mittlere_geschosshöhe.replace('2,,64', 2.64)
mittlere_geschosshöhe = mittlere_geschosshöhe.replace(np.nan, 0)

mittlere_geschosshöhe['sumproduct1'] = 0
mittlere_geschosshöhe['sumproduct2'] = 0
for i in range(1, 51):
   mittlere_geschosshöhe['sumproduct1'] += mittlere_geschosshöhe['z_height_{}'.format(i)] * mittlere_geschosshöhe['z_area_{}'.format(i)] * mittlere_geschosshöhe['z_th_cover_{}'.format(i)]
   mittlere_geschosshöhe['sumproduct2'] += mittlere_geschosshöhe['z_area_{}'.format(i)] * mittlere_geschosshöhe['z_th_cover_{}'.format(i)]

mittlere_geschosshöhe['mittlere_geschosshöhe'] = mittlere_geschosshöhe['sumproduct1'] / mittlere_geschosshöhe['sumproduct2'] / 0.86

data_final['mittlere_geschosshöhe'] = data_final['scr_gebaeude_id'].map(mittlere_geschosshöhe.set_index('scr_gebaeude_id')['mittlere_geschosshöhe'])

data_final['building_height'] = data_final['mittlere_geschosshöhe'] * data_final['b_storey_nr_1']


# base_area aus TE ##################################################
##############################################################################
# data_final['base_area'] = data_final['net_room_area'] / data_final['b_storey_nr_1']
data_final['base_area'] = data_final['energy_ref_area'] / (data_final['b_storey_nr_1'] * 0.87)


# building_width aus TE ######################################################
##############################################################################
data_final['building_width_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_l_fas_1'])
data_final['building_width_south'] = data_final['building_width_south'].replace(np.nan, 0) 
data_final['building_width_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_l_fas_4'])
data_final['building_width_north'] = data_final['building_width_north'].replace(np.nan, 0) 


# building_depth aus TE ######################################################
##############################################################################
data_final['building_depth_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_l_fas_2'])
data_final['building_depth_east'] = data_final['building_depth_east'].replace(np.nan, 0)  
data_final['building_depth_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_l_fas_3'])
data_final['building_depth_west'] = data_final['building_depth_west'].replace(np.nan, 0) 

data_final['building_width'] = data_final[['building_width_south', 'building_width_north']].values.max(1)
data_final['building_depth'] = data_final[['building_depth_east', 'building_depth_west']].values.max(1) 


# facade_area aus TE #########################################################
##############################################################################
# Länge der Fassade * Gebäudehöhe
data_final['facade_area_south'] = data_final['building_width_south'] * data_final['building_height']
# facade_area_east 
data_final['facade_area_east'] = data_final['building_depth_east'] * data_final['building_height']
# facade_area_west 
data_final['facade_area_west'] = data_final['building_depth_west'] * data_final['building_height']
# facade_area_north 
data_final['facade_area_north'] = data_final['building_width_north'] * data_final['building_height']


# window_share ###############################################################
##############################################################################
# Aus TE    
data_final['window_share_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_part_1'])
data_final['window_share_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_part_2'])
data_final['window_share_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_part_3'])
data_final['window_share_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_part_4'])
# Wandle Kommas zu Punkten
directions = ['south', 'east', 'north', 'west']
for i in directions:
    data_final['window_share_{}'.format(i)] = data_final['window_share_{}'.format(i)].replace(',','.', regex = True).astype(float).replace(np.nan, 0) 

# Fensterflächen
for i in directions:
    data_final['window_area_{}'.format(i)] = data_final['window_share_{}'.format(i)] * data_final['facade_area_{}'.format(i)] 


# Aus TE
data_final['window_share_te'] = (data_final['window_area_south'] + \
                                 data_final['window_area_west'] + \
                                 data_final['window_area_east'] + \
                                 data_final['window_area_north'])/ \
                                            (data_final['facade_area_south'] + data_final['facade_area_east'] + 
                                             data_final['facade_area_west'] + data_final['facade_area_north'])
data_final['window_share_te'] = data_final['window_share_te'].replace(np.nan, 0) 
      

# wall_area_og ##############################################################
##############################################################################
# Fassadenfläche - Fensterfläche
for i in directions:
    data_final['wall_area_og_{}'.format(i)] = data_final['facade_area_{}'.format(i)] - data_final['window_area_{}'.format(i)]

data_final['wall_area_og'] = data_final['wall_area_og_south'] + data_final['wall_area_og_east'] + data_final['wall_area_og_west'] + data_final['wall_area_og_north']


# wall_area_ug_heated #######################################################
##############################################################################
data_final['anzahl_geschosse_unterirdisch'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_storey_nr_unh'])
data_final['anzahl_geschosse_beheizt_unterirdisch'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_storey_nr_cel'])  

data_final['wall_area_ug_heated_south'] = data_final['building_width_south'] * data_final['anzahl_geschosse_beheizt_unterirdisch'] * data_final['mittlere_geschosshöhe']
data_final['wall_area_ug_heated_east'] = data_final['building_depth_east'] * data_final['anzahl_geschosse_beheizt_unterirdisch'] * data_final['mittlere_geschosshöhe']
data_final['wall_area_ug_heated_west'] = data_final['building_depth_west'] * data_final['anzahl_geschosse_beheizt_unterirdisch'] * data_final['mittlere_geschosshöhe']
data_final['wall_area_ug_heated_north'] = data_final['building_width_north'] * data_final['anzahl_geschosse_beheizt_unterirdisch'] * data_final['mittlere_geschosshöhe']

data_final['wall_area_ug'] = data_final['wall_area_ug_heated_south'] + data_final['wall_area_ug_heated_east'] + data_final['wall_area_ug_heated_west'] + data_final['wall_area_ug_heated_north']


# roof_area ##################################################################
##############################################################################
data_final['dachform'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_attic_cond'])

def teilbeheizungsfaktor_dach(row):
    if row['dachform'] == 'Steildach (mit beheiztem Dachgeschoss)':
        teilbeheizungsfaktor_dach = 1
    elif row['dachform'] == 'Steildach (mit teilweise beheiztem Dachgeschoss)':
        teilbeheizungsfaktor_dach = 0.5   
    else:   # 'Flachdach / flachgeneigtes Dach' oder 'oberste Geschossdecke zu unbeheiztem Dachgeschoss'
        teilbeheizungsfaktor_dach = 0
            
    return teilbeheizungsfaktor_dach

data_final['teilbeheizungsfaktor_dach'] = data_final.apply(teilbeheizungsfaktor_dach, axis = 1)   
  

def calc_roof_area(row):
    if row['dachform'] == 'Steildach (mit beheiztem Dachgeschoss)':
        roof_area = row['teilbeheizungsfaktor_dach'] * row['base_area'] * 1.51 + ((1 - row['teilbeheizungsfaktor_dach']) * row['base_area'])
    elif row['dachform'] == 'Steildach (mit teilweise beheiztem Dachgeschoss)': 
        roof_area = row['teilbeheizungsfaktor_dach'] * row['base_area'] * 1.51 + ((1 - row['teilbeheizungsfaktor_dach']) * row['base_area'])
    else:
        roof_area = row['teilbeheizungsfaktor_dach'] * row['base_area'] * 1.0 + ((1 - row['teilbeheizungsfaktor_dach']) * row['base_area'])
        
    return roof_area

data_final['roof_area'] = data_final.apply(calc_roof_area, axis = 1) 
    
# max_occupancy aus TE und BE ################################################
##############################################################################
# Aus (imputierten) Datensatz der Breitenerhebung
data_final['max_occupancy'] = data_final['scr_gebaeude_id'].map(max_occupancy_be_imputiert.set_index('scr_gebaeude_id')['q25_1'])

# Aus TE
max_occupancy = data_final[['scr_gebaeude_id']]

for x in range(50):
    x += 1
    max_occupancy['max_occupancy_' + str(x)] = max_occupancy['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['exemplary_room_max_persons_' + str(x)])
    max_occupancy['exemplary_room_area_' + str(x)] = max_occupancy['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['exemplary_room_area_' + str(x)])
    max_occupancy['z_per_dens_' + str(x)] = max_occupancy['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_per_dens_' + str(x)])
    max_occupancy['z_area_' + str(x)] = max_occupancy['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_area_' + str(x)])
  
    max_occupancy['max_occupancy_new_' + str(x)] = (max_occupancy['max_occupancy_' + str(x)] / max_occupancy['exemplary_room_area_' + str(x)]) * max_occupancy['z_area_' + str(x)]
    #max_occupancy['max_occupancy_den_' + str(x)] = (1/max_occupancy['z_per_dens_' + str(x)]) * max_occupancy['z_area_' + str(x)]

    
max_occupancy_sum = data_final[['scr_gebaeude_id']]
for x in range(50):
    x +=1
    max_occupancy_sum['max_occupancy_new_' + str(x)] = max_occupancy_sum['scr_gebaeude_id'].map(max_occupancy.set_index('scr_gebaeude_id')['max_occupancy_new_' + str(x)])

max_occupancy_sum['max_occupancy_te'] = max_occupancy_sum.sum(axis = 1)
# data_final['max_occupancy'] = data_final['scr_gebaeude_id'].map(max_occupancy_sum.set_index('scr_gebaeude_id')['max_occupancy_te'])


# u_windows aus TE ###########################################################
##############################################################################
# Glastyp nach Himmelsrichtung aus TE (z. B. WSV2: U= 1, 2)
data_final['b_gl_type_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_gl_type_1'])
data_final['b_gl_type_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_gl_type_2'])
data_final['b_gl_type_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_gl_type_3'])
data_final['b_gl_type_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_gl_type_4'])

# Extrahiere U-Wert aus b_gl_type 
for i in directions:
    data_final['u_g_{}'.format(i)] = (((data_final['b_gl_type_{}'.format(i)].str.split(':').str[1]).str.split('=').str[1]).str.strip()).replace(',','.', regex = True).astype(float).replace(np.nan, 0, regex = True)

# Finde häufigsten U_g-Wert aller Fenster
most_freq_u_g = data_final[['scr_gebaeude_id', 'u_g_south', 'u_g_east', 'u_g_west', 'u_g_north']]
most_freq_u_g = most_freq_u_g.replace(0, np.nan) 
most_freq_u_g = most_freq_u_g.set_index('scr_gebaeude_id')
most_freq_u_g['u_g_most_freq'] = most_freq_u_g.mode(axis=1).iloc[:, 0]
data_final['u_g_most_freq'] = data_final['scr_gebaeude_id'].map(most_freq_u_g['u_g_most_freq'])
data_final['u_g_most_freq'] = data_final['u_g_most_freq'].replace(np.nan, 0)

# Informationen über Rahmenart und Einbaujahr
data_final['rahmenart_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_frame_type_1'])
data_final['rahmenart_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_frame_type_2'])
data_final['rahmenart_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_frame_type_3'])
data_final['rahmenart_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_frame_type_4'])
data_final['rahmenart_einbau95_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_year_1'])
data_final['rahmenart_einbau95_south'] = np.where(data_final['rahmenart_einbau95_south'] == 'ja', '>=95', '<95')
data_final['rahmenart_einbau95_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_year_2'])
data_final['rahmenart_einbau95_east'] = np.where(data_final['rahmenart_einbau95_east'] == 'ja', '>=95', '<95')
data_final['rahmenart_einbau95_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_year_3'])
data_final['rahmenart_einbau95_west'] = np.where(data_final['rahmenart_einbau95_west'] == 'ja', '>=95', '<95')
data_final['rahmenart_einbau95_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_win_year_4'])
data_final['rahmenart_einbau95_north'] = np.where(data_final['rahmenart_einbau95_north'] == 'ja', '>=95', '<95')

array_u_rahmen = [['<95', '>=95']]
tuples_u_rahmen = list(zip(*array_u_rahmen))
index_u_rahmen = pd.MultiIndex.from_tuples(tuples_u_rahmen, names=['bak_rahmen'])
u_rahmen = pd.DataFrame(([np.inf, np.inf], 
                  [2.2, 1.9],
                  [2.6, 2],
                  [4.5, 3.4],
                  [1.2, 1]), index=['-', 'Holz', 'Kunststoff', 'Alu/Stahl', 'Passivhausqualität'], columns=index_u_rahmen)
u_rahmen = u_rahmen.unstack().reset_index().rename(columns = {'level_1': 'rahmenart', 0: 'u_rahmen'})

# U-Wert der Rahmen:
for i in directions:
    data_final = pd.merge(data_final, u_rahmen, left_on = ['rahmenart_einbau95_{}'.format(i), 'rahmenart_{}'.format(i)], right_on = ['bak_rahmen', 'rahmenart'], how = 'left')
    data_final = data_final.rename(columns = {'u_rahmen': 'u_rahmen_{}'.format(i)})   
    data_final.drop(['bak_rahmen', 'rahmenart'], axis = 1, inplace = True)  
    data_final['u_rahmen_{}'.format(i)] = data_final['u_rahmen_{}'.format(i)].replace(np.nan, 0)

# Zur Ermittlung des U-Werts der Fenster:
# u_windows = U_g * f_glas + u_rahmen(1 - f_glas) + win_l * frame_psi 
for i in directions:
    data_final['u_window_{}'.format(i)] = data_final['u_g_{}'.format(i)] * 0.7 + data_final['u_rahmen_{}'.format(i)]*(1-0.7)+0*0.07

                           
# Flächengewichtes Mittel
data_final['u_windows'] = ((data_final['u_window_south'] * data_final['window_share_south'] * data_final['facade_area_south']) + \
                            (data_final['u_window_east'] * data_final['window_share_east'] * data_final['facade_area_east']) + \
                            (data_final['u_window_west'] * data_final['window_share_west'] * data_final['facade_area_west']) + \
                            (data_final['u_window_north'] * data_final['window_share_north'] * data_final['facade_area_north'])) / \
                                ((data_final['window_share_south'] * data_final['facade_area_south']) + \
                                (data_final['window_share_east'] * data_final['facade_area_east']) + \
                                (data_final['window_share_west'] * data_final['facade_area_west']) + \
                                (data_final['window_share_north'] * data_final['facade_area_north']))
data_final['u_windows'] = data_final['u_windows'].replace(np.nan, 0)                                     

                                    
# glass_solar_transmittance aus TE ###########################################
##############################################################################
# Extrahiere Glastyp (z.B. WSV2) aus b_gl_type
# Ersetze '-' durch NANs
for i in directions:
    data_final['Verglasungstyp_{}'.format(i)] = data_final['b_gl_type_{}'.format(i)].str.split(':').str[0] 
    data_final['Verglasungstyp_{}'.format(i)] = data_final['Verglasungstyp_{}'.format(i)].replace('-', np.nan, regex = True)

# Finde häufigsten Verglasungstyp aller Fenster
most_freq_verglasungstyp = data_final[['scr_gebaeude_id', 'Verglasungstyp_south', 'Verglasungstyp_east', 'Verglasungstyp_west', 'Verglasungstyp_north']]
most_freq_verglasungstyp = most_freq_verglasungstyp.set_index('scr_gebaeude_id')
most_freq_verglasungstyp['most_freq_verglasungstyp'] = most_freq_verglasungstyp.mode(axis=1).iloc[:, 0]
data_final['most_freq_verglasungstyp'] = data_final['scr_gebaeude_id'].map(most_freq_verglasungstyp['most_freq_verglasungstyp'])


##############################################################################
# Verknüpfe Informationen aus u_windows und Verglasungstyp_himmelsrichtung
# mit Werten aus DIN V 18599-2
# g-Wert in erster Priorität nach Verglasungstyp, dann je nach U-Wert
# wenn es keinen dazugehörigen U-Wert in der Norm gibt, dann wähle größeren/konservativeren Wert für U aus
# und übernehme diesen g-Wert, wenn es keinen größeren/konservativeren U-Wert gibt, dann nehme kleineren U-Wert und 
# wähle dazugehörigen g-Wert

# data_final.drop(['b_gl_type_south', 'b_gl_type_east', 'b_gl_type_west', 'b_gl_type_north'], axis = 1, inplace = True)

cleanup_verglasung_sonnenschutz = pd.DataFrame({
                                                'Verglasungstyp':
                                                    ['ESV', 'ZSV', 'WSV2', 'WSV2', 'WSV2', 'WSV2', 'WSV3', 'WSV3', 'SSV3', 'SSV3', 'SSV3'],
                                                'U_g':
                                                    [5.8, 2.9, 1.7, 1.4, 1.1, 1.0, 0.8, 0.7, 0.7, 0.7, 0.7],
                                                'g':
                                                    [0.87, 0.78, 0.72, 0.67, 0.64, 0.53, 0.60, 0.53, 0.34, 0.24, 0.16],
                                                'A-jalou_10°_weiß':
                                                    [0.12, 0.1, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.04, 0.04, 0.03],
                                                'A-jalou_10°_grau':
                                                    [0.2, 0.15, 0.11, 0.1, 0.08, 0.08, 0.07, 0.06, 0.06, 0.06, 0.06],
                                                'A-jalou_45°_weiß':
                                                    [0.18, 0.15, 0.13, 0.12, 0.11, 0.1, 0.1, 0.09, 0.07, 0.06, 0.05],
                                                'A-jalou_45°_grau':
                                                    [0.21, 0.16, 0.12, 0.1, 0.09, 0.08, 0.07, 0.06, 0.06, 0.06, 0.06],
                                                'A-markise_weiß':
                                                    [0.28, 0.25, 0.23, 0.21, 0.2, 0.17, 0.19, 0.17, 0.12, 0.1, 0.08],
                                                'A-markise_grau':
                                                    [0.23, 0.19, 0.15, 0.14, 0.13, 0.11, 0.11, 0.1, 0.08, 0.07, 0.06],
                                                'I-jalou_45°_weiß':	
                                                    [0.45, 0.46, 0.46, 0.44, 0.44, 0.39, 0.42, 0.39, 0.28, 0.21, 0.15],
                                                'I-jalou_45°_hellgrau':	
                                                    [0.65, 0.64, 0.62, 0.58, 0.56, 0.48, 0.54, 0.48, 0.32, 0.23, 0.15],
                                                'I-texilrollo_weiß':	
                                                    [0.42, 0.42, 0.42 ,0.41, 0.4, 0.37, 0.39, 0.37, 0.27, 0.21, 0.14],
                                                'I-texilrollo_grau':	
                                                    [0.46, 0.47, 0.47, 0.45, 0.44, 0.4, 0.43, 0.4, 0.28, 0.21, 0.15],
                                                'Innen Folie':	
                                                    [0.38, 0.4, 0.4, 0.39, 0.39, 0.36, 0.38, 0.36, 0.27, 0.2, 0.14]
                                                })

subset_cleanup_verglasung_g_verglasung = cleanup_verglasung_sonnenschutz[['Verglasungstyp', 'U_g', 'g']]

##############################################################################
# Ermittle Gesamtenergiedurchlassgrad g der Verglasung in alle Himmelsrichtungen
for i in directions:
    mapping_g_verglasung = (pd.merge_asof(data_final.sort_values('u_g_{}'.format(i)), 
                        subset_cleanup_verglasung_g_verglasung.sort_values('U_g'), 
                        left_on='u_g_{}'.format(i), 
                        left_by='Verglasungstyp_{}'.format(i), 
                        right_on='U_g', 
                        right_by='Verglasungstyp').set_index('scr_gebaeude_id'))
    
    data_final = (pd.merge_asof(data_final.sort_values('u_g_{}'.format(i)), 
                        subset_cleanup_verglasung_g_verglasung.sort_values('U_g'), 
                        left_on='u_g_{}'.format(i), 
                        left_by='Verglasungstyp_{}'.format(i), 
                        right_on='U_g', 
                        right_by='Verglasungstyp',
                        direction = 'forward')
                        .set_index('scr_gebaeude_id')
                        .combine_first(mapping_g_verglasung)
                        .sort_index()
                        .reset_index()
                        )
    data_final.rename({'g': 'g_verglasung_{}'.format(i)}, axis=1, inplace=True)
    data_final.drop(['Verglasungstyp', 'U_g'], axis = 1, inplace = True)
    
    data_final['g_verglasung_{}'.format(i)] = data_final['g_verglasung_{}'.format(i)].replace(np.nan, 0) 


# Flächengewichtes Mittel
data_final['glass_solar_transmittance'] = ((data_final['g_verglasung_south'] * data_final['window_area_south']) + \
                                                        (data_final['g_verglasung_east'] * data_final['window_area_east']) + \
                                                        (data_final['g_verglasung_west'] * data_final['window_area_west']) + \
                                                        (data_final['g_verglasung_north'] * data_final['window_area_north'])) / \
                                                            (data_final['window_area_south'] + \
                                                            data_final['window_area_east'] + \
                                                            data_final['window_area_west'] + \
                                                            data_final['window_area_north'])
                                                                
# NW5894898_0_00, NW5917464_1_00, NW5962304_0_00, HE3585636_1_00, RP90636_0_00 haben keine Fenster, setze hier glass_solar_transmittance = 0
data_final['glass_solar_transmittance'] = data_final['glass_solar_transmittance'].replace(np.nan, 0)

                                                                
# glass_solar_shading_transmittance aus TE ###################################
##############################################################################
# Gleiche Methodik wie bei glass_solar_transmittance                                                            
data_final['b_blind_type_south'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_blind_type_1'])
data_final['b_blind_type_east'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_blind_type_2'])
data_final['b_blind_type_west'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_blind_type_3'])
data_final['b_blind_type_north'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_blind_type_4'])

# Ersetze '-' durch NAs (erst str.strip(), da ' -')
for i in directions:
    data_final['b_blind_type_{}'.format(i)] = data_final['b_blind_type_{}'.format(i)].str.strip().replace('-', np.nan)

subset_cleanup_verglasung_g_sonnenschutz = cleanup_verglasung_sonnenschutz.drop(['g'], axis = 1)
subset_cleanup_verglasung_g_sonnenschutz = subset_cleanup_verglasung_g_sonnenschutz.set_index(['Verglasungstyp', 'U_g'])
subset_cleanup_verglasung_g_sonnenschutz = subset_cleanup_verglasung_g_sonnenschutz.stack().reset_index().rename(columns = {'level_2':'Sonnenschutztyp', 0:'g_faktor'})

# Ermittle Energiedurchlassgrad bei aktiviertem Sonnenschutz je Himmelsrichtung
for i in directions:
    mapping_g_sonnenschutz = (pd.merge_asof(data_final.sort_values('u_g_{}'.format(i)), 
                                subset_cleanup_verglasung_g_sonnenschutz.sort_values('U_g'), 
                                left_on='u_g_{}'.format(i), 
                                left_by=['Verglasungstyp_{}'.format(i), 'b_blind_type_{}'.format(i)], 
                                right_on='U_g', 
                                right_by=['Verglasungstyp', 'Sonnenschutztyp']).set_index('scr_gebaeude_id'))
    
    data_final = (pd.merge_asof(data_final.sort_values('u_g_south'), 
                        subset_cleanup_verglasung_g_sonnenschutz.sort_values('U_g'), 
                        left_on='u_g_south', 
                        left_by=['Verglasungstyp_{}'.format(i), 'b_blind_type_{}'.format(i)], 
                        right_on='U_g', 
                        right_by=['Verglasungstyp', 'Sonnenschutztyp'],
                        direction = 'forward')
                        .set_index('scr_gebaeude_id')
                        .combine_first(mapping_g_sonnenschutz)
                        .sort_index()
                        .reset_index()
                        )
    data_final.rename({'g_faktor': 'g_sonnenschutz_{}'.format(i)}, axis=1, inplace=True)
    data_final.drop(['Sonnenschutztyp', 'U_g', 'Verglasungstyp'], axis = 1, inplace = True)
    
    data_final['g_sonnenschutz_{}'.format(i)] = data_final['g_sonnenschutz_{}'.format(i)].replace(np.nan, 0)

# Flächengewichtes Mittel hier vermutl. nicht sinnvoll
# Bsp.: Gebäude mit Fenstern an allen 4 Fassaden, aber Sonnenschutz an nur 3 Fassaden
# --> Bezieht man den g_sonnenschutz auf alle Fensterflächen, dann reduziert sich g_sonnenschutz,
# obwohl es nur an 3 Fassaden einen Sonnenschutz gibt. Das Gegeneteil müsste der Fall sein, g_sonnenschutz müsste steigen.
# Daher nur Fensterfläche einbeziehen, wenn es an dieser Fensterfläche auch einen Sonnenschutz gibt
# [1 if v > 0 else 0 for v in data_final['g_sonnenschutz_south']] --> Prüft ob wert in g_sonnenschutz_south > 0, wenn ja
# multipliziere Term mit 1, wenn nein, multipliziere Term mit 0 (Fläche wird dann nicht berücksichtigt)

data_final['glass_solar_shading_transmittance'] = ((data_final['g_sonnenschutz_south'] * data_final['window_area_south']) + \
                                                        (data_final['g_sonnenschutz_east'] * data_final['window_area_east']) + \
                                                        (data_final['g_sonnenschutz_west'] * data_final['window_area_west']) + \
                                                        (data_final['g_sonnenschutz_north'] * data_final['window_area_north'])) / \
                                                            ((data_final['window_area_south'] * [1 if x > 0 else 0 for x in data_final['g_sonnenschutz_south']]) + \
                                                            (data_final['window_area_east'] * [1 if x > 0 else 0 for x in data_final['g_sonnenschutz_east']]) + \
                                                            (data_final['window_area_west'] * [1 if x > 0 else 0 for x in data_final['g_sonnenschutz_west']]) + \
                                                            (data_final['window_area_north'] * [1 if x > 0 else 0 for x in data_final['g_sonnenschutz_north']]))

# Fülle np.nan mit 0 für Gebäude die keine Sonnenschutzvorrichtung haben 
data_final['glass_solar_shading_transmittance'] = data_final['glass_solar_shading_transmittance'].replace(np.nan, 0)

# Setze glass_solar_shading_transmittance = 0 für Gebäude die keine Fenster haben
data_final['glass_solar_shading_transmittance'] = np.where(data_final['glass_solar_transmittance'] == 0, 0, data_final['glass_solar_shading_transmittance'])


# glass_light_transmittance ##################################################
##############################################################################
# See Szokolay (1980): Environmental Science Handbook for Architects and Builders, p. 109
# Assumption
def set_lighting_maintenance_factor(row):
    if row['hk_geb'] == 'Produktions-, Werkstatt-, Lager- oder Betriebsgebäude':
        lighting_maintenance_factor = 0.8
    else:
        lighting_maintenance_factor = 0.9
    return lighting_maintenance_factor
data_final['lighting_maintenance_factor'] = data_final.apply(set_lighting_maintenance_factor, axis = 1)  

subset_glass_light_transmittance = data_final[['scr_gebaeude_id', 'Verglasungstyp_south', 'u_g_south', 'g_verglasung_south',
                                               'Verglasungstyp_east', 'u_g_east', 'g_verglasung_east',
                                               'Verglasungstyp_north', 'u_g_north', 'g_verglasung_north',
                                               'Verglasungstyp_west', 'u_g_west', 'g_verglasung_west',
                                               'lighting_maintenance_factor']]
for i in directions:
    subset_glass_light_transmittance['Verglasungstyp_{}'.format(i)] = subset_glass_light_transmittance['Verglasungstyp_{}'.format(i)].replace(np.nan, 'nan')

# Für alle Fenster k_1 = 0.7 wenn Details nicht bekannt (nach DIN V 18599-4, S.39)
subset_glass_light_transmittance['k_1'] =  0.7

# Für alle Fenster k_3 = 0.85 nach DIN V 18599-4, S.39
subset_glass_light_transmittance['k_3'] =  0.85

# DIN V 18599-4, Tab. 11, S.40
cleanup_glass_light_transmittance = pd.DataFrame({
                                                'Verglasungstyp':
                                                    ['ESV', 'ZSV', 'WSV2', 'WSV2', 'WSV2', 'WSV2', 'WSV3', 'WSV3', 'WSV3', 'WSV3', 'SSV2', 'SSV2', 'SSV2', 'SSV3', 'SSV3', 'SSV3'],
                                                'U_g': 
                                                    [5.8, 2.9, 1.7, 1.4, 1.1, 1.0, 0.8, 0.8, 0.7, 0.6, 1.3, 1.2, 1.2, 0.7, 0.7, 0.7],
                                                'g':
                                                    [0.87, 0.78, 0.72, 0.67, 0.6, 0.48, 0.5, 0.6, 0.5, 0.5, 0.48, 0.37, 0.25, 0.34, 0.24, 0.16],
                                                'tau_D65SNA':
                                                    [0.9, 0.82, 0.74, 0.78, 0.8, 0.71, 0.69, 0.74, 0.7, 0.69, 0.59, 0.67, 0.4, 0.63, 0.45, 0.27]})
           
cleanup_glass_light_transmittance.sort_values(by=['Verglasungstyp', 'U_g', 'g']).reset_index(drop=True)   

for i in directions:
    def find_tau_D65SNA(row):   
        tau_D65SNA = cleanup_glass_light_transmittance[
                            (cleanup_glass_light_transmittance['Verglasungstyp'] == row['Verglasungstyp_{}'.format(i)]) & 
                            (cleanup_glass_light_transmittance['U_g'] >= row['u_g_{}'.format(i)]) & 
                            (cleanup_glass_light_transmittance['g'] >= row['g_verglasung_{}'.format(i)])]
        if row['Verglasungstyp_{}'.format(i)] == 'nan':
            tau_D65SNA = 0
        elif len(tau_D65SNA) == 0:
            tau_D65SNA = cleanup_glass_light_transmittance[cleanup_glass_light_transmittance['Verglasungstyp'] == row['Verglasungstyp_{}'.format(i)]].iloc[-1,3]
        else:
            tau_D65SNA = tau_D65SNA.iloc[0,3]
        return tau_D65SNA


    subset_glass_light_transmittance['tau_D65SNA_{}'.format(i)] = subset_glass_light_transmittance.apply(find_tau_D65SNA, axis = 1)
    
    subset_glass_light_transmittance['glass_light_transmittance_{}'.format(i)] = subset_glass_light_transmittance['k_1'] * subset_glass_light_transmittance['lighting_maintenance_factor'] * subset_glass_light_transmittance['k_3'] * subset_glass_light_transmittance['tau_D65SNA_{}'.format(i)]
    data_final['glass_light_transmittance_{}'.format(i)] = data_final['scr_gebaeude_id'].map(subset_glass_light_transmittance.set_index('scr_gebaeude_id')['glass_light_transmittance_{}'.format(i)])

# Flächengewichtes Mittel
data_final['glass_light_transmittance'] = ((data_final['glass_light_transmittance_south'] * data_final['window_area_south']) + \
                                                        (data_final['glass_light_transmittance_east'] * data_final['window_area_east']) + \
                                                        (data_final['glass_light_transmittance_west'] * data_final['window_area_west']) + \
                                                        (data_final['glass_light_transmittance_north'] * data_final['window_area_north'])) / \
                                                            (data_final['window_area_south'] + \
                                                            data_final['window_area_east'] + \
                                                            data_final['window_area_west'] + \
                                                            data_final['window_area_north'])     

# lighting_control ###########################################################
##############################################################################  
data_final['lighting_control'] = data_final['typ_18599'].map(profile_data.set_index('typ_18599')['E_m'])


# lighting_load ##############################################################
############################################################################## 
# Erzeuge Subset von data_final mit ausschließlich scr_gebaeude_id
data_final_sub_lighting_load = data_final[['scr_gebaeude_id', 'typ_18599']]
data_te_sub_lighting_load = data_te[['pr_var_name']]



# Finde im DataFrame data_te alle Spalten mit 'z_use_type_' im Spaltennamen und speichere den neuen DF als find_max_zones.
# Hier 'z_use_type_' weil es andere Variablen gibt auf die der String 'l_type_' passt (z.B. 'b_gl_type_' oder 'c_chil_type_')
find_max_zones = data_te.filter(regex = 'z_use_type_')
# Lösche in diesem neuen DF alle Spalten mit NaN's und speichere/überschreibe den DF
find_max_zones = find_max_zones.dropna(axis = 1, how = 'all')
# Ermittle die Anzahl der Spalten von DataFrame find_max_zones und speichere das Ergebnis (int) als max_zones
max_zones = len(find_max_zones.columns)
Number_of_lights = max_zones


# Erzeuge Subset von data_te 
for x in range(Number_of_lights):
    x += 1
    data_te_sub_lighting_load['z_use_type_' + str(x)] = data_te[['z_use_type_' + str(x)]]
    data_te_sub_lighting_load['l_type_' + str(x)] = data_te[['l_type_' + str(x)]]
    data_te_sub_lighting_load['l_lp_' + str(x)] = data_te[['l_lp_' + str(x)]]
    data_te_sub_lighting_load['z_area_' + str(x)] = data_te[['z_area_' + str(x)]]

    data_te_sub_lighting_load['z_use_type_nr_' + str(x)] = data_te_sub_lighting_load['z_use_type_' + str(x)].str.split(' ').str[0]
    
subset_lighting_load = pd.merge(data_final_sub_lighting_load, data_te_sub_lighting_load, left_on = 'scr_gebaeude_id', right_on = 'pr_var_name')


# Ändere Labels von allen 26 Spalten l_lp_i
for x in range(Number_of_lights):
    x += 1
    
    # Füge Werte E_m, k_A, k_VB, k_WF, k (in Abhängigkeit des zugewiesenen Nutzungsprofils) zu subset_lighting_load hinzu 
    subset_lighting_load['E_m_' + str(x)] = subset_lighting_load['z_use_type_nr_' + str(x)].map(profile_data.set_index('nr_18599')['E_m'])
    subset_lighting_load['k_A_' + str(x)] = subset_lighting_load['z_use_type_nr_' + str(x)].map(profile_data.set_index('nr_18599')['k_A'])
    subset_lighting_load['k_VB_' + str(x)] = subset_lighting_load['z_use_type_nr_' + str(x)].map(profile_data.set_index('nr_18599')['k_VB'])
    subset_lighting_load['k_WF_' + str(x)] = subset_lighting_load['z_use_type_nr_' + str(x)].map(profile_data.set_index('nr_18599')['k_WF'])
    subset_lighting_load['k_' + str(x)] = subset_lighting_load['z_use_type_nr_' + str(x)].map(profile_data.set_index('nr_18599')['k'])
    
    cleanup_lampenart = {'l_lp_' + str(x): {
                                      'bulb': 'Glühlampe',                                           
                                      'halogen': 'Halogenglühlampe', 
                                      'led_repl_lamp': 'LED-Ersatzlampen', 
                                      'led_lamp': 'LEDs in LED-Leuchten', 
                                      'dis_cmp_ex_el': 'Leuchtstofflampe kompakt mit externem EVG',
                                      'dis_cmp_ex_con': 'Leuchtstofflampe kompakt mit externem KVG',
                                      'dis_cmp_ex_ll': 'Leuchtstofflampe kompakt mit externem VVG',
                                      'dis_cmp_in_el': 'Leuchtstofflampe kompakt mit integriertem EVG',
                                      'dis_rod_el': 'Leuchtstofflampe stabförmig mit EVG',
                                      'dis_rod_con': 'Leuchtstofflampe stabförmig mit KVG',
                                      'dis_rod_ll': 'Leuchtstofflampe stabförmig mit VVG',
                                      'hp_mercury': 'Quecksilberdampf - Hochdruck'}}
    subset_lighting_load.replace(cleanup_lampenart, inplace = True)

    # Füge Werte k_L für jede Zone hinzu
    k_L = pd.DataFrame({'l_amp':
                            ['Glühlampe', 
                              'Halogenglühlampe', 
                              'LED-Ersatzlampen', 
                              'LEDs in LED-Leuchten', 
                              'Leuchtstofflampe kompakt mit externem EVG',
                              'Leuchtstofflampe kompakt mit externem KVG',
                              'Leuchtstofflampe kompakt mit externem VVG',
                              'Leuchtstofflampe kompakt mit integriertem EVG',
                              'Leuchtstofflampe stabförmig mit EVG',
                              'Leuchtstofflampe stabförmig mit KVG',
                              'Leuchtstofflampe stabförmig mit VVG',
                              'Quecksilberdampf - Hochdruck'],
                        'k_L': 
                            [6,
                              5,
                              0.68,
                              0.44,
                              1.2,
                              1.5,
                              1.4,
                              1.6,
                              1,
                              1.14,
                              1.24,
                              1.7]})

    subset_lighting_load['k_L_' + str(x)] = subset_lighting_load['l_lp_' + str(x)].map(k_L.set_index('l_amp')['k_L'])

# Füge entsprechenden p_j_lx Wert zu subset_lighting_load hinzu
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
p_j_lx = p_j_lx.rename(columns={'beleuchtungsart': 'l_type_'})

# Ändere Labels aller 26 Spalten/Zonen
for x in range(Number_of_lights):
    x += 1
    cleanup_l_type_x = {'l_type_' + str(x): {
                                      'direct': 'Direkt (Licht fällt direkt auf den Arbeitsbereich)',                                           
                                      'indir_dir': 'Direkt / indirekt', 
                                      'indirect': 'Indirekt (Licht, das von Decken und Wänden reflektiert wird)'}}
    subset_lighting_load.replace(cleanup_l_type_x, inplace = True)


# Füge jeder Zone einen p_j_lx Wert hinzu
for x in range(Number_of_lights):
    x += 1
    subset_lighting_load = pd.merge(subset_lighting_load, p_j_lx, left_on = ['l_type_' + str(x), 'k_' + str(x)], right_on = ['l_type_', 'k'], how = 'left')
    subset_lighting_load = subset_lighting_load.rename(columns={'p_j_lx': 'p_j_lx_' + str(x)})
    subset_lighting_load = subset_lighting_load.drop(['l_type_'], axis = 1)

# Berechne spez. elektr. Bewertungsleistung nach p_j = p_j_lx * E_m * k_WF * k_A * k_L * k_VB
# Für alle 26 Zonen
for x in range(Number_of_lights): 
    x += 1 
    subset_lighting_load['p_j_' + str(x)] = subset_lighting_load['p_j_lx_' + str(x)] * subset_lighting_load['E_m_' + str(x)] * \
                                subset_lighting_load['k_WF_' + str(x)] * subset_lighting_load['k_L_' + str(x)] * subset_lighting_load['k_VB_' + str(x)]

# Fülle alle NaN's mit 0, da sonst nicht gerechnet werden kann 
subset_lighting_load.fillna(0, inplace = True)

# Gewichtetes Mittel
subset_lighting_load['sumproduct_zähler'] = 0
subset_lighting_load['sumproduct_nenner'] = 0

for i in range(1,Number_of_lights+1):
    subset_lighting_load['sumproduct_zähler'] += subset_lighting_load['p_j_{}'.format(i)] * subset_lighting_load['z_area_{}'.format(i)] 
    subset_lighting_load['sumproduct_nenner'] += subset_lighting_load['z_area_{}'.format(i)]
    
# Ergebnis     
subset_lighting_load['lighting_load'] = subset_lighting_load['sumproduct_zähler'] / subset_lighting_load['sumproduct_nenner']
      
                                                                                                              
subset_lighting_load_p_j_only = subset_lighting_load[['scr_gebaeude_id',
                                                        'lighting_load']] 

for x in range(Number_of_lights): 
    x += 1    
    subset_lighting_load_p_j_only['p_j_' + str(x)] = subset_lighting_load[['p_j_' + str(x)]]
                    
# Füge Ergbebnisse für p_j_i data_final hinzu 
data_final = pd.merge(data_final, subset_lighting_load_p_j_only, on = 'scr_gebaeude_id', how = 'left' )                           
                            

# u_walls ####################################################################
############################################################################## 
data_final['außenwand_material'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_wall_fabric'])
data_final['außenwand_dämmstärke'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_wall_ins'])
data_final['außenwand_dämmanteil'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_wall_ins_part'])

def create_bak(row):
    if row['baujahr'] <= 1918:
        auspraegung = 'bak_vor_1918' 
    elif 1919 <= row['baujahr'] <= 1948:
        auspraegung = 'bak_1919_1948' 
    elif 1949 <= row['baujahr'] <= 1957:
        auspraegung = 'bak_1949_1957' 
    elif 1958 <= row['baujahr'] <= 1968:
        auspraegung = 'bak_1958_1968' 
    elif 1969 <= row['baujahr'] <= 1978:
        auspraegung = 'bak_1969_1978' 
    elif 1979 <= row['baujahr'] <= 1983:
        auspraegung = 'bak_1979_1983' 
    elif 1984 <= row['baujahr'] <= 1994:
        auspraegung = 'bak_1984_1994' 
    elif 1995 <= row['baujahr'] <= 2001:
        auspraegung = 'bak_1995_2001'    
    elif 2002 <= row['baujahr'] <= 2006:
        auspraegung = 'bak_2002_2006' 
    else:
        auspraegung = 'bak_ab_2007'
    return auspraegung    
        
data_final['bak'] = data_final.apply(create_bak, axis = 1)        

# Wert für bak_1949_1957/Plattenbau = 2: eigene Annahme, da ein Gebäude davon betroffen (NW7410711_1_00)
außenwand_u_bak = pd.DataFrame({'baujahr': 
                                ['bak_vor_1918', 'bak_1919_1948', 'bak_1949_1957', 'bak_1958_1968', 'bak_1969_1978', 'bak_1979_1983', 'bak_1984_1994', 'bak_1995_2001', 'bak_2002_2006', 'bak_ab_2007'],
                            'massiv': 
                                [1.7, 1.7, 1.4, 1.4, 1, 0.8, 0.6, 0.5, 0.4, 0.3],
                            '2-schaliges Mauerwerk': 
                                [1.6, 1.4, 1.3, 1.2, 1.1, 0.6, 0.4, 0.3, 0.3, 0.2],
                            'Holz': 
                                [2, 2, 1.4, 1.4, 0.6, 0.5, 0.4, 0.4, 0.3, 0.2],
                            'Plattenbau': 
                                [np.nan, 2, np.nan, 1.8, 0.7, 0.7, 0.7, 0.5, 0.45, 0.35],
                            'vorgehängte Platten': 
                                [np.nan, np.nan, 2.5, 1.4, 1, 0.6, 0.5, 0.5, 0.4, 0.3],
                            'Wand gegen Erdreich': 
                                [2.4, 2.3, 2.3, 2.3, 1.2, 0.8, 0.6, 0.5, 0.5, 0.4]}).set_index('baujahr')

außenwand_u_bak = außenwand_u_bak.stack().reset_index().rename(columns = {'level_1': 'b_wall_fabric', 0: 'außenwand_U0'})
data_final = pd.merge(data_final, außenwand_u_bak, left_on = ['außenwand_material','bak'], right_on= ['b_wall_fabric', 'baujahr'], how = 'left')    
data_final = data_final.drop(['b_wall_fabric', 'baujahr_y'], axis = 1)  

# Korrigiere U-Wert falls Dämmung vorhanden
def adjust_u_walls(row):
    if row['außenwand_dämmstärke'] != 0:
        value = row['außenwand_U0']*(1-row['außenwand_dämmanteil'])+row['außenwand_dämmanteil']*1/(1/row['außenwand_U0']+row['außenwand_dämmstärke']/100/0.04)
    else:     
        value = row['außenwand_U0']
    return value

data_final['u_walls'] = data_final.apply(adjust_u_walls, axis = 1)     
    
                                 
# u_roof #####################################################################
############################################################################## 
data_final['dach_material'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_roof_fabric'])
data_final['dach_dämmstärke'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_roof_ins'])
data_final['dach_dämmanteil'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_roof_ins_part'])

dach_u_bak = pd.DataFrame({'baujahr': 
                                ['bak_vor_1918', 'bak_1919_1948', 'bak_1949_1957', 'bak_1958_1968', 'bak_1969_1978', 'bak_1979_1983', 'bak_1984_1994', 'bak_1995_2001', 'bak_2002_2006', 'bak_ab_2007'],
                            'massiv': 
                                [2.1, 2.1, 2.1, 2.1, 0.6, 0.5, 0.4, 0.3, 0.2, 0.2],
                            'Holz': 
                                [2.6, 1.4, 1.4, 1.4, 0.8, 0.5, 0.4, 0.3, 0.2, 0.2]}).set_index('baujahr')

dach_u_bak = dach_u_bak.stack().reset_index().rename(columns = {'level_1': 'b_roof_fabric', 0: 'dach_U0'})
data_final = pd.merge(data_final, dach_u_bak, left_on = ['dach_material','bak'], right_on= ['b_roof_fabric', 'baujahr'], how = 'left')    
data_final = data_final.drop(['b_roof_fabric', 'baujahr'], axis = 1)  

# Korrigiere U-Wert falls Dämmung vorhanden
def adjust_u_roof(row):
    if row['dach_dämmstärke'] != 0:
        value = row['dach_U0']*(1-row['dach_dämmanteil'])+row['dach_dämmanteil']*1/(1/row['dach_U0']+row['dach_dämmstärke']/100/0.04)
    else:     
        value = row['dach_U0']
    return value

data_final['u_roof'] = data_final.apply(adjust_u_roof, axis = 1) 


# u_base #####################################################################
############################################################################## 
# Kellerdecke/-fußboden
data_final['keller_material'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_floor_fabric'])
data_final['keller_dämmstärke'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_floor_ins'])
data_final['keller_dämmanteil'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_floor_ins_part'])

# NI2384586_0_00 hat keine Angaben zu keller_material
# Annahme: massiv, Ausprägung nicht relevant, da sowieso ungedämmt, dann Einteilung nach bak, alle 0.4
data_final.loc[data_final['scr_gebaeude_id'] == 'NI2384586_0_00', 'keller_material'] = 'massiv'

keller_u_bak = pd.DataFrame({'baujahr': 
                                ['bak_vor_1918', 'bak_1919_1948', 'bak_1949_1957', 'bak_1958_1968', 'bak_1969_1978', 'bak_1979_1983', 'bak_1984_1994', 'bak_1995_2001', 'bak_2002_2006', 'bak_ab_2007'],
                            'massiv': 
                                [1.2, 1.2, 1.5, 1, 1, 0.8, 0.6, 0.6, 0.5, 0.4],
                            'Holz': 
                                [1, 0.8, 0.8, 0.8, 0.6, 0.6, 0.4, 0.4, 0.4, 0.4],
                            'Decke gegen Tiefgarage':
                                [np.nan, np.nan, 4.1, 4.1, 4.1, 1.4, 1.2, 0.4, 0.4, 0.4]}).set_index('baujahr')

keller_u_bak = keller_u_bak.stack().reset_index().rename(columns = {'level_1': 'b_floor_fabric', 0: 'keller_U0'})
data_final = pd.merge(data_final, keller_u_bak, left_on = ['keller_material','bak'], right_on= ['b_floor_fabric', 'baujahr'], how = 'left')    
data_final = data_final.drop(['b_floor_fabric', 'baujahr'], axis = 1)  

# Korrigiere U-Wert falls Dämmung vorhanden
def adjust_u_floor(row):
    if row['keller_dämmstärke'] != 0:
        value = row['keller_U0']*(1-row['keller_dämmanteil'])+row['keller_dämmanteil']*1/(1/row['keller_U0']+row['keller_dämmstärke']/100/0.04)
    else:     
        value = row['keller_U0']
    return value

data_final['u_base'] = data_final.apply(adjust_u_floor, axis = 1) 
 
data_final = data_final.rename(columns = {'baujahr_x': 'baujahr'})



# temp_adj_base ##############################################################
##############################################################################
# Möglichkeiten

def fall_temp_adj_base(row):
    if row['anzahl_geschosse_unterirdisch'] == 0:                                                           # Wenn kein Keller, dann Mögl. 1), Fall 12
        return_value = 12
    elif (row['anzahl_geschosse_unterirdisch'] > 0) & (row['anzahl_geschosse_beheizt_unterirdisch'] == 0):  # Wenn Keller, aber unbeheizt, Mögl. 2), Fall 15/16
        return_value = 16                                                                             
    else:
        return_value = 10                                                                                   # Ansonsten muss Keller voll-/teilbeheizt sein, dann Mögl. 3), 4), also Fall 10
    return return_value

data_final['fall_temp_adj_base'] = data_final.apply(fall_temp_adj_base, axis = 1)   


arrays_fx = [['<5', '<5', '5 bis 10', '5 bis 10',  '>10', '>10'],
          ['<=1', '>1', '<=1', '>1', '<=1', '>1']]
tuples_fx = list(zip(*arrays_fx))

index_fx = pd.MultiIndex.from_tuples(tuples_fx, names=['B', 'R'])
fx = pd.DataFrame(([0.3, 0.45, 0.25, 0.4, 0.2, 0.35],
                    [0.4, 0.6, 0.4, 0.6, 0.4, 0.6],
                  [0.45, 0.6, 0.4, 0.5, 0.25, 0.35],
                  [0.55, 0.55, 0.5, 0.5, 0.45, 0.45],
                  [0.7, 0.7, 0.65, 0.65, 0.55, 0.55]), index=['10', '11', '12', '15', '16'], columns=index_fx)
fx = fx.unstack().reset_index()
fx = fx.rename(columns = {'level_2': 'fall_temp_adj', 0: 'temp_adj_factors'})
fx['fall_temp_adj'] = fx['fall_temp_adj'].astype(int)


data_final['B_raw'] = (2 * data_final['building_width']) + (2 * data_final['building_depth'])

def clean_B(row):
    if row['B_raw'] < 5:
        value = '<5'
    elif 5 <= row['B_raw'] <= 10:
        value = '5 bis 10'   
    else:
        value = '>10'
    return value    
data_final['B'] = data_final.apply(clean_B, axis = 1) 

data_final['R_raw'] = 1 / data_final['u_base']
def clean_R(row):
    if row['R_raw'] <= 1:
        value = '<=1'
    else:
        value = '>1'
    return value  
data_final['R'] = data_final.apply(clean_R, axis = 1)


data_final = pd.merge(data_final, fx, left_on = ['B', 'R', 'fall_temp_adj_base'], right_on = ['B', 'R', 'fall_temp_adj'], how = 'left' )


# temp_adj_walls_ug ##########################################################
##############################################################################
def fall_temp_adj_walls_ug(row):
    if row['anzahl_geschosse_beheizt_unterirdisch'] > 0:
        return_value = 11
    else: 
        return_value = 0
    return return_value
 
data_final['fall_temp_adj_walls_ug'] = data_final.apply(fall_temp_adj_walls_ug, axis = 1)  
   
data_final = pd.merge(data_final, fx, left_on = ['B', 'R', 'fall_temp_adj_walls_ug'], right_on = ['B', 'R', 'fall_temp_adj'], how = 'left' )
data_final = data_final.drop(['fall_temp_adj_x', 'fall_temp_adj_y'], axis = 1)     
data_final = data_final.rename(columns = {'temp_adj_factors_x': 'temp_adj_base', 
                                          'temp_adj_factors_y': 'temp_adj_walls_ug'})

# Fülle NaNs mit 0 für DIBS
data_final['temp_adj_walls_ug'] = data_final['temp_adj_walls_ug'].replace(np.nan, 0)


# heat_recovery_efficiency ###################################################
##############################################################################
# Erstelle Subset von data_final
heat_recovery_efficiency = data_final[['scr_gebaeude_id']]

# Füge Spalten v_hrc_eff_i aus data_te zu subset heat_recovery_efficiency hinzu
for x in range(10):
    x += 1
    heat_recovery_efficiency['v_hrc_type_' + str(x)] = heat_recovery_efficiency['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['v_hrc_type_' + str(x)])
    heat_recovery_efficiency['v_hrc_eff_' + str(x)] = heat_recovery_efficiency['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['v_hrc_eff_' + str(x)])

# Ersetze 0 durch np.nan in allen Spalten
heat_recovery_efficiency = heat_recovery_efficiency.replace(0, np.nan)

# in v_hrc_eff_1 und v_hrc_eff3 teilweise WRK-k ungleich 0: Wenn WRG-k, dann ersetze Wert mit 0
heat_recovery_efficiency['v_hrc_eff_1'] = np.where(heat_recovery_efficiency['v_hrc_type_1'] == 'WRG-k', np.nan, heat_recovery_efficiency['v_hrc_eff_1'])
heat_recovery_efficiency['v_hrc_eff_3'] = np.where(heat_recovery_efficiency['v_hrc_type_3'] == 'WRG-k', np.nan, heat_recovery_efficiency['v_hrc_eff_3'])

# Ersetze alle WRG-k mit np.nan
heat_recovery_efficiency = heat_recovery_efficiency.replace('WRG-k', np.nan)

heat_recovery_efficiency = heat_recovery_efficiency.set_index('scr_gebaeude_id')
heat_recovery_efficiency['heat_recovery_efficiency_building_mean'] = heat_recovery_efficiency.mean(axis = 1)
heat_recovery_efficiency = heat_recovery_efficiency.reset_index()

# Wenn heat_recovery_efficiency_building_mean = np.nan und ein belieber Eintrag in einer weiteren Spalte vorhanden, dann 
# fülle heat_recovery_efficiency_building_mean mit Mittelwert
heat_recovery_efficiency_mean_te = heat_recovery_efficiency['heat_recovery_efficiency_building_mean'].mean(axis = 0)
heat_recovery_efficiency = heat_recovery_efficiency.set_index('scr_gebaeude_id')
heat_recovery_efficiency['heat_recovery_efficiency_building_mean'] = np.where((pd.isnull(heat_recovery_efficiency['heat_recovery_efficiency_building_mean']) == True & 
                                                                                heat_recovery_efficiency.any(axis = 1)), 
                                                                                heat_recovery_efficiency_mean_te, heat_recovery_efficiency['heat_recovery_efficiency_building_mean'])
# Alle anderen Gebäude besitzen keine WR, daher WRG = 0
heat_recovery_efficiency['heat_recovery_efficiency_building_mean'] = heat_recovery_efficiency['heat_recovery_efficiency_building_mean'].replace(np.nan, 0)

# Füge Ergebnisse zu data_final hinzu 
data_final['heat_recovery_efficiency'] = data_final['scr_gebaeude_id'].map(heat_recovery_efficiency['heat_recovery_efficiency_building_mean'])


# heating_supply_system ######################################################
##############################################################################
heating_supply_system = data_final[['scr_gebaeude_id']]

for x in range(7):
    x += 1
    heating_supply_system['h_type_' + str(x)] = heating_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['h_type_' + str(x)])
    heating_supply_system['h_fuel_' + str(x)] = heating_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['h_fuel_' + str(x)])
    heating_supply_system['h_part_' + str(x)] = heating_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['h_part_' + str(x)])
    heating_supply_system['h_power_' + str(x)] = heating_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['h_power_' + str(x)])
    
    heating_supply_system['h_type_' + str(x)] = heating_supply_system['h_type_' + str(x)].replace(' -', np.nan)
    heating_supply_system['h_power_' + str(x)] = heating_supply_system['h_power_' + str(x)].replace('nicht bekannt', np.nan)
    heating_supply_system['h_power_' + str(x)] = heating_supply_system['h_power_' + str(x)].replace(0, np.nan)
    heating_supply_system['h_power_' + str(x)] = heating_supply_system['h_power_' + str(x)].replace('250-285', 276.5)
    heating_supply_system['h_power_' + str(x)] = heating_supply_system['h_power_' + str(x)].replace('200-300', 250)
    
# Ersetze solar mit np.nan
heating_supply_system = heating_supply_system.replace('solar', np.nan)
# Ersetze 'no' mit np.nan
heating_supply_system = heating_supply_system.replace('no', np.nan)
    
def h_type_1_only(row):
    if ((pd.isnull(row['h_type_1']) == False) and 
            (pd.isnull(row['h_type_2']) == True) and
            (pd.isnull(row['h_type_3']) == True) and
            (pd.isnull(row['h_type_4']) == True) and
            (pd.isnull(row['h_type_5']) == True) and
            (pd.isnull(row['h_type_6']) == True) and
            (pd.isnull(row['h_type_7']) == True)):
        value = row['h_type_1'] 
    else: 
        value = np.nan
    return value    

heating_supply_system['h_type_1_only'] = heating_supply_system.apply(h_type_1_only, axis = 1) 

# Heating supply systems die genau einen Wärmeerzeuger haben
heating_supply_system_only_one = heating_supply_system.loc[heating_supply_system['h_type_1_only'].notnull()]
heating_supply_system_only_one = heating_supply_system_only_one.drop(['h_type_1_only'], axis = 1) 
# Erstelle davon DF
heating_supply_system_ready = heating_supply_system_only_one[['scr_gebaeude_id', 'h_type_1', 'h_fuel_1', 'h_power_1']]
heating_supply_system_ready = heating_supply_system_ready.rename(columns = {'h_type_1': 'h_type',
                                                                              'h_fuel_1': 'h_fuel',
                                                                              'h_power_1': 'h_power'})
 
# Heating supply systems die mehr als einen Wärmeerzeuger haben
heating_supply_system_more_than_one = heating_supply_system.loc[heating_supply_system['h_type_1_only'].isnull()]  
heating_supply_system_more_than_one = heating_supply_system_more_than_one.drop(['h_type_1_only'], axis = 1)  
# Speichere DF mit mehr als einem Wärmeerzeuger als Excel 
# heating_supply_system_more_than_one.to_excel("heating_supply_system_more_than_one.xlsx", index = False)

# Auswahl des Heating Supply Systems via Excel
# Auswahl nach:
# 1. Priorität: total/high/medium/fix/low
# 2. Priorität: Leistung des Wärmeerzeugers (höhere Leistung bevorzugt) 
# heating_supply_system_more_than_one_adj = pd.read_excel(r'TE_data/heating_supply_system_more_than_one_adj_Auszug.xlsx') # moved to top
heating_supply_system_more_than_one_adj['sum_h_power'] = heating_supply_system_more_than_one_adj[['h_power_1',
                                                                                                  'h_power_2',
                                                                                                  'h_power_3',
                                                                                                  'h_power_4',
                                                                                                  'h_power_5',
                                                                                                  'h_power_6',
                                                                                                  'h_power_7']].sum(axis = 1)
heating_supply_system_more_than_one_adj_sub = heating_supply_system_more_than_one_adj[['scr_gebaeude_id', 'h_type_selected', 'h_fuel_selected', 'sum_h_power']]                                                             
heating_supply_system_more_than_one_adj_sub = heating_supply_system_more_than_one_adj_sub.rename(columns = {'h_type_selected': 'h_type',
                                                                                                            'h_fuel_selected':'h_fuel', 
                                                                                                            'sum_h_power': 'h_power'})
heating_supply_system_ready = pd.concat([heating_supply_system_ready, heating_supply_system_more_than_one_adj_sub])   

# Wenn h_type == np.nan, dann fülle h_power mit np.nan
heating_supply_system_ready['h_power'] = np.where(pd.isnull(heating_supply_system_ready['h_type']), 
                                            np.nan, 
                                            heating_supply_system_ready['h_power'])


# Ersetze Labels für DIBS
cleanup_heating_supply_system = {"h_type": {
                                      'cond_imp': 'BoilerCondensingImproved',                                           
                                      'cond_from95': 'BoilerCondensingFrom95',                                        
                                      'cond_bef95': 'BoilerCondensingBefore95',                                               
                                      'l_temp_from95': 'BoilerLowTempFrom95',
                                      'l_temp_bef95': 'BoilerLowTempBefore95',
                                      'l_temp_bef87': 'BoilerLowTempBefore87',                                                 
                                      'l_temp_gas_from95': 'BoilerLowTempSpecialFrom95',                                                                    
                                      'l_temp_gas_from78': 'BoilerLowTempSpecialFrom78', 
                                      'c_temp_from95': 'BoilerStandardFrom95',                           
                                      'c_temp_bef95': 'BoilerStandardBefore95',                                                                 
                                      'c_temp_bef86': 'BoilerStandardBefore86',                                             
                                      'wood-pellet_c_temp_buffer_from95': 'SolidFuelBoiler',                                                                 
                                      'wood-chip_c_temp_buffer_from95': 'SolidFuelBoiler',
                                      'district': 'DistrictHeating',
                                      'hp_earth': 'HeatPumpGroundSource', 
                                      'hp_air': 'HeatPumpAirSource',
                                      'chp_mini': 'CHP'},
                                "h_fuel": {
                                      'gas': 'Gas',
                                      'l_gas': 'LGas',
                                      'oil': 'Oil',
                                      'biogas': 'Biogas',
                                      'wood_pellet': 'WoodPellet',
                                      'wood_chip': 'WoodChip',
                                      'distr_cog_fos': '',
                                      'distr_cog_re': '',
                                      'distr_h_fos': '',
                                      'distr_h_re': '',
                                      'el_power_mix': '',
                                      'el_power_mix_b': ''}}

heating_supply_system_ready.replace(cleanup_heating_supply_system, inplace = True)


# Kombiniere Labels für DIBS
heating_supply_system_ready['heating_supply_system'] = heating_supply_system_ready['h_fuel'] + heating_supply_system_ready['h_type']

# Ersetze BiogasCHP durch GasCHP, da im DIBS nur eine Klasse
heating_supply_system_ready['heating_supply_system'] = heating_supply_system_ready['heating_supply_system'].replace('BiogasCHP', 'GasCHP')

# Ersetze GasDistrictHeating durch DistrictHeating, da im DIBS nur eine Klasse
heating_supply_system_ready['heating_supply_system'] = heating_supply_system_ready['heating_supply_system'].replace('GasDistrictHeating', 'DistrictHeating')

# Ersetze biooilBoilerLowTempBefore95 durch OilBoilerLowTempBefore95
heating_supply_system_ready['heating_supply_system'] = heating_supply_system_ready['heating_supply_system'].replace('biooilBoilerLowTempBefore95', 'OilBoilerLowTempBefore95')

# Wenn kein heating_system, dann NoHeating
heating_supply_system_ready['heating_supply_system'] = np.where(pd.isnull(heating_supply_system_ready['h_type']), 'NoHeating', heating_supply_system_ready['heating_supply_system'])
heating_supply_system_ready.loc[heating_supply_system_ready['scr_gebaeude_id'] == 'NI3891128_0_00', 'heating_supply_system'] = 'GasBoilerStandardBefore95'

# Füge Ergebnisse zu data_final hinzu
data_final['heating_supply_system'] = data_final['scr_gebaeude_id'].map(heating_supply_system_ready.set_index('scr_gebaeude_id')['heating_supply_system'])  

                            
# heating_emission_system ####################################################
##############################################################################
heating_emission_system = data_final[['scr_gebaeude_id']]

for x in range(50):
    x += 1
    heating_emission_system['z_heat_sys_' + str(x)] = heating_emission_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_heat_sys_' + str(x)])  

heating_emission_system = heating_emission_system.set_index('scr_gebaeude_id')
heating_emission_system['heating_emission_sys_most_freq'] = heating_emission_system.mode(axis = 1).iloc[:, 0]
heating_emission_system = heating_emission_system.reset_index()
heating_emission_system['heating_emission_system'] = heating_emission_system['heating_emission_sys_most_freq'].copy()

cleanup_heating_emission_system = {"heating_emission_system": {
                                      'Elektrische Direktheizung': 'AirConditioning',
                                      'Elektrische Speicherheizung': 'AirConditioning',
                                      'Flächen-Heizung (55/45) [Standard]': 'SurfaceHeatingCooling',
                                      'Flächen-Heizung (35/28)': 'SurfaceHeatingCooling',
                                      'Heizkörper (55/45)': 'AirConditioning',
                                      'Heizkörper (70/55) [Standard]': 'AirConditioning',
                                      'Heizkörper (90/70)': 'AirConditioning',
                                      'indirekt beheizt': 'ThermallyActivated',
                                      'Luftheizung': 'AirConditioning',
                                      'Strahlungsheizung (Gas)': 'AirConditioning'}}
heating_emission_system.replace(cleanup_heating_emission_system, inplace = True)
heating_emission_system.replace(np.nan, 'AirConditioning',  inplace = True) #Replacing nan to 'AirConditioning'
   
data_final['heating_emission_system'] = data_final['scr_gebaeude_id'].map(heating_emission_system.set_index('scr_gebaeude_id')['heating_emission_system'])

# Wenn kein heating_supply_system, auch kein heating_emission_system
data_final['heating_emission_system'] = np.where((data_final['heating_supply_system'] == 'NoHeating'), 'NoHeating', data_final['heating_emission_system'])

# cooling_supply_system ######################################################
##############################################################################
cooling_supply_system = data_final[['scr_gebaeude_id']]

for x in range(7):
    x += 1
    cooling_supply_system['c_type_' + str(x)] = cooling_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['c_type_' + str(x)])
    cooling_supply_system['c_chil_type_' + str(x)] = cooling_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['c_chil_type_' + str(x)])
    cooling_supply_system['c_power_' + str(x)] = cooling_supply_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['c_power_' + str(x)])

cooling_supply_system = cooling_supply_system.replace('n.bek.', np.nan) 
cooling_supply_system = cooling_supply_system.replace('nicht bekannt', np.nan)
cooling_supply_system = cooling_supply_system.replace('unbekannt', np.nan)
cooling_supply_system = cooling_supply_system.replace(0, np.nan)

cooling_supply_system['cooling_supply_system_chil'] = cooling_supply_system['c_chil_type_1']

cleanup_cooling_supply_system = {"cooling_supply_system_chil": {
                                      'air-pi-so step': 'AirCooledPistonScrollMulti',
                                      'air-pi-so on/of': 'AirCooledPistonScroll',
                                      'wat-pi-so on/of': 'WaterCooledPistonScroll',
                                      'abso-standard': 'AbsorptionRefrigerationSystem'
                                      }}
cooling_supply_system.replace(cleanup_cooling_supply_system, inplace = True)

data_final['cooling_supply_system'] = data_final['scr_gebaeude_id'].map(cooling_supply_system.set_index('scr_gebaeude_id')['cooling_supply_system_chil'])


# cooling_emission_system ####################################################
##############################################################################
cooling_emission_system = data_final[['scr_gebaeude_id']]   

for x in range(50):
    x += 1
    cooling_emission_system['z_cool_sys_' + str(x)] = cooling_emission_system['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['z_cool_sys_' + str(x)])
 
cooling_emission_system = cooling_emission_system.replace('keins', np.nan)

cooling_emission_system = cooling_emission_system.set_index('scr_gebaeude_id')
cooling_emission_system['cooling_emission_sys_most_freq'] = cooling_emission_system.mode(axis = 1).iloc[:, 0]
cooling_emission_system = cooling_emission_system.reset_index()
cooling_emission_system['cooling_emission_system'] = cooling_emission_system['cooling_emission_sys_most_freq'].copy()

cleanup_cooling_emission_system = {"cooling_emission_system": {
                                      '6 / 12 °C': 'AirConditioning',
                                      'Bauteilaktivierung': 'ThermallyActivated',
                                      'Kompaktklimagerät (Fenster, Wand)': 'AirConditioning',
                                      'Kühldecke': 'SurfaceHeatingCooling',
                                      'Multi-Split-System - ein/aus': 'AirConditioning',
                                      'Multi-Split-System - stetig geregelt': 'AirConditioning',
                                      'Split-System - ein/aus': 'AirConditioning',
                                      'Split-System - stetig geregelt': 'AirConditioning',
                                      'VRF-System variabler Kühlmassenstrom': 'AirConditioning',
                                      'Ventilatorkonvektor': 'AirConditioning'}}
cooling_emission_system.replace(cleanup_cooling_emission_system, inplace = True)

data_final['cooling_emission_system'] = data_final['scr_gebaeude_id'].map(cooling_emission_system.set_index('scr_gebaeude_id')['cooling_emission_system'])

# Wenn es für Gebäude ein cooling_emission_system gibt, aber kein cooling_supply_system, dann vermutlich
# dezentrale Kälteerzeugung --> Lösche Kälteanlage im Gebäude
# Wenn keine Angaben zum cooling_emission_system gemacht wurden, aber Angaben zum cooling_supply_system lösche Kälteanlage ebenso
data_final['cooling_supply_system_adj'] = np.where(((pd.isnull(data_final['cooling_supply_system']) == False) & (pd.isnull(data_final['cooling_emission_system']) == False)), data_final['cooling_supply_system'], np.nan)
data_final['cooling_emission_system_adj'] = np.where(((pd.isnull(data_final['cooling_supply_system']) == False) & (pd.isnull(data_final['cooling_emission_system']) == False)), data_final['cooling_emission_system'], np.nan)

# Wenn kein cooling_supply_system, dann NoCooling
data_final['cooling_supply_system_adj'] = np.where(pd.isnull(data_final['cooling_supply_system_adj']), 'NoCooling', data_final['cooling_supply_system_adj'])

# Wenn kein cooling_emission_system, NoCooling
data_final['cooling_emission_system_adj'] = np.where(pd.isnull(data_final['cooling_emission_system_adj']), 'NoCooling', data_final['cooling_emission_system_adj'])
    

# max_heating_energy_per_floor_area ##########################################
# max_cooling_energy_per_floor_area ##########################################
##############################################################################
# data_final['max_heating_energy_per_floor_area'] = -np.inf
data_final['max_heating_energy_per_floor_area'] = data_final['scr_gebaeude_id'].map(heating_supply_system_ready.set_index('scr_gebaeude_id')['h_power'])
data_final['max_heating_energy_per_floor_area'] = data_final['max_heating_energy_per_floor_area'] * 1000
data_final['max_heating_energy_per_floor_area'] = data_final['max_heating_energy_per_floor_area'].replace(0, np.nan)


# data_final['max_cooling_energy_per_floor_area'] = np.inf
cooling_supply_system['max_cooling_energy_per_floor_area'] = cooling_supply_system[['c_power_1', 'c_power_2', 'c_power_3', 'c_power_4', 'c_power_5', 'c_power_6', 'c_power_7']].sum(axis=1)
cooling_supply_system['max_cooling_energy_per_floor_area'] = cooling_supply_system['max_cooling_energy_per_floor_area'].replace(0, np.nan)
                                                                
data_final['max_cooling_energy_per_floor_area'] = data_final['scr_gebaeude_id'].map(cooling_supply_system.set_index('scr_gebaeude_id')['max_cooling_energy_per_floor_area'])
data_final['max_cooling_energy_per_floor_area'] = data_final['max_cooling_energy_per_floor_area'] * -1000


# Setze max_cooling_energy_per_floor_area = -inf
# max_heating_energy_per_floor_area = inf
# Wenn keine Werte vorhanden
data_final['max_cooling_energy_per_floor_area'] = np.where(pd.isnull(data_final['max_cooling_energy_per_floor_area']), -np.inf, data_final['max_cooling_energy_per_floor_area'])
data_final['max_heating_energy_per_floor_area'] = np.where(pd.isnull(data_final['max_heating_energy_per_floor_area']), np.inf, data_final['max_heating_energy_per_floor_area'])

data_final['max_cooling_energy_per_floor_area'] = np.where(data_final['cooling_supply_system_adj'] == 'NoCooling', 0, data_final['max_cooling_energy_per_floor_area'])
data_final['max_heating_energy_per_floor_area'] = np.where(data_final['heating_supply_system'] == 'NoHeating', 0, data_final['max_heating_energy_per_floor_area'])
    

# ach_min ####################################################################
############################################################################## 
data_final['Außenluftvolumenstrom'] = data_final['typ_18599'].map(profile_data.set_index('typ_18599')['Außenluftvolumenstrom'])

# Mindestaußenluftvolumenstrom in 18599-10 in m³/hm² angegeben, um auf 1/h umzurechnen muss Volumenstrom mit Kehrwert (also m²/m³) multipliziert werden
data_final['ach_min'] = (data_final['Außenluftvolumenstrom'] * data_final['net_room_area']) / (data_final['net_room_area'] * (data_final['building_height']/data_final['b_storey_nr_1']))

# # Einschub Anfang (prozentualer Verteilung von Standardnutzungszonen)
# ##############################################################################
# # Berechnung des Mindestaußenluftvolumenstroms nach prozentualer Verteilung der Standardnutzungszonen für Hörsaalgebäude
# data_final = data_final.loc[data_final['uk_geb'] == 'Hörsaalgebäude', :]

# nutzungszonen_mix = pd.DataFrame({
#         'typ_18599': ['Verkehrsfläche (Flur)', 
#                         'Hörsaal, Auditorium',
#                         'Lager (Technik, Archiv)',
#                         'Besprechung/Sitzungszimmer/Seminar',
#                         'WC und Sanitärräume in Nichtwohngebäuden',
#                         'Einzelbüro',
#                         'Sonstige Aufenthaltsräume (Garderobe, Teeküche, Lager, Archiv, Flur)',
#                         'Labor',
#                         'Gruppenbüro (2 bis 6 Arbeitsplätze)',
#                         'Theater (Foyer)'],
#         'zonenfläche_prozent':
#          [0.334, 0.26, 0.2, 0.084, 0.026, 0.023, 0.018, 0.016, 0.12, 0.11]})
# nutzungszonen_mix['außenluftvolumenstrom'] = nutzungszonen_mix['typ_18599'].map(profile_data.set_index('typ_18599')['Außenluftvolumenstrom'])

# nutzungszonen_mix['product'] = nutzungszonen_mix['zonenfläche_prozent'] * nutzungszonen_mix['außenluftvolumenstrom']
# außenluftvolumenstrom_mix = nutzungszonen_mix['product'].sum()

# # Mindestaußenluftvolumenstrom in 18599-10 in m³/hm² angegeben, um auf 1/h umzurechnen muss Volumenstrom mit Kehrwert (also m²/m³) multipliziert werden
# data_final['ach_min'] = (data_final['Außenluftvolumenstrom'] * data_final['net_room_area']) / (data_final['net_room_area'] * (data_final['building_height']/data_final['b_storey_nr_1']))

# Einschub Ende
##############################################################################
    
# ach_inf ###################################################################
############################################################################## 
data_final['gebäudedichtheit'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['b_air_tight'])

ach_inf = data_final[['scr_gebaeude_id', 'gebäudedichtheit', 'facade_area_south', 'facade_area_east', 'facade_area_west', 'facade_area_north', 'roof_area', 'building_depth', 'building_width', 'building_height', 'base_area', 'baujahr']]
ach_inf['n_50_standard_av'] = data_final['gebäudedichtheit'].copy()

cleanup_gebäudedichtheit = {"n_50_standard_av": {
                                    'Passivhausanforderung erfüllt': 0.6,
                                    'Neubau mit Dichtheitstest und raumlufttechnische Anlage': 1,
                                    'Neubau mit Dichtheitstest ohne raumlufttechnische Anlage': 2,
                                    'Neubau ohne Dichtheitstest': 4,
                                    'Bestehendes Gebäude ohne Dichtheitstest': 6,
                                    'Bestehndes Gebäude mit offensichtlichen Undichtheiten': 10}}
ach_inf.replace(cleanup_gebäudedichtheit, inplace = True)

ach_inf['standard av-verhältnis'] = 0.9

# AV-Verhältnis Gebäude = Thermische Hüllfläche des Gebäudes / beheiztes Bruttogebäudevolumen
ach_inf['facade_area'] = ach_inf['facade_area_south'] + ach_inf['facade_area_east'] + ach_inf['facade_area_west'] + ach_inf['facade_area_north']
ach_inf['av-verhältnis'] = (ach_inf['facade_area'] + ach_inf['roof_area'] + (ach_inf['base_area'])) / (ach_inf['base_area'] * ach_inf['building_height'])
# ach_inf['av-verhältnis'] = ach_inf['av-verhältnis'].replace(np.nan, 0)

# Luftdichtheit n50
ach_inf['n_50'] = ach_inf['n_50_standard_av'] * ach_inf['av-verhältnis'] / ach_inf['standard av-verhältnis']


# Abschätzung der Infiltrationsluftwechselrate nach ISO 13789 bzw. der früheren EN 832
# ach_inf = n_50 * e * fATD
# mit e = 0.07 (DIN V 18599-2, S. 58)
# mit fATD = 1 (keine Außenluftdurchlässe: Annahme, da keine Informationen vorhanden)
ach_inf['ach_inf'] = ach_inf['n_50'] * 0.07

data_final['ach_inf'] = data_final['scr_gebaeude_id'].map(ach_inf.set_index('scr_gebaeude_id')['ach_inf'])


# Nennvolumenstrom Zuluft in [m³/h] von RLT ##################################
##############################################################################
# Füge Anzahl der RLT-Anlagen hinzu, wenn keine Angabe, dann Annahme, dass keine RLT-Anlage existiert
data_final['anzahl_rlt_anlagen'] = data_final['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['number_of_HVACs'])
data_final['anzahl_rlt_anlagen'] = data_final['anzahl_rlt_anlagen'].replace(np.nan, 0)

rlt_vol_zu = data_final[['scr_gebaeude_id']]  

for x in range(10):
    x +=1
    rlt_vol_zu['v_vol_in_' + str(x)] = rlt_vol_zu['scr_gebaeude_id'].map(data_te.set_index('pr_var_name')['v_vol_in_' + str(x)])

rlt_vol_zu = rlt_vol_zu.replace('??', np.nan) 
rlt_vol_zu = rlt_vol_zu.replace('n.bek.', np.nan)    
rlt_vol_zu = rlt_vol_zu.replace('nicht bekannt', np.nan)  
rlt_vol_zu = rlt_vol_zu.replace(0, np.nan) 

rlt_vol_zu['rlt_flow_mean'] = rlt_vol_zu.mean(axis = 1, skipna = True)
rlt_vol_zu['rlt_flow_sum'] = rlt_vol_zu.sum(axis = 1, skipna = True)

data_final['rlt_flow_mean'] = data_final['scr_gebaeude_id'].map(rlt_vol_zu.set_index('scr_gebaeude_id')['rlt_flow_mean'])
data_final['rlt_flow_sum'] = data_final['scr_gebaeude_id'].map(rlt_vol_zu.set_index('scr_gebaeude_id')['rlt_flow_sum'])
data_final['rlt_flow_ach_mean'] = data_final['rlt_flow_mean'] / (data_final['base_area'] * data_final['building_height'])
data_final['rlt_flow_ach_sum'] = data_final['rlt_flow_sum'] / (data_final['base_area'] * data_final['building_height'])

data_final['rlt_flow_ach_mean'] = data_final['rlt_flow_ach_mean'].replace(np.nan, 0) 
data_final['rlt_flow_ach_sum'] = data_final['rlt_flow_ach_sum'].replace(np.nan, 0)


# ach_vent ###################################################################
##############################################################################
# Fallunterscheidung:
# (ach_min > ach_inf) & (AnzahlRLT = 0): Mindestluftwechsel wird durch Fensterlüftung gedeckt (ach_inf_win = ach_min)
# (ach_min > ach_inf) & (AnzahlRLT > 0) & (Angabe NVS): Mindestluftwechsel wird durch NVS_zu der RLT gedeckt 
#                                                        Falls dieser nicht ausreicht wird Rest durch Fensterlüftung gedeckt                         
# (ach_min > ach_inf) & (AnzahlRLT > 0) & (keine Angabe NVS): ach_vent = ach_min - ach_inf
# (ach_min < ach_inf) & (AnzahlRLT = 0): Luftwechsel durch Infiltration übersteigt Mindestluftwechsel, ok
# (ach_min < ach_inf) & (AnzahlRLT > 0) & (Angabe NVS): Luftwechsel durch Infiltration übersteigt Mindestluftwechsel,
#                                                        ach_vent = NVS_zu [in 1/h]
# (ach_min < ach_inf) & (AnzahlRLT > 0) & (keine Angabe NVS): Luftwechsel durch Infiltration übersteigt Mindestluftwechsel, ach_vent negativ, ach_vent = ach_vent_adj = 0 
    
def calc_ach_inf_win(row):   
    if (row['ach_min'] > row['ach_inf']):
        if row['anzahl_rlt_anlagen'] == 0:
            ach_inf_win = row['ach_min']                       # Infl wird durch Fensterlüftung gedeckt
        elif ((row['anzahl_rlt_anlagen'] > 0) & (row['rlt_flow_ach_mean'] > 0) & (row['rlt_flow_ach_mean'] < (row['ach_min'] - row['ach_inf']))):    
            ach_inf_win = row['ach_min'] - row['rlt_flow_ach_mean']    # RLT kann min nicht decken, Rest durch Fenster
        else:
            ach_inf_win = row['ach_inf']
    else:
        ach_inf_win = row['ach_inf']
        
    return ach_inf_win
        
data_final['ach_inf_win'] = data_final.apply(calc_ach_inf_win, axis = 1) 
data_final['ach_win'] = data_final['ach_inf_win'] - data_final['ach_inf']
  
def calc_ach_vent(row):
    if (row['ach_min'] > row['ach_inf']):
        if row['anzahl_rlt_anlagen'] == 0:
            ach_vent = 0
        elif ((row['anzahl_rlt_anlagen'] > 0) & (row['rlt_flow_ach_mean'] > 0)):    
            ach_vent = row['rlt_flow_ach_mean']
        else: # anzahl_rlt_anlagen > 0 & rlt_flow_ach_mean = 0
            ach_vent = row['ach_min'] - row['ach_inf']
    elif ((row['ach_min'] < row['ach_inf']) & (row['rlt_flow_ach_mean'] > 0)): 
        ach_vent = row['rlt_flow_ach_mean']
    else: 
        ach_vent = 0
        
    return ach_vent    

data_final['ach_vent'] = data_final.apply(calc_ach_vent, axis = 1) 


# night_flushing_flow ########################################################
##############################################################################
# Setze vorerst für alle Gebäude Null, da es keine Informationen darüber gibt ob Gebäude Nachtlüftung hat 
data_final['night_flushing_flow'] = 0


# lighting_utilisation_factor ################################################
##############################################################################
data_final['lighting_utilisation_factor'] = 0.45


##############################################################################
##############################################################################
# Clean data_final
##############################################################################
##############################################################################
data_final.drop([
                'building_area_value_heated_cooled_share', 
                'b_th_mass',
                'b_storey_nr_1',
                'b_gl_type_south',
                'b_gl_type_east',
                'b_gl_type_west',
                'b_gl_type_north',
                'most_freq_verglasungstyp',
                'bak',
                'B',
                'R',
                'rlt_flow_mean',
                'rlt_flow_sum',
                'rlt_flow_ach_mean',
                'rlt_flow_ach_sum',
                'ach_inf_win'], axis = 1, inplace = True) 


for x in range(Number_of_lights): 
    x += 1    
    data_final.drop(['p_j_' + str(x)], axis = 1, inplace = True)



##############################################################################
##############################################################################
SimulationData_Tiefenerhebung = data_final[[
                          'scr_gebaeude_id',
                          'plz',
                          'hk_geb',
                          'uk_geb',
                          'max_occupancy',
                          'wall_area_og',
                          'wall_area_ug',
                          'window_area_north',
                          'window_area_east',
                          'window_area_south',
                          'window_area_west',
                          'roof_area',
                          'net_room_area',
                          'base_area',
                          'energy_ref_area',
                          'building_height',
                          'lighting_load',
                          'lighting_control',
                          'lighting_utilisation_factor',
                          'lighting_maintenance_factor',
                          'glass_solar_transmittance',
                          'glass_solar_shading_transmittance',
                          'glass_light_transmittance',
                          'u_windows',
                          'u_walls',
                          'u_roof',
                          'u_base',
                          'temp_adj_base',
                          'temp_adj_walls_ug',
                          'ach_inf',
                          'ach_win',
                          'ach_vent',
                          'heat_recovery_efficiency',
                          'thermal_capacitance',
                          't_start',
                          't_set_heating',
                          't_set_cooling',
                          'night_flushing_flow',
                          'max_cooling_energy_per_floor_area',
                          'max_heating_energy_per_floor_area',
                          'heating_supply_system',  
                          'cooling_supply_system_adj',
                          'heating_emission_system',
                          'cooling_emission_system_adj']] 

SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.rename(columns = {'cooling_supply_system_adj': 'cooling_supply_system',
                                                                                    'cooling_emission_system_adj': 'cooling_emission_system'})


# # Entferne Gebäude RP90947_0_00, da keine Angaben zum Baujahr und Bauschwere
# # Entferne Gebäude NW977117_1_00, da keine Angaben zum Baujahr und Bauschwere
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.set_index('scr_gebaeude_id')
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.drop('RP90947_0_00')
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.drop('NW977117_1_00')
# # Entferne Gebäude RP2353061_1_00, da keine Angaben zum Wärmeübergabesystem
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.drop('RP2353061_1_00')
# # Entferne Gebäude NI4601502_0_00, da unbeheizt (building_area_value_heated_cooled = 0) und damit net_room_area = inf
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.drop('NI4601502_0_00')
# SimulationData_Tiefenerhebung = SimulationData_Tiefenerhebung.reset_index()

# Save data to \iso_simulator\examples\SimulationData_Tiefenerhebung.csv
SimulationData_Tiefenerhebung.to_csv(r'..\..\iso_simulator\annualSimulation\SimulationData_Tiefenerhebung.csv', index = False, sep = ';') 

