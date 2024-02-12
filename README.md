## Steps for running in local system
**STEP-1**: Clone the repo to your local system:
```
git clone https://github.com/SubhamZap/location-search-engine.git
```

**STEP-2**: Install all the dependencies mentioned in requirements.txt file. You can run the following command in your command prompt to install all the dependencies:
```python
pip install -r requirements.txt
```

**STEP-3:** After installing all the dependencies, open command prompt from the direction where main.py file is present and run the following command:

```python
streamlit run app.py
```

**STEP-4:** A web-ui will open, here you can search for location.

## Steps for accessing the web UI without cloning repo
**STEP-1**: Go to this link: `https://location-search-engine-dhxrzzifnrzciz3vr7cfty.streamlit.app/`

**STEP-2**: A web-ui will open, here you can search for location.

## Steps for analysing the EDA
**STEP-1**: Unzip the dataset.
```
unzip IN.zip
unzip IN_pincodes.zip
```

**STEP-2**: 
All the exploration are done in `EDA.ipynb` and for model training check `model_training.ipynb`.