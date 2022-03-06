# util

## Env
### pyenv
```
PYTHON_VERSION=3.7.12 # 3.8.10
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
```

### venv
```
mkdir .venv/
python -m venv ~/.venv/util
source ~/.venv/util/bin/activate
python -m pip install --upgrade pip==22.0.3
```

## Install
```
pip install .[dev]
```

## Docker
### Build
```
docker build -t util ./
```
### Run
```
docker run \
    -it \
    --rm \
    -v `pwd`:/project/ \
    util \
    /bin/bash
```

## Test
```
python -m pytest test/ \
    -v --cov=./ \
    --cov-report=html:test_report/html.coverage \
    --html=test_report/test-report.html \
    --self-contained-html
```
