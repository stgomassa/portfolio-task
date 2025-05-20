from fastapi import File, UploadFile, Form, HTTPException, FastAPI
from api.app.services.portfolio_optimizer import PortfolioOptimizer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Fintual Portfolio Optimizer"}

@app.post("/optimize-portfolio")
async def optimize_portfolio(
    file: UploadFile = File(...),
    risk_level: float = Form(...),
    max_weight: float = Form(...)
):
    try:
        # Initialize portfolio optimizer
        portfolio_optimizer = PortfolioOptimizer(file, risk_level, max_weight)

        # Parse input file and clean data
        portfolio_optimizer.clean_data()

        # Execute optimization
        portfolio_optimizer.optimize_portfolio()

        return portfolio_optimizer.get_result()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))