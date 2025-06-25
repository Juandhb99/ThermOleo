alcohol_code = {
        
    0: 'No alcohol', 
    1: 'Methanol',
    2: 'Ethanol',
    3: 'Propanol',
    4: 'Glycerol'

}

references = {
    
    '1a': ['B. B. França, F. M. Pinto, F. L. P. Pessoa, and A. M. C. Uller, “Liquid−Liquid Equilibria for Castor Oil Biodiesel + Glycerol + Alcohol,” J Chem Eng Data, vol. 54, no. 9, pp. 2359–2364, Sep. 2009, doi: 10.1021/je800564d.', 
           'Castor oil biodiesel - Methanol - Glycerol'],
    
    '2a': ['F. M. R. Mesquita, A. M. M. Bessa, D. D. de Lima, H. B. de Sant’Ana, and R. S. de Santiago-Aguiar, “Liquid–liquid equilibria of systems containing cottonseed biodiesel+glycerol+ethanol at 293.15, 313.15 and 333.15K,” Fluid Phase Equilib, vol. 318, pp. 51–55, Mar. 2012, doi: 10.1016/j.fluid.2012.01.016', 
           'Cottonseed oil biodiesel - Ethanol - Glycerol'],
    
    '3a': ['R. C. Basso, A. J. de Almeida Meirelles, and E. A. C. Batista, “Liquid–liquid equilibrium of pseudoternary systems containing glycerol+ethanol+ethylic biodiesel from crambe oil (Crambe abyssinica) at T/K=(298.2, 318.2, 338.2) and thermodynamic modeling,” Fluid Phase Equilib, vol. 333, pp. 55–62, Nov. 2012, doi: 10.1016/j.fluid.2012.07.018.', 
           'Cambre oil biodiesel - Ethanol - Glycerol'],
   
    '4a': ['M. Rostami, S. Raeissi, M. Mahmoodi, and M. Nowroozi, “Liquid–Liquid Equilibria in Biodiesel Production,” J Am Oil Chem Soc, vol. 90, no. 1, pp. 147–154, Jan. 2013, doi: 10.1007/s11746-012-2144-5.',
           'Sunflower oil biodiesel - Methanol - Glycerol'],
    
    '5a': ['M. Rostami, S. Raeissi, M. Mahmoodi, and M. Nowroozi, “Liquid–Liquid Equilibria in Biodiesel Production,” J Am Oil Chem Soc, vol. 90, no. 1, pp. 147–154, Jan. 2013, doi: 10.1007/s11746-012-2144-5.', 
           'Canola oil biodiesel - Methanol - Glycerol'], 
    
    '6a': ['X. Liu, X. Piao, Y. Wang, and S. Zhu, “Liquid–Liquid Equilibrium for Systems of (Fatty Acid Ethyl Esters + Ethanol + Soybean Oil and Fatty Acid Ethyl Esters + Ethanol + Glycerol),” J Chem Eng Data, vol. 53, no. 2, pp. 359–362, Feb. 2008, doi: 10.1021/je700382s.',
           'Soybean oil biodiesel - Ethanol - Glycerol'],  
    
    '7a': ['J. R. F. Silva et al., “Thermophysical properties of biodiesel and related systems: (Liquid + liquid) equilibrium data for Jatropha curcas biodiesel,” J Chem Thermodyn, vol. 58, pp. 467–475, Mar. 2013, doi: 10.1016/j.jct.2012.10.006.',
           'Jatropha oil biodiesel - Methanol - Glycerol'],
    
    '8a': ['M. A. Mazutti et al., “Thermophysical properties of biodiesel and related systems: (Liquid + liquid) equilibrium data for soybean biodiesel,” J Chem Thermodyn, vol. 58, pp. 83–94, Mar. 2013, doi: 10.1016/j.jct.2012.10.026.',
           'Soybean oil biodiesel - Methanol - Glycerol'],
    
    '9a': ['A. B. Machado, Y. C. Ardila, L. H. de Oliveira, M. Aznar, and M. R. Wolf Maciel, “Liquid–Liquid Equilibria in Ternary and Quaternary Systems Present in Biodiesel Production from Soybean Oil at (298.2 and 333.2) K,” J Chem Eng Data, vol. 57, no. 5, pp. 1417–1422, May 2012, doi: 10.1021/je201243u.',
           'Soybean oil biodiesel - Ethanol - Glycerol'],
    
    '10a': ['F. M. R. Mesquita, F. X. Feitosa, N. E. Sombra, R. S. de Santiago-Aguiar, and H. B. de Sant’Ana, “Liquid–Liquid Equilibrium for Ternary Mixtures of Biodiesel (Soybean or Sunflower) + Glycerol + Ethanol at Different Temperatures,” J Chem Eng Data, vol. 56, no. 11, pp. 4061–4067, Nov. 2011, doi: 10.1021/je200340x.',
            'Soybean oil biodiesel - Ethanol - Glycerol'],
    
    '10b': ['F. M. R. Mesquita, F. X. Feitosa, N. E. Sombra, R. S. de Santiago-Aguiar, and H. B. de Sant’Ana, “Liquid–Liquid Equilibrium for Ternary Mixtures of Biodiesel (Soybean or Sunflower) + Glycerol + Ethanol at Different Temperatures,” J Chem Eng Data, vol. 56, no. 11, pp. 4061–4067, Nov. 2011, doi: 10.1021/je200340x.',
            'Sunflower oil biodiesel - Ethanol - Glycerol'],
    
    '11a': ['F. M. R. Mesquita, N. S. Evangelista, H. B. de Sant’Ana, and R. S. de Santiago-Aguiar, “Liquid–Liquid Equilibrium for the Glycerol + Alcohol + Coconut Biodiesel System at Different Temperatures and Atmospheric Pressure,” J Chem Eng Data, vol. 57, no. 12, pp. 3557–3562, Dec. 2012, doi: 10.1021/je300749n.',
            'Coconut oil biodiesel - Ethanol - Glycerol'],
    
    '12a': ['L. A. Follegatti-Romero, M. B. Oliveira, F. R. M. Batista, E. A. C. Batista, J. A. P. Coutinho, and A. J. A. Meirelles, “Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15K,” Fuel, vol. 94, pp. 386–394, Apr. 2012, doi: 10.1016/j.fuel.2011.09.020.',
            'Linoleic oil biodiesel - Ethanol - Glycerol'],
    
    '12b': ['L. A. Follegatti-Romero, M. B. Oliveira, F. R. M. Batista, E. A. C. Batista, J. A. P. Coutinho, and A. J. A. Meirelles, “Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15K,” Fuel, vol. 94, pp. 386–394, Apr. 2012, doi: 10.1016/j.fuel.2011.09.020.',
            'Oleic oil biodiesel - Ethanol - Glycerol'],
    
    '12c': ['L. A. Follegatti-Romero, M. B. Oliveira, F. R. M. Batista, E. A. C. Batista, J. A. P. Coutinho, and A. J. A. Meirelles, “Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15K,” Fuel, vol. 94, pp. 386–394, Apr. 2012, doi: 10.1016/j.fuel.2011.09.020.',
            'Palmitic oil biodiesel - Ethanol - Glycerol'],
    
    '12d': ['L. A. Follegatti-Romero, M. B. Oliveira, F. R. M. Batista, E. A. C. Batista, J. A. P. Coutinho, and A. J. A. Meirelles, “Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15K,” Fuel, vol. 94, pp. 386–394, Apr. 2012, doi: 10.1016/j.fuel.2011.09.020.',
            'Lauric oil biodiesel - Ethanol - Glycerol'],
           
    '13a': ['R. C. Basso, C. A. S. da Silva, C. de O. Sousa, A. J. de A. Meirelles, and E. A. C. Batista, “LLE experimental data, thermodynamic modeling and sensitivity analysis in the ethyl biodiesel from macauba pulp oil settling step,” Bioresour Technol, vol. 131, pp. 468–475, Mar. 2013, doi: 10.1016/j.biortech.2012.12.190.',
            'Macuba oil biodiesel - Ethanol - Glycerol'],    
    
    '14a': ['H. Zhou, H. Lu, and B. Liang, “Solubility of Multicomponent Systems in the Biodiesel Production by Transesterification of Jatropha c urcas L. Oil with Methanol,” J Chem Eng Data, vol. 51, no. 3, pp. 1130–1135, May 2006, doi: 10.1021/je0600294.',
            'Jatropha oil biodiesel - Methanol - Glycerol'],
    
    '15a': ['M. B. Oliveira, Sérgio. Barbedo, J. I. Soletti, S. H. V. Carvalho, A. J. Queimada, and J. A. P. Coutinho, “Liquid–liquid equilibria for the canola oil biodiesel + ethanol + glycerol system,” Fuel, vol. 90, no. 8, pp. 2738–2745, Aug. 2011, doi: 10.1016/j.fuel.2011.03.017.',
            'Canola oil biodiesel - Methanol - Glycerol'],
    
    '16a': ['M.-J. Lee, Y.-C. Lo, and H.-M. Lin, “Liquid–liquid equilibria for mixtures containing water, methanol, fatty acid methyl esters, and glycerol,” Fluid Phase Equilib, vol. 299, no. 2, pp. 180–190, Dec. 2010, doi: 10.1016/j.fluid.2010.10.010.',
            'Oleic oil biodiesel - Methanol - Glycerol'],
    
    '17a': ['A. B. Machado, Y. C. Ardila, L. H. de Oliveira, M. Aznar, and M. R. Wolf Maciel, “Liquid−Liquid Equilibrium Study in Ternary Castor Oil Biodiesel + Ethanol + Glycerol and Quaternary Castor Oil Biodiesel + Ethanol + Glycerol + NaOH Systems at (298.2 and 333.2) K,” J Chem Eng Data, vol. 56, no. 5, pp. 2196–2201, May 2011, doi: 10.1021/je101235f.',
            'Castor oil biodiesel - Ethanol - Glycerol'],
    
    '18a': ['S. C. Beneti, M. Lanza, M. A. Mazutti, M. H. Kunita, L. Cardozo-Filho, and J. Vladimir Oliveira, “Experimental (liquid+liquid) equilibrium data for ternary and quaternary mixtures of fatty acid methyl and ethyl esters (FAME/FAEE) from soybean oil,” J Chem Thermodyn, vol. 68, pp. 60–70, Jan. 2014, doi: 10.1016/j.jct.2013.08.032.',
            'Soybean oil biodiesel - Methanol - Glycerol'],
    
    '19a': ['M. Rostami, S. Raeissi, M. Ranjbaran, M. Mahmoodi, and M. Nowroozi, “Experimental investigation and modeling of liquid–liquid equilibria in two systems of concern in biodiesel production,” Fluid Phase Equilib, vol. 353, pp. 31–37, Sep. 2013, doi: 10.1016/j.fluid.2013.05.015.',
            'Corn oil biodiesel - Methanol - Glycerol'],
     
    '19b': ['M. Rostami, S. Raeissi, M. Ranjbaran, M. Mahmoodi, and M. Nowroozi, “Experimental investigation and modeling of liquid–liquid equilibria in two systems of concern in biodiesel production,” Fluid Phase Equilib, vol. 353, pp. 31–37, Sep. 2013, doi: 10.1016/j.fluid.2013.05.015.',
            'Frying oil biodiesel - Methanol - Glycerol'],
    
    '20a': ['E. G. de A. Rocha, L. A. Follegatti-Romero, S. Duvoisin, and M. Aznar, “Liquid–liquid equilibria for ternary systems containing ethylic palm oil biodiesel+ethanol+glycerol/water: Experimental data at 298.15 and 323.15K and thermodynamic modeling,” Fuel, vol. 128, pp. 356–365, Jul. 2014, doi: 10.1016/j.fuel.2014.01.074.',
            'Palm oil biodiesel - Ethanol - Glycerol'],
   
    '21a': ['A. L. Esipovich, A. E. Rogozhin, A. S. Belousov, E. A. Kanakov, K. V. Otopkova, and S. M. Danov, “Liquid–liquid equilibrium in the systems FAMEs + vegetable oil + methyl alcohol and FAMEs + glycerol + methyl alcohol,” Fuel, vol. 217, pp. 31–37, Apr. 2018, doi: 10.1016/j.fuel.2017.12.083.',
           'Rapeseed oil biodiesel - Ethanol - Rapeseed oil'],
   
    '22a': ['J. D. S. Serres, D. Soares, M. L. Corazza, N. Krieger, and D. A. Mitchell, “Liquid–liquid equilibrium data and thermodynamic modeling for systems related to the production of ethyl esters of fatty acids from soybean soapstock acid oil,” Fuel, vol. 147, pp. 147–154, May 2015, doi: 10.1016/j.fuel.2015.01.059.',
           'Soybean oil biodiesel - Ethanol - Water'],
   
    '23a': ['R. C. Basso, F. H. Miyake, A. J. de Almeida Meirelles, and E. A. C. Batista, “Liquid–liquid equilibrium data and thermodynamic modeling, at T/K=298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils,” Fuel, vol. 117, pp. 590–597, Jan. 2014, doi: 10.1016/j.fuel.2013.09.020.',
           'Crambe oil biodiesel - Ethanol - Water'],     
    
    '23b': ['R. C. Basso, F. H. Miyake, A. J. de Almeida Meirelles, and E. A. C. Batista, “Liquid–liquid equilibrium data and thermodynamic modeling, at T/K=298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils,” Fuel, vol. 117, pp. 590–597, Jan. 2014, doi: 10.1016/j.fuel.2013.09.020.',
           'Fodder radish oil biodiesel - Ethanol - Water'],     

    '23c': ['R. C. Basso, F. H. Miyake, A. J. de Almeida Meirelles, and E. A. C. Batista, “Liquid–liquid equilibrium data and thermodynamic modeling, at T/K=298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils,” Fuel, vol. 117, pp. 590–597, Jan. 2014, doi: 10.1016/j.fuel.2013.09.020.',
           'Macauba oil biodiesel - Ethanol - Water'],
   
    '24a': ['M. Maghami, J. Yousefi Seyf, S. M. Sadrameli, and A. Haghtalab, “Liquid–liquid phase equilibrium in ternary mixture of waste fish oil biodiesel–methanol–glycerol: Experimental data and thermodynamic modeling,” Fluid Phase Equilib, vol. 409, pp. 124–130, Feb. 2016, doi: 10.1016/j.fluid.2015.09.046.',
           'Waste fish oil biodiesel - Methanol - Glycerol'],      

    '25a': ['J. D. Gonçalves, M. Aznar, and G. R. Santos, “Liquid–liquid equilibrium data for systems containing Brazil nut biodiesel+methanol+glycerin at 303.15K and 323.15K,” Fuel, vol. 133, pp. 292–298, Oct. 2014, doi: 10.1016/j.fuel.2014.05.004.',
           'Brazil nut oil biodiesel - Methanol - Glycerol'],
    
    '26a': ['M. Hakim, H. Abedini Najafabadi, G. Pazuki, and M. Vossoughi, “Novel Approach for Liquid–Liquid Phase Equilibrium of Biodiesel (Canola and Sunflower) + Glycerol + Methanol,” Ind Eng Chem Res, vol. 53, no. 2, pp. 855–864, Jan. 2014, doi: 10.1021/ie4031902.',
            'Canola oil biodiesel - Methanol - Glycerol'],
    
    '26b': ['M. Hakim, H. Abedini Najafabadi, G. Pazuki, and M. Vossoughi, “Novel Approach for Liquid–Liquid Phase Equilibrium of Biodiesel (Canola and Sunflower) + Glycerol + Methanol,” Ind Eng Chem Res, vol. 53, no. 2, pp. 855–864, Jan. 2014, doi: 10.1021/ie4031902.',
            'Sunflower oil biodiesel - Methanol - Glycerol'],

    '27a': ['M. A. Mazutti et al., “Thermophysical properties of biodiesel and related systems: (Liquid+liquid) equilibrium data for castor oil biodiesel,” J Chem Thermodyn, vol. 62, pp. 17–26, Jul. 2013, doi: 10.1016/j.jct.2013.02.016.',
            'Castor oil biodiesel - Methanol/Ethanol - Glycerol - Water'],
    
    '28a': ['B. B. França, H. G. D. Villardi, F. L. P. Pessoa, and A. M. C. Uller, “Liquid–Liquid Equilibrium for Compounds of Soybean Ethyl Biodiesel Production by Transesterification,” J Chem Eng Data, vol. 58, no. 7, pp. 1927–1933, Jul. 2013, doi: 10.1021/je301313c.',
            'Soybean oil biodiesel - Ethanol - Glycerol - Water'],
    
    '29a': ['E. Batista, S. Monnerat, L. Stragevitch, C. G. Pina, C. B. Gonçalves, and A. J. A. Meirelles, “Prediction of Liquid−Liquid Equilibrium for Systems of Vegetable Oils, Fatty Acids, and Ethanol,” J Chem Eng Data, vol. 44, no. 6, pp. 1365–1369, Nov. 1999, doi: 10.1021/je9900169.',
            'Triolein - Ethanol - Oleic acid'],
    
    '29b': ['E. Batista, S. Monnerat, L. Stragevitch, C. G. Pina, C. B. Gonçalves, and A. J. A. Meirelles, “Prediction of Liquid−Liquid Equilibrium for Systems of Vegetable Oils, Fatty Acids, and Ethanol,” J Chem Eng Data, vol. 44, no. 6, pp. 1365–1369, Nov. 1999, doi: 10.1021/je9900169.',
            'Corn oil - Ethanol - Oleic acid'],    
    
    '30a': ['C. E. C. Rodrigues, É. C. D. Reipert, A. F. de Souza, P. A. P. Filho, and A. J. A. Meirelles, “Equilibrium data for systems composed by cottonseed oil+commercial linoleic acid+ethanol+water+tocopherols at 298.2K,” Fluid Phase Equilib, vol. 238, no. 2, pp. 193–203, Dec. 2005, doi: 10.1016/j.fluid.2005.09.027.',
            'Refined cottonseed oil - Ethanol - Linoelic acid - Water'],
     
    '30b': ['C. E. C. Rodrigues, É. C. D. Reipert, A. F. de Souza, P. A. P. Filho, and A. J. A. Meirelles, “Equilibrium data for systems composed by cottonseed oil+commercial linoleic acid+ethanol+water+tocopherols at 298.2K,” Fluid Phase Equilib, vol. 238, no. 2, pp. 193–203, Dec. 2005, doi: 10.1016/j.fluid.2005.09.027.',
            'Pretreated cottonseed oil - Ethanol - Linoelic acid - Water'],
    
    '31a': ['C. E. C. Rodrigues, R. Antoniassi, and A. J. A. Meirelles, “Equilibrium Data for the System Rice Bran Oil + Fatty Acids + Ethanol + Water at 298.2 K,” J Chem Eng Data, vol. 48, no. 2, pp. 367–373, Mar. 2003, doi: 10.1021/je0255978.',
            'Rice bran oil - Ethanol - Oelic acid - Water'],
    
    '32a': ['C. M. Oliveira, B. R. Garavazo, and C. E. C. Rodrigues, “Liquid–liquid equilibria for systems composed of rice bran oil and alcohol-rich solvents: Application to extraction and deacidification of oil,” J Food Eng, vol. 110, no. 3, pp. 418–427, Jun. 2012, doi: 10.1016/j.jfoodeng.2011.12.027.',
            'Rice bran oil - Ethanol - Free Fatty Acids - Water'],
    
    '33a': ['C. B. Gonçalves, E. Batista, and A. J. A. Meirelles, “Liquid−Liquid Equilibrium Data for the System Corn Oil + Oleic Acid + Ethanol + Water at 298.15 K,” J Chem Eng Data, vol. 47, no. 3, pp. 416–420, May 2002, doi: 10.1021/je010273p.',
            'Corn oil - Oleic acid - Ethanol - Water'],
    
    '34a': ['C. B. Gonçalves and A. J. A. Meirelles, “Liquid–liquid equilibrium data for the system palm oil + fatty acids + ethanol + water at 318.2 K,” Fluid Phase Equilib, vol. 221, no. 1–2, pp. 139–150, Jul. 2004, doi: 10.1016/j.fluid.2004.05.002.',
            'Palm oil - Palmitic acid - Ethanol - Water'],
    
    '34b': ['C. B. Gonçalves and A. J. A. Meirelles, “Liquid–liquid equilibrium data for the system palm oil + fatty acids + ethanol + water at 318.2 K,” Fluid Phase Equilib, vol. 221, no. 1–2, pp. 139–150, Jul. 2004, doi: 10.1016/j.fluid.2004.05.002.',
            'Palm oil - Oleic acid - Ethanol - Water'],
    
    '35a': ['E. Batista, S. Monnerat, K. Kato, L. Stragevitch, and A. J. A. Meirelles, “Liquid−Liquid Equilibrium for Systems of Canola Oil, Oleic Acid, and Short-Chain Alcohols,” J Chem Eng Data, vol. 44, no. 6, pp. 1360–1364, Nov. 1999, doi: 10.1021/je990015g.',
            'Canola oil - Oleic acid - Methanol/Ethanol/Propanol'],
    
    '36a': ['G. F. Hirata, C. R. A. Abreu, L. C. B. A. Bessa, M. C. Ferreira, E. A. C. Batista, and A. J. A. Meirelles, “Liquid–liquid equilibrium of fatty systems: A new approach for adjusting UNIFAC interaction parameters,” Fluid Phase Equilib, vol. 360, pp. 379–391, Dec. 2013, doi: 10.1016/j.fluid.2013.10.004.',
            'Mixed oil - Oleic acid - Ethanol'],
    
    '37a': ['C. E. C. Rodrigues, A. Filipini, and A. J. A. Meirelles, “Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K,” J Chem Eng Data, vol. 51, no. 1, pp. 15–21, Jan. 2006, doi: 10.1021/je0495841.',
            'Garlic oil - Linoleic acid - Ethanol - Water'],
    
    '37b': ['C. E. C. Rodrigues, A. Filipini, and A. J. A. Meirelles, “Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K,” J Chem Eng Data, vol. 51, no. 1, pp. 15–21, Jan. 2006, doi: 10.1021/je0495841.',
            'Grape seed oil - Linoleic acid - Ethanol - Water'],
    
    '37c': ['C. E. C. Rodrigues, A. Filipini, and A. J. A. Meirelles, “Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K,” J Chem Eng Data, vol. 51, no. 1, pp. 15–21, Jan. 2006, doi: 10.1021/je0495841.',
            'Sesame oil - Linoleic acid - Ethanol - Water'],
    
    '38a': ['C. E. C. Rodrigues, E. C. D. Peixoto, and A. J. A. Meirelles, “Phase equilibrium for systems composed by refined soybean oil+commercial linoleic acid+ethanol+water, at 323.2K,” Fluid Phase Equilib, vol. 261, no. 1–2, pp. 122–128, Dec. 2007, doi: 10.1016/j.fluid.2007.07.021.',
            'Refined Soybean oil - Linoleic acid - Ethanol - Water'],
    
    '39a': ['C. E. C. Rodrigues and A. J. A. Meirelles, “Extraction of Free Fatty Acids from Peanut Oil and Avocado Seed Oil: Liquid−Liquid Equilibrium Data at 298.2 K,” J Chem Eng Data, vol. 53, no. 8, pp. 1698–1704, Aug. 2008, doi: 10.1021/je7007186.', 
            'Peanut oil - Oleic acid - Ethanol - Water'],
    
    '39b': ['C. E. C. Rodrigues and A. J. A. Meirelles, “Extraction of Free Fatty Acids from Peanut Oil and Avocado Seed Oil: Liquid−Liquid Equilibrium Data at 298.2 K,” J Chem Eng Data, vol. 53, no. 8, pp. 1698–1704, Aug. 2008, doi: 10.1021/je7007186.', 
            'Avocado Seed oil - Oleic acid - Ethanol - Water'],
    
    '40a': ['M. Mohsen-Nia and A. Khodayari, “De-acidification of sunflower oil by solvent extraction: (Liquid+liquid) equilibrium data at T=(303.15 and 313.15)K,” J Chem Thermodyn, vol. 40, no. 8, pp. 1325–1329, Aug. 2008, doi: 10.1016/j.jct.2008.01.029.',
            'Sunflower oil - Oleic acid - Methanol/Ethanol'],
    
    '41a': ['M. Mohsen‐Nia, H. Modarress, and H. R. Nabavi, “Measuring and Modeling Liquid–Liquid Equilibria for a Soybean Oil, Oleic Acid, Ethanol, and Water System,” J Am Oil Chem Soc, vol. 85, no. 10, pp. 973–978, Oct. 2008, doi: 10.1007/s11746-008-1288-9.',
            'Soybean oil - Oleic acid - Methanol/Ethanol - Water'],
    
    '42a': ['C. E. C. Rodrigues, F. A. Silva, A. Marsaioli, and A. J. A. Meirelles, “Deacidification of Brazil Nut and Macadamia Nut Oils by Solvent Extraction:  Liquid−Liquid Equilibrium Data at 298.2 K,” J Chem Eng Data, vol. 50, no. 2, pp. 517–523, Mar. 2005, doi: 10.1021/je049687j.',
            'Brazil Nut oil - Oleic acid - Ethanol - Water'],
    
    '42b': ['C. E. C. Rodrigues, F. A. Silva, A. Marsaioli, and A. J. A. Meirelles, “Deacidification of Brazil Nut and Macadamia Nut Oils by Solvent Extraction:  Liquid−Liquid Equilibrium Data at 298.2 K,” J Chem Eng Data, vol. 50, no. 2, pp. 517–523, Mar. 2005, doi: 10.1021/je049687j.',
            'Macadamia Nut oil - Oleic acid - Ethanol - Water'],
    
    '43a': ['M. Mohsen-Nia and Mahdi. Dargahi, “Liquid−Liquid Equilibrium for Systems of (Corn Oil + Oleic Acid + Methanol or Ethanol) at (303.15 and 313.15) K,” J Chem Eng Data, vol. 52, no. 3, pp. 910–914, May 2007, doi: 10.1021/je700051j.',
            'Corn oil - Oleic acid - Methanol/Ethanol'],
    
    '44a': ['G. Sanaiotti, J. S. R. Coimbra, J. C. Gomes, and L. A. Minim, “Liquid−Liquid Equilibrium for Systems Composed of Grape Seed Oil + Oleic Acid + Ethanol + Water at (283.2, 290.7, and 298.2) K,” J Chem Eng Data, vol. 53, no. 7, pp. 1492–1497, Jul. 2008, doi: 10.1021/je800034c.',
            'Crude grape seed oil - Oleic acid - Ethanol - Water'],
    
    '44b': ['G. Sanaiotti, J. S. R. Coimbra, J. C. Gomes, and L. A. Minim, “Liquid−Liquid Equilibrium for Systems Composed of Grape Seed Oil + Oleic Acid + Ethanol + Water at (283.2, 290.7, and 298.2) K,” J Chem Eng Data, vol. 53, no. 7, pp. 1492–1497, Jul. 2008, doi: 10.1021/je800034c.',
            'Refined grape seed oil - Oleic acid - Ethanol - Water'],
    
    '45a': ['M. Mohsen‐Nia, H. Modarress, and H. R. Nabavi, “Measuring and Modeling Liquid–Liquid Equilibria for a Soybean Oil, Oleic Acid, Ethanol, and Water System,” J Am Oil Chem Soc, vol. 85, no. 10, pp. 973–978, Oct. 2008, doi: 10.1007/s11746-008-1288-9.', 
            'Soybean oil - Oleic acid - Ethanol - Water'],
    
    '46a': ['É. C. D. Reipert, C. E. C. Rodrigues, and A. J. A. Meirelles, “Phase equilibria study of systems composed of refined babassu oil, lauric acid, ethanol, and water at 303.2K,” J Chem Thermodyn, vol. 43, no. 12, pp. 1784–1790, Dec. 2011, doi: 10.1016/j.jct.2011.05.039.',
            'Babassu oil - Lauric acid - Ethanol - Water'],
    
    '47a': ['X. Huang et al., “Liquid–liquid equilibrium of binary and ternary systems composed by palm oil or palm oil fractions with methanol/ethanol and water,” Fluid Phase Equilib, vol. 404, pp. 17–25, Oct. 2015, doi: 10.1016/j.fluid.2015.06.028.',
             'Refined Palm oil - Ethanol/Methanol - Waterl'],
    
    '47b': ['X. Huang et al., “Liquid–liquid equilibrium of binary and ternary systems composed by palm oil or palm oil fractions with methanol/ethanol and water,” Fluid Phase Equilib, vol. 404, pp. 17–25, Oct. 2015, doi: 10.1016/j.fluid.2015.06.028.',
             'Refined palm olein - Ethanol/Methanol- Water'],
    
    '47c': ['X. Huang et al., “Liquid–liquid equilibrium of binary and ternary systems composed by palm oil or palm oil fractions with methanol/ethanol and water,” Fluid Phase Equilib, vol. 404, pp. 17–25, Oct. 2015, doi: 10.1016/j.fluid.2015.06.028.',
             'Refined palm stearin - Ethanol/Methanol- Water'],
    
    '48a': ['Y. C. Ardila, A. B. Machado, G. M. F. Pinto, R. M. Filho, and M. R. W. Maciel, “Liquid–Liquid Equilibrium in Ternary Systems Present in Biodiesel Purification from Soybean Oil and Castor Oil at (298.2 and 333.2) K,” J Chem Eng Data, vol. 58, no. 3, pp. 605–610, Mar. 2013, doi: 10.1021/je301028r.',
            'Soybean oil biodiesel - Ethanol - Water'],
    
    '48b': ['Y. C. Ardila, A. B. Machado, G. M. F. Pinto, R. M. Filho, and M. R. W. Maciel, “Liquid–Liquid Equilibrium in Ternary Systems Present in Biodiesel Purification from Soybean Oil and Castor Oil at (298.2 and 333.2) K,” J Chem Eng Data, vol. 58, no. 3, pp. 605–610, Mar. 2013, doi: 10.1021/je301028r.',
            'Castor oil biodiesel - Ethanol - Water'],
    
    '49a': ['S. Shiozawa, D. Gonçalves, M. C. Ferreira, A. J. A. Meirelles, and E. A. C. Batista, “Liquid-liquid equilibrium data and thermodynamic modeling of systems involved in the biodiesel production in terms of acylglycerols, free fatty acids, ethyl esters, and ethanol at 303.2 and 318.2 K and local pressure,” Fluid Phase Equilib, vol. 507, p. 112431, Mar. 2020, doi: 10.1016/j.fluid.2019.112431.',
            'Soybean oil - Ethyl linoleate - Linoleic acid - DAG - MAG - Ethanol'],

    '49b': ['S. Shiozawa, D. Gonçalves, M. C. Ferreira, A. J. A. Meirelles, and E. A. C. Batista, “Liquid-liquid equilibrium data and thermodynamic modeling of systems involved in the biodiesel production in terms of acylglycerols, free fatty acids, ethyl esters, and ethanol at 303.2 and 318.2 K and local pressure,” Fluid Phase Equilib, vol. 507, p. 112431, Mar. 2020, doi: 10.1016/j.fluid.2019.112431.',
            'Cottonseed oil - Ethyl linoleate - Linoleic acid - DAG - MAG - Ethanol'],
    
    '49c': ['S. Shiozawa, D. Gonçalves, M. C. Ferreira, A. J. A. Meirelles, and E. A. C. Batista, “Liquid-liquid equilibrium data and thermodynamic modeling of systems involved in the biodiesel production in terms of acylglycerols, free fatty acids, ethyl esters, and ethanol at 303.2 and 318.2 K and local pressure,” Fluid Phase Equilib, vol. 507, p. 112431, Mar. 2020, doi: 10.1016/j.fluid.2019.112431.',
            'Rice bran oil - Ethyl oleate - Oleic acid - Ethyl linoleate - Linoleic acid - DAG - MAG - Ethanol'],
    
    '50a': ['M. C. Ferreira, D. Gonçalves, L. C. B. A. Bessa, A. J. A. Meirelles, and E. A. C. Batista, “Performance of different UNIFAC parameter sets in describing experimental liquid–liquid equilibrium data of biodiesel systems,” J Mol Liq, vol. 383, p. 122022, Aug. 2023, doi: 10.1016/j.molliq.2023.122022.',
            'Olive oil - Capric acid - DAG - MAG - Ethanol'],
    
    '50b': ['M. C. Ferreira, D. Gonçalves, L. C. B. A. Bessa, A. J. A. Meirelles, and E. A. C. Batista, “Performance of different UNIFAC parameter sets in describing experimental liquid–liquid equilibrium data of biodiesel systems,” J Mol Liq, vol. 383, p. 122022, Aug. 2023, doi: 10.1016/j.molliq.2023.122022.',
            'Sunflower oil - DAG - MAG - Ethanol'],  
    
    '50c': ['M. C. Ferreira, D. Gonçalves, L. C. B. A. Bessa, A. J. A. Meirelles, and E. A. C. Batista, “Performance of different UNIFAC parameter sets in describing experimental liquid–liquid equilibrium data of biodiesel systems,” J Mol Liq, vol. 383, p. 122022, Aug. 2023, doi: 10.1016/j.molliq.2023.122022.',
            'Coconut oil - Caporic ester - Ethanol'],  
    
    '51a': ['J. C. G. Filho et al., “Liquid–Liquid Equilibrium Measurement and Thermodynamic Modeling of the { Sterculia striata Biodiesel + Glycerol + Ethanol} System,” J Chem Eng Data, vol. 66, no. 8, pp. 3293–3299, Aug. 2021, doi: 10.1021/acs.jced.1c00341.',
            'Chicha oil biodiesel - Ethanol - Glycerol'],
     
    '52a': ['A. Asoodeh, F. Eslami, and S. M. Sadrameli, “Liquid–liquid equilibria of systems containing linseed oil biodiesel + methanol + glycerol: Experimental data and thermodynamic modeling,” Fuel, vol. 253, pp. 460–473, Oct. 2019, doi: 10.1016/j.fuel.2019.04.170.',
            'Linseed oil biodiesel - Methanol - Glycerol'], 
    
    '53a': ['I. E. P. Toledo et al., “Liquid–Liquid Equilibrium of the System {Peanut Biodiesel + Glycerol + Ethanol} at Atmospheric Pressure,” J Chem Eng Data, vol. 64, no. 5, pp. 2207–2212, May 2019, doi: 10.1021/acs.jced.8b01185.',
            'Penaut oil biodiesel - Ethanol - Glycerol'], 
     
    '54a': ['J. C. Nunes et al., “Experimental Data and Phase Equilibrium Modeling in Ternary and Pseudoquaternary Systems of Sunflower Oil for Biodiesel Production,” J Chem Eng Data, vol. 64, no. 2, pp. 412–420, Feb. 2019, doi: 10.1021/acs.jced.8b00276.',
            'Refined sunflower oil biodiesel - Methanol - Glycerol - Water'],
    
    '55a': ['S. Shiozawa, M. C. Ferreira, D. Gonçalves, A. J. A. Meirelles, and E. A. C. Batista, “Liquid–Liquid Equilibrium Data for Systems Involving Triacylglycerols from (Soybean, Cottonseed, or Rice Bran) Oil + Partial Acylglycerols + Anhydrous Ethanol at T = 303.2 and 318.2 K,” J Chem Eng Data, vol. 64, no. 5, pp. 2153–2162, May 2019, doi: 10.1021/acs.jced.8b01119.',
            'Refined soybean oil biodiesel - DAG - MAG - Ethanol'],
    
    '55b': ['S. Shiozawa, M. C. Ferreira, D. Gonçalves, A. J. A. Meirelles, and E. A. C. Batista, “Liquid–Liquid Equilibrium Data for Systems Involving Triacylglycerols from (Soybean, Cottonseed, or Rice Bran) Oil + Partial Acylglycerols + Anhydrous Ethanol at T = 303.2 and 318.2 K,” J Chem Eng Data, vol. 64, no. 5, pp. 2153–2162, May 2019, doi: 10.1021/acs.jced.8b01119.',
            'Refined cottonseed oil biodiesel - DAG - MAG - Ethanol'],
    
    '55c': ['S. Shiozawa, M. C. Ferreira, D. Gonçalves, A. J. A. Meirelles, and E. A. C. Batista, “Liquid–Liquid Equilibrium Data for Systems Involving Triacylglycerols from (Soybean, Cottonseed, or Rice Bran) Oil + Partial Acylglycerols + Anhydrous Ethanol at T = 303.2 and 318.2 K,” J Chem Eng Data, vol. 64, no. 5, pp. 2153–2162, May 2019, doi: 10.1021/acs.jced.8b01119.',
            'Refined rice bran oil biodiesel - DAG - MAG - Ethanol'],
    
    '56a': ['B. Khdir and H. Amin, “DETERMINATION AND MODELLING OF LIQUID-LIQUID PHASE EQUILIBRIUM FOR TERNARY SYSTEMS IN BIODIESEL PRODUCTION FROM VEGETABLE OIL AND ANIMAL FAT MIXTURES,” 2019.',
            'Sunflower oil biodiesel - Methanol - Glycerol'],
    
    '56b': ['B. Khdir and H. Amin, “DETERMINATION AND MODELLING OF LIQUID-LIQUID PHASE EQUILIBRIUM FOR TERNARY SYSTEMS IN BIODIESEL PRODUCTION FROM VEGETABLE OIL AND ANIMAL FAT MIXTURES,” 2019.',
            '10 % Beef Tallow/Sunflower oil biodiesel - Methanol - Glycerol'],
    
    '56c': ['B. Khdir and H. Amin, “DETERMINATION AND MODELLING OF LIQUID-LIQUID PHASE EQUILIBRIUM FOR TERNARY SYSTEMS IN BIODIESEL PRODUCTION FROM VEGETABLE OIL AND ANIMAL FAT MIXTURES,” 2019.',
            '20 % Beef Tallow/Sunflower oil biodiesel - Methanol - Glycerol'],     
    
    '57a': ['O. Z. Sampaio Neto, D. Gonçalves, S. de F. Bergara, E. A. C. Batista, and A. J. de A. Meirelles, “Oil extraction from semi-defatted babassu bagasse with ethanol: Liquid-liquid equilibrium and solid-liquid extraction in a single stage,” J Food Eng, vol. 276, p. 109845, Jul. 2020, doi: 10.1016/j.jfoodeng.2019.109845.',
            'Babassu oil - Ethanol - Water'],
}



len(list(references.keys()))


# Hay 1277 lineas de atadura en la base de datos original, 879 en la tabla 1, 398 en la tabla 2.

# 1264 lineas de atadura en la base de datos re ordenada
# Yo adicioné 204 lineas de atadura nuevas.

# Para la referencia 50 para el DAG se usa el perfil del aceite de girasol pero para el MAG si se usa el perfil dado en el paper.
