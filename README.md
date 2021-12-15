# IEEETCSSStudy
A repository to conduct a comparative analysis on community-aware centrality measures.
The paper is submitted for review.

Comments and questions are welcome, contact: `stephany.rajeh(at)u-bourgogne.fr`

The sources of datasets used in the study are available within the article.

## Phase 1: Working on networks individually
__Notebook: NetworkName-CentralityCalculation.ipynb__: Calculates the community-aware centrality for a given network. 
__Notebook: NetworkName-CorrelationHeatmap.ipynb__: Computes the correlation for all possible combinations between the community-aware centrality measures and represents the values in a heatmap.
__Notebook: NetworkName-SIRSimulations.ipynb__: Runs the SIR simulation of the EoN library (https://epidemicsonnetworks.readthedocs.io/en/latest/) using the community-aware centrality measures ranks plots the $\Delta R$.

Those 3 notebooks are used for each of the 15 networks under study.

## Phase 2: Analyzing networks altogether
__Notebook: CorrelationAndViolinPlotsAcrossNetworks.ipynb__: Computing the correlation across and between networks and the violin plots of the correlation distribution.
__Notebook: LinearRegression.ipynb__: Running a linear regression to study the relationship between the correlation between the community-aware centrality measures and the community structure strength.
