# Limitations and Assumptions

This tool is under active development. The following limitations and assumptions currently apply, but many of these features are planned for future releases:

- **Multilateral wells:**  
  Multilateral wells are not yet supported via deviation files. For advanced well architectures, please use the detailed trajectory formats (see the well-module). Support for multilateral wells via deviation files is planned.

- **System configuration:**  
  The current implementation is optimized for doublet systems (one injector and one producer or multilateral variants). While the codebase is being extended to support more complex well arrangements, some features (such as friction loss calculations) may not yet be fully robust for systems with more than two wells vertical wells (multilateral doublet systems are supported).

- **Other features:**  
  Additional features and improvements—including enhanced error handling, more flexible input formats, and expanded economic modeling—are planned for future updates.

- **Reporting steps and time resolution:**  
  When using simulation time-series as input (i.e., summary data), reporting steps are currently filtered and clipped to exact integer years from the start of the simulation. This means that only annual values are used in the economic calculations. In future versions, support will be added for arbitrary reporting steps, allowing the full accuracy of the simulation data (e.g., weekly or daily) to be reflected in the economic results.

If you have specific requirements or would like to contribute, please open an issue or pull request on the project repository!