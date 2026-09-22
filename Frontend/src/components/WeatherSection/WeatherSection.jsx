import "./WeatherSection.css";

export default function WeatherSection({ weather }) {
  if (!weather || !weather.forecast || weather.forecast.length === 0) return null;

  function getWeatherEmoji(description) {
    const d = (description || "").toLowerCase();
    if (d.includes("clear") || d.includes("sun")) return "☀️";
    if (d.includes("cloud")) return "☁️";
    if (d.includes("rain") || d.includes("drizzle")) return "🌧️";
    if (d.includes("thunder") || d.includes("storm")) return "⛈️";
    if (d.includes("snow")) return "❄️";
    if (d.includes("fog") || d.includes("mist")) return "🌫️";
    return "🌤️";
  }

  return (
    <section className="section weather-section">
      <h2 className="section-title">
        <span className="section-icon">🌦️</span>
        Weather Forecast
        {weather.city && (
          <span className="weather-location">
            {weather.city}{weather.country ? `, ${weather.country}` : ""}
          </span>
        )}
      </h2>

      <div className="weather-grid">
        {weather.forecast.map((day, i) => (
          <div key={i} className="weather-card">
            <div className="weather-date">{day.date}</div>
            <div className="weather-emoji">{getWeatherEmoji(day.description)}</div>
            <div className="weather-temp">
              <span className="temp-high">{Math.round(day.temp_max)}°</span>
              <span className="temp-divider">/</span>
              <span className="temp-low">{Math.round(day.temp_min)}°</span>
            </div>
            <div className="weather-desc">{day.description}</div>
            <div className="weather-details">
              {day.humidity != null && (
                <span className="detail">💧 {day.humidity}%</span>
              )}
              {day.wind_speed != null && (
                <span className="detail">💨 {day.wind_speed} m/s</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {weather.warnings && weather.warnings.length > 0 && (
        <div className="weather-warnings">
          {weather.warnings.map((w, i) => (
            <div key={i} className="warning-item">⚠️ {w}</div>
          ))}
        </div>
      )}
    </section>
  );
}
