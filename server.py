if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=7000,access_log=True, reload=True)