<h3 align="center">Birdnest Project</h3>

  <p align="center">
    Full-stack website implemented using Flask and React
    <br />
    <br />
    <a href="https://birdnest-project.vercel.app/">View Demo</a>
    ·
    <a href="https://github.com/AzimovS/birdnest-project/issues">Report Bug</a>
    ·
    <a href="https://github.com/AzimovS/birdnest-project/issues">Request Feature</a>
  </p>
<!-- ABOUT THE PROJECT -->

## About The Project
![Screenshot from 2023-01-16 07-11-22](https://user-images.githubusercontent.com/35425540/212614109-14f83ca6-6c9d-4fb3-a532-e38440c3b8e0.png)

A Monadikuikka, which is a rare and endangered bird, has been observed building a nest at a nearby lake.
However, some bird enthusiasts have been excessively eager to get a glimpse of the elusive bird, flying their drones too close to the nest and disturbing the birds in the process.
In order to protect the nesting birds, a no-drone zone (NDZ) has been established within 100 meters of the nest. Despite this, it is suspected that some drone pilots may still be disregarding this rule. 
This project demonstrates the detected violators for the last 10 minutes with the data provided by Reactor.


### Requirements

* Persist the pilot information for 10 minutes since their drone was last seen by the equipment
* Display the closest confirmed distance to the nest
* Contain the pilot name, email address and phone number
* Immediately show the information from the last 10 minutes to anyone opening the application
* Not require the user to manually refresh the view to see up-to-date information

### Built With

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [React](https://reactjs.org/)
* [Material UI](https://material-ui.com/)
* [SQLite](https://www.sqlite.org/index.html)


### Installation

   ```sh
   git clone https://github.com/AzimovS/birdnest-project
   cd backend && pip install -r requirements.txt && python main.py
   cd frontend && npm install && npm start
   ```


## Notes

- This project was created for Reactor by using provided API
