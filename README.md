# Snapp/Tapsi price comparison

## Components:

### Price Fetcher
- fetches prices from snapp and tapsi
- saves them in a file

**RUN:**
```bash
# Add your routes to configs/routes.json
cp configs/routes.json.sample configs/routes.json

# Set your snapp/tapsi headers and coockies
# You can use browser inspector to get them
cp configs/snapp.json.sample configs/snapp.json
cp configs/tapsi.json.sample configs/tapsi.json

SCRAPE_INTERVAL=300 python3 src/price_fetcher.py
```

### Exporter
- reads the file
- exports the data to /metrics endpoint

**RUN:**
```bash
cd src/exporter
flask run --host 0.0.0.0 --port 5000
```

### Prometheus
- scrapes the data from exporter

**RUN:**
```bash
docker run  --network host -d --rm -v prom_data:/prometheus  -v /path/to/project/configs/prometheus.yml:/etc/prometheus/prometheus.yml --name prometheus prom/prometheus
```

### Grafana
- reads the data from prometheus
- shows the data in a dashboard

**RUN:**
```bash
ocker run --restart always --env-file /path/to/project/.env -d --name=grafana --network host -v grafana:/var/lib/grafana grafana/grafana
```

### Grafana Image Renderer
- renders the dashboard as an image

**RUN:**
```bash
docker run --restart always -d --name=grafana-renderer --network host  grafana/grafana-image-renderer:latest
```

### Price Reporter
- gets the panel images from grafana
- post them on social media
    * Telegram
    * Twitter

```bash
mkdir panels
python3 price_reporter.py
```