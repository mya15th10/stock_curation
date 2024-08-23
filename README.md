Overview
This project provides a RESTful API to fetch, process, and store stock market data. The API allows fetching detailed stock prices, session information, and stock categories from various external sources, and stores them in a database for further analysis.

Directory Structure
The repository is organized into several main components:

RESTFUL_API/
│
├── api/
│   ├── detail_stock_price/
│   │   ├── __init__.py
│   │   ├── library_ma.py
│   │   ├── model.py
│   │   ├── route.py
│   │   ├── service.py
│   │
│   ├── session/
│   │   ├── __init__.py
│   │   ├── library_ma.py
│   │   ├── model.py
│   │   ├── route.py
│   │   ├── service.py
│   │
│   ├── stock/
│   │   ├── __init__.py
│   │   ├── library_ma.py
│   │   ├── model.py
│   │   ├── route.py
│   │   ├── service.py
│   │
│   ├── config.py
│   ├── extension.py
│   ├── route.py
│   └── app.py
│
├── .env
