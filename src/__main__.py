import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",           # points to the FastAPI instance in main.py
        host="0.0.0.0",       # accessible on all network interfaces
        port=8000,            # port number
        reload=True,          # auto-reload on code changes
        log_level="info"      # log level
    )
