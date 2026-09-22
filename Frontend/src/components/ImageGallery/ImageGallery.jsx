import { useState } from "react";
import "./ImageGallery.css";

export default function ImageGallery({ images }) {
  const [lightbox, setLightbox] = useState(null);

  if (!images || !images.images || Object.keys(images.images).length === 0) return null;

  // Flatten all images into a flat list with their subject for display
  const allImages = [];
  for (const [subject, items] of Object.entries(images.images)) {
    if (!Array.isArray(items)) continue;
    for (const img of items) {
      if (img && img.url) {
        allImages.push({ ...img, subject });
      }
    }
  }

  // Deduplicate by URL
  const seen = new Set();
  const uniqueImages = allImages.filter((img) => {
    if (seen.has(img.url)) return false;
    seen.add(img.url);
    return true;
  });

  if (uniqueImages.length === 0) return null;

  return (
    <section className="section image-gallery-section">
      <h2 className="section-title">
        <span className="section-icon">📸</span>
        Photo Gallery
      </h2>

      <div className="gallery-grid">
        {uniqueImages.map((img, i) => (
          <div
            key={i}
            className="gallery-item"
            onClick={() => setLightbox(img)}
          >
            <img
              src={img.url}
              alt={img.alt_text || img.subject}
              className="gallery-img"
              loading="lazy"
              onError={(e) => { e.target.closest(".gallery-item").style.display = "none"; }}
            />
            <div className="gallery-overlay">
              <span className="gallery-subject">{img.subject}</span>
            </div>
          </div>
        ))}
      </div>

      {lightbox && (
        <div className="lightbox" onClick={() => setLightbox(null)}>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <button className="lightbox-close" onClick={() => setLightbox(null)}>✕</button>
            <img
              src={lightbox.url}
              alt={lightbox.alt_text || lightbox.subject}
              className="lightbox-img"
            />
            <div className="lightbox-caption">
              <strong>{lightbox.subject}</strong>
              {lightbox.alt_text && <span>{lightbox.alt_text}</span>}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
