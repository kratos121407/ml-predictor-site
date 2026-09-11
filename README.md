# ML Prediction Hub

A 3-page Streamlit website: one page per ML project, each with input fields and a Predict button.

## Folder structure
```
ml-predictor-site/
├── app.py                      # Home page
├── style.py                    # Shared CSS/theme
├── requirements.txt
├── .streamlit/config.toml      # Color theme
├── models/                     # Put your .pkl model files here
│   ├── project_one.pkl
│   ├── project_two.pkl
│   └── project_three.pkl
└── pages/
    ├── 1_📈_Project_One.py
    ├── 2_📊_Project_Two.py
    └── 3_🎯_Project_Three.py
```

## 1. Add your real models
Each page currently has 3 placeholder number inputs (Feature 1/2/3) and,
if no model file is found, does a dummy weighted-average calculation so the
site still works out of the box.

To make it real:
1. In Colab: `joblib.dump(your_model, "project_one.pkl")`, download it.
2. Drop it into `models/project_one.pkl` (same for two/three).
3. In the matching page file, rename the `feature_1/2/3` inputs to your
   actual feature names, and match the order to what your model expects.

## 2. Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the printed local URL (usually http://localhost:8501).

## 3. Deploy on your VPS
```bash
# On the VPS
sudo apt update && sudo apt install -y python3-pip python3-venv nginx
git clone <your-repo-or-scp-the-folder> ml-predictor-site
cd ml-predictor-site
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Keep it running (systemd)
Create `/etc/systemd/system/ml-predictor.service`:
```ini
[Unit]
Description=ML Prediction Hub
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ml-predictor-site
ExecStart=/path/to/ml-predictor-site/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```
Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ml-predictor
```

### Nginx reverse proxy + HTTPS
`/etc/nginx/sites-available/ml-predictor`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/ml-predictor /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d yourdomain.com
```

Your site is now live at `https://yourdomain.com`.
