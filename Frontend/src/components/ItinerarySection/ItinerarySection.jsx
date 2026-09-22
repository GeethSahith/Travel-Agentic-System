import "./ItinerarySection.css";

export default function ItinerarySection({ itinerary }) {
  if (!itinerary || itinerary.length === 0) return null;

  return (
    <section className="section itinerary-section">
      <h2 className="section-title">
        <span className="section-icon">📅</span>
        Day-by-Day Itinerary
      </h2>

      <div className="itinerary-timeline">
        {itinerary.map((day, i) => (
          <div key={i} className="itinerary-day">
            <div className="day-marker">
              <span className="day-number">Day {day.day}</span>
            </div>
            <div className="day-content">
              <h3 className="day-title">{day.title}</h3>
              {day.activities && day.activities.length > 0 && (
                <ul className="activity-list">
                  {day.activities.map((activity, j) => (
                    <li key={j} className="activity-item">{activity}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
