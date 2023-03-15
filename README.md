![DIBS_Logo](doc/img/DIBS_Logo.png)
Dynamic ISO Building Simulator (DIBS) is a simulation program for calculating the space heating, occupancy hot water, cooling and electricity demand of German non-residential buildings. Further the DIBS calculates the heating value based energy uses, the primary energy and the greenhouse gas emission based on the defined factors of the German building energy ordinance (Gebäudeenergiegesetz). The adapted hourly dynamic building energy simulator for single buildings and building stocks is ready to use with [ENOB:dataNWG interview](https://www.datanwg.de/stichprobenerhebung/breitenerhebung) and [on-site inspection](https://www.datanwg.de/stichprobenerhebung/tiefenerhebung) data. The underlying resistance-capacity-model is based on the simplified hourly method of ISO 13790:2008. DIBS is based on the [RC_BuildingSimulator](https://github.com/architecture-building-systems/RC_BuildingSimulator) and represents an extension of capabilities and adaptation to the requirements of the ENOB:dataNWG project.

## Getting Started
You can install DIBS via downloading the zip file or either clone this repository. Unfortunately there's no pip install at this stage. 

Python packages you need to use DIBS:  
- [Pandas](https://pypi.org/project/pandas/)
- [Numpy](https://pypi.org/project/numpy/)
- [Namedlist](https://pypi.org/project/namedlist/)
- [Geopy](https://pypi.org/project/geopy/)

## Further information

For a detailed installation guide and further information on DIBS see the [wiki](https://github.com/IWUGERMANY/DIBS---Dynamic-ISO-Building-Simulator/wiki)

## References
- DIN EN ISO 13790:2008-09. Energieeffizienz von Gebäuden - Berechnung des Energiebedarfs für Heizung und Kühlung (ISO 13790:2008). Berlin: Beuth Verlag.
- Jayathissa, P. (2020). 5R1C Building Simulation Model. URL: https://github.com/architecture-building-systems/RC_BuildingSimulator  

---

## Publications
- Bischof, Julian; Knoll, Simon; Duffy, Aidan (2022): DEVELOPMENT OF A PYTHON-BASED SIMPLIFIED HOURLY BUILDING MODEL FOR NON-DOMESTIC BUILDING STOCK OPERATIONAL ENERGY SIMULATIONS. In the proceedings of the BauSIM 2022 in Weimar, 20. – 22. September 2022. In: BauSIM2022 2022. URL: https://www.researchgate.net/publication/364386249_DEVELOPMENT_OF_A_PYTHON-BASED_SIMPLIFIED_HOURLY_BUILDING_MODEL_FOR_NON-DOMESTIC_BUILDING_STOCK_OPERATIONAL_ENERGY_SIMULATIONS.

---

The Dynamic ISO Building Simulator has been developed in context of the 'ENOB:DataNWG Forschungsdatenbank Nichtwohngebäude' (www.datanwg.de) project and the project 'FlexGeber - Demonstration of flexibility options in the building sector and their integration with the energy system in Germany' at Institut Wohnen und Umwelt (IWU), Darmstadt.
<p float="left">
  <img src="doc/img/IWU_Logo.PNG" width="15%" /> 
</p>  

<b>ENOB:DataNWG<b>
<b>Funding code:</b>  Fkz.: 03ET1315  
<b>Project duration:</b>  01.12.2015 until 31.05.2021

<b>FlexGeber<b>
<b>Funding code:</b>  Fkz.: 03EGB0001  
<b>Project duration:</b>  01.10.2017 until 31.07.2022
  
<b>Both funded by:</b> 
<p float="left">
  <img src="doc/img/BMWi_Logo.png" width="30%" /> 
</p> 
in accordance with the parliamentary resolution of the German Parliament.

Total number of individual page views: 
<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/kye4dwl8mw0i15cfzxfk" alt="trackgit-views" />
</a>
