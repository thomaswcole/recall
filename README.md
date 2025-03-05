# Recall

This Python package provides a simple way to retrieve recall data from the National Highway Traffic Safety Administration (NHTSA) API. You can query recall information based on various criteria such as make, model, and year.

## Features

- Fetch recall data by vehicle make, model, and year.
- Retrieve a list of all makes, models, and years.
- Simple and easy-to-use API for working with NHTSA recall data.

## Installation

To install the package, use pip:

```bash
pip install nhtsa-recall-fetcher
```

## Usage

### Import

```python
from recall import NHTSA
```

#### Example Usage

**Fetch recall data by make, model, year**

```python
nthsa = NHTSA()
recalls = nhtsa.get_recalls_by_make_model_year('Toyota', 'Camry', '2010')
print(recalls)
```

**Get all makes**

```python
nthsa = NHTSA()
makes = nhtsa.get_all_makes()
print(makes)
```

**Get all models for a given make and year**

```python
nthsa = NHTSA()
models = nhtsa.get_models_by_make_year('Toyota', '2010')
print(models)
```


