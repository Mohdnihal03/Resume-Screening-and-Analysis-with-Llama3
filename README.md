# Resume screening and evaluation using Llama3 spun up on a local network.

## Run on the computer

1. Clone the repo
```bash
git clone https://github.com/Mohdnihal03/Resume-Screening-and-Analysis-with-Llama3.git
```
2. Install requirements
```bash
python3 -m install -r requirements.txt
```
3. Spin up the app
```bash
streamlit run app.py
```

## Run with docker 

1. Build the image
```bash
docker build -t your-name-here .
```
2. Run the container
```bash
docker run your-name-here
```
3. Follow the local link displayed. Usually it's similar to http://172.17.0.2:8501
