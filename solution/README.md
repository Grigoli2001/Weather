# Weather Dashboard Application Documentation

The Weather Dashboard is a full-stack web application designed to provide users with current weather conditions and detailed forecasts for selected locations. It utilizes Nuxt.js for the frontend and FastAPI for the backend.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Frontend](#frontend)
   - [Layout](#layout)
   - [Components](#components)
   - [Pages](#pages)
   - [API Integration](#api-integration)
3. [Backend](#backend)
   - [Endpoints](#endpoints)
   - [Database Integration](#database-integration)
   - [External API Integration](#external-api-integration)
4. [Functionality](#functionality)
5. [Usage](#usage)
6. [Possible Enhancments](#possible-enhancements)
7. [My Proposed Solution](#my-proposed-solution)
8. [Challenges](#challenges)
9. [Contributors](#contributors)

## Project Structure

The Weather Dashboard project consists of both frontend and backend components:

- **Frontend:** Developed using Nuxt3.js, a Vue.js framework for building web applications.
- **Backend:** Built with FastAPI, a modern web framework for building APIs with Python.

## Frontend

The frontend of the Weather Dashboard is responsible for the user interface, including displaying weather information, managing user interactions, and making API requests to the backend.

### Layout

Layout contains the header of the web page, Logo is manually created since it was not provided.

### Components

The frontend consists of various components, including following custom ones:

- `Table`: Displays weather information in a tabular format using NuxtUI's UTable component
- `Sidebar`: Provides a detailed forecast when a location row is clicked using NuxtUI's USlideover component.
- `Modal`: Allows users to add new locations through a modal popup using NuxtUI's UModal component.
- `Notificatoins`: Using NuxtUI's UNotification component we let users know when some action happens.

### Pages

The main pages of the application include:

- `index.vue`: The main dashboard page featuring the weather table, sidebar and modals.

### API Integration

The frontend interacts with our fastAPI backend to fetch weather data and manage locations. I could have used axios but nuxt provides sufficient in built functions like useFetch, useLazyAsyncData and many more. These functions allowed me to simply implement loading screen and refresh the data after some change.

## Backend

The backend of the Weather Dashboard is responsible for handling API requests, interacting with the database, and fetching weather data from external APIs.

### Endpoints

The backend provides the following endpoints:

- `/locations/`: Manages locations, allowing users to retrieve location with weather data, and add locations.
- `/locations/{location_id}`: Delete location endpoint
- `/search/{location}`: Searches for locations based on the provided query string.
- `/forecast/{location_id}`: Retrieves a detailed 7-day weather forecast for a specified location. I still created this api endpoint to follow the guidlines but after some testing I discovered that fetching only daily forecast from open-meteo takes exaclty the same time as fetching daily and current data together. So, I think that fetching the data with daily and current weather together, while loading the dashboard will reduce overall number of requests and loading time.

### Database Integration

The backend integrates with a PostgreSQL database using SQLAlchemy ORM. It defines a `Location` model to store location information without associated weather data because weather data is dynamic and it changes frequently.

### External API Integration

To fetch weather data, the backend makes requests to the OpenMeteo API based on latitude and longitude coordinates obtained from the database.

## Functionality

The Weather Dashboard application offers the following functionality:

- Displaying current weather conditions and detailed forecasts for selected locations.
- Adding new locations and removing existing ones.
- Providing search functionality to find locations based on user input.

## Usage

To run the Weather Dashboard application locally:

1. Start the backend server by running `main.py` using UVicorn.
2. Start the frontend development server by running `npm run dev`.
3. Access the application in your web browser at the specified URL.

## Possible Enhancements

Some possible enhancements to the Weather Dashboard application include:

- Implementing user authentication to allow users to save their preferred locations if we do not want user to go through authentication proccess we can generate unique identifier using time and random values and we can plant it in the user cookies or localstorage, and in the databse modal just add one more field.
- Enhancing the user interface with additional features such as charts, graphs and hourly weather data in the sidebar.

## My Proposed Solution

Instead of fetching forecast data using the `/forecast/{location_id}` API endpoint, I propose fetching all weather data when the website is loaded and passing it as a prop to the necessary components. This approach can improve performance by reducing the number of API requests and providing faster access to weather information for the user.

## challenges

Nuxt is not as popular as other frameworks, thus there are not many tutorials in the web, so debugging was a bit challenging but I managed to resolve all the issues by myslef.
Customizing NuxtUI components was challenging part as well but their documentation helped me a lot.

## Contributors

The Weather Dashboard application was developed by Grigoli Patsatsia for coding challenge at DataCose
