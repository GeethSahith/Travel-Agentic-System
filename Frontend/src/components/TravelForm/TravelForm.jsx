import { useState } from "react";
import "./TravelForm.css";

const BUDGET_OPTIONS = ["budget", "moderate", "luxury"];
const PREFERENCE_OPTIONS = [
  "beaches",
  "culture",
  "food",
  "nightlife",
  "adventure",
  "museums",
  "shopping",
  "nature",
  "history",
  "relaxation",
];

export default function TravelForm({ onSubmit, isLoading }) {
  const [form, setForm] = useState({
    destination: "",
    country: "",
    dates: "",
    budget: "moderate",
    preferences: [],
  });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function togglePreference(pref) {
    setForm((prev) => ({
      ...prev,
      preferences: prev.preferences.includes(pref)
        ? prev.preferences.filter((p) => p !== pref)
        : [...prev.preferences, pref],
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (!form.destination.trim()) return;
    onSubmit(form);
  }

  return (
    <form className="travel-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <span className="form-icon">✈️</span>
        <h2>Plan Your Trip</h2>
        <p className="form-subtitle">Tell us where you'd like to go</p>
      </div>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="destination">Destination *</label>
          <input
            id="destination"
            name="destination"
            type="text"
            placeholder="e.g. Paris, Tokyo, Goa..."
            value={form.destination}
            onChange={handleChange}
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="country">Country</label>
          <input
            id="country"
            name="country"
            type="text"
            placeholder="e.g. France, Japan, India..."
            value={form.country}
            onChange={handleChange}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="dates">Travel Dates</label>
          <input
            id="dates"
            name="dates"
            type="text"
            placeholder="e.g. December 20-27, 2026"
            value={form.dates}
            onChange={handleChange}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="budget">Budget</label>
          <select
            id="budget"
            name="budget"
            value={form.budget}
            onChange={handleChange}
            disabled={isLoading}
          >
            {BUDGET_OPTIONS.map((b) => (
              <option key={b} value={b}>
                {b.charAt(0).toUpperCase() + b.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="form-group preferences-group">
        <label>Preferences</label>
        <div className="preference-chips">
          {PREFERENCE_OPTIONS.map((pref) => (
            <button
              key={pref}
              type="button"
              className={`chip ${form.preferences.includes(pref) ? "chip-active" : ""}`}
              onClick={() => togglePreference(pref)}
              disabled={isLoading}
            >
              {pref}
            </button>
          ))}
        </div>
      </div>

      <button type="submit" className="submit-btn" disabled={isLoading || !form.destination.trim()}>
        {isLoading ? (
          <span className="btn-loading">
            <span className="spinner"></span>
            Creating your travel plan...
          </span>
        ) : (
          "✨ Generate Travel Plan"
        )}
      </button>
    </form>
  );
}
