# Gutter Tracker - AI-Powered Mobile App

This is a Flask-based web application for gutter installation businesses, supercharged with Google Gemini for AI-powered features.

## 🚀 Features

- **AI-Powered Estimates**: Generate cost estimates from job descriptions.
- **AI Photo Analysis**: Analyze photos of gutters for damage assessment.
- **AI Smart Scheduling**: Get suggestions for optimal job scheduling.
- **Mobile-Friendly**: Responsive design for phones, tablets, and desktops.
- **Database-Backed**: Uses PostgreSQL for production and SQLite for local development.

## 📋 Setup and Usage

### 1. Prerequisites

- Python 3.10+
- [Google AI API Key](https://aistudio.google.com/app/apikey)

### 2. Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd gutter-tracker
```

Create a `.env` file and add your configuration:

```bash
# .env
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///instance/gutter_tracker.db # or your postgresql url
SECRET_KEY=a-strong-secret-key-you-generate
APP_PASSWORD=your-app-password
```

### 3. Using the Makefile

This project uses a `Makefile` for common commands.

- **Install dependencies and set up the virtual environment:**
  ```bash
  make install
  ```

- **Run the application:**
  ```bash
  make run
  ```
  The application will be available at `http://127.0.0.1:5000`.

- **Run tests:**
  ```bash
  make test
  ```

- **Lint the code:**
  ```bash
  make lint
  ```

- **Initialize the database:**
  ```bash
  make db-init
  ```

- **Clean the project directory:**
  ```bash
  make clean
  ```

- **See all available commands:**
  ```bash
  make help
  ```

## 🚀 Deployment

This application is configured for deployment on [Vercel](https://vercel.com).

**Note for PostgreSQL deployments:** If you are using a PostgreSQL database for your deployment, you will need to add `psycopg2-binary` to your `requirements.txt` file.

1.  **Login to Vercel:**
    ```bash
    vercel login
    ```

2.  **Deploy:**
    ```bash
    vercel --prod
    ```

3.  **Set environment variables** in the Vercel dashboard for your project:
    - `GEMINI_API_KEY`
    - `DATABASE_URL`
    - `SECRET_KEY`
    - `APP_PASSWORD`

## 🔒 Security

- Keep your `.env` file secure and do not commit it to version control.
- Use a strong, randomly generated `SECRET_KEY` for production environments.

## 💡 Contributing

Feel free to open issues or pull requests.

---

*This project was reorganized and improved by Gemini.*