alcohol_code = {
        
    0: 'Glycerol', 
    1: 'Methanol',
    2: 'Ethanol',
    3: 'Propanol'
}


references = {
    
    '1a': ['Liquid-Liquid Equilibria for Castor Oil Biodiesel + Glycerol + Alcohol† Bruno B. Franc¸a,*,‡ Fabio M. Pinto,§ Fernando Luiz P. Pessoa,§ and Angela Maria C. Uller‡', 
           'Castor Oil'],
    
    '2a': ['Liquid–liquid equilibria of systems containing cottonseed biodiesel + glycerol + ethanol at 293.15, 313.15 and 333.15K Francisca M.R. Mesquita, Aline M.M. Bessa, Daniel D. de Lima, Hosiberto B. de Sant’Ana, Rílvia S. de Santiago-Aguiar', 
           'Cottonseed Oil'],
    
    '3a': ['Liquid–liquid equilibrium of pseudoternary systems containing glycerol + ethanol + ethylic biodiesel from crambe oil (Crambe abyssinica) at T/K = (298.2, 318.2, 338.2) and thermodynamic modeling Rodrigo Corrêa Basso?, Antonio José de Almeida Meirelles, Eduardo Augusto Caldas Batista', 
           'Crambe Oil'],
   
    '4a': ['Liquid–Liquid Equilibria in Biodiesel Production Sunflower Masoume Rostami • Sona Raeissi • Maziyar Mahmoodi • Masoud Nowroozi',
           'Sunflower Oil'],
    
    '5a': ['Liquid–Liquid Equilibria in Biodiesel Production Canola Masoume Rostami • Sona Raeissi • Maziyar Mahmoodi • Masoud Nowroozi', 
           'Canola Oil'], 
    
    '6a': ['Liquid–Liquid Equilibrium for Systems of (Fatty Acid Ethyl Esters + Ethanol + Soybean Oil and Fatty Acid Ethyl Esters + Ethanol + Glycerol) Xuejun Liu, Xianglan Piao, Yujun Wang,* and Shenlin Zhu',
           'Soybean Oil'],  
    
    '7a': ['Thermophysical properties of biodiesel and related systems: (Liquid + liquid) equilibrium data for Jatropha curcas biodiesel Juliana R.F. Silva a, Marcio A. Mazutti b, Fernando A.P. Voll c, Lúcio Cardozo-Filho c, Marcos L. Corazza d, Marcelo Lanza e, Wagner L. Priamo f, J. Vladimir Oliveira',
           'Jatropha Oil'],
    
    '8a': ['Thermophysical properties of biodiesel and related systems: (Liquid + liquid) equilibrium data for soybean biodiesel Marcio A. Mazutti a, Fernando A.P. Voll b, Lúcio Cardozo-Filho b, Marcos L. Corazza c, Marcelo Lanza d, Wagner L. Priamo e, J. Vladimir Oliveira',
           'Soybean Oil'],
    
    '9a': ['Liquid?Liquid Equilibria in Ternary and Quaternary Systems Present in Biodiesel Production from Soybean Oil at (298.2 and 333.2) K Alex Barreto Machado,† Yurany Camacho Ardila, Leonardo Hadlich de Oliveira, Martín Aznar, and Maria Regina Wolf Macie',
           'Soybean Oil'],
    
    '10a': ['Liquid-Liquid Equilibrium for Ternary Mixtures of Biodiesel (Soybean or Sunflower) + Glycerol + Ethanol at Different Temperatures Francisca Maria R. Mesquita, Filipe X. Feitosa, Nathan E. Sombra, Rílvia Saraiva de Santiago-Aguiar, and Hosiberto B. de SantAna*',
            'Soybean Oil'],
    
    '10b': ['Liquid-Liquid Equilibrium for Ternary Mixtures of Biodiesel (Soybean or Sunflower) + Glycerol + Ethanol at Different Temperatures Francisca Maria R. Mesquita, Filipe X. Feitosa, Nathan E. Sombra, Rílvia Saraiva de Santiago-Aguiar, and Hosiberto B. de SantAna*',
            'Sunflower Oil'],
    
    '11a': ['Liquid?Liquid Equilibrium for the Glycerol + Alcohol + Coconut Biodiesel System at Different Temperatures and Atmospheric Pressure Francisca Maria R. Mesquita, Nathan Sombra Evangelista, Hosiberto Batista de Sant’Ana,and Rílvia Saraiva de Santiago-Aguiar*',
            'Coconut Oil'],
    
    '12a': ['Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15 K Luis A. Follegatti-Romero a, Mariana B. Oliveira b, Fabio R.M. Batista a, Eduardo A.C. Batista a, João A.P. Coutinho b, Antonio J.A. Meirelles a,',
            'Linoleic Oil'],
    
    '12b': ['Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15 K Luis A. Follegatti-Romero a, Mariana B. Oliveira b, Fabio R.M. Batista a, Eduardo A.C. Batista a, João A.P. Coutinho b, Antonio J.A. Meirelles a,',
            'Oleic Oil'],
    
    '12c': ['Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15 K Luis A. Follegatti-Romero a, Mariana B. Oliveira b, Fabio R.M. Batista a, Eduardo A.C. Batista a, João A.P. Coutinho b, Antonio J.A. Meirelles a,',
            'Palmitic Oil'],
    
    '12d': ['Liquid–liquid equilibria for ternary systems containing ethyl esters, ethanol and glycerol at 323.15 and 353.15 K Luis A. Follegatti-Romero a, Mariana B. Oliveira b, Fabio R.M. Batista a, Eduardo A.C. Batista a, João A.P. Coutinho b, Antonio J.A. Meirelles a,',
            'Lauric Oil'],
           
    '13a': ['%LLE experimental data, thermodynamic modeling and sensitivity analysis in the ethyl biodiesel from macauba pulp oil settling step Rodrigo Corrêa Basso ?, César Augusto Sodré da Silva, Camila de Oliveira Sousa, Antonio José de Almeida Meirelles, Eduardo Augusto Caldas Batista',
            'Macauba Oil'],    
    
    '14a': ['%Solubility of Multicomponent Systems in the Biodiesel Production by Transesterification of Jatropha curcas L. Oil with Methanol Hui Zhou, Houfang Lu, and Bin Liang* College of Chemical Engineering, Sichuan University, Chengdu 610065, People’s Republic of China',
            'Jatropha Oil'],
    
    '15a': ['Liquid–liquid equilibria for the canola oil biodiesel + ethanol + glycerol system Mariana B. Oliveira a,b, Sérgio. Barbedo b,c, João I. Soletti c,?, Sandra H.V. Carvalho c, António J. Queimada a, João A.P. Coutinho b',
            'Canola Oil'],
    
    '16a': ['Liquid–liquid equilibria for mixtures containing water, methanol, fatty acid methyl esters, and glycerol Ming-Jer Lee?, Yuan-Chen Lo, Ho-Mu Lin',
            'Oelic Oil'],
    
    '17a': ['Liquid-Liquid Equilibrium Study in Ternary Castor Oil Biodiesel þ Ethanol þ Glycerol and Quaternary Castor Oil Biodiesel þ Ethanol þ Glycerol þ NaOH Systems at (298.2 and 333.2) K Alex Barreto Machado,† Yurany Camacho Ardila, Leonardo Hadlich de Oliveira, Martín Aznar, and Maria Regina Wolf Maciel*',
            'Castor Oil'],
    
    '18a': ['Experimental (liquid + liquid) equilibrium data for ternary and quaternary mixtures of fatty acid methyl and ethyl esters (FAME/FAEE) from soybean oil Stéphani C. Beneti a,b,?, Marcelo Lanza c, Marcio A. Mazutti d, Marcos Hiroiuqui Kunita e, Lúcio Cardozo-Filho f, J. Vladimir Oliveira a,c',
            'Soybean Oil'],
    
    '19a': ['Experimental investigation and modeling of liquid–liquid equilibria intwo systems of concern in biodiesel production Masoume Rostamia, Sona Raeissia,?, Mohammad Ranjbarana, Maziyar Mahmoodia,Masoud Nowrooziba',
            'Corn Oil'],
     
    '19b': ['Experimental investigation and modeling of liquid–liquid equilibria intwo systems of concern in biodiesel production Masoume Rostamia, Sona Raeissia,?, Mohammad Ranjbarana, Maziyar Mahmoodia,Masoud Nowrooziba',
            'Frying Oil'],
    
    '20a': ['Liquid–liquid equilibria for ternary systems containing ethylic palm oil biodiesel + ethanol + glycerol/water: Experimental data at 298.15 and 323.15 K and thermodynamic modeling. Enio G. de Azevedo Rocha a,Luis A. Follegatti-Romero a, Sérgio Duvoisin Jr. b, Martín Aznar',
            'Palm Oil'],
   
    '21a': ['Liquid–liquid equilibrium in the systems FAMEs+vegetable oil+methyl alcohol and FAMEs+glycerol+methyl alcohol',
           'Rapeseed Oil'],
   
    '22a': ['Liquid–liquid equilibrium data and thermodynamic modeling for systems related to the production of ethyl esters of fatty acids from soybean soapstock acid oil',
           'Soybean Oil'],
   
    '23a': ['Liquid–liquid equilibrium data and thermodynamic modeling, at T/K = 298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils',
           'Crambe Oil'],     
    
    '23b': ['Liquid–liquid equilibrium data and thermodynamic modeling, at T/K = 298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils',
           'Fodder Radish Oil'],     

    '23b': ['Liquid–liquid equilibrium data and thermodynamic modeling, at T/K = 298.2, in the washing step of ethyl biodiesel production from crambe, fodder radish and macauba pulp oils',
           'Macauba Oil'],
   
    '24a': ['Liquid-liquid phase equilibrium in ternary mixture of waste fish oil biodiesel-methanol-glycerol: Experimental data and thermodynamic modeling M. Maghami, J. Yousefi Seyf, S.M. Sadrameli*, A. Haghtalab',
           'Waste Fish Oil'],      

    '25a': ['Liquid–liquid equilibrium data for systems containing Brazil nut biodiesel + methanol + glycerin at 303.15 K and 323.15 K',
           'Brazil nut Oil'],
    
    '26a': ['Novel Approach for Liquid−Liquid Phase Equilibrium of Biodiesel (Canola and Sunflower) + Glycerol + Methanol',
            'Canola Oil'],
    
    '26b': ['Novel Approach for Liquid−Liquid Phase Equilibrium of Biodiesel (Canola and Sunflower) + Glycerol + Methanol',
            'Sunflower Oil'],

    '27a': ['Thermophysical properties of biodiesel and related systems: (Liquid + liquid) equilibrium data for castor oil biodiesel Marcio A. Mazutti a , Fernando A.P. Voll b , Lúcio Cardozo-Filho b , Marcos L. Corazza c , Marcelo Lanza d , Wagner L. Priamo e, J. Vladimir Oliveira d,f,⇑',
            'Castor Oil'],
    
    '28a': ['Liquid−Liquid Equilibrium for Compounds of Soybean Ethyl Biodiesel Production by Transesterification',
            'Soybean Oil'],
    
    '29a': ['Prediction of Liquid-Liquid Equilibrium for Systems of Vegetable Oils, Fatty Acids, and Ethanol Eduardo Batista, Sandra Monnerat, Luiz Stragevitch, Carla G. Pina, Cintia B. Goncü alves, and Antonio J. A. Meirelles*',
            'Triolein'],
    
    '29b': ['Prediction of Liquid-Liquid Equilibrium for Systems of Vegetable Oils, Fatty Acids, and Ethanol Eduardo Batista, Sandra Monnerat, Luiz Stragevitch, Carla G. Pina, Cintia B. Goncü alves, and Antonio J. A. Meirelles*',
            'Corn Oil'],    
    
    '30a': ['Equilibrium data for systems composed by cottonseed oil + commercial linoleic acid + ethanol +water + tocopherols at 298.2K Christianne E.C. Rodrigues a,?, ´ Erika C.D. Reipert b, Ana Fl´avia de Souza b, Pedro A. Pessˆoa Filho c, Antonio J.A. Meirelles b',
            'Refined cottonseed Oil'],
     
    '30b': ['Equilibrium data for systems composed by cottonseed oil + commercial linoleic acid + ethanol +water + tocopherols at 298.2K Christianne E.C. Rodrigues a,?, ´ Erika C.D. Reipert b, Ana Fl´avia de Souza b, Pedro A. Pessˆoa Filho c, Antonio J.A. Meirelles b',
            'Refined cottonseed Oil'],
    
    '31a': ['Equilibrium Data for the System Rice Bran Oil + Fatty Acids + Ethanol + Water at 298.2 K Christianne E. C. Rodrigues, Rosemar Antoniassi, and Antonio J. A. Meirelles*',
            'Rice Bran Oil'],
    
    '32a': ['Liquid–liquid equilibria for systems composed of rice bran oil and alcohol-rich solvents: Application to extraction and deacidification of oil Cássia M. Oliveira, Bruna R. Garavazo, Christianne E.C. Rodrigues',
            'Rice Bran Oil'],
    
    '33a': ['Liquid-Liquid Equilibrium Data for the System Corn Oil + Oleic Acid + Ethanol + Water at 298.15 K Cintia B. Goncü alves, Eduardo Batista, and Antonio J. A. Meirelles',
            'Corn Oil'],
    
    '34a': ['Liquid–liquid equilibrium data for the system palm oil + fatty acids + ethanol + water at 318.2K Cintia B. Gonçalves, Antonio J.A. Meirelles',
            'Palm Oil and Palmitic acid'],
    
    '34b': ['Liquid–liquid equilibrium data for the system palm oil + fatty acids + ethanol + water at 318.2K Cintia B. Gonçalves, Antonio J.A. Meirelles',
            'Palm Oil and Oleic acid'],
    
    '35a': ['Liquid-Liquid Equilibrium for Systems of Canola Oil, Oleic Acid, and Short-Chain Alcohols Eduardo Batista, Sandra Monnerat, Keˆnia Kato, Luiz Stragevitch, and Antonio J. A. Meirelles*',
            'Canola Oil'],
    
    '36a': ['Liquid–liquid equilibrium of fatty systems: A new approach for adjusting UNIFAC interaction parameters Gláucia F. Hirataa, Charlles R.A. Abreub, Larissa C.B.A. Bessaa, Marcela C. Ferreiraa, Eduardo A.C. Batista a, Antonio J.A. Meirellesa,?',
            'Mixed Oil'],
    
    '37a': ['Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K Christianne E. C. Rodrigues,† Anderson Filipini,‡ and Antonio J. A. Meirelles*,‡',
            'Garlic Oil'],
    
    '37b': ['Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K Christianne E. C. Rodrigues,† Anderson Filipini,‡ and Antonio J. A. Meirelles*,‡',
            'Grape seed Oil'],
    
    '37c': ['Phase Equilibrium for Systems Composed by High Unsaturated Vegetable Oils + Linoleic Acid + Ethanol + Water at 298.2 K Christianne E. C. Rodrigues,† Anderson Filipini,‡ and Antonio J. A. Meirelles*,‡',
            'Sesame Oil'],
    
    '38a': ['Phase equilibrium for systems composed by refined soybean oil + commercial linoleic acid + ethanol +water, at 323.2K Christianne E.C. Rodrigues a,?, Elaine C.D. Peixoto b, Antonio J.A. Meirelles b',
            'Refined soybean Oil']
    
}


# Quede en la linea 3604 