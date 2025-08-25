# Limitations and Assumptions

This tool is under active development. The following limitations and assumptions currently apply, but many of these features are planned for future releases:

- **Multilateral wells:**  
  Multilateral wells are not yet supported via deviation files. For advanced well architectures, please use the detailed trajectory formats (see the well-module). Support for multilateral wells via deviation files is planned.

- **System configuration:**  
  The current implementation is optimized for doublet systems (one injector and one producer). While the codebase is being extended to support more complex well arrangements, some features (such as friction loss calculations) may not yet be fully robust for systems with more than two wells.

- **Time stepping:**  
  Simulation time steps are assumed to be in whole years. Support for arbitrary time steps and finer temporal resolution is on the roadmap.

- **Other features:**  
  Additional features and improvements—including enhanced error handling, more flexible input formats, and expanded economic modeling—are planned for future updates.


If you have specific requirements or would like to contribute, please open an issue or pull request on the project repository!