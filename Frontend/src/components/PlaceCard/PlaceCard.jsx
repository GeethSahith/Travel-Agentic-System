import "./PlaceCard.css";

export default function PlaceCard({ place, images }) {
  if (!place || !place.name) return null;

  const placeImages = images?.images?.[place.name] || [];
  const heroImage = placeImages.length > 0 ? placeImages[0] : null;

  return (
    <div className="place-card">
      {heroImage && (
        <div className="place-card-img-wrap">
          <img
            src={heroImage.url}
            alt={heroImage.alt_text || place.name}
            className="place-card-img"
            loading="lazy"
            onError={(e) => { e.target.style.display = "none"; }}
          />
        </div>
      )}
      <div className="place-card-body">
        <div className="place-card-header">
          <h3 className="place-card-name">{place.name}</h3>
          {place.rating != null && (
            <span className="place-card-rating">★ {place.rating}</span>
          )}
        </div>
        {place.category && (
          <span className="place-card-category">{place.category}</span>
        )}
        {place.description && (
          <p className="place-card-desc">{place.description}</p>
        )}
      </div>
    </div>
  );
}
