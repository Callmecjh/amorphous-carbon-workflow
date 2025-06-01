# amorphous-carbon-workflow
This study presents a computational workflow for simulating disordered carbon structures, comprising three integrated modules:

1. Training Workflow

Implements an automated neural network potential (NNP) training cycle via the LASP software package. Automates: structural sampling → DFT calculations → NNP training → iterative refinement until target accuracy is achieved.

2. Voltage Workflow

Quantifies sodium storage behavior in arbitrary disordered carbon hosts by:

(i) Identifying optimal Na⁺ adsorption sites

(ii) Calculating thermodynamic energies at sequential sodiation concentrations

(iii) Deriving voltage profiles from free energy landscapes

Enables mechanistic interpretation of electrochemical performance variations across carbon architectures.

3. Post-Processing Module

Performs atomistic structural fingerprinting including:

(i) Hybridization analysis: sp/sp²/sp³ bond quantification

(ii) Ring statistics: Identification of carbon rings (4–9 membered)

(iii) Defect characterization: Edge/curvature defect mapping

Provides quantitative metrics for comparative structure-property analysis.

Core implementation: All subpackages are developed in Python, ensuring modularity and extensibility
