import fastapi
import uvicorn
from fastapi import Request, File, UploadFile, Form
from api.app.services.portfolio_optimizer import PortfolioOptimizer

app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World Madafaca!"}

@app.post("/optimize-portfolio")
async def optimize_portfolio(
    file: UploadFile = File(...),
    risk_level: float = Form(...),
    max_weight: float = Form(...)
):
    portfolio_optimizer = PortfolioOptimizer(file, risk_level, max_weight)

    data = portfolio_optimizer.read_and_clean_file()
    cvars = portfolio_optimizer.calculate_cvar(data)
    optimal_weights = portfolio_optimizer.optimize_portfolio(data, cvars, max_weight)
    output_json = portfolio_optimizer.generate_output(optimal_weights)

    return output_json