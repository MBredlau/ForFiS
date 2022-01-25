# ForFiS - A FORest FIre firefighting Simulation tool for education and research

>This tool is still in progress. Feel free to add your issues and/or contribute in the software development by commiting

>This tool shall be used to compare your strategie finding algorithms to other state-of-the-art approaches. I'd appreciate, if you add your algorithm so that everyone can compare to it.

**ForFiS** is a Python tool to simulate forest fires along with firefighting agents with an interface for strategie finding algorithms. 
This tool is highly configurable, simplest by adapting parameters in the included 'config.yaml' file. After configuring the tool to your desire just run the 'main.py' script with the python 3 interpreter:
```
git clone https://github.com/MarvinS23/ForFiS.git
chmod +x main.py
./main.py
```

---
Dependencies (indicated versions are approved. May work with lower versions as well):
* python 3.8.5
* hexalattice-1.1.0 (https://github.com/alexkaz2/hexalattice)
`pip install hexalattice`
* matplotlib 3.3.2
* numpy 1.19.2

---
Please cite ForFiS if you use it in your work. Here is a suitable BibTeX entry:
```
@ARTICLE{Simon:ForFiS,
  author  = {Marvin Simon, Alexander Weber and Alexander Knoll},
  title   = {FORFIS: A forest fire firefighting simulation tool for education and research},
  journal = {???},
  year    = {2022},
  pages   = {???}
}
```
