import "./HotelCard.css";

export default function HotelCard({ hotel, images }) {
  if (!hotel || !hotel.name) return null;

  const hotelImages = images?.images?.[hotel.name] || [];
  const heroImage = hotelImages.length > 0 ? hotelImages[0] : null;

  return (
    <div className="hotel-card">
      {heroImage && (
        <div className="hotel-card-img-wrap">
          <img
            src={heroImage.url}
            alt={heroImage.alt_text || hotel.name}
            className="hotel-card-img"
            loading="lazy"
            onError={(e) => { e.target.style.display = "none"; }}
          />
        </div>
      )}
      <div className="hotel-card-body">
        <div className="hotel-card-header">
          <h3 className="hotel-card-name">{hotel.name}</h3>
          {hotel.rating != null && (
            <span className="hotel-card-rating">★ {hotel.rating}</span>
          )}
        </div>

        <div className="hotel-card-meta">
          {hotel.price_per_night && (
            <span className="hotel-price">💰 {hotel.price_per_night}/night</span>
          )}
          {hotel.location && (
            <span className="hotel-location">📍 {hotel.location}</span>
          )}
        </div>

        {hotel.amenities && hotel.amenities.length > 0 && (
          <div className="hotel-amenities">
            {hotel.amenities.map((a, i) => (
              <span key={i} className="amenity-tag">{a}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
