import "./RestaurantCard.css";

export default function RestaurantCard({ restaurant, images }) {
  if (!restaurant || !restaurant.name) return null;

  const restaurantImages = images?.images?.[restaurant.name] || [];
  const heroImage = restaurantImages.length > 0 ? restaurantImages[0] : null;

  return (
    <div className="restaurant-card">
      {heroImage && (
        <div className="restaurant-card-img-wrap">
          <img
            src={heroImage.url}
            alt={heroImage.alt_text || restaurant.name}
            className="restaurant-card-img"
            loading="lazy"
            onError={(e) => { e.target.style.display = "none"; }}
          />
        </div>
      )}
      <div className="restaurant-card-body">
        <div className="restaurant-card-header">
          <h3 className="restaurant-card-name">{restaurant.name}</h3>
          {restaurant.rating != null && (
            <span className="restaurant-card-rating">★ {restaurant.rating}</span>
          )}
        </div>

        <div className="restaurant-card-meta">
          {restaurant.cuisine && (
            <span className="restaurant-cuisine">🍽️ {restaurant.cuisine}</span>
          )}
          {restaurant.price_range && (
            <span className="restaurant-price">{restaurant.price_range}</span>
          )}
        </div>

        {restaurant.address && (
          <p className="restaurant-address">📍 {restaurant.address}</p>
        )}
      </div>
    </div>
  );
}
