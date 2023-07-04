# **General Building DataFeed Specification (GBDS)**

## **Introduction**

The goal of this document is to define the goal of the GBDS, define the fields used in the GBDS, and provide general insights into how the GBDS functions.

### **Specification Goal**

The goal of the GBDS is to translate municipal construction permitting data into a standardized format that can be more easily understood by city stakeholders at every level, from local residents to contractors and developers, and more easily utilized by public, private, and non-profit organizations involved in the urban development and planning sector.

### **Specification Input**

Currently, the GBDS uses API calls to either pull in .csv files from each municipality's open data Primer website or run JSON queries. These API calls translate the queried datasets into local dataframes without locally downloading any municipality's permitting dataset.

### **Specification Output**

The output of the GBDS is a comma-separated value (.csv) file that can be uploaded as a feature-layer in this project's ArcGIS Online generated map
