# ForFiS - A FORest FIre firefighting Simulation tool for education and research

>This tool is still in progress. Feel free to add your issues and/or contribute in the software development by commiting

>This tool shall be used to compare your strategie finding algorithms to other state-of-the-art approaches. I'd appreciate, if you add your algorithm so that everyone can compare to it.

**ForFiS** is a Python tool to simulate forest fires along with firefighting agents with an interface for strategie finding algorithms. 
This tool is highly configurable, simplest by adapting parameters in the included `config.yaml` file. After configuring the tool to your desire just run the `main.py` script with the python 3 interpreter.
For detailed informations about the underlying mathematical models and the integrated heuristic strategies please have a look at our paper (Status: Submitted), as soon as it is published.

---
Dependencies (indicated versions are approved. May work with lower versions as well):
* python 3.8.5
* hexalattice-1.1.0 (https://github.com/alexkaz2/hexalattice)
`pip install hexalattice`
* matplotlib 3.3.2
* numpy 1.19.2
* tkinter 8.6

---
Please cite ForFiS if you use it in your work. Here is a suitable BibTeX entry:
```
@ARTICLE{Bredlau:ForFiS,
  author  = {Marvin Bredlau, Alexander Weber and Alexander Knoll},
  title   = {FORFIS: A forest fire firefighting simulation tool for education and research},
  journal = {}, % submitted to 'Journal of open research software'
  year    = {2022},
}
```
