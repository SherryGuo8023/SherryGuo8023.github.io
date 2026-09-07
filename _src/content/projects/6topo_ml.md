---
slug: 6topo_ml
order: 8
title: Predicting topological materials with language models
tagline: Predicting topological properties of materials with a BERT classifier over chemical formulas.
years: 2018 – 2019
role: Bachelor's thesis, UCAS, with Max Planck Institute for Solid State Research
thumb: topo-ml-banner.png
hero: topo-ml-banner.png
links:
  - ["Materiae database", "https://cmpdc.iphy.ac.cn/materiae/#/"]
---

A machine learning approach to predicting the topological properties of materials using natural language processing techniques. In 2018 that meant treating a chemical formula as a sequence and training a language model to classify it.

## How it works

**Data.** Materials data from the Materiae database, with chemical formulas converted into vector representations through one-hot encoding.

**Model.** BERT adapted for materials property prediction as a multi-label binary classifier, using transfer learning from the pre-trained language model.

**Result.** About 89.5% prediction accuracy on the test set, and an early demonstration that language models can be useful for scientific prediction.

Built with TensorFlow and Python.
