from app import create_app

app = create_app()

# Vercel serverless function handler
def handler(request, response):
    return app(request, response)
