import React, { useEffect, useState } from "react";
import "./index.css";

const VehiclesList = () => {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await fetch("http://localhost:5000/vehicles");
        const data = await response.json();
        setVehicles(data.vehicles);
      } catch (error) {
        console.error("Error fetching vehicles:", error);
      }
    };

    fetchVehicles();
  }, []);

  return (
    <div className="vehicle-list-container">
      <h2>Vehicles</h2>
      <ul>
        {vehicles.map((vehicle, index) => (
          <li key={index} className="vehicle-item">
            <div className="vehicle-image-container">
              <img
                src="https://clipart-library.com/images_k/silhouette-of-car/silhouette-of-car-18.png"
                alt={`Vehicle ${index}`}
                className="vehicle-image"
              />
            </div>
            <div className="vehicle-info">
              <div className="vehicle-name">
                <span>{vehicle}</span>
              </div>
              <div className="vehicle-buttons">
                <button className="action-button">Edit</button>
                <button className="action-button">Delete</button>
                <button className="action-button">View Details</button>
                <button className="action-button">Contact</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VehiclesList;
