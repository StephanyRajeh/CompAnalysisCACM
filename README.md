# CompAnalysisCACM
A repository to conduct a comparative analysis on community-aware centrality measures.

Following is the reference for the paper: Rajeh, S., Savonnet, M., Leclercq, E., & Cherifi, H. (2022). <i> Comparative evaluation of community-aware centrality measures. </i> Quality & Quantity, 1-30. It can be accessed at: https://arxiv.org/pdf/2205.06995.pdf

Comments and questions are welcome, please contact: `stephany.rajeh(at)u-bourgogne.fr`

The sources of datasets used in the study are available within the article.

## Phase 1: Working on networks individually
__Notebook: NetworkName-CentralityCalculation.ipynb__: Calculates the community-aware centrality for a given network. <br>
__Notebook: NetworkName-CorrelationHeatmap.ipynb__: Computes the correlation for all possible combinations between the community-aware centrality measures and represents the values in a heatmap. <br>
__Notebook: NetworkName-SIRSimulations.ipynb__: Runs the SIR simulation of the EoN library (https://epidemicsonnetworks.readthedocs.io/en/latest/) using the community-aware centrality measures ranks plots the ΔR.

Those 3 notebooks are used for each of the 15 networks under study.

## Phase 2: Analyzing networks altogether
__Notebook: CorrelationAndViolinPlotsAcrossNetworks.ipynb__: Computing the correlation across and between networks and the violin plots of the correlation distribution. <br>
__Notebook: LinearRegression.ipynb__: Running a linear regression to study the relationship between the correlation between the community-aware centrality measures and the community structure strength.
