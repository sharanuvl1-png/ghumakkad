# Ghumakkad

A phone-first travel website: **https://sharanuvl1-png.github.io/ghumakkad/**

Search any place to get, in one page:

- An embedded **Google Map**, with a Route button on every place (directions from your base) and an "All pins" overview map
- **Must-see places**, ranked by Wikipedia readership over the last 30 days, plus the Wikivoyage "See" list
- **Offbeat spots**: quiet Wikipedia sights plus viewpoints, waterfalls, caves, ruins and peaks mapped on OpenStreetMap that have no Wikipedia page
- **Which part to stay in**: areas where stays cluster closest to the top sights, plus Wikivoyage's "Sleep" advice and districts
- **Best stays**: Wikivoyage Budget / Mid-range / Splurge listings and star-rated hotels and homestays from OpenStreetMap, with links out for live prices
- A **day-by-day plan** for your dates: pick arrive and leave dates, it counts the days and groups nearby sights into each day in the shortest order, with lighter arrival and departure days, the forecast and a Google Maps route per day
- **Best time to visit**: month-by-month temperatures and wet days from last year's real weather records, with your travel month marked
- **Book & get ideas**: one tap to Google Flights, IRCTC, redBus, Booking.com, Airbnb, Agoda, GetYourGuide, Klook, Zomato, Reddit and YouTube, already searching your place and dates (links only, nothing is booked here)
- **Works offline** for places you've already opened, and **Share plan** sends your itinerary to WhatsApp
- Recent searches and tappable "Go next" destinations
- A 7-day forecast, getting-around tips, and a **My trip** planner that orders your stops and opens the route in Google Maps

All data is fetched live in the browser from free sources with no API keys: Wikivoyage, Wikipedia, OpenStreetMap (Overpass, Nominatim, Photon), Open-Meteo and Google Maps embeds. It never books or pays for anything; booking links just open those sites.

Installs on a phone as its own app (Chrome ⋮ → Install app).

## Publishing

Every push to `main` publishes the site (**Publish travel site** action). One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
