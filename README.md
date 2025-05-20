# Portfolio Optimization API

A FastAPI-based portfolio optimization service that implements the Markowitz Mean-Variance Model to generate optimal portfolio weights based on historical daily data.

## Features

- Portfolio optimization using Modern Portfolio Theory (MPT)
- Efficient Frontier implementation using PyPortfolioOpt
- Sharpe ratio maximization
- Customizable risk constraints and weight bounds

## API Endpoints

### POST /optimize-portfolio
Optimizes a portfolio based on provided historical data.

**Parameters:**
- `file`: CSV file containing historical returns data (UTF-8 format)
- `risk_level`: Float value representing risk tolerance
- `max_weight`: Float value representing maximum weight per asset

**Request Format:**
- Content-Type: multipart/form-data
- File format: CSV with dates as index and asset returns as columns

## Usage Example

```
curl -X POST http://44.203.200.171/optimize-portfolio \
    -H "Content-Type: multipart/form-data" \
    -F "file=@returns.csv" \
    -F "risk_level=1.0" \
    -F "max_weight=0.15"'''
```
Note: included fixed IP address for exercise-simplicity purposes only

**Response:**
```json
{
    "optimal_portfolio": {
        "ticker_1": weight_1,
        "ticker_2": weight_2,
        ...
    }
}
```

## Método de optimización 

La método que se utilizó para la optimizaciónd el portafolio fue emplear el modelo de Markowitz maximizando el Sharpe ratio, empleando como métrica de riesgo la varianza.
Esto porque se hizo un breve análisis de los activos presentes en el archivo .csv que sugiere que el perfil es de una persona
tolerante al riesgo, entonces, aplicando éste método se propone una estrategia que prioriza el crecimiento del capital antes que la estabilidad, lo que se alinea
en teoría, al usuario.

## URL

http://44.203.200.171/optimize-portfolio
 

