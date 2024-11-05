# Image Editor Project

This project is a simple image editor application that allows users to upload images and apply various editing features such as brightness adjustment, contrast adjustment, blur effect, and grayscale conversion.


## Technologies Used
- React (Frontend)
- Flask (Backend)
- Axios (for making HTTP requests)

## Getting Started


### Clone the Repository
   Clone the backend repository (if it’s separate) to your local machine. Navigate to the backend directory:
   ```
   git clone --branch docker-compose https://github.com/hhwrxhh/flask-app1.git
```
### Docker Setup

To start both the frontend and backend using Docker, follow these instructions.

1. **Build the Docker containers**  
   In the root directory containing the `docker-compose.yml` file, run:
   ```bash
   docker-compose up --build
   ```

   This will build the Docker images for both the frontend and backend and start the containers.

2. **Access the Application**  
   - **Frontend (React)**: The application will be available at `http://localhost:3000`.
   - **Backend (Flask)**: The backend server will be available at `http://localhost:5000`.

3. **Stop the Docker Containers**  
   To stop the containers, press `CTRL+C` in the terminal where they are running or run:
   ```bash
   docker-compose down
   ```

This will stop and remove the running containers while keeping the images intact for future use.


