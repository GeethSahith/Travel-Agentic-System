import { useState } from "react";
import TravelForm from "./components/TravelForm/TravelForm";
import WeatherSection from "./components/WeatherSection/WeatherSection";
import ItinerarySection from "./components/ItinerarySection/ItinerarySection";
import PlaceCard from "./components/PlaceCard/PlaceCard";
import HotelCard from "./components/HotelCard/HotelCard";
import RestaurantCard from "./components/RestaurantCard/RestaurantCard";
import ImageGallery from "./components/ImageGallery/ImageGallery";
import { generateTravelPlan } from "./services/travelApi";
import "./App.css";

function App() {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(formData) {
    setLoading(true);
    setError(null);
    setPlan(null);

    try {
      const result = await generateTravelPlan(formData);
      setPlan(result);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const hasPlaces = plan?.places?.places?.length > 0;
  const hasHotels = plan?.hotels?.hotels?.length > 0;
  const hasRestaurants = plan?.restaurants?.restaurants?.length > 0;
  const hasItinerary = plan?.itinerary?.length > 0;
  const hasWeather = plan?.weather?.forecast?.length > 0;
  const hasImages = plan?.images?.images && Object.keys(plan.images.images).length > 0;

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">🌍</span>
            Travel Planner
          </h1>
          <p className="app-tagline">Multi Agent Travel Planning Assistant</p>
        </div>
      </header>

      {/* Form Section */}
      <main className="app-main">
        <TravelForm onSubmit={handleSubmit} isLoading={loading} />

        {/* Loading State */}
        {loading && (
          <div className="loading-state">
            <div className="loading-animation">
              <span className="loading-globe">🌎</span>
            </div>
            <h3 className="loading-title">Creating your travel plan...</h3>
            <p className="loading-subtitle">
              Our AI agents are researching weather, places, hotels, restaurants, and more.
              This may take 30–60 seconds.
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error-state">
            <span className="error-icon">⚠️</span>
            <h3>Something went wrong</h3>
            <p>{error}</p>
          </div>
        )}

        {/* Results */}
        {plan && (
          <div className="plan-results">
            {/* Destination Header */}
            <div className="plan-hero">
              <h2 className="plan-destination">
                📍 {plan.destination}
              </h2>
              {plan.summary && (
                <p className="plan-summary">{plan.summary}</p>
              )}
            </div>

            {/* Weather */}
            {hasWeather && <WeatherSection weather={plan.weather} />}

            {/* Itinerary */}
            {hasItinerary && <ItinerarySection itinerary={plan.itinerary} />}

            {/* Places */}
            {hasPlaces && (
              <section className="section">
                <h2 className="section-title">
                  <span className="section-icon">🏛️</span>
                  Top Attractions
                </h2>
                <div className="card-grid">
                  {plan.places.places.map((place, i) => (
                    <PlaceCard key={i} place={place} images={plan.images} />
                  ))}
                </div>
              </section>
            )}

            {/* Hotels */}
            {hasHotels && (
              <section className="section">
                <h2 className="section-title">
                  <span className="section-icon">🏨</span>
                  Recommended Hotels
                </h2>
                <div className="card-grid">
                  {plan.hotels.hotels.map((hotel, i) => (
                    <HotelCard key={i} hotel={hotel} images={plan.images} />
                  ))}
                </div>
              </section>
            )}

            {/* Restaurants */}
            {hasRestaurants && (
              <section className="section">
                <h2 className="section-title">
                  <span className="section-icon">🍽️</span>
                  Recommended Restaurants
                </h2>
                <div className="card-grid">
                  {plan.restaurants.restaurants.map((restaurant, i) => (
                    <RestaurantCard key={i} restaurant={restaurant} images={plan.images} />
                  ))}
                </div>
              </section>
            )}

            {/* Image Gallery */}
            {hasImages && <ImageGallery images={plan.images} />}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Built with React, FastAPI and LangGraph</p>
      </footer>
    </div>
  );
}

export default App;
