import uvicorn

"""絶対パスじゃないと動かなかったのでimportではなく、絶対"""
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
